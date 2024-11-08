import random
import string

from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contas.models import AtivacaoConta, PerfilUsuario
from contas.serializers import (
    AlterarEmailSerializer,
    AlterarPerfilSerializer,
    AlterarSenhaSerializer,
    AtivacaoContaSerializer,
    CadastroSerializer,
    LoginSerializer,
    PerfilSerializer,
    ResetSenhaSerializer,
    SolicitarNovoCodigoAtivacaoSerializer,
    VerificarAlteracaoEmailSerializer,
    VerificarResetSenhaSerializer,
)
from contas.swagger.swagger_contas import (
    alterar_email_schema,
    alterar_perfil_schema,
    alterar_senha_schema,
    ativacao_conta_schema,
    cadastrar_usuario_schema,
    login_schema,
    logout_schema,
    novo_codigo_ativacao_conta_schema,
    perfil_schema,
    reset_senha_schema,
    verificar_alteracao_email_schema,
    verificar_reset_senha_schema,
)


class CadastrarUsuarioView(APIView):
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

            # Cria um token para o novo usuário
            Token.objects.create(user=usuario)

            # Cria e envia o código de ativação
            confirmacao_email = AtivacaoConta(usuario=usuario)
            codigo_confirmacao = confirmacao_email.criar_confirmacao()

            subject = _("Ative Sua Conta")
            message = f"Seu código de ativação de conta é: {codigo_confirmacao}"
            from_email = "seu_email@exemplo.com"  # Substitua pelo email correto
            to_email = [email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
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


class PerfilView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PerfilSerializer

    @perfil_schema
    def get(self, request, fmt=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class AlterarPerfilView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlterarPerfilSerializer

    @alterar_perfil_schema
    def post(self, request, fmt=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            usuario = request.user

            if "nome" in serializer.validated_data:
                usuario.nome = serializer.validated_data["nome"]

            usuario.save()

            content = {"success": _("Informações do usuário alteradas.")}
            return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @login_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            usuario = serializer.validated_data["usuario"]

            token, created = Token.objects.get_or_create(user=usuario)
            if usuario is not None and usuario.email_confirmed:
                login(request, usuario)
                response_data = {
                    "user_id": usuario.id,
                    "success": _("Usuário autenticado."),
                }

                # Inclui o token no cabeçalho da resposta
                response = Response(response_data, status=status.HTTP_200_OK)
                response["Authorization"] = f"Token {token.key}"
                return response
            elif usuario is not None and not usuario.email_confirmed:
                return Response(
                    {"error": _("Email não confirmado. Por favor, ative sua conta.")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                return Response(
                    {"error": _("Email ou senha inválidos.")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtivacaoContaView(APIView):
    serializer_class = AtivacaoContaSerializer

    @ativacao_conta_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            codigo_ativacao = serializer.validated_data.get("codigo")

            confirmacao_email = AtivacaoConta.objects.filter(
                codigo_ativacao=codigo_ativacao
            ).first()

            if confirmacao_email:
                if confirmacao_email.verificar_confirmacao(codigo_ativacao):
                    return Response(
                        {"success": _("Conta Ativada. Prossiga para o Login")},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": _("Código de confirmação inválido.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": _("Código de confirmação inválido.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @logout_schema
    def post(self, request, fmt=None):
        logout(request)
        return Response(
            {"success": "Usuário deslogado com sucesso."}, status=status.HTTP_200_OK
        )


# Gera um código aleatório de 6 dígitos
def gerar_codigo_verificacao():
    return "".join(random.choices(string.digits, k=6))


class ResetSenhaView(APIView):
    serializer_class = ResetSenhaSerializer

    @reset_senha_schema
    def post(self, request, fmt=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                # Encontra o usuário com o email fornecido
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": _("Usuário com este email não existe.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Gera um código único para redefinição de senha
            code = gerar_codigo_verificacao()

            # Anexa o código ao usuário
            user.email_verification_code = code
            user.save()

            # Envia o email de redefinição de senha
            subject = _("Redefina Sua Senha")
            message = f"Seu código de verificação é: {code}"
            from_email = "Seu Email"
            to_email = [email]

            try:
                # Envia o email
                send_mail(subject, message, from_email, to_email, fail_silently=True)
            except Exception:
                # Trata falha no envio do email
                return Response(
                    {"error": _("Falha ao enviar email de redefinição.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"success": _("Código de verificação enviado com sucesso.")},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificarResetSenhaView(APIView):
    serializer_class = VerificarResetSenhaSerializer

    @verificar_reset_senha_schema
    def post(self, request, fmt=None):
        serializer = VerificarResetSenhaSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data["code"]
            new_password = serializer.validated_data["new_password"]

            # Encontra o usuário com o código de verificação fornecido
            try:
                user = get_user_model().objects.get(email_verification_code=code)
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": _("Código de verificação inválido.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Define a nova senha e limpa o código de verificação
            user.set_password(new_password)
            user.email_verification_code = None
            user.save()

            return Response(
                {"success": _("Senha redefinida com sucesso.")},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlterarEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlterarEmailSerializer

    def enviar_confirmacao_alteracao_email(self, user):
        code = get_random_string(length=6)
        user.email_verification_code = code
        user.save()

        subject = "Confirme a Alteração de Email"
        message = f"Seu código de verificação é: {code}"
        from_email = "Seu Email"
        to_email = user.email

        # Envia o email
        send_mail(subject, message, from_email, [to_email], fail_silently=True)

    @alterar_email_schema
    def post(self, request, fmt=None):
        serializer = AlterarEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data["email"]

            # Verifica se o email fornecido corresponde ao email do usuário logado
            if new_email != user.email:
                raise PermissionDenied(
                    "O email fornecido não corresponde ao email do usuário logado."
                )

            # Envia o email de confirmação de alteração com o código
            self.enviar_confirmacao_alteracao_email(user)

            return Response(
                {"success": "Solicitação de alteração de email enviada com sucesso."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificarAlteracaoEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerificarAlteracaoEmailSerializer

    @verificar_alteracao_email_schema
    def post(self, request, fmt=None):
        serializer = VerificarAlteracaoEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            code = serializer.validated_data["code"]
            new_email = serializer.validated_data["new_email"]

            # Valida o código e atualiza o email se for válido
            if user.email_verification_code == code:
                user.email = new_email
                user.email_verification_code = None  # Limpa o código de verificação
                user.save()
                return Response(
                    {"success": "Email alterado com sucesso."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Código de verificação inválido ou expirado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlterarSenhaView(APIView):
    permission_classes = (IsAuthenticated,)

    @alterar_senha_schema
    def post(self, request, fmt=None):
        serializer = AlterarSenhaSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            # Verifica se a senha atual está correta
            if not user.check_password(old_password):
                return Response(
                    {"error": _("Senha atual incorreta.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Define a nova senha e salva o usuário
            user.set_password(new_password)
            user.save()

            # Opcional: Invalidar tokens de autenticação existentes, se necessário

            return Response(
                {"success": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolicitarNovoCodigoAtivacaoView(APIView):
    serializer_class = SolicitarNovoCodigoAtivacaoSerializer

    @novo_codigo_ativacao_conta_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                usuario = PerfilUsuario.objects.get(email=email)
            except PerfilUsuario.DoesNotExist:
                return Response(
                    {"erro": _("Usuário não encontrado.")},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if usuario.email_confirmado:
                return Response(
                    {"erro": _("Esta conta já está ativada.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Cria e envia o novo código de ativação
            confirmacao_email = AtivacaoConta.objects.filter(usuario=usuario).first()
            if not confirmacao_email:
                confirmacao_email = AtivacaoConta(usuario=usuario)

            novo_codigo = confirmacao_email.criar_confirmacao()

            subject = _("Novo Código de Ativação de Conta")
            message = f"Seu novo código de ativação de conta é: {novo_codigo}"
            from_email = "seu_email@exemplo.com"  # Substitua pelo email correto
            to_email = [email]

            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
            except Exception:
                return Response(
                    {"erro": _("Falha ao enviar email com novo código de ativação.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "sucesso": _(
                        "Novo código de ativação enviado com sucesso. Verifique seu email."
                    )
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# analisa a saude da api
def health_check(request):
    return JsonResponse({"status": "ok"})
