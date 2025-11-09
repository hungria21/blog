# coding: utf-8
import asyncio
from functools import wraps
from telethon.errors import FloodWaitError, ChatWriteForbiddenError, MessageNotModifiedError
from userbot import logger

def handle_errors(func):
    """Decorator para tratar erros comuns da API do Telegram."""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except FloodWaitError as e:
            logger.warning(f"Flood wait de {e.seconds} segundos no comando {func.__name__}.")
            await event.edit(f"`Estou sobrecarregado! Aguardando {e.seconds} segundos...`")
            await asyncio.sleep(e.seconds + 5)
        except MessageNotModifiedError:
            # Erro comum quando não há nada a editar, pode ser ignorado
            pass
        except ChatWriteForbiddenError:
            logger.warning(f"Não foi possível enviar mensagem em {event.chat_id}. Permissões insuficientes.")
            await event.client.send_message(
                "me",
                f"**Erro de Permissão**\n\nNão tenho permissão para escrever no chat `{event.chat_id}`."
            )
            await event.delete()
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado no comando {func.__name__}: {e}", exc_info=True)
            await event.edit(f"**Ocorreu um erro!**\n\n`{type(e).__name__}`: {e}")
    return wrapper
