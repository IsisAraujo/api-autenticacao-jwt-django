from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.contas.api.views import (
    AlterarEmailView,
    AlterarPerfilView,
    AlterarSenhaView,
    AtivacaoContaView,
    CadastrarUsuarioView,
    LoginView,
    LogoutView,
    PerfilView,
    ResetSenhaView,
    SolicitarNovoCodigoAtivacaoView,
    VerificarAlteracaoEmailView,
    VerificarResetSenhaView,
    health_check,
)

app_name = "contas"

urlpatterns = [
    # Endpoints de autenticação
    path(
        "auth/",
        include(
            [
                path("login/", LoginView.as_view(), name="login"),
                path("logout/", LogoutView.as_view(), name="logout"),
                path("token/", TokenObtainPairView.as_view(), name="obter_token"),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="atualizar_token"
                ),
            ]
        ),
    ),
    # Endpoints de usuário
    path(
        "usuario/",
        include(
            [
                path(
                    "cadastrar/",
                    CadastrarUsuarioView.as_view(),
                    name="cadastrar_usuario",
                ),
                path("perfil/", PerfilView.as_view(), name="perfil_usuario"),
                path(
                    "alterar-perfil/",
                    AlterarPerfilView.as_view(),
                    name="alterar_perfil",
                ),
                path(
                    "alterar-senha/", AlterarSenhaView.as_view(), name="alterar_senha"
                ),
                path(
                    "alterar-email/", AlterarEmailView.as_view(), name="alterar_email"
                ),
                path(
                    "verificar-alteracao-email/",
                    VerificarAlteracaoEmailView.as_view(),
                    name="verificar_alteracao_email",
                ),
            ]
        ),
    ),
    # Endpoints de ativação de conta
    path(
        "ativacao/",
        include(
            [
                path("ativar/", AtivacaoContaView.as_view(), name="ativar_conta"),
                path(
                    "novo-codigo/",
                    SolicitarNovoCodigoAtivacaoView.as_view(),
                    name="solicitar_novo_codigo_ativacao",
                ),
            ]
        ),
    ),
    # Endpoints de recuperação de senha
    path(
        "senha/",
        include(
            [
                path("reset/", ResetSenhaView.as_view(), name="reset_senha"),
                path(
                    "verificar-reset/",
                    VerificarResetSenhaView.as_view(),
                    name="verificar_reset_senha",
                ),
            ]
        ),
    ),
    # Health check
    path("health/", health_check, name="health-check"),
]
