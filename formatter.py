import re
import mistune
from utils import escape_markdown_v2

class TelegramRenderer(mistune.HTMLRenderer):
    """
    Mistune renderer that produces Telegram MarkdownV2.
    Note: We inherit from HTMLRenderer but override methods to return MarkdownV2.
    """
    def text(self, text):
        return escape_markdown_v2(text)

    def emphasis(self, text, **attrs):
        return f'_{text}_'

    def strong(self, text, **attrs):
        return f'*{text}*'

    def strikethrough(self, text, **attrs):
        return f'~{text}~'

    def link(self, text, url, **attrs):
        # Escape ) and \ inside link URL
        clean_link = url.replace('\\', '\\\\').replace(')', '\\)')
        return f'[{text}]({clean_link})'

    def codespan(self, text, **attrs):
        return f'`{escape_markdown_v2(text, is_code=True)}`'

    def block_code(self, text, info=None, **attrs):
        lang = info.split()[0] if info else ""
        return f'``` {lang}\n{escape_markdown_v2(text, is_code=True)}```\n'

    def paragraph(self, text, **attrs):
        return f'{text}\n\n'

    def heading(self, text, level, **attrs):
        # Telegram MarkdownV2 doesn't have headings, so we use Bold
        return f'*{text}*\n\n'

    def list(self, text, ordered, **attrs):
        return f'{text}\n'

    def list_item(self, text, **attrs):
        # Remove trailing newlines from text which might come from paragraph()
        text = text.strip()
        return f'• {text}\n'

    def block_quote(self, text, **attrs):
        lines = text.strip().split('\n')
        quoted = '\n'.join([f'>{line}' for line in lines])
        return f'{quoted}\n\n'

    def thematic_break(self, **attrs):
        return '────────────────────\n\n'

def format_gfm(text):
    markdown = mistune.create_markdown(
        renderer=TelegramRenderer(),
        plugins=['strikethrough', 'table']
    )
    # Note: Table support in MarkdownV2 is limited (no native tables),
    # so we might need a custom table renderer or just ignore it for now.
    return markdown(text).strip()

def format_rst(text):
    from rst_parser import format_rst_advanced
    return format_rst_advanced(text)

def format_latex(text):
    # Simple LaTeX detection for inline and block math
    # We'll keep them as is but escaped, or wrap in code if it's a block
    if '$$' in text or '\\begin{' in text:
        return f'```latex\n{escape_markdown_v2(text, is_code=True)}\n```'

    # Escape for MarkdownV2
    return escape_markdown_v2(text)

def format_asciidoc(text):
    # Basic AsciiDoc conversion
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        # Heading
        heading_match = re.match(r'^={1,6} (.+)', line)
        if heading_match:
            # We escape the content but wrap it in *
            content = escape_markdown_v2(heading_match.group(1))
            formatted_lines.append(f"*{content}*")
            continue

        # Lists
        list_match = re.match(r'^\*+ (.+)', line)
        if list_match:
            content = escape_markdown_v2(list_match.group(1))
            formatted_lines.append(f"• {content}")
            continue

        formatted_lines.append(escape_markdown_v2(line))

    return '\n'.join(formatted_lines)

def detect_format(text):
    if text.startswith('= ') or '\n= ' in text:
        return 'asciidoc'
    if '.. ' in text[:50] or '::\n' in text:
        return 'rest'
    if '\\begin{' in text or '$$' in text:
        return 'latex'
    return 'gfm'

def format_message(text, syntax=None):
    if not syntax:
        syntax = detect_format(text)

    syntax = syntax.lower().strip('/')

    if syntax in ['gfm', 'commonmark', 'markdown', 'md']:
        return format_gfm(text)
    elif syntax in ['rest', 'rst']:
        return format_rst(text)
    elif syntax in ['latex', 'tex']:
        return format_latex(text)
    elif syntax in ['asciidoc', 'adoc']:
        return format_asciidoc(text)
    else:
        # Default to GFM if unknown
        return format_gfm(text)
