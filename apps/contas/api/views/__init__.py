# Views de Autenticação
from apps.contas.api.views.autenticacao import LoginView, LogoutView

# Views de Cadastro
from apps.contas.api.views.cadastro import (
    AtivacaoContaView,
    CadastrarUsuarioView,
    SolicitarNovoCodigoAtivacaoView,
)

# Views de Email
from apps.contas.api.views.email import AlterarEmailView, VerificarAlteracaoEmailView

# Views de Monitoramento
from apps.contas.api.views.monitoramento import health_check

# Views de Perfil
from apps.contas.api.views.perfil import AlterarPerfilView, PerfilView

# Views de Senha
from apps.contas.api.views.senha import (
    AlterarSenhaView,
    ResetSenhaView,
    VerificarResetSenhaView,
)

__all__ = [
    # Autenticação
    "LoginView",
    "LogoutView",
    # Perfil
    "PerfilView",
    "AlterarPerfilView",
    # Cadastro
    "CadastrarUsuarioView",
    "AtivacaoContaView",
    "SolicitarNovoCodigoAtivacaoView",
    # Senha
    "ResetSenhaView",
    "VerificarResetSenhaView",
    "AlterarSenhaView",
    # Email
    "AlterarEmailView",
    "VerificarAlteracaoEmailView",
    # Monitoramento
    "health_check",
]
