# Telegram Rich Text Bot 🤖

A modern Telegram bot built with [Pyrogram](https://docs.pyrogram.org/) that converts raw Markdown directly into Layer 227 `InputRichMessageMarkdown` entities.

## Features
- **Private Chat Conversion:** Send any Markdown code directly to the bot, and it returns the beautifully formatted Rich Text.
- **Inline Mode (Edit-on-the-fly):** Call the bot in any group or chat via `@botname <markdown>`. It instantly sends and edits the message to apply the rich formatting without requiring admin permissions.
- **RTL Support:** Full support for right-to-left text formatting.
- **Real-time Processing:** Async/await architecture for high-performance message handling.

## Prerequisites
1. Python 3.8+
2. A Telegram API ID and Hash from [my.telegram.org](https://my.telegram.org)
3. A Bot Token from [@BotFather](https://t.me/BotFather)

## Critical Setup in BotFather ⚠️
For the Inline functionality to work, you **must** enable 100% Inline Feedback:
1. Open [@BotFather](https://t.me/BotFather)
2. Send `/setinlinefeedback`
3. Select your bot.
4. Choose `Enabled`.
5. Choose `100%`.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yitzhak050/MarkdownRichBot.git
   cd MarkdownRichBot
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the root directory:**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your credentials:
   ```
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   BOT_TOKEN=your_bot_token_here
   ```

5. **Run the bot:**
   ```bash
   python main.py
   ```

## Usage

### Private Chat Mode
1. Start a conversation with the bot
2. Send any Markdown formatted text
3. The bot will convert and send it back as Rich Text

### Inline Mode
1. In any group or private chat, type `@BotUsername markdown_text_here`
2. Select the result
3. The message will be sent and automatically formatted as Rich Text

## Markdown Formatting Examples
```
**Bold text**
__Italic text__
~~Strikethrough~~
`code`
```

## Project Structure
- `main.py` - Main bot logic with handlers
- `config.py` - Configuration and environment variable loading
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

## Security Notes
⚠️ **NEVER** commit your `.env` file containing API credentials to version control.
The `.gitignore` file is configured to protect it automatically.

## License
This project is open source. Feel free to modify and distribute.

## Support
For issues or questions, please open an issue on GitHub.
