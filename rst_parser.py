from docutils import core, nodes
from docutils.writers import Writer
from utils import escape_markdown_v2

class TelegramRstWriter(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = TelegramRstTranslator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

class TelegramRstTranslator(nodes.NodeVisitor):
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.output = []
        self.section_level = 0

    def astext(self):
        return ''.join(self.output)

    def visit_Text(self, node):
        self.output.append(escape_markdown_v2(node.astext()))

    def depart_Text(self, node):
        pass

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        self.output.append('\n\n')

    def visit_emphasis(self, node):
        self.output.append('_')

    def depart_emphasis(self, node):
        self.output.append('_')

    def visit_strong(self, node):
        self.output.append('*')

    def depart_strong(self, node):
        self.output.append('*')

    def visit_literal(self, node):
        self.output.append('`')
        self.output.append(escape_markdown_v2(node.astext(), is_code=True))
        raise nodes.SkipChildren

    def depart_literal(self, node):
        self.output.append('`')

    def visit_literal_block(self, node):
        self.output.append('```\n')
        self.output.append(escape_markdown_v2(node.astext(), is_code=True))
        self.output.append('\n```\n\n')
        raise nodes.SkipChildren

    def visit_title(self, node):
        self.output.append('*')

    def depart_title(self, node):
        self.output.append('*\n\n')

    def visit_list_item(self, node):
        self.output.append('• ')

    def depart_list_item(self, node):
        pass

    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        self.output.append('\n')

    def visit_reference(self, node):
        self.output.append('[')

    def depart_reference(self, node):
        refuri = node.get('refuri') or ''
        clean_link = refuri.replace('\\', '\\\\').replace(')', '\\)')
        self.output.append(f']({clean_link})')

    def unknown_visit(self, node):
        pass

    def unknown_departure(self, node):
        pass

def format_rst_advanced(text):
    try:
        parts = core.publish_parts(
            source=text,
            writer=TelegramRstWriter(),
            settings_overrides={'report_level': 5} # Suppress errors
        )
        return parts['whole'].strip()
    except Exception:
        # Simple rst to MarkdownV2 conversion via regex for common elements
        # Fallback if docutils fails
        import re
        processed = text
        # Headings
        processed = re.sub(r'^([=*-^~]{3,})\n(.+)\n\1', r'*\2*', processed, flags=re.MULTILINE)
        processed = re.sub(r'^(.+)\n([=*-^~]{3,})', r'*\1*', processed, flags=re.MULTILINE)
        # Bold/Italic
        processed = re.sub(r'\*\*(.+?)\*\*', r'*\1*', processed)
        processed = re.sub(r'\*(.+?)\*', r'_\1_', processed)
        # Inline code
        processed = re.sub(r'``(.+?)``', r'`\1`', processed)
        return escape_markdown_v2(processed)

if __name__ == "__main__":
    test_rst = "Hello **World**\n\n* List item 1\n* List item 2\n\n``code``\n\nSection\n======="
    print(format_rst_advanced(test_rst))
