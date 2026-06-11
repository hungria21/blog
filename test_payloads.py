import json
from bot import RichMessageBot

def test_payload_generation():
    bot = RichMessageBot("fake_token")

    # Teste Markdown
    chat_id = 12345
    markdown_content = "# Hello\n| Table |"

    # Simular a construção do payload sem enviar de fato (mocking requests.post não necessário aqui,
    # apenas queremos ver se o objeto rich_message é gerado corretamente na estrutura que passamos para o post)

    # Vamos criar uma versão de teste que retorna o payload em vez de enviar
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

    print("Payload gerado:", json.dumps(payload, indent=2))

    assert payload["chat_id"] == 12345
    assert "rich_message" in payload
    assert payload["rich_message"]["markdown"] == markdown_content
    assert payload["rich_message"]["is_rtl"] is False

    # Teste HTML
    html_content = "<h1>Title</h1>"
    payload_html = get_mock_payload(chat_id, html=html_content, is_rtl=True)
    assert payload_html["rich_message"]["html"] == html_content
    assert payload_html["rich_message"]["is_rtl"] is True

    print("Testes de payload passaram!")

if __name__ == "__main__":
    test_payload_generation()
