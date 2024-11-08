from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import AtivacaoConta, PerfilUsuario


class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "nome",
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
            {"fields": ("username", "nome", "avatar", "telefone")},
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
                    "telefone",
                    "is_active",
                    "is_staff",
                    "email_confirmado",
                ),
            },
        ),
    )
    search_fields = ("email", "username", "nome")
    ordering = ("email",)


class AtivacaoContaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "codigo_ativacao", "criado_em")
    search_fields = ("usuario__email", "codigo_ativacao")
    readonly_fields = ("criado_em",)


admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(AtivacaoConta, AtivacaoContaAdmin)
