import os
import re
import uuid
import yt_dlp

def get_platform_name(url):
    """Retorna o nome amigável da plataforma com base na URL."""
    url_lower = url.lower()
    if "tiktok" in url_lower:
        return "TikTok"
    elif "instagram" in url_lower:
        return "Instagram"
    elif "twitter" in url_lower or "x.com" in url_lower:
        return "Twitter / X"
    elif "youtube" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    return "Rede Social"

def download_video(url, progress_callback=None):
    """
    Usa yt-dlp para extrair metadados e baixar um vídeo de redes sociais.
    Retorna um dicionário com metadados do vídeo e o caminho do arquivo baixado.
    O callback de progresso recebe um dicionário com as informações do download.
    """
    # Gera um nome de arquivo temporário único no diretório atual ou /tmp
    temp_id = str(uuid.uuid4())
    out_template = f"temp_{temp_id}.%(ext)s"

    # Hook interno de progresso para yt-dlp
    def ytdl_hook(d):
        if progress_callback:
            status = d.get("status")
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            speed = d.get("speed", 0)
            eta = d.get("eta", 0)

            percentage = 0.0
            if total > 0:
                percentage = (downloaded / total) * 100

            progress_callback({
                "status": status,
                "downloaded_bytes": downloaded,
                "total_bytes": total,
                "percentage": percentage,
                "speed": speed,
                "eta": eta
            })

    # Opções robustas para evitar bloqueio e carregar metadados
    ydl_opts = {
        "outtmpl": out_template,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [ytdl_hook],
        # Configurações anti-bloqueio
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-Fetch-Mode": "navigate"
        },
        "socket_timeout": 15,
        "retries": 3,
        "fragment_retries": 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Primeiro extraímos as informações
            info = ydl.extract_info(url, download=True)

            # Localizar o arquivo baixado
            # O arquivo final pode ter extensão mp4 ou similar devido ao merge
            expected_prefix = f"temp_{temp_id}"
            local_filepath = None
            for filename in os.listdir("."):
                if filename.startswith(expected_prefix) and not filename.endswith(".part"):
                    local_filepath = filename
                    break

            if not local_filepath or not os.path.exists(local_filepath):
                raise FileNotFoundError("Não foi possível localizar o arquivo de vídeo baixado.")

            # Metadados extraídos
            title = info.get("title") or info.get("description") or "Vídeo Sem Título"
            # Trunca o título para exibição limpa se for longo demais
            if len(title) > 80:
                title = title[:77] + "..."

            description = info.get("description") or ""
            # Trunca descrição se for gigante para caber na legenda do telegram
            if len(description) > 500:
                description = description[:497] + "..."

            # Uploader/Autor
            # TikTok uploader é frequentemente o nickname
            author_username = info.get("uploader_id") or info.get("uploader")
            author_name = info.get("uploader") or info.get("creator") or "Autor Desconhecido"

            # Tentar limpar username de caracteres indesejados
            if author_username and not author_username.startswith("@"):
                # Limpa espaços ou tags comuns
                author_username = re.sub(r'\s+', '', author_username)

            duration = info.get("duration", 0)
            size = os.path.getsize(local_filepath)
            platform = get_platform_name(url)

            metadata = {
                "filepath": local_filepath,
                "title": title,
                "description": description,
                "author_username": author_username,
                "author_name": author_name,
                "duration": duration,
                "size": size,
                "platform": platform,
                "original_url": url,
            }
            return metadata

    except Exception as e:
        # Limpa arquivos órfãos caso ocorra erro
        expected_prefix = f"temp_{temp_id}"
        for filename in os.listdir("."):
            if filename.startswith(expected_prefix):
                try:
                    os.remove(filename)
                except Exception:
                    pass
        raise e
