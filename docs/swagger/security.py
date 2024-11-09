from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Definição do schema de segurança JWT
security_schema = {
    "Bearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Autenticação JWT. Formato: Bearer <token>",
    }
}

# Respostas padrão
UNAUTHORIZED_RESPONSE = openapi.Response(
    "Não autorizado ou token inválido",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"erro": openapi.Schema(type=openapi.TYPE_STRING)},
    ),
)

SERVER_ERROR_RESPONSE = openapi.Response(
    "Erro interno do servidor",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"erro": openapi.Schema(type=openapi.TYPE_STRING)},
    ),
)

INVALID_REQUEST_RESPONSE = openapi.Response(
    "Requisição inválida",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"erro": openapi.Schema(type=openapi.TYPE_STRING)},
    ),
)

# Schema para tokens JWT
TOKEN_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(
            type=openapi.TYPE_STRING, description="Token de acesso JWT"
        ),
        "refresh": openapi.Schema(
            type=openapi.TYPE_STRING, description="Token de atualização JWT"
        ),
    },
)

# Decorator de segurança padrão
security_decorator = {
    "security": [{"Bearer": []}],
    "responses": {
        401: UNAUTHORIZED_RESPONSE,
        403: openapi.Response(
            "Acesso proibido",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"erro": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        500: SERVER_ERROR_RESPONSE,
    },
}

# Schema para endpoints protegidos
protected_endpoint_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            "Authorization",
            openapi.IN_HEADER,
            description="Token JWT. Formato: Bearer <token>",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    **security_decorator
)
