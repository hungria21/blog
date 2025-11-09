# coding: utf-8
import os
import json
import asyncio
import gallery_dl
from telethon import events
from userbot import client, logger
from userbot.config import COMMAND_PREFIX, DOWNLOADS_PATH, MAX_DOWNLOAD_SIZE
from userbot.utils import db_manager
from userbot.utils.decorators import handle_errors
from userbot.utils.rate_limiter import rate_limiter

# --- Configurações do gallery-dl ---
gallery_dl.config.set(("extractor",), "base-directory", DOWNLOADS_PATH)
gallery_dl.config.set(("extractor",), "timeout", 30.0)
gallery_dl.config.set(("extractor",), "retries", 3)
gallery_dl.config.set(("extractor",), "sleep", 1.0)
gallery_dl.config.set(("extractor",), "max-filesize", MAX_DOWNLOAD_SIZE)

# --- Comandos ---
@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}gallery (.*)$", from_me=True))
@handle_errors
async def gallery(event):
    """Baixa uma galeria de uma URL."""
    url = event.pattern_match.group(1)
    await download_gallery(event, url)

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}galleryinfo (.*)$", from_me=True))
@handle_errors
async def galleryinfo(event):
    """Mostra informações de uma galeria sem baixar."""
    url = event.pattern_match.group(1)
    await event.edit("`Obtendo informações da galeria...`")

    try:
        job = gallery_dl.job.Job(url)
        metadata = [data for data in job.run(get_metadata=True)]

        if not metadata:
            await event.edit("`Nenhuma mídia encontrada na URL.`")
            return

        # Extrai informações relevantes (exemplo, pode variar por site)
        first_item = metadata[0] if isinstance(metadata, list) else metadata
        author = first_item.get('author') or first_item.get('uploader') or 'N/A'
        platform = first_item.get('extractor') or 'N/A'
        num_media = len(first_item) if isinstance(first_item, list) else 1

        caption = (
            f"**Informações da Galeria**\n\n"
            f"**Plataforma**: {platform}\n"
            f"**Autor**: {author}\n"
            f"**Mídias**: {num_media}\n"
            f"**URL**: `{url}`"
        )
        await event.edit(caption)

    except Exception as e:
        await event.edit(f"`Erro ao obter informações: {e}`")

async def download_gallery(event, url):
    """Lógica principal para download de galerias."""
    await rate_limiter.wait_if_needed()
    await event.edit("`Processando URL...`")

    try:
        # Pega as informações sem baixar
        job = gallery_dl.job.Job(url)
        metadata = [data for data in job.run(get_metadata=True)]

        if not metadata:
            await event.edit("`Nenhuma mídia encontrada na URL.`")
            return

        files_to_download = []
        total_size = 0

        # O gallery-dl pode retornar metadados aninhados
        def find_files(data):
            nonlocal total_size
            if isinstance(data, list):
                for item in data:
                    find_files(item)
            elif isinstance(data, dict):
                if data.get('dest'):
                    files_to_download.append(data['dest'])
                    total_size += data.get('size', 0)

        find_files(metadata)

        if len(files_to_download) > 10:
            await event.edit(f"`A galeria contém {len(files_to_download)} mídias. O limite é 10. Canceleando.`")
            return

        if total_size > MAX_DOWNLOAD_SIZE:
            await event.edit(f"`O tamanho total da galeria excede o limite de {MAX_DOWNLOAD_SIZE/1024/1024/1024} GB.`")
            return

        # Baixa os arquivos
        await event.edit(f"`Baixando {len(files_to_download)} mídias...`")
        gallery_dl.job.Job(url).run()

        # Formatação da caption
        first_item = metadata[0] if isinstance(metadata, list) else metadata
        author = first_item.get('author') or first_item.get('uploader') or 'N/A'
        platform = first_item.get('extractor') or 'N/A'

        caption = (
            f"**Galeria de {platform}**\n\n"
            f"**Autor**: {author}\n"
            f"**URL**: `{url}`\n\n"
            f"#gallery #download"
        )

        # Envia como álbum se houver mais de uma mídia
        if len(files_to_download) > 1:
            await client.send_file(
                event.chat_id,
                files_to_download,
                caption=caption,
                reply_to=event.id
            )
        elif files_to_download:
            await client.send_file(
                event.chat_id,
                files_to_download[0],
                caption=caption,
                reply_to=event.id
            )

        db_manager.increment_stat("downloads_realizados", len(files_to_download))
        db_manager.increment_stat("uploads_realizados", len(files_to_download))
        db_manager.increment_stat("espaco_usado", total_size)

    except Exception as e:
        logger.error(f"Erro no gallery-dl: {e}")
        await event.edit(f"`Erro ao baixar a galeria: {e}`")
    finally:
        # Limpa os arquivos baixados
        for filepath in files_to_download:
            if os.path.exists(filepath):
                os.remove(filepath)
        await event.delete()
