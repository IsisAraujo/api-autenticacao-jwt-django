from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token

from apps.contas.models import AtivacaoConta, PerfilUsuario


class PerfilUsuarioFactory(DjangoModelFactory):
    class Meta:
        model = PerfilUsuario
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: f"usuario{n}@exemplo.com")
    username = factory.Sequence(lambda n: f"usuario_{n}")
    nome = factory.Faker("name", locale="pt_BR")
    celular = factory.Sequence(lambda n: f"+5511999{n:05d}")
    cpf = factory.Sequence(lambda n: f"{n:011d}")
    password = factory.PostGenerationMethodCall("set_password", "senha123")
    email_confirmado = False
    is_active = True


class AtivacaoContaFactory(DjangoModelFactory):
    class Meta:
        model = AtivacaoConta
        django_get_or_create = ("usuario",)

    usuario = factory.SubFactory(PerfilUsuarioFactory)
    codigo_ativacao = factory.Sequence(lambda n: f"{n:06d}")
    expira_em = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=24))
    tentativas = 0
    email_enviado = factory.Faker("text", max_nb_chars=200)


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token
        django_get_or_create = ("user",)

    user = factory.SubFactory(PerfilUsuarioFactory)
    key = factory.Sequence(lambda n: f"token{n:032x}")
