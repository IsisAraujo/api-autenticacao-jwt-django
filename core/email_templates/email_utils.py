import logging

from django.conf import settings
from django.core.mail import send_mail
from logs.utils import registrar_email

logger = logging.getLogger(__name__)


def enviar_email_ativacao(email, codigo):
    """
    Envia email de ativação e registra o log
    """
    subject = "Ative Sua Conta"
    message = f"Seu código de ativação de conta é: {codigo}"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        registrar_email(email, subject, message, codigo, "ativacao")
        logger.info(f"Email de ativação enviado para {email}")
    except Exception as e:
        registrar_email(email, subject, message, codigo, "ativacao", "erro")
        logger.error(f"Erro ao enviar email de ativação para {email}: {str(e)}")
        raise


def enviar_novo_codigo(email, codigo):
    """
    Envia email com novo código e registra o log
    """
    subject = "Novo Código de Ativação"
    message = f"Seu novo código de ativação de conta é: {codigo}"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        registrar_email(email, subject, message, codigo, "novo_codigo")
        logger.info(f"Novo código de ativação enviado para {email}")
    except Exception as e:
        registrar_email(email, subject, message, codigo, "novo_codigo", "erro")
        logger.error(f"Erro ao enviar novo código para {email}: {str(e)}")
        raise


def enviar_email_alteracao(email, codigo):
    """
    Envia email com código de alteração de email e registra o log
    """
    subject = "Confirme a Alteração de Email"
    message = f"Seu código de verificação é: {codigo}"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        registrar_email(email, subject, message, codigo, "alteracao_email")
        logger.info(f"Email de alteração enviado para {email}")
    except Exception as e:
        registrar_email(email, subject, message, codigo, "alteracao_email", "erro")
        logger.error(f"Erro ao enviar email de alteração para {email}: {str(e)}")
        raise
