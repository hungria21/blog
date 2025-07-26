import re
from telethon import TelegramClient, events
from config import api_id, api_hash, phone_number, search_delay

# Regex to find bot usernames
bot_regex = re.compile(r'@(\w*bot\w*)', re.IGNORECASE)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/search'))
async def search_handler(event):
    try:
        entity = await client.get_entity(event.text.split(' ', 1)[1])
        await event.respond(f'Searching for bots in {entity.title}...')
        async for message in client.iter_messages(entity):
            bots = bot_regex.findall(message.text)
            if bots:
                with open('bots.txt', 'a') as f:
                    for bot in bots:
                        f.write(f'@{bot}\n')
                print(f'Bots found and saved: {bots}')
            await asyncio.sleep(search_delay)
    except Exception as e:
        await event.respond(f'Error: {e}')

async def main():
    await client.start(phone_number)
    print('Client Created')
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
