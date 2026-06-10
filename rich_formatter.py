from pyrogram import enums
from pyrogram.parser import Parser

async def parse_markdown(client, text):
    """
    Uses Pyrogram's internal parser to convert Markdown to text and entities.
    """
    # Replace checklists
    text = text.replace("[ ]", "⬜").replace("[x]", "✅").replace("[X]", "✅")

    # We use the internal Parser class
    parser = Parser(client)
    res = await parser.parse(text)
    return {"text": res["message"], "entities": res.get("entities")}
