from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


from random import randint

def upload_to(instance, filename):
    return f'avatars/{instance.id}/{filename}'

class Usuario(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser preenchido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        user.save(using=self._db)


class PerfilUsuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, verbose_name='Nome de Usuário')
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name='Foto de Perfil')
    nome = models.CharField(max_length=30, verbose_name='Nome Completo')
    data_cadastro = models.DateTimeField(default=timezone.now)
    email_confirmado = models.BooleanField(default=False, verbose_name=_('Email Confirmado'))
    codigo_verificacao_email = models.CharField(max_length=6, null=True, blank=True, verbose_name=_('Código de Verificação'))
    telefone = PhoneNumberField(unique=True) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Quando vc nao quer dar status de superuser mas ele pode usar o admin

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    objects = Usuario()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'telefone']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
        ordering = ['-data_cadastro']


class AtivacaoConta(models.Model):
    usuario = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE, related_name='confirmacao_email')
    codigo_ativacao = models.CharField(max_length=6, null=True, blank=True, verbose_name=_('Código de Ativação'))
    criado_em = models.DateTimeField(default=timezone.now, verbose_name=_('Data de Criação'))

    def __str__(self):
        return f"Confirmação de Email para {self.usuario.email}"

    def criar_confirmacao(self):
        codigo = str(randint(100000, 999999))  # Gera um código aleatório de 6 dígitos
        self.codigo_ativacao = codigo
        self.save()
        return codigo

    def verificar_confirmacao(self, codigo):
        if self.codigo_ativacao == codigo:
            self.delete()  # Remove o registro de confirmação
            return True
        return False  # Código de confirmação inválido

    class Meta:
        verbose_name = 'Ativação de Conta'
        verbose_name_plural = 'Ativações de Contas'
        ordering = ['-criado_em']
