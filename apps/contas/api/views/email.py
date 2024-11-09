from pathlib import Path

from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.email_templates.email_utils import enviar_email_alteracao
from docs.swagger.contas import alterar_email_schema, verificar_alteracao_email_schema

from ..serializers import AlterarEmailSerializer, VerificarAlteracaoEmailSerializer


def salvar_email_tmp(mensagem_email, codigo):
    try:
        projeto_dir = Path(__file__).resolve().parent.parent.parent
        tmp_dir = projeto_dir / "content" / "tmp" / "emails"
        tmp_dir.mkdir(parents=True, exist_ok=True)

        arquivo_email = tmp_dir / f"email_ativacao_{codigo}.txt"
        arquivo_email.write_text(str(mensagem_email), encoding="utf-8")

        # Simplifica a impressão do email no console
        print("\n=== Email Enviado ===")
        print("Assunto: Novo")
        print("De: test@example.com")
        print("Para: usuario1@exemplo.com")
        print("\nCorpo da mensagem:")
        print(f"Seu novo código de ativação de conta é: {codigo}")
        print("==================\n")

        return str(arquivo_email)
    except Exception as e:
        print(f"Erro ao salvar email temporário: {str(e)}")
        return None


class AlterarEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlterarEmailSerializer

    def enviar_confirmacao_alteracao_email(self, user):
        code = get_random_string(length=6)
        user.email_verification_code = code
        user.save()

        try:
            enviar_email_alteracao(user.email, code)
        except Exception as e:
            raise PermissionDenied("Falha ao enviar email de confirmação.") from e

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
