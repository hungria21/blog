import requests
import time
import sys
from config import BOT_TOKEN
from rich_models import RichMessageBuilder, Heading, RichText, Photo, Slideshow

class RichMessageBot:
    """
    Implementação de um bot para a versão 10.1 da API de Bots do Telegram.
    Focada no novo recurso de 'Rich Messages', com conexão robusta.
    """
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "RichMessageBot/10.1 (Python Requests Robust Version)"
        })

    def send_rich_message(self, chat_id, markdown=None, html=None, is_rtl=False, skip_detection=False):
        """
        Envia uma Rich Message usando o novo método da API 10.1.
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
            response = self.session.post(url, json=payload, timeout=10)
            response_json = response.json()
            if not response_json.get("ok"):
                print(f"Aviso da API: {response_json.get('description')}")
            return response_json
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede ao enviar Rich Message: {e}")
            return None

    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": 20}
        try:
            # Long polling com timeout maior no requests para evitar aborts prematuros
            response = self.session.get(url, params=params, timeout=25)
            return response.json()
        except requests.exceptions.ConnectionError as e:
            print(f"Erro de conexão (abortado?): {e}. Tentando novamente em 5 segundos...")
            time.sleep(5)
            return None
        except requests.exceptions.Timeout:
            # Timeout normal do long polling, não é erro
            return {"ok": True, "result": []}
        except Exception as e:
            print(f"Erro inesperado ao buscar updates: {e}")
            return None

    def handle_start(self, chat_id):
        text = (
            "# Bem-vindo ao RichBot v10.1 (Estável)! 🚀\n\n"
            "Este bot agora usa uma conexão persistente para evitar erros de rede.\n\n"
            "Use `/demo` para ver as novas formatações estruturadas."
        )
        self.send_rich_message(chat_id, markdown=text)

    def handle_demo(self, chat_id):
        demo_markdown = (
            "# 📊 Demonstração de Rich Messages\n\n"
            "## 1. Tabelas Nativas\n"
            "| Recurso | Status | Estabilidade |\n"
            "|:---|:---:|:---:|\n"
            "| Tabelas | ✅ OK | Pro |\n"
            "| Sessão | ✅ OK | Alta |\n\n"
            "## 2. LaTeX\n"
            "$$e^{i\\pi} + 1 = 0$$\n\n"
            "--- \n"
            "<footer>Conexão Robustecida via requests.Session</footer>"
        )
        self.send_rich_message(chat_id, markdown=demo_markdown)

    def handle_slideshow(self, chat_id):
        """
        Cria um Slideshow usando os links fornecidos.
        """
        builder = RichMessageBuilder()
        builder.add(Heading(RichText("🎞️ Meu SlideShow"), level=1))

        photos = [
            Photo("https://i.ibb.co/jP0Jcgwz/file-529.jpg", caption="Primeira Imagem"),
            Photo("https://i.ibb.co/KpDX3N4m/file-530.jpg", caption="Segunda Imagem")
        ]

        builder.add(Slideshow(photos, caption="Coleção de Fotos do Usuário"))

        self.send_rich_message(chat_id, markdown=builder.build_markdown())

    def run(self):
        if self.token == "SEU_TOKEN_AQUI":
            print("Erro: Você esqueceu de configurar seu BOT_TOKEN no arquivo config.py!")
            sys.exit(1)

        print("RichMessageBot v10.1 (Versão Robusta) iniciado... Ctrl+C para parar.")
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
                            elif text == "/slideshow":
                                self.handle_slideshow(chat_id)
                            elif text:
                                echo = f"### Recebido:\n\n> {text}\n\n*Processado com sucesso.*"
                                self.send_rich_message(chat_id, markdown=echo)

                # Pequena pausa entre iterações se não houver updates para aliviar a CPU
                if updates and not updates["result"]:
                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nBot parado pelo usuário.")
        finally:
            self.session.close()

if __name__ == "__main__":
    bot = RichMessageBot(BOT_TOKEN)
    bot.run()
