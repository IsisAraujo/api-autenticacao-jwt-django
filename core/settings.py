import os
from pathlib import Path

# Configuração de caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Determina o ambiente de execução
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")

# Carrega as configurações apropriadas com base no ambiente
if DJANGO_ENV == "production":
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env.production")
    from .conf.production import settings as production_settings

    settings_module = production_settings
else:
    from .conf.development import settings as development_settings

    settings_module = development_settings

# Define todas as configurações do módulo escolhido no escopo global
globals().update(vars(settings_module))

# Imprime informações sobre o ambiente de execução
print(
    f"Executando em modo {'Produção' if DJANGO_ENV == 'production' else 'Desenvolvimento'}"
)
