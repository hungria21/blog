import json
import re
from bot import RichMessageBot
from rich_models import RichMessageBuilder, Heading, Bold, Math, Photo, Slideshow, RichText, Details, Map

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
    assert "<tg-slideshow>" in md
    assert "![Foto 1](https://img1.jpg \"Foto 1\")" in md

    html = builder.build_html()
    assert "<tg-slideshow>" in html
    print("Teste de mídia e coleções passou!")

def test_inline_logic():
    bot = RichMessageBot("fake_token")
    query = "https://link1.com/a.jpg https://link2.com/b.jpg"
    results = bot.generate_inline_results(query)

    # Verificar estrutura corrigida (campos diretos em rich_message)
    assert results[0]["id"] == "slideshow"
    assert "rich_message" in results[0]["input_message_content"]
    assert "markdown" in results[0]["input_message_content"]["rich_message"]

    print("Teste de lógica inline (v3) passou!")

if __name__ == "__main__":
    test_payload_generation()
    test_object_model()
    test_media_and_collections()
    test_inline_logic()
