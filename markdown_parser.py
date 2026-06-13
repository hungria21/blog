import mistune
import re
from rich_models import (
    PageBlockParagraph, PageBlockHeading, PageBlockPreformatted,
    PageBlockMath, PageBlockDivider, PageBlockTable, PageBlockList,
    RichTextPlain, RichTextBold, RichTextItalic, RichTextUnderline,
    RichTextStrikethrough, RichTextUrl, RichTextMath, RichTextConcat
)

class RichMessageRenderer(mistune.BaseRenderer):
    def __init__(self):
        super().__init__()

    def render_token(self, token, state):
        func = self._get_method(token['type'])
        attrs = token.get('attrs', {})

        if 'children' in token:
            children = self.render_tokens(token['children'], state)
            return func(children, **attrs)

        if 'raw' in token:
            return func(token['raw'], **attrs)

        return func(**attrs)

    def text(self, text):
        return RichTextPlain(text)

    def emphasis(self, children):
        return RichTextItalic(children)

    def strong(self, children):
        return RichTextBold(children)

    def strikethrough(self, children):
        return RichTextStrikethrough(children)

    def link(self, children, url, title=None):
        return RichTextUrl(children, url)

    def codespan(self, text):
        return RichTextPlain(f"`{text}`")

    def block_code(self, text, info=None):
        return PageBlockPreformatted(RichTextPlain(text), language=info or "")

    def paragraph(self, children):
        return PageBlockParagraph(children)

    def heading(self, children, level):
        return PageBlockHeading(children, level=min(level, 6))

    def list(self, children, ordered, start=None):
        # children is a RichTextConcat of list_items
        items = children.texts if isinstance(children, RichTextConcat) else [children]
        return PageBlockList(items, ordered=ordered)

    def list_item(self, children):
        return children

    def thematic_break(self):
        return PageBlockDivider()

    def blank_line(self):
        return None

    def table(self, children):
        # children should be list of row objects
        rows = children.texts if isinstance(children, RichTextConcat) else [children]
        return PageBlockTable(rows)

    def table_row(self, children):
        return children.texts if isinstance(children, RichTextConcat) else [children]

    def table_cell(self, children, **attrs):
        return children

    def table_head(self, children, **attrs):
        return children

    def table_body(self, children, **attrs):
        return children

    def render_tokens(self, tokens, state):
        res = []
        for tok in tokens:
            out = self.render_token(tok, state)
            if out:
                res.append(out)

        if not res:
            return RichTextPlain("")
        if len(res) == 1:
             return res[0]

        return RichTextConcat(res)

    def __call__(self, tokens, state):
        return self.render_tokens(tokens, state)

def parse_markdown_to_rich(text):
    # Handle Math placeholders
    import re
    math_blocks = {}
    def math_block_repl(m):
        placeholder = f"MATHBLOCK{len(math_blocks)}Z"
        math_blocks[placeholder] = m.group(1)
        return f"\n\n{placeholder}\n\n"

    text = re.sub(r'\$\$(.*?)\$\$', math_block_repl, text, flags=re.DOTALL)

    inline_math = {}
    def inline_math_repl(m):
        placeholder = f"MATHINLINE{len(inline_math)}Z"
        inline_math[placeholder] = m.group(1)
        return placeholder

    text = re.sub(r'\$(.*?)\$', inline_math_repl, text)

    markdown = mistune.create_markdown(renderer=RichMessageRenderer(), plugins=['strikethrough', 'table'])
    res = markdown(text)

    if isinstance(res, RichTextConcat):
        blocks = res.texts
    elif isinstance(res, list):
        blocks = res
    else:
        blocks = [res]

    # Flatten if nested list
    if blocks and isinstance(blocks[0], list):
        blocks = [item for sublist in blocks for item in sublist]

    final_blocks = []
    for b in blocks:
        if isinstance(b, PageBlockParagraph) and isinstance(b.text, RichTextPlain) and b.text.text.strip() in math_blocks:
            final_blocks.append(PageBlockMath(math_blocks[b.text.text.strip()]))
        else:
            # Post-process inline math
            if isinstance(b, PageBlockParagraph):
                b.text = _process_inline_math(b.text, inline_math)
            final_blocks.append(b)

    return final_blocks

def _process_inline_math(rich_text, math_map):
    if isinstance(rich_text, RichTextPlain):
        parts = re.split(r'(MATHINLINE\d+Z)', rich_text.text)
        if len(parts) == 1:
            return rich_text
        res = []
        for p in parts:
            if p in math_map:
                res.append(RichTextMath(math_map[p]))
            elif p:
                res.append(RichTextPlain(p))
        return RichTextConcat(res)
    elif isinstance(rich_text, RichTextConcat):
        rich_text.texts = [_process_inline_math(t, math_map) for t in rich_text.texts]
        return rich_text
    elif hasattr(rich_text, 'text'):
        rich_text.text = _process_inline_math(rich_text.text, math_map)
        return rich_text
    return rich_text
