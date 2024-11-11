FROM python:3.11-slim

WORKDIR /code

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Instalar dependências
RUN poetry install --no-root

# Copiar código do projeto
COPY . .

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
