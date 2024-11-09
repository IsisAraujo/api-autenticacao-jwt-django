from datetime import timedelta
from random import randint

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class AtivacaoConta(models.Model):
    usuario = models.OneToOneField(
        "contas.PerfilUsuario",
        on_delete=models.CASCADE,
        related_name="confirmacao_email",
    )
    codigo_ativacao = models.CharField(
        max_length=6, null=True, blank=True, verbose_name=_("Código de Ativação")
    )
    criado_em = models.DateTimeField(
        default=timezone.now, verbose_name=_("Data de Criação")
    )
    tentativas = models.IntegerField(
        default=0, verbose_name=_("Tentativas de Ativação")
    )
    expira_em = models.DateTimeField(verbose_name=_("Data de Expiração"), null=True)
    email_enviado = models.TextField(
        verbose_name=_("Email Enviado"), null=True, blank=True
    )

    def criar_confirmacao(self):
        codigo = str(randint(100000, 999999))
        self.codigo_ativacao = codigo
        self.expira_em = timezone.now() + timedelta(minutes=30)
        self.tentativas = 0
        self.save()
        return codigo

    def verificar_confirmacao(self, codigo):
        agora = timezone.now()

        if self.expira_em < agora:
            raise ValidationError(_("Código expirado. Solicite um novo código."))

        if self.tentativas >= 3:
            raise ValidationError(
                _("Número máximo de tentativas excedido. Solicite um novo código.")
            )

        self.tentativas += 1
        self.save()

        if self.codigo_ativacao == codigo:
            self.usuario.email_confirmado = True
            self.usuario.save()
            self.delete()
            return True

        return False

    class Meta:
        verbose_name = "Ativação de Conta"
        verbose_name_plural = "Ativações de Contas"
        ordering = ["-criado_em"]
