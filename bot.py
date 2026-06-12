import requests
import time
import sys
import re
from config import BOT_TOKEN
from rich_models import RichMessageBuilder, Heading, RichText, Photo, Slideshow, Collage, Table, TableCell, Bold, Math, Details

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
        self.user_states = {} # chat_id: {"mode": "collage"|"slideshow", "photos": []}

    def get_file_url(self, file_id):
        """
        Obtém a URL direta de um arquivo usando getFile.
        """
        url = f"{self.base_url}/getFile"
        params = {"file_id": file_id}
        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            if data.get("ok"):
                file_path = data["result"]["file_path"]
                return f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        except Exception as e:
            print(f"Erro ao obter URL do arquivo: {e}")
        return None

    def send_rich_message(self, chat_id, markdown=None, html=None, is_rtl=False, skip_detection=False, photos=None, documents=None):
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

        if photos:
            rich_message["photos"] = photos
        if documents:
            rich_message["documents"] = documents

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

    def handle_done(self, chat_id):
        state = self.user_states.get(chat_id)
        if not state or not state.get("photos"):
            self.send_rich_message(chat_id, markdown="Nenhuma imagem recebida. Use /colagem ou /slideShow primeiro.")
            return

        mode = state["mode"]
        file_ids = state["photos"]
        builder = RichMessageBuilder()

        # No Markdown das Rich Messages, para mídias internas, usamos o índice no vetor de photos/documents
        # Sintaxe: attach://<index>
        rich_photos = [Photo(f"attach://{i}") for i in range(len(file_ids))]

        if mode == "collage":
            builder.add(Heading(RichText("🖼️ Sua Colagem"), level=1))
            builder.add(Collage(rich_photos))
        else:
            builder.add(Heading(RichText("🎞️ Seu SlideShow"), level=1))
            builder.add(Slideshow(rich_photos))

        self.send_rich_message(chat_id, markdown=builder.build_markdown(), photos=file_ids)
        del self.user_states[chat_id]

    def answer_inline_query(self, inline_query_id, results):
        url = f"{self.base_url}/answerInlineQuery"
        payload = {
            "inline_query_id": inline_query_id,
            "results": results,
            "cache_time": 60
        }
        try:
            self.session.post(url, json=payload)
        except Exception as e:
            print(f"Erro ao responder query inline: {e}")

    def generate_inline_results(self, query_text):
        results = []
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', query_text)

        if len(urls) >= 2:
            # 1. Template Slideshow
            b_slideshow = RichMessageBuilder()
            b_slideshow.add(Heading(RichText("🎞️ Galeria Slideshow"), level=2))
            photos = [Photo(u) for u in urls[:10]]
            b_slideshow.add(Slideshow(photos))

            results.append({
                "type": "article",
                "id": "slideshow",
                "title": "Criar SlideShow",
                "description": f"Criar galeria com {len(urls)} links",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_slideshow.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

            # 2. Template Colagem
            b_collage = RichMessageBuilder()
            b_collage.add(Heading(RichText("🖼️ Colagem de Mídia"), level=2))
            b_collage.add(Collage(photos))

            results.append({
                "type": "article",
                "id": "collage",
                "title": "Criar Colagem",
                "description": "Exibir imagens em mosaico",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_collage.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

        # 3. Template Tabela Comparativa (mesmo sem links)
        if query_text.strip():
            b_table = RichMessageBuilder()
            b_table.add(Heading(RichText("📊 Tabela de Dados"), level=2))
            header = [TableCell(RichText("Item"), is_header=True), TableCell(RichText("Valor"), is_header=True)]
            row = [TableCell(RichText(query_text[:20])), TableCell(RichText("Data: 2026"))]
            b_table.add(Table([header, row]))

            results.append({
                "type": "article",
                "id": "table",
                "title": "Criar Tabela",
                "description": f"Gerar tabela com: {query_text[:15]}...",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_table.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

            # 4. Template Nota Matemática
            b_math = RichMessageBuilder()
            b_math.add(Heading(RichText("🧮 Expressão Científica"), level=2))
            b_math.add(Math(query_text, block=True))

            results.append({
                "type": "article",
                "id": "math",
                "title": "Converter para LaTeX",
                "description": "Formatar como fórmula matemática",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_math.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

            # 5. Template Bloco Expansível
            b_details = RichMessageBuilder()
            b_details.add(Details(
                summary=RichText(f"Detalhes de: {query_text[:15]}..."),
                content=[RichText(f"Conteúdo expandido para: {query_text}")]
            ))

            results.append({
                "type": "article",
                "id": "details",
                "title": "Criar Bloco Expansível",
                "description": "Conteúdo oculto que abre ao clicar",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_details.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

        return results

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

                        # Mensagens privadas
                        if "message" in update:
                            msg = update["message"]
                            chat_id = msg["chat"]["id"]
                            text = msg.get("text", "")

                            if text == "/start":
                                self.handle_start(chat_id)
                            elif text == "/demo":
                                self.handle_demo(chat_id)
                            elif text == "/colagem":
                                self.user_states[chat_id] = {"mode": "collage", "photos": []}
                                self.send_rich_message(chat_id, markdown="Modo Colagem ativado. Envie as imagens e termine com /done.")
                            elif text == "/slideShow":
                                self.user_states[chat_id] = {"mode": "slideshow", "photos": []}
                                self.send_rich_message(chat_id, markdown="Modo SlideShow ativado. Envie as imagens e termine com /done.")
                            elif text == "/done":
                                self.handle_done(chat_id)
                            elif "photo" in msg:
                                if chat_id in self.user_states:
                                    # Pega a maior resolução disponível
                                    file_id = msg["photo"][-1]["file_id"]
                                    self.user_states[chat_id]["photos"].append(file_id)
                                    count = len(self.user_states[chat_id]["photos"])
                                    self.send_rich_message(chat_id, markdown=f"Imagem {count} recebida.")
                            elif text:
                                # Envia o texto puro como Rich Message para permitir testes de formatação manual
                                self.send_rich_message(chat_id, markdown=text)

                        # Modo Inline
                        elif "inline_query" in update:
                            query = update["inline_query"]
                            results = self.generate_inline_results(query["query"])
                            self.answer_inline_query(query["id"], results)

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
