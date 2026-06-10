import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.network import ConnectionTcpIntermediate
import config
from rich_formatter import parse_rich_message
from layer227 import (
    InputRichMessageMarkdown,
    InputBotInlineMessageRichMessage,
    InputBotInlineResult,
    SetInlineBotResultsLayer227Request,
    SendMessageLayer227Request
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize client with Pydroid 3 / Android stability settings
client = TelegramClient(
    'rich_bot_session',
    config.API_ID,
    config.API_HASH,
    connection=ConnectionTcpIntermediate,
    device_model="RichMessageBot v2",
    system_version="Android 14",
    app_version="1.0"
)

@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.is_private:
        text = event.text
        if not text:
            return

        logger.info(f"Received message: {text[:50]}...")

        try:
            # Try native rich message (Layer 227)
            rich_md = InputRichMessageMarkdown(markdown=text)
            await client(SendMessageLayer227Request(
                peer=await event.get_input_chat(),
                message="", # Message can be empty when rich_message is present
                rich_message=rich_md
            ))
        except Exception as e:
            logger.warning(f"Native rich message failed, falling back to entities: {e}")
            # Fallback to manual entity parsing
            clean_text, entities = parse_rich_message(text)
            await event.respond(clean_text, formatting_entities=entities)

@client.on(events.InlineQuery)
async def handle_inline_query(event):
    query = event.text
    if not query:
        return

    logger.info(f"Inline query: {query[:50]}...")

    try:
        # Construct native rich result
        rich_md = InputRichMessageMarkdown(markdown=query)
        rich_message_content = InputBotInlineMessageRichMessage(rich_message=rich_md)

        result = InputBotInlineResult(
            id='1',
            type='article',
            title='Enviar Mensagem Rica (Nativo)',
            description=query[:100],
            send_message=rich_message_content
        )

        await client(SetInlineBotResultsLayer227Request(
            query_id=event.id,
            results=[result],
            cache_time=0
        ))
    except Exception as e:
        logger.error(f"Native inline failed, falling back: {e}")
        # Fallback to standard entity-based inline (Simplified)
        clean_text, entities = parse_rich_message(query)
        builder = event.builder
        await event.answer([
            builder.article(
                'Enviar Mensagem Rica (Fallback)',
                text=clean_text,
                formatting_entities=entities,
                description="Usando modo de compatibilidade"
            )
        ], cache_time=0)

async def main():
    logger.info("Bot is starting...")
    await client.start(bot_token=config.BOT_TOKEN)
    logger.info("Bot is online!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
