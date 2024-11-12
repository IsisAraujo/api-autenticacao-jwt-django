FROM python:3.11-slim as builder

WORKDIR /code

# Instalar dependências do sistema e poetry
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry \
    && poetry config virtualenvs.create false

# Copiar apenas os arquivos de dependência
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

# Imagem final
FROM python:3.11-slim

WORKDIR /code

# Copiar dependências da imagem builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Instalar apenas as dependências de runtime necessárias
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar código do projeto
COPY . .

EXPOSE 8000

# Adicionar healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
