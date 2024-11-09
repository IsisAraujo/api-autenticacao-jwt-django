import logging

from .models import EmailLog

logger = logging.getLogger(__name__)


def registrar_email(destinatario, assunto, conteudo, codigo, tipo, status="sucesso"):
    """
    Registra o envio de email no banco de dados
    """
    try:
        return EmailLog.objects.create(
            destinatario=destinatario,
            assunto=assunto,
            conteudo=conteudo,
            codigo=codigo,
            tipo=tipo,
            status=status,
        )
    except Exception as e:
        logger.error(f"Erro ao registrar email: {str(e)}")
        raise
