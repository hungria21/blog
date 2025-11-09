# coding: utf-8
import os
import time
import asyncio
import yt_dlp
from telethon import events
from userbot import client, logger
from userbot.config import COMMAND_PREFIX, DOWNLOADS_PATH, MAX_DOWNLOAD_SIZE
from userbot.utils import db_manager
from userbot.utils.decorators import handle_errors
from userbot.utils.rate_limiter import rate_limiter

# --- Configurações do yt-dlp ---
ydl_opts_video = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.join(DOWNLOADS_PATH, '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'max_filesize': MAX_DOWNLOAD_SIZE,
    'writethumbnail': True,
    'merge_output_format': 'mp4',
    'socket_timeout': 30,
    'retries': 3,
    'fragment_retries': 3,
}

ydl_opts_audio = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(DOWNLOADS_PATH, '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'max_filesize': MAX_DOWNLOAD_SIZE,
    'writethumbnail': True,
    'extract_audio': True,
    'audio_format': 'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# --- Funções Auxiliares ---
async def upload_progress_callback(current, total, event):
    """Callback para mostrar o progresso do upload."""
    percent = current / total * 100
    progress_str = (
        f"**Enviando...**\n"
        f"`Progresso`: {percent:.1f}%\n"
        f"`Enviado`: {current/1024/1024:.2f} MB / {total/1024/1024:.2f} MB"
    )
    try:
        await event.edit(progress_str)
        await asyncio.sleep(2) # Evitar flood
    except:
        pass

async def progress_hook(d, event):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)

        if total_bytes > 0:
            percent = downloaded_bytes / total_bytes * 100
            progress_str = (
                f"**Baixando...**\n"
                f"`Progresso`: {percent:.1f}%\n"
                f"`Tamanho`: {downloaded_bytes/1024/1024:.2f} MB / {total_bytes/1024/1024:.2f} MB\n"
                f"`Velocidade`: {speed/1024/1024:.2f} MB/s\n"
                f"`Tempo restante`: {eta}s"
            )
            try:
                await event.edit(progress_str)
                await asyncio.sleep(2) # Evitar flood
            except:
                pass

# --- Comandos ---
@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}ytdl (.*)$", from_me=True))
@handle_errors
async def ytdl(event):
    """Baixa um vídeo de uma URL."""
    url = event.pattern_match.group(1)
    await download_media(event, url, 'video')

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}ytaudio (.*)$", from_me=True))
@handle_errors
async def ytaudio(event):
    """Baixa o áudio de uma URL."""
    url = event.pattern_match.group(1)
    await download_media(event, url, 'audio')

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}ytinfo (.*)$", from_me=True))
@handle_errors
async def ytinfo(event):
    """Mostra informações de um vídeo sem baixar."""
    url = event.pattern_match.group(1)
    await event.edit("`Obtendo informações...`")

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            # Formatação da duração
            duration = time.strftime('%Hh %Mm %Ss', time.gmtime(info_dict.get('duration', 0)))

            # Formatação da data de upload
            upload_date = info_dict.get('upload_date')
            if upload_date:
                upload_date = f"{upload_date[6:8]}/{upload_date[4:6]}/{upload_date[0:4]}"
            else:
                upload_date = "N/A"

            caption = (
                f"**Título**: {info_dict.get('title', 'N/A')}\n\n"
                f"**Autor**: {info_dict.get('uploader', 'N/A')}\n"
                f"**Duração**: {duration}\n"
                f"**Visualizações**: {info_dict.get('view_count', 0):,}\n"
                f"**Data**: {upload_date}\n\n"
                f"**Descrição**:\n{info_dict.get('description', 'N/A')[:200]}..."
            )
            await event.edit(caption, link_preview=True)

    except Exception as e:
        await event.edit(f"`Erro ao obter informações: {e}`")

async def download_media(event, url, media_type):
    """Lógica principal para download de mídias."""
    await rate_limiter.wait_if_needed()
    await event.edit(f"`Processando URL...`")

    ydl_opts = ydl_opts_video if media_type == 'video' else ydl_opts_audio
    ydl_opts['progress_hooks'] = [lambda d: asyncio.ensure_future(progress_hook(d, event))]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            file_size = info_dict.get('filesize') or info_dict.get('filesize_approx', 0)

            if file_size > MAX_DOWNLOAD_SIZE:
                await event.edit(f"`Erro: O arquivo excede o tamanho máximo de {MAX_DOWNLOAD_SIZE/1024/1024/1024} GB.`")
                return

            await event.edit("`Iniciando download...`")
            ydl.download([url])

            # Pega o nome do arquivo baixado
            filename = ydl.prepare_filename(info_dict)
            if media_type == 'audio':
                filename = f"{os.path.splitext(filename)[0]}.mp3"

    except Exception as e:
        logger.error(f"Erro no download: {e}")
        await event.edit(f"`Erro ao baixar: {e}`")
        return

    if not os.path.exists(filename):
        await event.edit("`Erro: O arquivo não foi encontrado após o download.`")
        return

    # Upload para o Telegram
    await event.edit("`Download concluído. Iniciando upload...`")
    try:
        # Formatação da caption
        duration = time.strftime('%Hh %Mm %Ss', time.gmtime(info_dict.get('duration', 0)))
        upload_date = info_dict.get('upload_date')
        if upload_date:
            upload_date = f"{upload_date[6:8]}/{upload_date[4:6]}/{upload_date[0:4]}"
        else:
            upload_date = "N/A"

        caption = (
            f"**Título**: {info_dict.get('title', 'N/A')}\n\n"
            f"**Autor**: {info_dict.get('uploader', 'N/A')}\n"
            f"**Duração**: {duration}\n"
            f"**Visualizações**: {info_dict.get('view_count', 0):,}\n"
            f"**Data**: {upload_date}\n\n"
            f"#ytdl #download"
        )

        await client.send_file(
            event.chat_id,
            filename,
            caption=caption,
            reply_to=event.id,
            progress_callback=lambda c, t: asyncio.ensure_future(
                upload_progress_callback(c, t, event)
            )
        )
        db_manager.increment_stat("downloads_realizados")
        db_manager.increment_stat("uploads_realizados")
        db_manager.increment_stat("espaco_usado", os.path.getsize(filename))
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        await event.edit(f"`Erro ao enviar: {e}`")
    finally:
        os.remove(filename)
        if os.path.exists(f"{os.path.splitext(filename)[0]}.webp"):
             os.remove(f"{os.path.splitext(filename)[0]}.webp") # Remove thumbnail
        await event.delete()
