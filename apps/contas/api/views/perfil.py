from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.swagger.contas import alterar_perfil_schema, perfil_schema

from ..serializers import AlterarPerfilSerializer, PerfilSerializer


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
