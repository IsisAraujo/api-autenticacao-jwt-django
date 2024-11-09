from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contas.models import AtivacaoConta, PerfilUsuario
from core.email_templates.email_utils import enviar_email_ativacao, enviar_novo_codigo
from docs.swagger.contas import (
    ativacao_conta_schema,
    cadastrar_usuario_schema,
    novo_codigo_ativacao_conta_schema,
)

from ..serializers import (
    AtivacaoContaSerializer,
    CadastroSerializer,
    SolicitarNovoCodigoAtivacaoSerializer,
)


class CadastrarUsuarioView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = CadastroSerializer

    @cadastrar_usuario_schema
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            if PerfilUsuario.objects.filter(email=email).exists():
                return Response(
                    {"erro": _("Email já cadastrado")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            usuario = serializer.save()
            Token.objects.create(user=usuario)

            # Cria e envia o código de ativação
            confirmacao_email = AtivacaoConta(usuario=usuario)
            codigo_confirmacao = confirmacao_email.criar_confirmacao()

            try:
                enviar_email_ativacao(email, codigo_confirmacao)
            except Exception:
                return Response(
                    {"erro": _("Falha ao enviar email de ativação.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "sucesso": _(
                        "Usuário cadastrado com sucesso. Verifique seu email para ativar a conta."
                    )
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtivacaoContaView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AtivacaoContaSerializer

    @ativacao_conta_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            codigo_ativacao = serializer.validated_data.get("codigo")

            try:
                confirmacao_email = AtivacaoConta.objects.filter(
                    codigo_ativacao=codigo_ativacao
                ).first()

                if not confirmacao_email:
                    return Response(
                        {"erro": _("Código de ativação não encontrado.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    # Tenta verificar o código
                    if confirmacao_email.verificar_confirmacao(codigo_ativacao):
                        return Response(
                            {
                                "sucesso": _(
                                    "Conta ativada com sucesso. Prossiga para o Login"
                                )
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"erro": _("Código de ativação inválido.")},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                except ValidationError as e:
                    # Captura erros de validação (tentativas excedidas ou código expirado)
                    return Response(
                        {"erro": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except Exception:
                return Response(
                    {"erro": _("Erro ao processar a ativação.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolicitarNovoCodigoAtivacaoView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SolicitarNovoCodigoAtivacaoSerializer

    @novo_codigo_ativacao_conta_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                usuario = PerfilUsuario.objects.get(email=email)

                if usuario.email_confirmado:
                    return Response(
                        {"erro": _("Esta conta já está ativada.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                confirmacao_email, created = AtivacaoConta.objects.get_or_create(
                    usuario=usuario
                )

                novo_codigo = confirmacao_email.criar_confirmacao()

                try:
                    enviar_novo_codigo(email, novo_codigo)

                    return Response(
                        {
                            "sucesso": _(
                                "Novo código de ativação enviado com sucesso. Verifique seu email."
                            )
                        },
                        status=status.HTTP_200_OK,
                    )
                except Exception:
                    return Response(
                        {
                            "erro": _(
                                "Falha ao enviar email com novo código de ativação."
                            )
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            except PerfilUsuario.DoesNotExist:
                return Response(
                    {"erro": _("Usuário não encontrado.")},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
