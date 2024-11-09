from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .security import (
    INVALID_REQUEST_RESPONSE,
    SERVER_ERROR_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)

# Schemas de resposta comuns
SUCESSO_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"success": openapi.Schema(type=openapi.TYPE_STRING)},
)

ERRO_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"erro": openapi.Schema(type=openapi.TYPE_STRING)},
)

# Schema para cadastro de usuário
cadastrar_usuario_schema = swagger_auto_schema(
    operation_description="Cadastra um novo usuário no sistema",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password", "username", "celular", "cpf"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email do usuário"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Senha do usuário"
            ),
            "nome": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nome completo do usuário"
            ),
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nome de usuário para login"
            ),
            "celular": openapi.Schema(
                type=openapi.TYPE_STRING, description="Número de celular do usuário"
            ),
            "cpf": openapi.Schema(
                type=openapi.TYPE_STRING, description="CPF do usuário (apenas números)"
            ),
        },
    ),
    responses={
        201: openapi.Response(
            description="Usuário cadastrado com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(description="Dados inválidos", schema=ERRO_RESPONSE),
        500: SERVER_ERROR_RESPONSE,
    },
)

# Schema para login
login_schema = swagger_auto_schema(
    operation_description="Realiza o login do usuário",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={
        200: openapi.Response(
            description="Login realizado com sucesso",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "success": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            headers={
                "Authorization": openapi.Parameter(
                    "Authorization",
                    openapi.IN_HEADER,
                    description="Token de autenticação",
                    type=openapi.TYPE_STRING,
                )
            },
        ),
        401: UNAUTHORIZED_RESPONSE,
        400: INVALID_REQUEST_RESPONSE,
    },
)

# Schema para ativação de conta
ativacao_conta_schema = swagger_auto_schema(
    operation_description="Ativa a conta do usuário usando código de confirmação",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["codigo"],
        properties={
            "codigo": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Código de ativação recebido por email",
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Conta ativada com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(description="Código inválido", schema=ERRO_RESPONSE),
    },
)

# Schema para solicitação de novo código de ativação
novo_codigo_ativacao_conta_schema = swagger_auto_schema(
    operation_description="Solicita um novo código de ativação",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email da conta a ser ativada"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Novo código enviado com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(
            description="Conta já ativada ou email inválido", schema=ERRO_RESPONSE
        ),
        404: openapi.Response(
            description="Usuário não encontrado", schema=ERRO_RESPONSE
        ),
        500: SERVER_ERROR_RESPONSE,
    },
)

# Schema para alteração de senha
alterar_senha_schema = swagger_auto_schema(
    operation_description="Altera a senha do usuário logado",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["old_password", "new_password"],
        properties={
            "old_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Senha atual"
            ),
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nova senha"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Senha alterada com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(
            description="Senha atual incorreta ou nova senha inválida",
            schema=ERRO_RESPONSE,
        ),
        401: UNAUTHORIZED_RESPONSE,
    },
)

# Schema para reset de senha
reset_senha_schema = swagger_auto_schema(
    operation_description="Solicita redefinição de senha",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email da conta"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Código de verificação enviado", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(description="Email não encontrado", schema=ERRO_RESPONSE),
        500: SERVER_ERROR_RESPONSE,
    },
)

# Schema para verificação de reset de senha
verificar_reset_senha_schema = swagger_auto_schema(
    operation_description="Verifica código e define nova senha",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["code", "new_password"],
        properties={
            "code": openapi.Schema(
                type=openapi.TYPE_STRING, description="Código de verificação"
            ),
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nova senha"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Senha redefinida com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(
            description="Código inválido ou senha inválida", schema=ERRO_RESPONSE
        ),
    },
)

# Schema para alteração de email
alterar_email_schema = swagger_auto_schema(
    operation_description="Solicita alteração de email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email atual do usuário"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Código de verificação enviado", schema=SUCESSO_RESPONSE
        ),
        400: INVALID_REQUEST_RESPONSE,
        401: UNAUTHORIZED_RESPONSE,
        403: openapi.Response(
            description="Email não corresponde ao usuário logado", schema=ERRO_RESPONSE
        ),
    },
)

# Schema para verificação de alteração de email
verificar_alteracao_email_schema = swagger_auto_schema(
    operation_description="Verifica código e altera email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["code", "new_email"],
        properties={
            "code": openapi.Schema(
                type=openapi.TYPE_STRING, description="Código de verificação"
            ),
            "new_email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Novo email"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Email alterado com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: openapi.Response(
            description="Código inválido ou email inválido", schema=ERRO_RESPONSE
        ),
        401: UNAUTHORIZED_RESPONSE,
    },
)

# Schema para perfil do usuário
perfil_schema = swagger_auto_schema(
    operation_description="Obtém dados do perfil do usuário",
    responses={
        200: openapi.Response(
            description="Dados do perfil",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "nome": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        401: UNAUTHORIZED_RESPONSE,
    },
)

# Schema para alteração de perfil
alterar_perfil_schema = swagger_auto_schema(
    operation_description="Altera dados do perfil do usuário",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "nome": openapi.Schema(
                type=openapi.TYPE_STRING, description="Novo nome do usuário"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Perfil alterado com sucesso", schema=SUCESSO_RESPONSE
        ),
        400: INVALID_REQUEST_RESPONSE,
        401: UNAUTHORIZED_RESPONSE,
    },
)

# Schema para logout
logout_schema = swagger_auto_schema(
    operation_description="Realiza logout do usuário",
    responses={
        200: openapi.Response(
            description="Logout realizado com sucesso", schema=SUCESSO_RESPONSE
        ),
        401: UNAUTHORIZED_RESPONSE,
    },
)
