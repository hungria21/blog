import asyncio
import uuid
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ChosenInlineResult,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.raw import functions, types
from pyrogram.utils import unpack_inline_message_id
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Manual .env loader
def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

# Load existing environment variables
load_env()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Interactive setup if credentials are missing
if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("\n--- Configuração do Bot ---")
    if not API_ID: API_ID = input("Digite seu API_ID: ").strip()
    if not API_HASH: API_HASH = input("Digite seu API_HASH: ").strip()
    if not BOT_TOKEN: BOT_TOKEN = input("Digite seu BOT_TOKEN: ").strip()

    with open(".env", "w") as f:
        f.write(f"API_ID={API_ID}\nAPI_HASH={API_HASH}\nBOT_TOKEN={BOT_TOKEN}\n")
    print("Configurações salvas no arquivo .env!\n")

# Initialize client
app = Client("rich_text_bot", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)

# Temporary memory for inline drafts
drafts_cache = {}

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    logger.info("Received /start command in private chat.")
    await message.reply(
        "Bem-vindo! ✍️\n\n"
        "Envie-me um código Markdown aqui, ou use-me em qualquer grupo/chat marcando meu nome de usuário para converter texto em Rich Text instantaneamente."
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def format_private(client, message):
    logger.info("Formatting private text message.")
    try:
        peer = await client.resolve_peer(message.chat.id)
        payload = types.InputRichMessageMarkdown(markdown=message.text, rtl=False)

        await client.invoke(
            functions.messages.SendMessage(
                peer=peer,
                message="Esta mensagem requer um aplicativo atualizado.",
                random_id=client.rnd_id(),
                rich_message=payload
            )
        )
        logger.info("Private rich message sent successfully.")
    except Exception as e:
        logger.error(f"Failed to format private message: {e}")
        await message.reply("❌ Ocorreu um erro ao codificar o texto.")

@app.on_inline_query()
async def inline_handler(client, query: InlineQuery):
    text = query.query.strip()

    if not text:
        await query.answer([
            InlineQueryResultArticle(
                title="Digite o texto para formatar...",
                input_message_content=InputTextMessageContent("Por favor, digite o texto para formatar.")
            )
        ], cache_time=1)
        return

    # Generate unique ID for the draft
    result_id = str(uuid.uuid4())
    drafts_cache[result_id] = text

    # Dummy keyboard is strictly required to receive the inline_message_id from Telegram
    dummy_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⏳ Processando...", callback_data="processing_dummy")]]
    )

    results = [
        InlineQueryResultArticle(
            id=result_id,
            title="✨ Enviar como Rich Text",
            description="Clique para enviar e converter instantaneamente",
            input_message_content=InputTextMessageContent("⏳ Processando formatação..."),
            reply_markup=dummy_keyboard
        )
    ]

    await query.answer(results, cache_time=0)

@app.on_chosen_inline_result()
async def chosen_result_handler(client, chosen_result: ChosenInlineResult):
    result_id = chosen_result.result_id
    inline_msg_id_str = chosen_result.inline_message_id

    if not inline_msg_id_str:
        logger.warning("No inline_message_id received. Inline Feedback might be off in BotFather.")
        return

    if result_id not in drafts_cache:
        logger.warning(f"Result ID {result_id} not found in drafts cache.")
        return

    raw_markdown = drafts_cache.pop(result_id)

    try:
        # Unpack the string ID into a Raw API object
        raw_inline_id_obj = unpack_inline_message_id(inline_msg_id_str)

        # Invoke the edit to apply the rich text payload directly
        await client.invoke(
            functions.messages.EditInlineBotMessage(
                id=raw_inline_id_obj,
                message="Formatação completa:",
                rich_message=types.InputRichMessageMarkdown(
                    markdown=raw_markdown,
                    rtl=False
                )
            )
        )
        logger.info("Inline message successfully edited to Rich Text!")
    except Exception as e:
        logger.error(f"Error editing inline message: {e}")

if __name__ == "__main__":
    logger.info("Bot is starting up...")
    app.run()
