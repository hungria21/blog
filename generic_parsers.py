import re
from rich_models import (
    PageBlockParagraph, PageBlockHeading, PageBlockMath, PageBlockList,
    RichTextPlain, RichTextBold, RichTextItalic
)

def parse_rst_to_rich(text):
    """Basic rST to Rich blocks converter."""
    blocks = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Headings
        if i + 1 < len(lines) and re.match(r'^[=*-^~]{3,}$', lines[i+1].strip()):
            blocks.append(PageBlockHeading(RichTextPlain(line), level=1))
            i += 2
            continue

        # List items
        if line.startswith('* '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('* '):
                items.append(RichTextPlain(lines[i].strip()[2:]))
                i += 1
            blocks.append(PageBlockList(items))
            continue

        # Normal paragraph
        blocks.append(PageBlockParagraph(RichTextPlain(line)))
        i += 1
    return blocks

def parse_adoc_to_rich(text):
    """Basic AsciiDoc to Rich blocks converter."""
    blocks = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue

        if line.startswith('= '):
            blocks.append(PageBlockHeading(RichTextPlain(line[2:]), level=1))
        elif line.startswith('* '):
            # Very basic, doesn't group lists
            blocks.append(PageBlockList([RichTextPlain(line[2:])]))
        else:
            blocks.append(PageBlockParagraph(RichTextPlain(line)))
    return blocks

def detect_syntax(text):
    if text.startswith('= ') or '\n= ' in text:
        return 'asciidoc'
    if '.. ' in text[:50] or '::\n' in text:
        return 'rest'
    if '\\begin{' in text or '$$' in text:
        return 'latex'
    return 'gfm'
