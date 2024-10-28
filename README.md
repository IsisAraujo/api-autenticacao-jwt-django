# API de Autenticação Django Rest Framework

A API de Autenticação do Django é um sistema de autenticação robusto, construído com Django e Django Rest Framework. Ela oferece funcionalidades como registro de usuários, login, redefinição de senha, alteração de e-mail, entre outros recursos relacionados à autenticação.

## Índice

- [API de Autenticação Django Rest Framework](#api-de-autenticação-django-rest-framework)
  - [Índice](#índice)
  - [Introdução](#introdução)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
  - [Uso](#uso)
    - [Endpoints da API](#endpoints-da-api)
    - [Autenticação](#autenticação)
  - [Contribuição](#contribuição)

## Introdução

### Pré-requisitos

Certifique-se de ter os seguintes pré-requisitos instalados:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)


### Instalação

1. **Clone o repositório:**

    ```bash
    
    ```

2. **Navegue até o diretório do projeto:**

    ```bash
    cd base_user
    ```

3. **Instale as dependências necessárias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Aplique as migrações:**

    ```bash
    python manage.py migrate
    ```

5. **Execute o servidor de desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

A API deve estar acessível em `http://localhost:8000/api/contas/`.

## Uso

### Endpoints da API

Todos os endpoints da API estão acessíveis sob o prefixo `/api/contas/`. Os endpoints disponíveis são:

1. **Informações da Conta do Usuário:** `/api/contas/`
    - Método: `GET`
    - Requer autenticação

2. **Alteração de Conta do Usuário:** `/api/contas/editar-detalhes/`
    - Método: `POST`
    - Requer autenticação
    - Atualiza informações do usuário (primeiro nome, sobrenome)

3. **Login de Usuário:** `/api/contas/login/`
    - Método: `POST`
    - Entrada: E-mail e senha
    - Retorna informações do usuário

4. **Cadastro de Usuário:** `/api/contas/cadastro/`
    - Método: `POST`
    - Entrada: Primeiro nome, sobrenome, e-mail e senha
    - Retorna mensagem de sucesso

5. **Ativação de Conta:** `/api/contas/ativar-conta/`
    - Método: `POST`
    - Entrada: Código de ativação
    - Ativa a conta do usuário para que ele possa fazer login

6. **Logout do Usuário:** `/api/contas/logout/`
    - Método: `POST`
    - Requer autenticação
    - Faz o logout do usuário

7. **Solicitação de Redefinição de Senha:** `/api/contas/resetar-senha/`
    - Método: `POST`
    - Entrada: E-mail
    - Envia um código de verificação para redefinir a senha para o e-mail do usuário

8. **Verificação de Redefinição de Senha:** `/api/contas/resetar-senha/verificar/`
    - Método: `POST`
    - Entrada: Código de verificação e nova senha
    - Redefine a senha do usuário

9. **Solicitação de Alteração de E-mail:** `/api/contas/alterar-email/`
    - Método: `POST`
    - Requer autenticação
    - Envia um código de verificação para alterar o e-mail para o e-mail do usuário

10. **Verificação de Alteração de E-mail:** `/api/contas/alterar-email/verificar/`
    - Método: `POST`
    - Entrada: Código de verificação e novo e-mail
    - Altera o e-mail do usuário

11. **Alteração de Senha:** `/api/contas/alterar-senha/`
    - Método: `POST`
    - Requer autenticação
    - Entrada: Senha antiga e nova senha
    - Altera a senha do usuário

### Autenticação

- A API utiliza Token Authentication para proteger os endpoints quando necessário.

## Contribuição

- Faça um fork do repositório.
- Crie um novo branch para sua feature: `git checkout -b feature-name`.
- Commite suas mudanças: `git commit -m 'Adicionar nova feature'`.
- Envie para o branch: `git push origin feature-name`.
- Envie um pull request.

---
