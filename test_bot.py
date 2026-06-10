from rich_formatter import parse_rich_message, get_utf16_len
from telethon.tl.types import MessageEntityBlockquote, MessageEntityBold, MessageEntityPre, MessageEntityTextUrl, MessageEntityItalic

def test_parsing():
    test_cases = [
        ("Normal text with **bold**", 1, MessageEntityBold, 17, 4),
        ("> Simple quote", 1, MessageEntityBlockquote, 0, 12),
        (">> Collapsed quote", 1, MessageEntityBlockquote, 0, 15),
        ("```mermaid\ngraph TD; A-->B;\n```", 1, MessageEntityTextUrl, 0, 20),
        ("$$a^2 + b^2 = c^2$$", 1, MessageEntityTextUrl, 0, 27),
    ]

    for text, expected_count, expected_type, exp_offset, exp_len in test_cases:
        clean_text, entities = parse_rich_message(text)
        print(f"Testing: {text}")
        if len(entities) != expected_count:
            print(f"  FAILED: Expected {expected_count} entities, got {len(entities)}")
            for i, e in enumerate(entities):
                print(f"    {i}: {type(e).__name__} offset={e.offset} length={e.length}")
            assert len(entities) == expected_count
        assert isinstance(entities[0], expected_type)
        if entities[0].offset != exp_offset or entities[0].length != exp_len:
             print(f"  FAILED: Expected offset={exp_offset}, len={exp_len}. Got offset={entities[0].offset}, len={entities[0].length}")
             assert entities[0].offset == exp_offset
             assert entities[0].length == exp_len
        print("  Pass!")

def test_emoji_utf16():
    # Emoji 🚀 is \U0001f680, which is 2 UTF-16 units
    text = "🚀 **bold**"
    clean_text, entities = parse_rich_message(text)
    print(f"Testing emoji: {text}")
    # "🚀 " is 2 + 1 = 3 UTF-16 units
    assert entities[0].offset == 3
    assert entities[0].length == 4
    assert isinstance(entities[0], MessageEntityBold)
    print("  Pass!")

def test_nesting():
    text = "> block with **bold** and *italic*"
    clean_text, entities = parse_rich_message(text)
    print(f"Testing nesting: {text}")
    # "> block with **bold** and *italic*"
    # -> "block with bold and italic" (Quote starts at 0)
    # Blockquote should contain the whole line
    # Markers for bold and italic are stripped.
    # Original len: 1 + 1 + 11 + 2 + 4 + 2 + 5 + 1 + 6 + 1 = 34
    # Stripped: 2 (marker > ) + 4 (markers **) + 2 (markers *) = 8
    # Final len: 34 - 8 = 26

    quote = [e for e in entities if isinstance(e, MessageEntityBlockquote)][0]
    bold = [e for e in entities if isinstance(e, MessageEntityBold)][0]
    italic = [e for e in entities if isinstance(e, MessageEntityItalic)][0]

    print(f"  Quote: offset={quote.offset}, length={quote.length}")
    print(f"  Bold: offset={bold.offset}, length={bold.length}")
    print(f"  Italic: offset={italic.offset}, length={italic.length}")

    assert quote.length == get_utf16_len(clean_text)
    assert bold.offset == 11
    assert italic.offset == 20
    print("  Pass!")

if __name__ == "__main__":
    try:
        test_parsing()
        test_emoji_utf16()
        test_nesting()
        print("\nAll advanced tests passed!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nTest failed: {e}")
        exit(1)
