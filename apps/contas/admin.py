from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.contas.models import AtivacaoConta, PerfilUsuario


class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "nome",
        "cpf",
        "is_active",
        "is_staff",
        "email_confirmado",
        "codigo_verificacao_email",
    )
    list_filter = ("is_active", "is_staff", "email_confirmado")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Informações Pessoais"),
            {"fields": ("username", "nome", "avatar", "celular")},
        ),
        (
            _("Permissões"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_confirmado",
                    "codigo_verificacao_email",
                )
            },
        ),
        (_("Datas importantes"), {"fields": ("last_login", "data_cadastro")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "nome",
                    "celular",
                    "is_active",
                    "is_staff",
                    "email_confirmado",
                ),
            },
        ),
    )
    search_fields = ("email", "username", "nome")
    ordering = ("email",)


@admin.register(AtivacaoConta)
class AtivacaoContaAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "codigo_ativacao",
        "criado_em",
        "expira_em",
        "tentativas",
    )
    search_fields = ("usuario__email", "codigo_ativacao")
    readonly_fields = ("criado_em", "expira_em", "tentativas", "email_enviado")
    list_filter = ("criado_em", "expira_em")


admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
