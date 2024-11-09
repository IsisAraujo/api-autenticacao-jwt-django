import os

# =========================================
# SELEÇÃO DE AMBIENTE
# =========================================

# Define o ambiente padrão como development se não estiver especificado
environment = os.getenv("DJANGO_ENVIRONMENT", "development")

# Carrega as configurações apropriadas baseado no ambiente
if environment == "production":
    from core.settings.production import *  # noqa: F403
else:
    from core.settings.development import *  # noqa: F403
