from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.contas.models.usuario import UsuarioManager


def upload_to(instance, filename):
    return f"avatars/{instance.id}/{filename}"


class PerfilUsuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, verbose_name="Nome de Usuário")
    avatar = models.ImageField(
        upload_to=upload_to, blank=True, null=True, verbose_name="Foto de Perfil"
    )
    nome = models.CharField(
        max_length=60, verbose_name="Nome Completo", null=False, blank=False
    )
    cpf = models.CharField(
        max_length=11,
        verbose_name="CPF",
        unique=True,
        null=False,
        blank=False,
        help_text="Digite apenas os números do CPF, sem pontos ou traços",
    )
    data_cadastro = models.DateTimeField(default=timezone.now)
    email_confirmado = models.BooleanField(
        default=False, verbose_name=_("Email Confirmado")
    )
    codigo_verificacao_email = models.CharField(
        max_length=6, null=True, blank=True, verbose_name=_("Código de Verificação")
    )
    celular = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
        help_text=_("Digite o número no formato: DDD9XXXX-XXXX"),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False
    )  # Quando vc nao quer dar status de superuser mas ele pode usar o admin

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "celular", "nome", "cpf"]

    def __str__(self):
        return self.email

    class Meta:
        app_label = "contas"
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
        ordering = ["-data_cadastro"]
