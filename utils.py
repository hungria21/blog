import re
from telegram.helpers import escape_markdown

def escape_markdown_v2(text, is_code=False):
    if is_code:
        return text.replace('\\', '\\\\').replace('`', '\\`')
    return escape_markdown(text, version=2)
