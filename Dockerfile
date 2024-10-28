# Use a imagem oficial do Python
FROM python:3.12.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY requirements.txt /app/

# Instala as dependências diretamente (sem ambiente virtual)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para dentro do contêiner
COPY . /app

# Define as variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expõe a porta 8000
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]