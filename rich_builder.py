from rich_models import InputRichMessage
from markdown_parser import parse_markdown_to_rich
from generic_parsers import parse_rst_to_rich, parse_adoc_to_rich, detect_syntax

class RichMessageBuilder:
    def __init__(self):
        pass

    def from_text(self, text: str, syntax: str = None) -> InputRichMessage:
        if not syntax:
            syntax = detect_syntax(text)

        syntax = syntax.lower().strip('/')

        if syntax in ['gfm', 'markdown', 'md', 'latex', 'tex']:
            blocks = parse_markdown_to_rich(text)
        elif syntax in ['rest', 'rst']:
            blocks = parse_rst_to_rich(text)
        elif syntax in ['asciidoc', 'adoc']:
            blocks = parse_adoc_to_rich(text)
        else:
            blocks = parse_markdown_to_rich(text)

        return InputRichMessage(blocks)

    def build_payload(self, text: str, syntax: str = None) -> dict:
        rich_msg = self.from_text(text, syntax)
        return rich_msg.to_dict()

    def split_rich_payload(self, payload: dict, max_blocks: int = 500) -> list:
        """Splits payload into multiple ones if block count exceeds max_blocks."""
        blocks = payload.get("blocks", [])
        if len(blocks) <= max_blocks:
            return [payload]

        split_payloads = []
        for i in range(0, len(blocks), max_blocks):
            new_payload = payload.copy()
            new_payload["blocks"] = blocks[i:i+max_blocks]
            split_payloads.append(new_payload)
        return split_payloads
