import re
import urllib.parse
import base64
import zlib
from telethon.tl.types import (
    MessageEntityBold, MessageEntityItalic, MessageEntityCode,
    MessageEntityPre, MessageEntityTextUrl, MessageEntityStrike,
    MessageEntityUnderline, MessageEntitySpoiler, MessageEntityBlockquote
)

def get_utf16_len(s):
    """Calculates length of string in UTF-16 code units."""
    return len(s.encode('utf-16-le')) // 2

def get_kroki_url(diagram_type, diagram_source):
    """Generates a Kroki URL for the given diagram type and source."""
    # Kroki expects raw DEFLATE compression.
    # zlib.compress adds ZLIB headers (0x78...), so we use a Compressor with -zlib.MAX_WBITS for raw deflate.
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-zlib.MAX_WBITS)
    compressed = compressor.compress(diagram_source.encode('utf-8')) + compressor.flush()
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return f"https://kroki.io/{diagram_type}/png/{encoded}"

def parse_rich_message(text):
    """
    Parses a subset of markdown and returns (clean_text, entities).
    Calculates offsets and lengths in UTF-16 code units.
    """
    entities = []
    current_text = text

    # 1. Blockquotes (Handle these first as they are line-based)
    lines = current_text.split('\n')
    temp_text = ""
    for line in lines:
        if line.startswith('>> '):
            content = line[3:]
            start = get_utf16_len(temp_text) + (1 if temp_text else 0)
            length = get_utf16_len(content)
            entities.append(MessageEntityBlockquote(offset=start, length=length, collapsed=True))
            temp_text += ('\n' if temp_text else '') + content
        elif line.startswith('> '):
            content = line[2:]
            start = get_utf16_len(temp_text) + (1 if temp_text else 0)
            length = get_utf16_len(content)
            entities.append(MessageEntityBlockquote(offset=start, length=length, collapsed=False))
            temp_text += ('\n' if temp_text else '') + content
        else:
            temp_text += ('\n' if temp_text else '') + line
    current_text = temp_text

    # Helper to adjust existing entities
    def adjust_entities(entities, u_start, u_marker_len, u_inner_len):
        u_diff = u_marker_len - u_inner_len
        for ent in entities:
            # If entity starts after the marker start
            if ent.offset >= u_start + u_marker_len:
                ent.offset -= u_diff
            # If entity starts before and ends after or inside the marker
            elif ent.offset <= u_start:
                if ent.offset + ent.length > u_start:
                    # If it wraps the whole marker
                    if ent.offset + ent.length >= u_start + u_marker_len:
                        ent.length -= u_diff
                    # If it ends inside the marker
                    else:
                        ent.length = u_start - ent.offset + u_inner_len
            # If entity starts inside the marker
            elif ent.offset > u_start and ent.offset < u_start + u_marker_len:
                 ent.offset = u_start
                 if ent.offset + ent.length > u_start + u_marker_len:
                     ent.length -= u_diff
                 else:
                     ent.length = min(ent.length, u_inner_len)

    # 2. Pre and Diagrams
    kroki_types = ['mermaid', 'plantuml', 'graphviz', 'dot', 'ditaa', 'c4plantuml', 'erd', 'nomnoml', 'vega', 'vegalite', 'wavedrom', 'bpmn', 'bytefield', 'actdiag', 'nwdiag', 'packetdiag', 'rackdiag', 'seqdiag', 'svgbob', 'umlet', 'pikchr', 'structurizr', 'diagramsnet', 'excalidraw', 'tikz', 'symbolator']

    while True:
        match = re.search(r'```(\w*)\n?(.*?)\n?```', current_text, re.DOTALL)
        if not match: break

        start_char, end_char = match.span()
        lang = match.group(1).lower()
        code = match.group(2)

        prefix = current_text[:start_char]
        u_start = get_utf16_len(prefix)
        u_full_match_len = get_utf16_len(match.group(0))

        if lang in kroki_types:
            url = get_kroki_url(lang if lang != 'dot' else 'graphviz', code)
            replacement = f"📊 Diagram ({lang})"
            u_replacement_len = get_utf16_len(replacement)
            current_text = prefix + replacement + current_text[end_char:]
            adjust_entities(entities, u_start, u_full_match_len, u_replacement_len)
            entities.append(MessageEntityTextUrl(offset=u_start, length=u_replacement_len, url=url))
        else:
            current_text = prefix + code + current_text[end_char:]
            u_replacement_len = get_utf16_len(code)
            adjust_entities(entities, u_start, u_full_match_len, u_replacement_len)
            entities.append(MessageEntityPre(offset=u_start, length=u_replacement_len, language=lang or ''))

    # 3. LaTeX $$...$$
    while True:
        match = re.search(r'\$\$(.*?)\$\$', current_text)
        if not match: break
        start_char, end_char = match.span()
        formula = match.group(1)
        prefix = current_text[:start_char]
        u_start = get_utf16_len(prefix)
        u_full_match_len = get_utf16_len(match.group(0))

        url = f"https://latex.codecogs.com/png.latex?%5Cdpi%7B200%7D%20%5Cbg_white%20{urllib.parse.quote(formula)}"
        replacement = f"🔢 Formula: {formula}"
        u_replacement_len = get_utf16_len(replacement)
        current_text = prefix + replacement + current_text[end_char:]
        adjust_entities(entities, u_start, u_full_match_len, u_replacement_len)
        entities.append(MessageEntityTextUrl(offset=u_start, length=u_replacement_len, url=url))

    # 4. Inline entities and Links
    patterns = [
        (r'\*\*(.*?)\*\*', MessageEntityBold),
        (r'__(.*?)__', MessageEntityUnderline),
        (r'\*(.*?)\*', MessageEntityItalic),
        (r'_(.*?)_', MessageEntityItalic),
        (r'~~(.*?)~~', MessageEntityStrike),
        (r'\|\|(.*?)\|\|', MessageEntitySpoiler),
        (r'`(.*?)`', MessageEntityCode),
    ]

    for pattern, entity_class in patterns:
        while True:
            match = re.search(pattern, current_text, re.DOTALL)
            if not match: break

            start_char, end_char = match.span()
            inner_text = match.group(1)
            prefix = current_text[:start_char]
            u_start = get_utf16_len(prefix)
            u_full_match_len = get_utf16_len(match.group(0))
            u_inner_len = get_utf16_len(inner_text)

            current_text = prefix + inner_text + current_text[end_char:]
            adjust_entities(entities, u_start, u_full_match_len, u_inner_len)
            entities.append(entity_class(offset=u_start, length=u_inner_len))

    while True:
        match = re.search(r'\[(.*?)\]\((.*?)\)', current_text)
        if not match: break
        start_char, end_char = match.span()
        inner_text = match.group(1)
        url = match.group(2)
        prefix = current_text[:start_char]
        u_start = get_utf16_len(prefix)
        u_full_match_len = get_utf16_len(match.group(0))
        u_inner_len = get_utf16_len(inner_text)

        current_text = prefix + inner_text + current_text[end_char:]
        adjust_entities(entities, u_start, u_full_match_len, u_inner_len)
        entities.append(MessageEntityTextUrl(offset=u_start, length=u_inner_len, url=url))

    entities.sort(key=lambda x: x.offset)
    return current_text, entities
