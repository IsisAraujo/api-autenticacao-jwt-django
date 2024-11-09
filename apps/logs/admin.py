from django.contrib import admin

from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("destinatario", "assunto", "codigo", "tipo", "status", "data_envio")
    list_filter = ("tipo", "status", "data_envio")
    search_fields = ("destinatario", "assunto", "codigo")
    readonly_fields = ("data_envio",)
    ordering = ("-data_envio",)
