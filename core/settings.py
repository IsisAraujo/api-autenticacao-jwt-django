import os
from pathlib import Path
from dotenv import load_dotenv

# Configuração de caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Determina o ambiente de execução
DJANGO_ENV = os.environ.get("DJANGO_ENV", "development")

# Carrega o arquivo .env apropriado
env_file = ".env.production" if DJANGO_ENV == "production" else ".env.development"
load_dotenv(BASE_DIR / env_file)

# Carrega as configurações apropriadas com base no ambiente
if DJANGO_ENV == "production":
    from .conf.production.settings import *
else:
    from .conf.development.settings import *

# Imprime informações sobre o ambiente de execução
print(f"Executando em modo {'Produção' if DJANGO_ENV == 'production' else 'Desenvolvimento'}")
print(f"Usando configurações de: {'production' if DJANGO_ENV == 'production' else 'development'}")
print(f"Usando arquivo .env: {env_file}")
