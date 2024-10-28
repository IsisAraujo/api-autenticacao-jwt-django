from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import AtivacaoConta

class ContaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dados_usuario = {
            'email': 'teste@exemplo.com',
            'password': 'senhateste'
        }
        self.usuario = get_user_model().objects.create_user(**self.dados_usuario)
        self.client.force_authenticate(user=self.usuario)

    def test_obter_conta(self):
        url = reverse('contas')
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_alterar_informacoes_conta(self):
        url = reverse('editar-detalhes')
        dados = {'primeiro_nome': 'Novo', 'sobrenome': 'Nome'}
        resposta = self.client.post(url, dados)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['success'], 'Informações do usuário alteradas.')
        
class AutenticacaoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dados_usuario = {
            'email': 'teste@exemplo.com',
            'password': 'senhateste',
            'email_confirmed': True  # Garante que o usuário está confirmado
        }
        self.usuario = get_user_model().objects.create_user(**self.dados_usuario)

    def test_login(self):
        url = reverse('login')
        dados = {'email': 'teste@exemplo.com', 'password': 'senhateste'}
        resposta = self.client.post(url, dados)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn('Authorization', resposta.headers)

    def test_login_invalido(self):
        url = reverse('login')
        dados = {'email': 'teste@exemplo.com', 'password': 'senhaerrada'}
        resposta = self.client.post(url, dados)
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

class CadastroTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_cadastro(self):
        url = reverse('cadastro')
        dados = {'email': 'novousuario@exemplo.com', 'password': 'senhanovousuario', 'primeiro_nome': 'Sarah', 'sobrenome': 'Connor'}
        resposta = self.client.post(url, dados)
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        
    def test_cadastro_duplicado(self):
        url = reverse('cadastro')
        dados = {
            'email': 'teste@exemplo.com',
            'password': 'senhateste',
            'primeiro_nome': 'João',
            'sobrenome': 'Silva',
        }
        
        # Cria um usuário com o mesmo email antes de fazer a solicitação de cadastro duplicado
        get_user_model().objects.create_user(email='teste@exemplo.com', password='senhaexistente')

        resposta = self.client.post(url, dados)
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resposta.data)
        
class AtivacaoContaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dados_usuario = {
            'email': 'teste@exemplo.com',
            'password': 'senhateste'
        }
        self.usuario = get_user_model().objects.create_user(**self.dados_usuario)
        self.codigo_ativacao = '123456'
        self.ativacao_conta = AtivacaoConta.objects.create(usuario=self.usuario, codigo_ativacao=self.codigo_ativacao)
        self.url_ativacao = reverse('ativacao-conta')

    def test_ativacao_conta(self):
        dados_ativacao = {'codigo': self.codigo_ativacao}
        resposta = self.client.post(self.url_ativacao, dados_ativacao)

        # Atualiza a instância do usuário a partir do banco de dados
        self.usuario.refresh_from_db()

        # Verifica a resposta e o perfil do usuário atualizado
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn('success', resposta.data)
        self.assertTrue(self.usuario.email_confirmed)

        # Verifica se a instância de AtivacaoConta foi excluída
        self.assertFalse(AtivacaoConta.objects.filter(pk=self.ativacao_conta.pk).exists())

    def test_codigo_ativacao_invalido(self):
        dados_ativacao = {'codigo': 'codigoinvalido'}
        resposta = self.client.post(self.url_ativacao, dados_ativacao)
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['error'], 'Código de confirmação inválido.')
