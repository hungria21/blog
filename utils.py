import html

def generate_progress_bar(percentage, length=20):
    """
    Gera uma barra de progresso em texto simples usando blocos cheios e vazios.
    Evita emojis decorativos de acordo com as restrições estéticas do projeto.
    """
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100

    filled_length = int(round(length * percentage / 100))
    bar = "█" * filled_length + "░" * (length - filled_length)
    return f"[{bar}] {percentage:.1f}%"

def format_size(size_bytes):
    """Formata bytes em strings legíveis por humanos (KB, MB)."""
    if not size_bytes:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def escape_html(text):
    """Escapa caracteres HTML para evitar erros de renderização no Telegram."""
    if not text:
        return ""
    return html.escape(text)

def format_rich_caption(title, description, author_username, author_name, platform, original_url):
    """
    Gera uma legenda elegante usando a formatação rica (HTML) suportada pelo Telegram.
    Não usa emojis decorativos para manter uma estética profissional e limpa.
    Menciona o autor/username se disponível com links dinâmicos dependendo da plataforma.
    """
    title_esc = escape_html(title or "Vídeo Sem Título")
    desc_esc = escape_html(description or "")
    author_name_esc = escape_html(author_name or "Autor Desconhecido")
    platform_esc = escape_html(platform or "Rede Social")

    # Determina o link do autor de acordo com a plataforma detectada
    author_mention = f"<b>{author_name_esc}</b>"
    if author_username:
        author_username_clean = author_username.strip("@")
        platform_lower = platform_esc.lower()

        if "tiktok" in platform_lower:
            author_url = f"https://www.tiktok.com/@{author_username_clean}"
            author_mention = f"<a href=\"{author_url}\">@{author_username_clean}</a>"
        elif "instagram" in platform_lower:
            author_url = f"https://www.instagram.com/{author_username_clean}/"
            author_mention = f"<a href=\"{author_url}\">@{author_username_clean}</a>"
        elif "twitter" in platform_lower or "x.com" in platform_lower or "x" in platform_lower:
            author_url = f"https://x.com/{author_username_clean}"
            author_mention = f"<a href=\"{author_url}\">@{author_username_clean}</a>"
        elif "youtube" in platform_lower:
            author_url = f"https://www.youtube.com/@{author_username_clean}"
            author_mention = f"<a href=\"{author_url}\">@{author_username_clean}</a>"
        else:
            # Padrão amigável se a plataforma for desconhecida
            author_mention = f"@{author_username_clean}"

    caption_lines = [
        f"<b>{title_esc}</b>",
    ]

    if desc_esc:
        caption_lines.append(f"<i>{desc_esc}</i>")

    caption_lines.append("") # Linha em branco
    caption_lines.append(f"<b>Autor:</b> {author_mention}")
    caption_lines.append(f"<b>Plataforma:</b> {platform_esc}")
    caption_lines.append(f"<b>Link Original:</b> <a href=\"{original_url}\">Acessar Postagem</a>")

    return "\n".join(caption_lines)
