from markdown_parser import parse_markdown_to_rich
from rich_models import PageBlockParagraph, PageBlockHeading, PageBlockMath, PageBlockTable

def test_markdown_to_rich():
    md = "# Heading\n\nThis is a paragraph with **bold** and $E=mc^2$ inline.\n\n$$E=mc^2$$\n\n| Col 1 | Col 2 |\n|---|---|\n| Cell 1 | Cell 2 |"
    blocks = parse_markdown_to_rich(md)

    print(f"Generated {len(blocks)} blocks.")
    for i, b in enumerate(blocks):
        print(f"Block {i}: {type(b).__name__}")

    assert any(isinstance(b, PageBlockHeading) for b in blocks)
    assert any(isinstance(b, PageBlockParagraph) for b in blocks)
    assert any(isinstance(b, PageBlockMath) for b in blocks)
    assert any(isinstance(b, PageBlockTable) for b in blocks)

    print("Test passed!")

if __name__ == "__main__":
    test_markdown_to_rich()
