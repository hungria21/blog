import os
import re
import asyncio
import logging
from telethon import TelegramClient, events, types, errors
from telethon.tl.types import InputDocument

import config
import database
import downloader
import utils

# Configuração de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Expressão regular simples para identificar URLs
URL_PATTERN = re.compile(r'https?://[^\s]+')

# Inicializa o Banco de Dados
database.init_db()

# Inicializa o cliente do bot Telethon
bot = TelegramClient("bot_session", config.API_ID, config.API_HASH)

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    """Envia uma mensagem de boas-vindas."""
    welcome_text = (
        "<b>Bot de Download de Vídeos</b>\n\n"
        "Envie um link de vídeo do TikTok, Instagram, Twitter/X ou YouTube "
        "para baixar o vídeo diretamente com legendas formatadas.\n\n"
        "Você também pode me usar no modo inline escrevendo meu username seguido do link "
        "em qualquer chat!"
    )
    await event.respond(welcome_text, parse_mode="html")

@bot.on(events.NewMessage(pattern="/help"))
async def help_handler(event):
    """Envia instruções de uso."""
    help_text = (
        "<b>Como usar:</b>\n\n"
        "1. <b>Mensagem Direta:</b> Cole o link de um vídeo suportado aqui.\n"
        "2. <b>Modo Inline:</b> Digite <code>@username [link]</code> em qualquer chat, "
        "aguarde o resultado carregar e clique nele para enviar o vídeo.\n\n"
        "Os vídeos baixados anteriormente ficam guardados no cache e carregam de forma instantânea!"
    )
    await event.respond(help_text, parse_mode="html")

