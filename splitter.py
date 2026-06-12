from telegram.constants import MessageLimit

def split_message(text, limit=MessageLimit.MAX_TEXT_LENGTH):
    """Splits a long message into multiple parts."""
    if len(text) <= limit:
        return [text]

    parts = []
    while text:
        if len(text) <= limit:
            parts.append(text)
            break

        # Try to split at the last newline before the limit
        split_at = text.rfind('\n', 0, limit)
        if split_at == -1:
            # If no newline, just split at the limit
            split_at = limit

        parts.append(text[:split_at])
        text = text[split_at:].lstrip()

    return parts
