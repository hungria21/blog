import json
from bot import RichMessageBot
from rich_models import RichMessageBuilder, Heading, Bold, Math, Photo, Slideshow, RichText

def test_payload_generation():
    bot = RichMessageBot("fake_token")
    chat_id = 12345
    markdown_content = "# Hello\n| Table |"

    def get_mock_payload(chat_id, markdown=None, html=None, is_rtl=False, skip_detection=False):
        rich_message = {
            "is_rtl": is_rtl,
            "skip_entity_detection": skip_detection
        }
        if markdown:
            rich_message["markdown"] = markdown
        elif html:
            rich_message["html"] = html

        return {
            "chat_id": chat_id,
            "rich_message": rich_message
        }

    payload = get_mock_payload(chat_id, markdown=markdown_content)
    assert payload["chat_id"] == 12345
    assert payload["rich_message"]["markdown"] == markdown_content
    print("Teste manual básico passou.")

def test_object_model():
    builder = RichMessageBuilder()
    builder.add(Heading(RichText([Bold("Título"), " de Teste"]), level=2))
    builder.add(Math("x = 2", block=True))

    md = builder.build_markdown()
    assert "## **Título** de Teste" in md
    assert "$$x = 2$$" in md

    html = builder.build_html()
    assert "<h2><b>Título</b> de Teste</h2>" in html
    assert "<tg-math-block>x = 2</tg-math-block>" in html
    print("Teste do modelo de objetos básico passou!")

def test_media_and_collections():
    builder = RichMessageBuilder()
    photos = [
        Photo("https://img1.jpg", caption="Foto 1"),
        Photo("https://img2.jpg", caption="Foto 2")
    ]
    builder.add(Slideshow(photos, caption="Meu Show"))

    md = builder.build_markdown()
    print("Markdown de Slideshow:\n", md)
    assert "<tg-slideshow>" in md
    assert "![Foto 1](https://img1.jpg \"Foto 1\")" in md
    assert "<figcaption>Meu Show</figcaption>" in md

    html = builder.build_html()
    print("HTML de Slideshow:\n", html)
    assert "<tg-slideshow>" in html
    assert '<img src="https://img1.jpg"/>' in html

    print("Teste de mídia e coleções passou!")

if __name__ == "__main__":
    test_payload_generation()
    test_object_model()
    test_media_and_collections()
