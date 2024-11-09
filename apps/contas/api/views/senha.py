import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.swagger.contas import (
    alterar_senha_schema,
    reset_senha_schema,
    verificar_reset_senha_schema,
)

from ..serializers import (
    AlterarSenhaSerializer,
    ResetSenhaSerializer,
    VerificarResetSenhaSerializer,
)


# Gera um código aleatório de 6 dígitos
def gerar_codigo_verificacao():
    return "".join(random.choices(string.digits, k=6))


class ResetSenhaView(APIView):
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
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


class AlterarSenhaView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlterarSenhaSerializer

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

            return Response(
                {"success": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
