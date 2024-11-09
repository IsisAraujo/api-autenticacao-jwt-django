from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.contas.api.views import CadastrarUsuarioView
from apps.contas.models import AtivacaoConta, PerfilUsuario
from apps.contas.tests.factories import AtivacaoContaFactory, PerfilUsuarioFactory


class CadastroUsuarioTests(APITestCase):
    def setUp(self):
        self.url = reverse("contas:cadastrar_usuario")
        self.dados_validos = {
            "email": "novo@exemplo.com",
            "password": "Senha123!",
            "nome": "Usuário Teste",
            "celular": "+5511999999999",
            "cpf": "12345678901",
            "username": "usuario_teste",
        }

    @patch("apps.contas.api.views.cadastro.enviar_email_ativacao")
    def test_cadastro_usuario_sucesso(self, mock_enviar_email):
        """Teste de cadastro de usuário com dados válidos"""
        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            PerfilUsuario.objects.filter(email=self.dados_validos["email"]).exists()
        )
        self.assertTrue(
            AtivacaoConta.objects.filter(
                usuario__email=self.dados_validos["email"]
            ).exists()
        )
        mock_enviar_email.assert_called_once()

    def test_cadastro_email_existente(self):
        """Teste de tentativa de cadastro com email já existente"""
        # Usa a factory para criar um usuário
        PerfilUsuarioFactory(email=self.dados_validos["email"])

        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(
            PerfilUsuario.objects.filter(email=self.dados_validos["email"]).count(), 1
        )

    def test_cadastro_dados_invalidos(self):
        """Teste de cadastro com dados inválidos"""
        dados_invalidos = self.dados_validos.copy()
        dados_invalidos["email"] = "email_invalido"

        response = self.client.post(self.url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cadastro_com_ativacao_pendente(self):
        """Teste de usuário com ativação pendente tentando novo cadastro"""
        # Cria usuário e ativação pendente usando factories
        usuario = PerfilUsuarioFactory(
            email=self.dados_validos["email"], email_confirmado=False
        )
        AtivacaoContaFactory(usuario=usuario)

        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    @patch("apps.contas.api.views.cadastro.enviar_email_ativacao")
    def test_falha_envio_email_ativacao(self, mock_enviar_email):
        mock_enviar_email.side_effect = Exception("Erro ao enviar email")

        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["erro"], "Falha ao enviar email de ativação.")

    def test_serializer_invalido(self):
        """Teste com dados inválidos no serializer"""
        # Enviando dados inválidos específicos ao invés de um dicionário vazio
        dados_invalidos = {
            "email": "email_invalido",  # Email em formato inválido
        }

        response = self.client.post(self.url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # Verifica se há erro no campo email
        self.assertTrue(
            "Insira um endereço" in str(response.data["email"][0])
        )  # Verifica a mensagem de erro

    def test_schema_decorador(self):
        """Teste para garantir que o decorador do schema está funcionando"""
        view = CadastrarUsuarioView()
        self.assertTrue(hasattr(view.post, "_swagger_auto_schema"))


class AtivacaoContaTests(APITestCase):
    def setUp(self):
        self.url = reverse("contas:ativar_conta")
        self.usuario = PerfilUsuarioFactory(email_confirmado=False)
        self.ativacao = AtivacaoContaFactory(usuario=self.usuario)
        self.dados_validos = {"codigo": self.ativacao.codigo_ativacao}

    def test_ativacao_sucesso(self):
        """Teste de ativação com código válido"""
        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["sucesso"], "Conta ativada com sucesso. Prossiga para o Login"
        )

    def test_codigo_nao_encontrado(self):
        """Teste com código de ativação inexistente"""
        dados = {"codigo": "000000"}
        response = self.client.post(self.url, dados)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["erro"], "Código de ativação não encontrado.")

    def test_codigo_invalido(self):
        """Teste com código de ativação inválido"""
        with patch(
            "apps.contas.models.AtivacaoConta.verificar_confirmacao", return_value=False
        ):
            response = self.client.post(self.url, self.dados_validos)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data["erro"], "Código de ativação inválido.")

    def test_erro_validacao_codigo(self):
        """Teste quando ocorre erro de validação no código"""
        with patch("apps.contas.models.AtivacaoConta.verificar_confirmacao") as mock:
            mock.side_effect = ValidationError("Código expirado")
            response = self.client.post(self.url, self.dados_validos)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue("Código expirado" in str(response.data["erro"]))

    def test_erro_generico_ativacao(self):
        """Teste de erro genérico durante ativação"""
        with patch("apps.contas.models.AtivacaoConta.objects.filter") as mock_filter:
            mock_filter.side_effect = Exception("Erro inesperado")

            response = self.client.post(self.url, self.dados_validos)

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data["erro"], "Erro ao processar a ativação.")

    def test_serializer_ativacao_invalido(self):
        """Teste com dados inválidos no serializer de ativação"""
        dados_invalidos = {}  # Dados vazios para forçar erro de validação

        response = self.client.post(self.url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SolicitarNovoCodigoTests(APITestCase):
    def setUp(self):
        self.url = reverse("contas:solicitar_novo_codigo_ativacao")
        self.usuario = PerfilUsuarioFactory(email_confirmado=False)
        self.dados_validos = {"email": self.usuario.email}

    def test_solicitar_novo_codigo_sucesso(self):
        """Teste de solicitação de novo código com sucesso"""
        with patch("apps.contas.api.views.cadastro.enviar_novo_codigo"):
            response = self.client.post(self.url, self.dados_validos)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("sucesso", response.data)

    def test_conta_ja_ativada(self):
        """Teste quando a conta já está ativada"""
        self.usuario.email_confirmado = True
        self.usuario.save()

        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["erro"], "Esta conta já está ativada.")

    def test_usuario_nao_encontrado(self):
        """Teste com email não cadastrado"""
        dados = {"email": "naoexiste@exemplo.com"}
        response = self.client.post(self.url, dados)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["erro"], "Usuário não encontrado.")

    @patch("apps.contas.api.views.cadastro.enviar_novo_codigo")
    def test_falha_envio_novo_codigo(self, mock_enviar):
        """Teste quando falha o envio do novo código"""
        mock_enviar.side_effect = Exception("Erro ao enviar email")

        response = self.client.post(self.url, self.dados_validos)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data["erro"], "Falha ao enviar email com novo código de ativação."
        )

    def test_serializer_novo_codigo_invalido(self):
        """Teste com dados inválidos no serializer de novo código"""
        dados_invalidos = {}  # Dados vazios para forçar erro de validação

        response = self.client.post(self.url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
