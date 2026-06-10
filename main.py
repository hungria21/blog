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

# Import configuration safely
from config import API_ID, API_HASH, BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize client
app = Client("rich_text_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Temporary memory for inline drafts
drafts_cache = {}

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    logger.info("Received /start command in private chat.")
    await message.reply(
        "ברוך הבא! ✍️\n\n"
        "שלח לי פה קוד ב-Markdown, או השתמש בי בכל קבוצה/צ'אט באמצעות תיוג הבוט שלי כדי להמיר טקסט לעיצוב Rich Text באופן מיידי."
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def format_private(client, message):
    logger.info("Formatting private text message.")
    try:
        from rich_formatter import parse_markdown
        parsed = await parse_markdown(client, message.text)

        # We try to use the 'rich_message' attribute if the library supports it,
        # otherwise we fall back to standard entities.
        try:
            peer = await client.resolve_peer(message.chat.id)
            payload = types.InputRichMessageMarkdown(markdown=message.text, rtl=True)

            await client.invoke(
                functions.messages.SendMessage(
                    peer=peer,
                    message="ההודעה דורשת אפליקציה מעודכנת.",
                    random_id=client.rnd_id(),
                    rich_message=payload
                )
            )
            logger.info("Private rich message sent via native support.")
        except (AttributeError, TypeError):
            # Fallback to standard entities
            await message.reply(parsed["text"], entities=parsed["entities"])
            logger.info("Private rich message sent via entity fallback.")

    except Exception as e:
        logger.error(f"Failed to format private message: {e}")
        await message.reply("❌ חלה שגיאה בקידוד הטקסט.")

@app.on_inline_query()
async def inline_handler(client, query: InlineQuery):
    text = query.query.strip()

    if not text:
        await query.answer([
            InlineQueryResultArticle(
                title="הקלד טקסט לעיצוב...",
                input_message_content=InputTextMessageContent("אנא הקלד טקסט לעיצוב.")
            )
        ], cache_time=1)
        return

    result_id = str(uuid.uuid4())
    drafts_cache[result_id] = text

    dummy_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⏳ מעבד...", callback_data="processing_dummy")]]
    )

    results = [
        InlineQueryResultArticle(
            id=result_id,
            title="✨ שלח כטקסט עשיר (Rich Text)",
            description="לחץ לשליחה והמרה מיידית",
            input_message_content=InputTextMessageContent("⏳ מעבד עיצוב..."),
            reply_markup=dummy_keyboard
        )
    ]

    await query.answer(results, cache_time=0)

@app.on_chosen_inline_result()
async def chosen_result_handler(client, chosen_result: ChosenInlineResult):
    result_id = chosen_result.result_id
    inline_msg_id_str = chosen_result.inline_message_id

    if not inline_msg_id_str or result_id not in drafts_cache:
        return

    raw_markdown = drafts_cache.pop(result_id)

    try:
        raw_inline_id_obj = unpack_inline_message_id(inline_msg_id_str)
        from rich_formatter import parse_markdown
        parsed = await parse_markdown(client, raw_markdown)

        try:
            # Attempt to use native rich text if available
            await client.invoke(
                functions.messages.EditInlineBotMessage(
                    id=raw_inline_id_obj,
                    message="העיצוב המלא:",
                    rich_message=types.InputRichMessageMarkdown(
                        markdown=raw_markdown,
                        rtl=True
                    )
                )
            )
            logger.info("Inline message edited via native rich text.")
        except (AttributeError, TypeError):
            # Fallback to standard entities
            await client.invoke(
                functions.messages.EditInlineBotMessage(
                    id=raw_inline_id_obj,
                    message=parsed["text"],
                    entities=parsed["entities"]
                )
            )
            logger.info("Inline message edited via entity fallback.")
    except Exception as e:
        logger.error(f"Error editing inline message: {e}")

if __name__ == "__main__":
    logger.info("Bot is starting up...")
    app.run()
