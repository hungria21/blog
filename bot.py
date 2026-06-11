import requests
import time
import sys
from config import BOT_TOKEN

class RichMessageBot:
    """
    Implementação de um bot para a versão 10.1 da API de Bots do Telegram.
    Focada no novo recurso de 'Rich Messages'.
    """
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0

    def send_rich_message(self, chat_id, markdown=None, html=None, is_rtl=False, skip_detection=False):
        """
        Envia uma Rich Message usando o novo método da API 10.1.
        Aceita markdown ou html como entrada para o objeto InputRichMessage.
        """
        url = f"{self.base_url}/sendRichMessage"

        rich_message = {
            "is_rtl": is_rtl,
            "skip_entity_detection": skip_detection
        }

        if markdown:
            rich_message["markdown"] = markdown
        elif html:
            rich_message["html"] = html
        else:
            raise ValueError("É necessário fornecer 'markdown' ou 'html' no objeto rich_message.")

        payload = {
            "chat_id": chat_id,
            "rich_message": rich_message
        }

        try:
            response = requests.post(url, json=payload)
            response_json = response.json()
            if not response_json.get("ok"):
                print(f"Aviso da API: {response_json.get('description')}")
            return response_json
        except Exception as e:
            print(f"Erro ao enviar Rich Message: {e}")
            return None

    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": 20}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar updates: {e}")
            return None

    def handle_start(self, chat_id):
        text = (
            "# Bem-vindo ao RichBot! 🚀\n\n"
            "Eu sou um bot demonstrativo da **Bot API 10.1** (Junho 2026).\n"
            "Minha especialidade é formatar mensagens usando o novo recurso **Rich Messages**.\n\n"
            "Use `/demo` para ver meu poder total de formatação estruturada!"
        )
        self.send_rich_message(chat_id, markdown=text)

    def handle_demo(self, chat_id):
        """
        Exemplo complexo utilizando os novos blocos suportados pela versão 10.1.
        """
        demo_markdown = (
            "# 📊 Demonstração de Rich Messages\n\n"
            "As Rich Messages permitem estruturas complexas diretamente no chat.\n\n"
            "## 1. Tabelas Nativas\n"
            "| Recurso | Status | Nível |\n"
            "|:---|:---:|:---:|\n"
            "| Tabelas | ✅ Ativo | Pro |\n"
            "| LaTeX | ✅ Ativo | Científico |\n"
            "| Checklists | ✅ Ativo | Task |\n\n"
            "## 2. Fórmulas Matemáticas (LaTeX)\n"
            "A equação de Einstein é $$E = mc^2$$.\n"
            "Ou em bloco complexo:\n"
            "```math\n"
            "\\int_{a}^{b} x^2 dx = \\frac{b^3 - a^3}{3}\n"
            "```\n\n"
            "## 3. Checklists Estruturadas\n"
            "- [x] Criar o bot v10.1\n"
            "- [x] Adicionar suporte a tabelas\n"
            "- [ ] Enviar para os usuários\n\n"
            "## 4. Blocos Expansíveis (via HTML)\n"
            "Você pode aninhar HTML dentro do Rich Markdown para recursos extras:\n"
            "<details><summary>Clique para ver detalhes</summary>Este conteúdo estava oculto em uma Rich Message!</details>\n\n"
            "--- \n"
            "<footer>Gerado por RichMessageBot v10.1</footer>"
        )
        self.send_rich_message(chat_id, markdown=demo_markdown)

    def run(self):
        if self.token == "SEU_TOKEN_AQUI":
            print("Erro: Você esqueceu de configurar seu BOT_TOKEN no arquivo config.py!")
            sys.exit(1)

        print("RichMessageBot v10.1 iniciado... Pressione Ctrl+C para parar.")
        try:
            while True:
                updates = self.get_updates()
                if updates and updates.get("ok"):
                    for update in updates["result"]:
                        self.offset = update["update_id"] + 1
                        if "message" in update:
                            msg = update["message"]
                            chat_id = msg["chat"]["id"]
                            text = msg.get("text", "")

                            if text == "/start":
                                self.handle_start(chat_id)
                            elif text == "/demo":
                                self.handle_demo(chat_id)
                            elif text:
                                echo = f"### Você enviou:\n\n> {text}\n\n*Processado via Rich Message API.*"
                                self.send_rich_message(chat_id, markdown=echo)

                time.sleep(1)
        except KeyboardInterrupt:
            print("\nBot parado pelo usuário.")

if __name__ == "__main__":
    bot = RichMessageBot(BOT_TOKEN)
    # Para rodar o bot de fato, você deve preencher o token no config.py
    # e descomentar a linha abaixo.
    bot.run()
