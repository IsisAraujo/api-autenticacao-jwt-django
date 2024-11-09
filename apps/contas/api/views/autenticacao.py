from django.contrib.auth import login, logout
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.swagger.contas import login_schema, logout_schema

from ..serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @login_schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            usuario = serializer.validated_data["usuario"]
            token, created = Token.objects.get_or_create(user=usuario)

            if usuario is not None and usuario.email_confirmado:
                login(request, usuario)
                response_data = {
                    "user_id": usuario.id,
                    "success": _("Usuário autenticado."),
                }
                response = Response(response_data, status=status.HTTP_200_OK)
                response["Authorization"] = f"Token {token.key}"
                return response
            elif usuario is not None and not usuario.email_confirmado:
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


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @logout_schema
    def post(self, request, fmt=None):
        logout(request)
        return Response(
            {"success": "Usuário deslogado com sucesso."}, status=status.HTTP_200_OK
        )
