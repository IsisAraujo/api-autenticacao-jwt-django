from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint para verificar a saúde da API
    """
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
