from django.db import models
from django.utils.translation import gettext as _


class EmailLog(models.Model):
    destinatario = models.EmailField(_("Destinatário"))
    assunto = models.CharField(_("Assunto"), max_length=255)
    conteudo = models.TextField(_("Conteúdo"))
    codigo = models.CharField(_("Código"), max_length=10)
    data_envio = models.DateTimeField(_("Data de Envio"), auto_now_add=True)
    tipo = models.CharField(
        _("Tipo"),
        max_length=50,
        choices=[
            ("ativacao", _("Ativação de Conta")),
            ("novo_codigo", _("Novo Código")),
        ],
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("sucesso", _("Sucesso")),
            ("erro", _("Erro")),
        ],
    )

    class Meta:
        verbose_name = _("Log de Email")
        verbose_name_plural = _("Logs de Email")
        ordering = ["-data_envio"]

    def __str__(self):
        return f"{self.tipo} - {self.destinatario} - {self.data_envio}"
