from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from contas.serializers import (
    AlterarPerfilSerializer,
    CadastroSerializer,
    LoginSerializer,
    PerfilSerializer,
)

cadastrar_usuario_schema = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "username", "password", "telefone"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email do usuário"
            ),
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nome de usuário"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Senha do usuário"
            ),
            "telefone": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Número de telefone do usuário com DDD",
            ),
            "nome": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nome Completo"
            ),
        },
    ),
    responses={
        201: openapi.Response("Criado com sucesso", CadastroSerializer),
        400: "Requisição inválida",
        500: "Erro interno do servidor",
    },
)

perfil_schema = swagger_auto_schema(
    operation_description="Obtém o perfil do usuário autenticado",
    responses={200: PerfilSerializer, 401: "Não autorizado"},
)

alterar_perfil_schema = swagger_auto_schema(
    operation_description="Altera o perfil do usuário",
    request_body=AlterarPerfilSerializer,
    responses={
        200: openapi.Response("Perfil alterado com sucesso"),
        400: "Dados inválidos",
        401: "Não autorizado",
    },
)

login_schema = swagger_auto_schema(
    operation_description="Realiza o login do usuário",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            "Login bem-sucedido",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "success": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        401: "Credenciais inválidas ou conta não ativada",
    },
)

ativacao_conta_schema = swagger_auto_schema(
    operation_description="Ativa a conta do usuário",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["codigo"],
        properties={
            "codigo": openapi.Schema(
                type=openapi.TYPE_STRING, description="Código de ativação"
            ),
        },
    ),
    responses={200: "Conta ativada com sucesso", 400: "Código de ativação inválido"},
)
novo_codigo_ativacao_conta_schema = swagger_auto_schema(
    operation_description="Solicita um novo código de ativação para a conta do usuário",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email do usuário"
            ),
        },
    ),
    responses={
        200: openapi.Response("Novo código de ativação enviado com sucesso"),
        400: "Requisição inválida ou conta já ativada",
        404: "Usuário não encontrado",
        500: "Erro ao enviar email com novo código de ativação",
    },
)
reset_senha_schema = swagger_auto_schema(
    operation_description="Solicita redefinição de senha",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="Email do usuário"
            ),
        },
    ),
    responses={
        200: "Código de verificação enviado com sucesso",
        400: "Email não encontrado",
        500: "Erro ao enviar email",
    },
)

verificar_reset_senha_schema = swagger_auto_schema(
    operation_description="Verifica o código e redefine a senha",
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
        200: "Senha redefinida com sucesso",
        400: "Código de verificação inválido",
    },
)

logout_schema = swagger_auto_schema(
    operation_description="Realiza o logout do usuário",
    responses={200: "Logout realizado com sucesso", 401: "Não autorizado"},
)

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
        200: "Solicitação de alteração de email enviada com sucesso",
        400: "Dados inválidos",
        401: "Não autorizado",
        403: "Email fornecido não corresponde ao email do usuário logado",
    },
)

verificar_alteracao_email_schema = swagger_auto_schema(
    operation_description="Verifica o código e altera o email",
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
        200: "Email alterado com sucesso",
        400: "Código de verificação inválido ou expirado",
        401: "Não autorizado",
    },
)

alterar_senha_schema = swagger_auto_schema(
    operation_description="Altera a senha do usuário",
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
        200: "Senha alterada com sucesso",
        400: "Senha atual incorreta ou dados inválidos",
        401: "Não autorizado",
    },
)
