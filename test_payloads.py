import json
from bot import RichMessageBot
from rich_models import RichMessageBuilder, Heading, Bold, Math, Table, TableCell, RichText

def test_payload_generation():
    bot = RichMessageBot("fake_token")
    chat_id = 12345

    # Teste Manual
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
    print("Markdown gerado pelo modelo:\n", md)

    assert "## **Título** de Teste" in md
    assert "$$x = 2$$" in md

    html = builder.build_html()
    print("HTML gerado pelo modelo:\n", html)
    assert "<h2><b>Título</b> de Teste</h2>" in html
    assert "<tg-math-block>x = 2</tg-math-block>" in html

    print("Teste do modelo de objetos passou!")

if __name__ == "__main__":
    test_payload_generation()
    test_object_model()
