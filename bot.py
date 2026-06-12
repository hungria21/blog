import requests
import time
import sys
import re
import hashlib
from config import BOT_TOKEN
from rich_models import RichMessageBuilder, Heading, RichText, Photo, Slideshow, Collage, Table, TableCell, Bold, Math, Details, Map
from dialects import MARKDOWN_CATALOG

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
            "# Bem-vindo ao RichBot v10.1! 🚀\n\n"
            "Eu dou suporte a todas as sintaxes e dialetos de Markdown através do novo recurso de **Rich Messages**.\n\n"
            "Escolha uma categoria abaixo para ver guias e referências:"
        )

        # Criar teclado inline com as categorias do catálogo
        keyboard = []
        row = []
        for category in MARKDOWN_CATALOG.keys():
            # Usar hash da categoria para o callback_data (limite de 64 bytes)
            cat_id = hashlib.md5(category.encode()).hexdigest()[:10]
            row.append({"text": category, "callback_data": f"cat_{cat_id}"})
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        url = f"{self.base_url}/sendRichMessage"
        payload = {
            "chat_id": chat_id,
            "rich_message": {"markdown": text},
            "reply_markup": {"inline_keyboard": keyboard}
        }
        self.session.post(url, json=payload)

    def handle_callback_query(self, callback_query):
        data = callback_query["data"]
        chat_id = callback_query["message"]["chat"]["id"]
        cq_id = callback_query["id"]

        # Sempre responder a callback query IMEDIATAMENTE para parar o ícone de carregamento
        try:
            self.session.post(f"{self.base_url}/answerCallbackQuery", json={"callback_query_id": cq_id})
        except Exception as e:
            print(f"Erro ao responder callback query: {e}")

        if data.startswith("cat_"):
            target_cat_id = data[4:]
            selected_category = None
            for category in MARKDOWN_CATALOG.keys():
                if hashlib.md5(category.encode()).hexdigest()[:10] == target_cat_id:
                    selected_category = category
                    break

            if selected_category:
                links = MARKDOWN_CATALOG[selected_category]
                builder = RichMessageBuilder()
                builder.add(Heading(RichText(f"📚 {selected_category}"), level=2))

                rows = [[TableCell(RichText("Nome"), is_header=True), TableCell(RichText("Link"), is_header=True)]]
                for item in links:
                    rows.append([
                        TableCell(RichText(item["name"])),
                        TableCell(RichText(f"[Site]({item['url']})"))
                    ])

                builder.add(Table(rows))
                self.send_rich_message(chat_id, markdown=builder.build_markdown())

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

            # 6. Template Ficha Técnica
            b_info = RichMessageBuilder()
            b_info.add(Heading(RichText(f"📋 Ficha: {query_text[:15]}"), level=2))
            b_info.add(Table([
                [TableCell(RichText("Propriedade"), is_header=True), TableCell(RichText("Descrição"), is_header=True)],
                [TableCell(RichText("Nome")), TableCell(RichText(query_text[:20]))],
                [TableCell(RichText("Tipo")), TableCell(RichText("Objeto Rich"))],
                [TableCell(RichText("Versão")), TableCell(RichText("API 10.1"))]
            ]))

            results.append({
                "type": "article",
                "id": "info_sheet",
                "title": "Criar Ficha Técnica",
                "description": "Tabela estruturada de informações",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_info.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

            # 7. Template Aviso Importante
            b_warn = RichMessageBuilder()
            b_warn.add(Heading(RichText("⚠️ AVISO IMPORTANTE"), level=1))
            b_warn.add(RichText([Bold("Atenção: "), query_text]))

            results.append({
                "type": "article",
                "id": "warning",
                "title": "Criar Alerta",
                "description": "Mensagem de destaque com cabeçalho",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_warn.build_markdown(),
                        "is_rtl": False,
                        "skip_entity_detection": False
                    }
                }
            })

            # 8. Template Mapa de Localização
            b_map = RichMessageBuilder()
            b_map.add(Heading(RichText("📍 Localização do Evento"), level=2))
            b_map.add(Map(lat=-23.5505, long=-46.6333, zoom=15, caption="Centro de São Paulo"))

            results.append({
                "type": "article",
                "id": "location_map",
                "title": "Enviar Mapa Rich",
                "description": "Mapa interativo com legenda",
                "input_message_content": {
                    "rich_message": {
                        "markdown": b_map.build_markdown(),
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

                        # Debug: Mostrar o tipo de update recebido
                        update_type = list(update.keys())[-1]
                        print(f"Update recebido: {update_type} (ID: {update['update_id']})")

                        # Mensagens privadas
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
                                # Envia o texto puro como Rich Message para permitir testes de formatação manual
                                self.send_rich_message(chat_id, markdown=text)

                        # Modo Inline
                        elif "inline_query" in update:
                            query = update["inline_query"]
                            results = self.generate_inline_results(query["query"])
                            self.answer_inline_query(query["id"], results)

                        # Callback Queries (Teclado Inline)
                        elif "callback_query" in update:
                            self.handle_callback_query(update["callback_query"])

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
