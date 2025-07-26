import re
from telethon import TelegramClient, events
from config import api_id, api_hash, phone_number

# Regex to find bot usernames
bot_regex = re.compile(r'@(\w*bot\w*)', re.IGNORECASE)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    bots = bot_regex.findall(event.raw_text)
    if bots:
        with open('bots.txt', 'a') as f:
            for bot in bots:
                f.write(f'@{bot}\n')
        print(f'Bots found and saved: {bots}')

async def main():
    await client.start(phone_number)
    print('Client Created')
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
