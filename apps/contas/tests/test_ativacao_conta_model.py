from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.contas.models.ativacao_conta import AtivacaoConta
from apps.contas.models.perfil_usuario import PerfilUsuario


class AtivacaoContaTests(TestCase):
    def setUp(self):
        self.user = PerfilUsuario.objects.create_user(
            email="teste@exemplo.com",
            username="usuarioteste",
            password="senha123",
            nome="Usuario Teste",
            celular="+5511999999999",
            cpf="12345678901",
        )
        self.ativacao = AtivacaoConta.objects.create(usuario=self.user)

    def test_criar_confirmacao(self):
        codigo = self.ativacao.criar_confirmacao()
        self.assertEqual(len(codigo), 6)
        self.assertEqual(self.ativacao.tentativas, 0)
        self.assertTrue(self.ativacao.expira_em > timezone.now())

    def test_verificar_confirmacao_sucesso(self):
        codigo = self.ativacao.criar_confirmacao()
        resultado = self.ativacao.verificar_confirmacao(codigo)
        self.assertTrue(resultado)
        self.assertTrue(self.user.email_confirmado)

        # Verifica se o registro foi deletado
        with self.assertRaises(AtivacaoConta.DoesNotExist):
            AtivacaoConta.objects.get(pk=self.ativacao.pk)

    def test_verificar_confirmacao_codigo_invalido(self):
        self.ativacao.criar_confirmacao()
        resultado = self.ativacao.verificar_confirmacao("000000")
        self.assertFalse(resultado)
        self.assertEqual(self.ativacao.tentativas, 1)

    def test_verificar_confirmacao_expirado(self):
        self.ativacao.criar_confirmacao()
        self.ativacao.expira_em = timezone.now() - timedelta(minutes=1)
        self.ativacao.save()

        with self.assertRaises(ValidationError):
            self.ativacao.verificar_confirmacao("000000")

    def test_max_tentativas_excedidas(self):
        self.ativacao.criar_confirmacao()
        self.ativacao.tentativas = 3
        self.ativacao.save()

        with self.assertRaises(ValidationError):
            self.ativacao.verificar_confirmacao("000000")
