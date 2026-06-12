from formatter import format_message

def test_markdown():
    print("Testing Markdown...")
    md_text = "# Title\n\n**Bold** and *Italic*\n\n- Item 1\n- Item 2\n\n`code` and [link](https://example.com)"
    formatted = format_message(md_text, syntax='gfm')
    print(f"Input:\n{md_text}")
    print(f"Output:\n{formatted}")
    assert "*Title*" in formatted
    assert "*Bold*" in formatted
    assert "_Italic_" in formatted
    assert "• Item 1" in formatted
    assert "`code`" in formatted
    print("Markdown test passed!\n")

def test_rst():
    print("Testing reStructuredText...")
    rst_text = "Title\n=====\n\n**Bold** and *Italic*\n\n* Item 1\n* Item 2\n\n``code`` and `link <https://example.com>`_"
    formatted = format_message(rst_text, syntax='rst')
    print(f"Input:\n{rst_text}")
    print(f"Output:\n{formatted}")
    assert "*Title*" in formatted
    assert "*Bold*" in formatted
    assert "_Italic_" in formatted
    assert "• Item 1" in formatted
    assert "`code`" in formatted
    print("reStructuredText test passed!\n")

def test_asciidoc():
    print("Testing AsciiDoc...")
    adoc_text = "= Title\n\n*Bold* and _Italic_\n\n* Item 1\n* Item 2\n\n`code`"
    formatted = format_message(adoc_text, syntax='asciidoc')
    print(f"Input:\n{adoc_text}")
    print(f"Output:\n{formatted}")
    assert "*Title*" in formatted
    assert "• Item 1" in formatted
    print("AsciiDoc test passed!\n")

def test_latex():
    print("Testing LaTeX...")
    latex_text = "\\begin{equation}\ne = mc^2\n\\end{equation}"
    formatted = format_message(latex_text, syntax='latex')
    print(f"Input:\n{latex_text}")
    print(f"Output:\n{formatted}")
    assert "```latex" in formatted
    print("LaTeX test passed!\n")

def test_autodetect():
    print("Testing Auto-detection...")
    assert format_message("= AsciiDoc Title") == format_message("= AsciiDoc Title", 'asciidoc')
    assert "```latex" in format_message("$$E=mc^2$$")
    print("Auto-detection test passed!\n")

if __name__ == "__main__":
    test_markdown()
    test_rst()
    test_asciidoc()
    test_latex()
    test_autodetect()
    print("All tests passed!")