@bot.on(events.NewMessage)
async def message_handler(event):
    """Processa mensagens diretas recebidas pelo bot."""
    if event.text and (event.text.startswith("/") or event.text.startswith("!")):
        return # Ignora comandos que já possuem handlers dedicados

    url_match = URL_PATTERN.search(event.text or "")
    if not url_match:
        return # Se não contiver um link válido, ignora de forma silenciosa

    url = url_match.group(0)
    logger.info(f"Recebido link para processamento no chat {event.chat_id}: {url}")

    # Verifica cache
    cached = database.get_cached_video(url)
    if cached:
        logger.info(f"Vídeo em cache localizado para {url}")
        try:
            # Cria o InputDocument
            doc = InputDocument(
                id=cached["document_id"],
                access_hash=cached["access_hash"],
                file_reference=cached["file_reference"]
            )
            # Envia usando o documento em cache
            await bot.send_file(
                event.chat_id,
                doc,
                caption=cached["caption"],
                parse_mode="html",
                reply_to=event.message.id
            )
            return
        except Exception as e:
            logger.warning(f"Falha ao enviar usando cache: {e}. Tentando download novamente.")

    # Status inicial do processamento
    status_msg = await event.respond("Processando o link... Preparando download.", reply_to=event.message.id)

    # Controle de atualização da barra de progresso para evitar flood de mensagens
    last_update_time = 0
    main_loop = asyncio.get_running_loop()

    def on_download_progress(d):
        nonlocal last_update_time
        now = main_loop.time()

        # Atualiza a cada 3 segundos para evitar rate-limit/flooding
        if now - last_update_time >= 3.0:
            percentage = d.get("percentage", 0.0)
            pbar = utils.generate_progress_bar(percentage)
            speed = utils.format_size(d.get("speed", 0)) + "/s" if d.get("speed") else "N/A"
            eta = f"{d.get('eta')}s" if d.get("eta") else "N/A"
            status_text = (
                f"Baixando mídia...\n\n"
                f"{pbar}\n"
                f"Velocidade: {speed}\n"
                f"Tempo Restante (ETA): {eta}"
            )
            # Agenda a edição da mensagem de forma assíncrona usando o loop principal capturado
            asyncio.run_coroutine_threadsafe(
                safe_edit_message(status_msg, status_text),
                main_loop
            )
            last_update_time = now

    # Executa o download em um pool de threads para não bloquear o loop de eventos
    try:
        metadata = await main_loop.run_in_executor(
            None,
            lambda: downloader.download_video(url, progress_callback=on_download_progress)
        )
    except Exception as e:
        logger.error(f"Erro no download: {e}")
        await safe_edit_message(status_msg, f"Falha ao baixar o vídeo. Erro: {utils.escape_html(str(e))}")
        return

    filepath = metadata["filepath"]
    caption = utils.format_rich_caption(
        title=metadata["title"],
        description=metadata["description"],
        author_username=metadata["author_username"],
        author_name=metadata["author_name"],
        platform=metadata["platform"],
        original_url=metadata["original_url"]
    )

    await safe_edit_message(status_msg, "Download concluído! Iniciando envio para o Telegram...")

    # Upload do arquivo com callback de progresso
    last_upload_update_time = 0

    def on_upload_progress(uploaded_bytes, total_bytes):
        nonlocal last_upload_update_time
        now = main_loop.time()

        if now - last_upload_update_time >= 3.0:
            percentage = (uploaded_bytes / total_bytes) * 100 if total_bytes else 0.0
            pbar = utils.generate_progress_bar(percentage)
            status_text = (
                f"Enviando mídia para o Telegram...\n\n"
                f"{pbar}\n"
                f"Enviado: {utils.format_size(uploaded_bytes)} / {utils.format_size(total_bytes)}"
            )
            asyncio.run_coroutine_threadsafe(
                safe_edit_message(status_msg, status_text),
                main_loop
            )
            last_upload_update_time = now

    try:
        # Envia o arquivo e captura a mensagem final com o arquivo
        sent_msg = await bot.send_file(
            event.chat_id,
            filepath,
            caption=caption,
            parse_mode="html",
            progress_callback=on_upload_progress,
            reply_to=event.message.id
        )

        # Remove o arquivo temporário imediatamente
        if os.path.exists(filepath):
            os.remove(filepath)

        # Deleta a mensagem de status antiga
        await status_msg.delete()

        # Salva o arquivo enviado no cache de banco de dados para envios instantâneos futuros
        if sent_msg and sent_msg.media and sent_msg.media.document:
            doc = sent_msg.media.document
            database.save_cached_video(
                url=url,
                document_id=doc.id,
                access_hash=doc.access_hash,
                file_reference=doc.file_reference,
                mime_type=doc.mime_type,
                size=doc.size,
                title=metadata["title"],
                caption=caption
            )
            logger.info(f"Mídia salva com sucesso no banco de dados para {url}")

    except Exception as e:
        logger.error(f"Erro no envio do arquivo: {e}")
        # Limpeza caso ocorra erro
        if os.path.exists(filepath):
            os.remove(filepath)
        await safe_edit_message(status_msg, f"Falha no envio do vídeo: {utils.escape_html(str(e))}")


