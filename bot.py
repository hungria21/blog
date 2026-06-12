import requests
import time
import sys
import re
import uuid
from config import BOT_TOKEN
from rich_models import RichMessageBuilder, Heading, RichText, Photo, Slideshow, Collage, Table, TableCell, Bold
from dialects import MARKDOWN_CATALOG

class RichMessageBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RichMessageBot/10.1"})

    def get_updates(self):
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": 20}
        try:
            resp = self.session.get(url, params=params, timeout=25).json()
            return resp
        except Exception as e:
            print(f"Erro Polling: {e}")
            return None

    def handle_start(self, chat_id):
        # Texto simplificado exatamente como pedido
        text = (
            "Links e referências rápidas:\n"
            "• Guia de referência Markdown\n"
            "• Guia de formatação do Telegram\n"
            "• GEM para auxiliar na formatação\n"
            "• Adicionar estilo de IA no Telegram (Ajuda a expandir/converter texto comum em Markdown)"
        )
        keyboard = [[{"text": "📚 Ver Referências e Dialetos", "callback_data": "refs"}]]
        self.session.post(f"{self.base_url}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {"inline_keyboard": keyboard}
        })

    def handle_callback(self, cq):
        self.session.post(f"{self.base_url}/answerCallbackQuery", json={"callback_query_id": cq["id"]})

        if cq["data"] == "refs":
            msg_parts = ["📖 *Catálogo de Dialetos Markdown Suportados*\n"]
            for category, items in MARKDOWN_CATALOG.items():
                msg_parts.append(f"\n*[{category}]*")
                for item in items[:5]: # Mostrar os 5 principais de cada para não exceder limites
                    msg_parts.append(f"• [{item['name']}]({item['url']})")

            msg_parts.append("\n\n_Para a lista completa com mais de 50 dialetos, veja o arquivo RICHTEXT_GUIDE.md_")

            full_msg = "\n".join(msg_parts)
            self.session.post(f"{self.base_url}/sendMessage", json={
                "chat_id": cq["message"]["chat"]["id"],
                "text": full_msg,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            })

    def generate_inline(self, query):
        results = []
        urls = re.findall(r'https?://\S+', query)

        if len(urls) >= 2:
            # Slideshow
            b_ss = RichMessageBuilder()
            b_ss.add(Heading(RichText("🎞️ SlideShow"), level=2))
            b_ss.add(Slideshow([Photo(u) for u in urls[:10]]))
            results.append({
                "type": "article",
                "id": str(uuid.uuid4()),
                "title": "🎞️ Criar SlideShow",
                "input_message_content": {
                    "rich_message": {"markdown": b_ss.build_markdown()}
                }
            })

            # Collage
            b_co = RichMessageBuilder()
            b_co.add(Heading(RichText("🖼️ Colagem"), level=2))
            b_co.add(Collage([Photo(u) for u in urls[:10]]))
            results.append({
                "type": "article",
                "id": str(uuid.uuid4()),
                "title": "🖼️ Criar Colagem",
                "input_message_content": {
                    "rich_message": {"markdown": b_co.build_markdown()}
                }
            })

        if query.strip():
            # Tabela
            b = RichMessageBuilder()
            b.add(Table([[TableCell(RichText(Bold("Texto"))), TableCell(RichText(query[:30]))]]))
            results.append({
                "type": "article",
                "id": str(uuid.uuid4()),
                "title": "📊 Criar Tabela",
                "input_message_content": {
                    "rich_message": {"markdown": b.build_markdown()}
                }
            })

            # Fallback Simples (Sempre funciona se o Rich Message falhar)
            results.append({
                "type": "article",
                "id": str(uuid.uuid4()),
                "title": "📝 Texto Simples",
                "input_message_content": {
                    "message_text": f"Formatado: {query}",
                    "parse_mode": "Markdown"
                }
            })
        return results

    def run(self):
        print("Bot 10.1 iniciado...")
        while True:
            upds = self.get_updates()
            if upds and upds.get("ok"):
                for u in upds["result"]:
                    self.offset = u["update_id"] + 1

                    if "message" in u:
                        m = u["message"]
                        print(f"Update: Mensagem de {m['chat']['id']}")
                        if m.get("text") == "/start": self.handle_start(m["chat"]["id"])
                        elif m.get("text"):
                            # Echo direto como Rich Message
                            requests.post(f"{self.base_url}/sendRichMessage", json={
                                "chat_id": m["chat"]["id"],
                                "rich_message": {"markdown": m["text"]}
                            })

                    elif "inline_query" in u:
                        iq = u["inline_query"]
                        print(f"Update: Inline Query '{iq['query']}'")
                        res = self.generate_inline(iq["query"])
                        requests.post(f"{self.base_url}/answerInlineQuery", json={
                            "inline_query_id": iq["id"], "results": res
                        })

                    elif "callback_query" in u:
                        print("Update: Callback Query")
                        self.handle_callback(u["callback_query"])
            time.sleep(0.1)

if __name__ == "__main__":
    if BOT_TOKEN == "SEU_TOKEN_AQUI":
        print("Erro: Token não configurado.")
        sys.exit(1)
    RichMessageBot(BOT_TOKEN).run()
