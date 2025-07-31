# Telegram Bot Crawler

This is a Python script to crawl websites and find links to Telegram bots, based on the structure of the [telegram-crawler](https://github.com/MarshalX/telegram-crawler) repository.

## Installation

1. Clone this repository or download the files.
2. Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Open the `tracked_links.txt` file and add the websites you want to crawl, one URL per line.

2. Run the crawler from your terminal:

```bash
python3 crawler.py
```

3. The script will create a file named `found_bots.txt` in the same directory, containing a list of the unique Telegram bot links it found.
