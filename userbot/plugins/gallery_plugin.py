"""
Plugin: gallery-dl
Download de galerias de imagens de diversas plataformas
(Instagram, Twitter, Reddit, Pinterest, etc)
"""

import os
import asyncio
import json
import subprocess
from pathlib import Path
from telethon import events
from datetime import datetime
import re

def format_size(bytes_size):
    """Formata tamanho de arquivo"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def sanitize_text(text, max_length=200):
    """Sanitiza texto para caption"""
    if not text:
        return ""
    text = re.sub(r'[^\w\s\-.,!?@#]', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + "..."
    return text

def create_caption(metadata, platform=""):
    """Cria caption formatada com metadados"""
    lines = []

    # Plataforma
    if platform:
        platform_emoji = {
            'instagram': '📷',
            'twitter': '🐦',
            'reddit': '🤖',
            'pinterest': '📌',
            'tumblr': '📝',
        }
        emoji = platform_emoji.get(platform.lower(), '🌐')
        lines.append(f"{emoji} **{platform.title()}**\n")

    # Autor/Usuário
    author = metadata.get('author') or metadata.get('username') or metadata.get('user')
    if author:
        lines.append(f"👤 **Autor:** @{author}")

    # Título/Descrição
    description = metadata.get('description') or metadata.get('title') or metadata.get('caption')
    if description:
        clean_desc = sanitize_text(description, max_length=300)
        if clean_desc:
            lines.append(f"\n💬 {clean_desc}")

    # Data
    date = metadata.get('date') or metadata.get('created_at')
    if date:
        if isinstance(date, str):
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = dt.strftime('%d/%m/%Y %H:%M')
                lines.append(f"\n📅 {date_str}")
            except:
                pass

    # Likes/Engajamento
    likes = metadata.get('likes') or metadata.get('favorite_count')
    if likes:
        lines.append(f"❤️ {likes:,} curtidas")

    comments = metadata.get('comments') or metadata.get('comment_count')
    if comments:
        lines.append(f"💬 {comments:,} comentários")

    # Hashtags
    tags = []

    # Extrair hashtags da descrição
    if description:
        found_tags = re.findall(r'#(\w+)', description)
        tags.extend(found_tags[:5])

    # Tags do metadata
    if metadata.get('tags') and isinstance(metadata['tags'], list):
        tags.extend([str(t).replace(' ', '_') for t in metadata['tags'][:5]])

    if tags:
        unique_tags = list(dict.fromkeys(tags))[:5]  # Remove duplicatas
        tag_str = ' '.join([f"#{tag}" for tag in unique_tags])
        lines.append(f"\n🏷️ {tag_str}")

    # URL
    url = metadata.get('url') or metadata.get('post_url')
    if url:
        lines.append(f"\n🔗 {url}")

    return "\n".join(lines)

def setup(bot, Config, stats, safe_send, safe_edit):
    """Configura o plugin"""

    download_path = Path(Config.DOWNLOAD_PATH) / "gallery"
    download_path.mkdir(exist_ok=True)

    @bot.on(events.NewMessage(outgoing=True, pattern=r'^\.gdl\s+(.+)'))
    async def gallerydl_handler(event):
        """Download de galerias usando gallery-dl"""
        stats.commands_executed += 1

        url = event.pattern_match.group(1).strip()

        # Validar URL
        if not url.startswith(('http://', 'https://')):
            await safe_edit(event, "❌ URL inválida! Use: `.gdl <url>`")
            return

        # Detectar plataforma
        platform = "Desconhecido"
        if 'instagram.com' in url:
            platform = "Instagram"
        elif 'twitter.com' in url or 'x.com' in url:
            platform = "Twitter"
        elif 'reddit.com' in url:
            platform = "Reddit"
        elif 'pinterest.com' in url:
            platform = "Pinterest"
        elif 'tumblr.com' in url:
            platform = "Tumblr"

        status_msg = await event.edit(f"🔍 Analisando {platform}...")

        # Criar pasta temporária para este download
        import uuid
        temp_id = str(uuid.uuid4())[:8]
        temp_path = download_path / temp_id
        temp_path.mkdir(exist_ok=True)

        try:
            # Configurar gallery-dl
            config = {
                'extractor': {
                    'base-directory': str(temp_path),
                    'skip': False,
                },
            }

            config_file = temp_path / 'config.json'
            with open(config_file, 'w') as f:
                json.dump(config, f)

            await safe_edit(
                status_msg,
                f"📥 **Baixando de {platform}...**\n"
                f"🔗 Processando galeria..."
            )

            # Executar gallery-dl
            process = await asyncio.create_subprocess_exec(
                'gallery-dl',
                '--config', str(config_file),
                '--write-metadata',
                '--no-mtime',
                url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='ignore')[:300]
                await safe_edit(
                    status_msg,
                    f"❌ **Erro no download:**\n`{error_msg}`\n\n"
                    f"💡 Certifique-se de que gallery-dl está instalado:\n"
                    f"`pip install gallery-dl`"
                )
                stats.errors += 1
                return

            # Encontrar arquivos baixados
            files = []
            metadata_files = {}

            for file in temp_path.rglob('*'):
                if file.is_file():
                    if file.suffix == '.json':
                        # Arquivo de metadata
                        key = file.stem
                        with open(file, 'r', encoding='utf-8') as f:
                            metadata_files[key] = json.load(f)
                    elif file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm']:
                        files.append(file)

            if not files:
                await safe_edit(
                    status_msg,
                    f"❌ Nenhum arquivo foi baixado.\n"
                    f"Verifique se a URL é válida e pública."
                )
                return

            # Ordenar arquivos
            files.sort()
            total_files = len(files)
            total_size = sum(f.stat().st_size for f in files)

            await safe_edit(
                status_msg,
                f"✅ **Download concluído!**\n\n"
                f"📁 Arquivos: {total_files}\n"
                f"💾 Tamanho total: {format_size(total_size)}\n\n"
                f"📤 Enviando arquivos..."
            )

            # Enviar arquivos
            sent_count = 0
            album_files = []

            for idx, file in enumerate(files, 1):
                try:
                    file_size = file.stat().st_size

                    # Limite do Telegram: 2GB por arquivo
                    if file_size > 2000 * 1024 * 1024:
                        await safe_send(
                            event,
                            f"⚠️ Arquivo {file.name} muito grande ({format_size(file_size)}), pulando..."
                        )
                        continue

                    # Buscar metadata correspondente
                    metadata = {}
                    for key, meta in metadata_files.items():
                        if key in file.stem:
                            metadata = meta
                            break

                    # Criar caption
                    caption = create_caption(metadata, platform)
                    if not caption:
                        caption = f"📷 {platform}\n{idx}/{total_files}"

                    # Atualizar status
                    if idx % 5 == 0 or idx == total_files:
                        await safe_edit(
                            status_msg,
                            f"📤 **Enviando...**\n"
                            f"📊 Progresso: {idx}/{total_files}\n"
                            f"✅ Enviados: {sent_count}"
                        )

                    # Enviar arquivo
                    async with bot.action(event.chat_id, 'photo' if file.suffix.lower() != '.mp4' else 'video'):
                        await bot.send_file(
                            event.chat_id,
                            file,
                            caption=caption[:1024],
                            force_document=False,
                            supports_streaming=True,
                        )

                    sent_count += 1
                    stats.files_downloaded += 1

                    # Delay anti-flood
                    await asyncio.sleep(2)

                except Exception as e:
                    await safe_send(
                        event,
                        f"⚠️ Erro ao enviar {file.name}: `{str(e)[:100]}`"
                    )
                    stats.errors += 1

            # Mensagem final
            await safe_edit(
                status_msg,
                f"✅ **Concluído!**\n\n"
                f"📁 Total: {total_files} arquivos\n"
                f"✅ Enviados: {sent_count}\n"
                f"💾 {format_size(total_size)}\n"
                f"🌐 Origem: {platform}"
            )

        except FileNotFoundError:
            await safe_edit(
                status_msg,
                "❌ **gallery-dl não encontrado!**\n\n"
                "📦 Instale com:\n"
                "`pip install gallery-dl`\n\n"
                "Ou use apt/brew dependendo do seu sistema."
            )
            stats.errors += 1

        except Exception as e:
            await safe_edit(
                status_msg,
                f"❌ **Erro inesperado:**\n`{str(e)[:300]}`"
            )
            stats.errors += 1

        finally:
            # Limpar arquivos temporários
            import shutil
            try:
                shutil.rmtree(temp_path)
            except:
                pass

    # Comando info de plataformas suportadas
    @bot.on(events.NewMessage(outgoing=True, pattern=r'^\.gdlinfo$'))
    async def gdlinfo_handler(event):
        """Mostra plataformas suportadas"""
        stats.commands_executed += 1

        info_text = """
🌐 **PLATAFORMAS SUPORTADAS**

gallery-dl suporta mais de 100 sites!

**Principais:**
📷 **Instagram** - Posts, stories, reels
🐦 **Twitter/X** - Tweets, mídia
🤖 **Reddit** - Posts, galerias
📌 **Pinterest** - Pins, boards
📝 **Tumblr** - Posts, blogs
📺 **DeviantArt** - Arte, galerias
🎨 **ArtStation** - Portfólios
🖼️ **Imgur** - Álbuns, imagens
💬 **Pixiv** - Arte, mangá

**Como usar:**
`.gdl <url>` - Download da galeria

**Requisito:**
`pip install gallery-dl`

Para lista completa, visite:
https://github.com/mikf/gallery-dl
"""

        await safe_edit(event, info_text.strip())