# Estágio de build - usado apenas para instalar dependências
FROM python:3.11-slim AS builder

WORKDIR /code

# Instalando dependências de sistema necessárias para compilação
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Configuração do gerenciador de pacotes Poetry
RUN pip install -U pip setuptools poetry
RUN poetry config virtualenvs.create false

# Copia arquivos de dependência e instala pacotes
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-root

# Estágio final - apenas com as dependências necessárias
FROM python:3.11-slim

WORKDIR /code

# Instala apenas o driver PostgreSQL necessário em runtime
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root por segurança
RUN useradd -m -s /bin/bash devops_user

# Copia as dependências instaladas do estágio de build
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY . /code/

# Ajusta permissões e muda para usuário não-root
RUN chown -R devops_user:devops_user /code
USER devops_user

# Configuração de healthcheck para verificar se a API está respondendo
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Comando padrão para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