@bot.on(events.InlineQuery)
async def inline_handler(event):
    """
    Tratamento de consultas inline.
    Se o link estiver no cache, retorna imediatamente o documento em cache.
    Se não, tenta baixar/enviar rapidamente em um curto limite de tempo ou orienta o usuário.
    """
    query_text = event.text.strip() if event.text else ""
    url_match = URL_PATTERN.search(query_text)

    if not url_match:
        # Retorna uma mensagem amigável instruindo a usar um link
        builder = event.builder
        result = builder.article(
            title="Insira um link válido",
            description="Cole o link do vídeo do TikTok, Instagram ou Twitter para baixar.",
            text="Por favor, digite meu username seguido do link do vídeo no chat. Exemplo: <code>@bot_username link</code>",
            parse_mode="html"
        )
        await event.answer([result], cache_time=5)
        return

    url = url_match.group(0)
    logger.info(f"InlineQuery recebida para: {url}")

    # 1. Verifica cache local do banco de dados
    cached = database.get_cached_video(url)
    if cached:
        logger.info(f"Vídeo em cache localizado para inline: {url}")
        try:
            doc = InputDocument(
                id=cached["document_id"],
                access_hash=cached["access_hash"],
                file_reference=cached["file_reference"]
            )

            # Constrói o resultado inline usando o builder que formata os rich-texts
            inline_id = str(hash(url) & 0xffffffff)
            res = await event.builder.document(
                file=doc,
                title=cached["title"] or "Vídeo",
                description="Carregado instantaneamente do cache!",
                text=cached["caption"],
                parse_mode="html",
                id=inline_id
            )
            await event.answer([res], cache_time=3600)
            return
        except Exception as e:
            logger.warning(f"Erro ao usar cache na consulta inline: {e}. Removendo entrada corrompida.")

    # 2. Se não estiver no cache ou se o cache falhou, tenta baixar/upload em 5 segundos
    try:
        async def quick_download_and_cache():
            loop = asyncio.get_running_loop()
            metadata = await loop.run_in_executor(
                None,
                lambda: downloader.download_video(url, progress_callback=None)
            )
            # Faz o upload silencioso do arquivo para o Telegram (para gerar o DocumentID)
            filepath = metadata["filepath"]
            caption = utils.format_rich_caption(
                title=metadata["title"],
                description=metadata["description"],
                author_username=metadata["author_username"],
                author_name=metadata["author_name"],
                platform=metadata["platform"],
                original_url=metadata["original_url"]
            )
            try:
                # Faz o upload para "me" (o chat privado do bot consigo mesmo para gerar o documento)
                sent_msg = await bot.send_file(
                    "me",
                    filepath,
                    caption=caption,
                    parse_mode="html"
                )

                if os.path.exists(filepath):
                    os.remove(filepath)

                if sent_msg and sent_msg.media and sent_msg.media.document:
                    doc = sent_msg.media.document
                    database.save_cached_video(
                        url=url,
                        document_id=doc.id,
                        access_hash=doc.access_hash,
                        file_reference=doc.file_reference,
                        mime_type=doc.mime_type,
                        size=doc.size,
                        title=metadata["title"],
                        caption=caption
                    )
                    return doc, caption, metadata["title"]
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise e
            return None, None, None

        # Aguarda a tarefa com timeout de 5 segundos
        doc, caption, title = await asyncio.wait_for(quick_download_and_cache(), timeout=5.0)

        if doc:
            inline_id = str(hash(url) & 0xffffffff)
            res = await event.builder.document(
                file=doc,
                title=title or "Vídeo",
                description="Vídeo processado com sucesso!",
                text=caption,
                parse_mode="html",
                id=inline_id
            )
            await event.answer([res], cache_time=3600)
            return

    except Exception as e:
        logger.info(f"Incapaz de obter vídeo inline em tempo real ({e}). Sugerindo PV.")

    # Retorna uma mensagem pedindo para ir no PV
    builder = event.builder
    result = builder.article(
        title="Processando o vídeo...",
        description="Clique aqui para processar e registrar o vídeo no chat privado.",
        text=f"Por favor, me envie o link no privado primeiro para realizar o processamento: {url}",
        parse_mode="html"
    )
    await event.answer([result], cache_time=5)


async def safe_edit_message(msg, text):
    """Edita uma mensagem de forma segura contra erros comuns do Telegram."""
    try:
        await msg.edit(text, parse_mode="html")
    except errors.MessageNotModifiedError:
        pass
    except Exception as e:
        logger.warning(f"Erro ao editar mensagem: {e}")

if __name__ == "__main__":
    success, msg = config.validate_config()
    if not success:
        logger.critical(f"Configuração inválida: {msg}")
        exit(1)

    logger.info("Iniciando Bot de Download de Vídeos...")
    bot.start(bot_token=config.BOT_TOKEN)
    logger.info("Bot conectado e pronto para uso!")
    bot.run_until_disconnected()
