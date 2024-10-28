from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from contas.views import (
    CadastrarUsuarioView,
    PerfilView,
    AlterarPerfilView,
    LoginView,
    AtivacaoContaView,
    LogoutView,
    ResetSenhaView,
    VerificarResetSenhaView,
    AlterarEmailView,
    VerificarAlteracaoEmailView,
    AlterarSenhaView,
    SolicitarNovoCodigoAtivacaoView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('usuario/cadastrar/', CadastrarUsuarioView.as_view(), name='cadastrar_usuario'),
    path('usuario/perfil/', PerfilView.as_view(), name='perfil_usuario'),
    path('usuario/alterar-perfil/', AlterarPerfilView.as_view(), name='alterar_perfil'),
    path('usuario/login/', LoginView.as_view(), name='login'),
    path('usuario/ativar-conta/', AtivacaoContaView.as_view(), name='ativar_conta'),
    path('usuario/logout/', LogoutView.as_view(), name='logout'),
    path('usuario/reset-senha/', ResetSenhaView.as_view(), name='reset_senha'),
    path('usuario/verificar-reset-senha/', VerificarResetSenhaView.as_view(), name='verificar_reset_senha'),
    path('usuario/alterar-email/', AlterarEmailView.as_view(), name='alterar_email'),
    path('usuario/verificar-alteracao-email/', VerificarAlteracaoEmailView.as_view(), name='verificar_alteracao_email'),
    path('usuario/alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
    path('token/', TokenObtainPairView.as_view(), name='obter_token'),
    path('token/atualizar/', TokenRefreshView.as_view(), name='atualizar_token'),
    path('solicitar-novo-codigo-ativacao/', SolicitarNovoCodigoAtivacaoView.as_view(), name='solicitar_novo_codigo_ativacao'),
]
