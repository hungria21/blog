"""
Plugin: yt-dlp
Download de vídeos e áudios de diversas plataformas
"""

import os
import asyncio
import yt_dlp
from pathlib import Path
from telethon import events
import re

def format_size(bytes_size):
    """Formata tamanho de arquivo"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def format_duration(seconds):
    """Formata duração em tempo legível"""
    if not seconds:
        return "N/A"
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    return f"{minutes}m {seconds}s"

def sanitize_filename(text, max_length=100):
    """Remove caracteres inválidos do nome do arquivo"""
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0]
    return text

def format_description(info):
    """Formata descrição com metadados"""
    lines = []

    # Título
    if info.get('title'):
        lines.append(f"**{info['title']}**\n")

    # Uploader
    if info.get('uploader'):
        lines.append(f"👤 **Canal:** {info['uploader']}")

    # Data de upload
    if info.get('upload_date'):
        date_str = info['upload_date']
        formatted_date = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[0:4]}"
        lines.append(f"📅 **Data:** {formatted_date}")

    # Visualizações
    if info.get('view_count'):
        lines.append(f"👁️ **Visualizações:** {info['view_count']:,}")

    # Duração
    if info.get('duration'):
        lines.append(f"⏱️ **Duração:** {format_duration(info['duration'])}")

    # Descrição original (limitada)
    if info.get('description'):
        desc = info['description'][:300]
        if len(info['description']) > 300:
            desc += "..."
        lines.append(f"\n📝 **Descrição:**\n{desc}")

    # Hashtags
    tags = []
    if info.get('tags'):
        tags = [f"#{tag.replace(' ', '_')}" for tag in info['tags'][:5]]
    if tags:
        lines.append(f"\n🏷️ {' '.join(tags)}")

    # URL
    if info.get('webpage_url'):
        lines.append(f"\n🔗 {info['webpage_url']}")

    return "\n".join(lines)

def setup(bot, Config, stats, safe_send, safe_edit):
    """Configura o plugin"""

    download_path = Path(Config.DOWNLOAD_PATH) / "ytdl"
    download_path.mkdir(exist_ok=True)

    @bot.on(events.NewMessage(outgoing=True, pattern=r'^\.ytdl\s+(.+)'))
    async def ytdl_handler(event):
        """Download de vídeos/áudios usando yt-dlp"""
        stats.commands_executed += 1

        url = event.pattern_match.group(1).strip()

        # Validar URL
        if not url.startswith(('http://', 'https://')):
            await safe_edit(event, "❌ URL inválida! Use: `.ytdl <url>`")
            return

        status_msg = await event.edit("🔍 Obtendo informações...")

        try:
            # Configuração do yt-dlp
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': str(download_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'merge_output_format': 'mp4',
                'max_filesize': 2000 * 1024 * 1024,  # 2GB limite Telegram
                'socket_timeout': 30,
                'retries': 3,
            }

            # Extrair informações
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            if not info:
                await safe_edit(status_msg, "❌ Não foi possível obter informações do vídeo")
                return

            # Exibir informações
            title = info.get('title', 'Sem título')
            duration = format_duration(info.get('duration'))
            uploader = info.get('uploader', 'Desconhecido')

            await safe_edit(
                status_msg,
                f"📹 **{title}**\n"
                f"👤 {uploader}\n"
                f"⏱️ {duration}\n\n"
                f"⬇️ Iniciando download..."
            )

            # Hook de progresso
            downloaded_size = [0]
            last_update = [0]

            def progress_hook(d):
                if d['status'] == 'downloading':
                    downloaded_size[0] = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                    # Atualizar a cada 5 segundos
                    import time
                    current_time = time.time()
                    if current_time - last_update[0] > 5:
                        last_update[0] = current_time

                        if total > 0:
                            percent = (downloaded_size[0] / total) * 100
                            speed = d.get('speed', 0)
                            eta = d.get('eta', 0)

                            progress_text = (
                                f"📥 **Baixando...**\n\n"
                                f"📹 {title[:50]}...\n"
                                f"📊 Progresso: {percent:.1f}%\n"
                                f"💾 {format_size(downloaded_size[0])} / {format_size(total)}\n"
                                f"⚡ Velocidade: {format_size(speed)}/s\n"
                                f"⏱️ Restante: {eta}s"
                            )

                            bot.loop.create_task(safe_edit(status_msg, progress_text))

            ydl_opts['progress_hooks'] = [progress_hook]

            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                download_info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(download_info)

            if not os.path.exists(filename):
                await safe_edit(status_msg, "❌ Erro: arquivo não encontrado após download")
                return

            file_size = os.path.getsize(filename)

            # Verificar limite do Telegram (2GB)
            if file_size > 2000 * 1024 * 1024:
                os.remove(filename)
                await safe_edit(
                    status_msg,
                    f"❌ Arquivo muito grande ({format_size(file_size)})\n"
                    f"Limite do Telegram: 2GB"
                )
                return

            await safe_edit(
                status_msg,
                f"📤 Enviando arquivo...\n"
                f"📦 Tamanho: {format_size(file_size)}"
            )

            # Preparar caption formatada
            caption = format_description(download_info)

            # Upload com progresso
            upload_msg = await status_msg.edit(
                f"📤 **Enviando...**\n"
                f"📦 {format_size(file_size)}"
            )

            # Enviar arquivo
            async with bot.action(event.chat_id, 'document'):
                sent_msg = await bot.send_file(
                    event.chat_id,
                    filename,
                    caption=caption[:1024],  # Limite do Telegram
                    supports_streaming=True,
                    force_document=False,
                    thumb=None,
                )

            stats.files_downloaded += 1

            # Limpar
            await upload_msg.delete()
            os.remove(filename)

            await asyncio.sleep(2)

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            await safe_edit(
                status_msg,
                f"❌ **Erro no download:**\n`{error_msg[:200]}`"
            )
            stats.errors += 1

        except Exception as e:
            await safe_edit(
                status_msg,
                f"❌ **Erro inesperado:**\n`{str(e)[:200]}`"
            )
            stats.errors += 1

        finally:
            # Limpar arquivos residuais
            for file in download_path.glob("*"):
                try:
                    if file.is_file():
                        file.unlink()
                except:
                    pass

    # Comando de áudio
    @bot.on(events.NewMessage(outgoing=True, pattern=r'^\.ytmp3\s+(.+)'))
    async def ytmp3_handler(event):
        """Download apenas de áudio"""
        stats.commands_executed += 1

        url = event.pattern_match.group(1).strip()

        if not url.startswith(('http://', 'https://')):
            await safe_edit(event, "❌ URL inválida! Use: `.ytmp3 <url>`")
            return

        status_msg = await event.edit("🎵 Baixando áudio...")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_path / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            # Encontrar arquivo MP3
            base_filename = ydl.prepare_filename(info)
            mp3_filename = os.path.splitext(base_filename)[0] + '.mp3'

            if not os.path.exists(mp3_filename):
                await safe_edit(status_msg, "❌ Erro ao processar áudio")
                return

            caption = format_description(info)

            await status_msg.edit("📤 Enviando áudio...")

            await bot.send_file(
                event.chat_id,
                mp3_filename,
                caption=caption[:1024],
                attributes=[],
            )

            stats.files_downloaded += 1

            await status_msg.delete()
            os.remove(mp3_filename)

        except Exception as e:
            await safe_edit(status_msg, f"❌ Erro: `{str(e)[:200]}`")
            stats.errors += 1