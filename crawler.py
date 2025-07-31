import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def read_tracked_links(filename="tracked_links.txt"):
    """Reads a list of URLs from a file."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def find_telegram_bots(urls):
    """
    Crawls a list of URLs to find Telegram bot links.

    Args:
        urls: A list of website URLs to crawl.

    Returns:
        A list of unique Telegram bot links found.
    """
    bot_links = set()
    telegram_bot_regex = re.compile(r"https?://t\.me/([a-zA-Z0-9_]+bot)")
    bot_page_regex = re.compile(r"/c/([a-zA-Z0-9_]+)/?$")

    for url in urls:
        try:
            print(f"Crawling {url} for bot pages...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            bot_page_links = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if bot_page_regex.search(href):
                    bot_page_links.add(urljoin(url, href))

            print(f"Found {len(bot_page_links)} bot pages on {url}. Now crawling them...")
            for bot_page_url in bot_page_links:
                try:
                    print(f"  Crawling bot page: {bot_page_url}")
                    page_response = requests.get(bot_page_url, timeout=10)
                    page_response.raise_for_status()
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')

                    for a_tag in page_soup.find_all('a', href=True):
                        href = a_tag['href']
                        absolute_url = urljoin(bot_page_url, href)

                        match = telegram_bot_regex.search(absolute_url)
                        if match:
                            bot_links.add(match.group(0))
                except requests.exceptions.RequestException as e:
                    print(f"  Error crawling bot page {bot_page_url}: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")

    return list(bot_links)

def save_bots_to_file(bots, filename="found_bots.txt"):
    """Saves a list of bot links to a file."""
    with open(filename, "w") as f:
        for bot in bots:
            f.write(bot + "\n")

if __name__ == "__main__":
    target_urls = read_tracked_links()
    if not target_urls:
        print("No target URLs found in tracked_links.txt")
    else:
        found_bots = find_telegram_bots(target_urls)
        save_bots_to_file(found_bots)
        print(f"Found {len(found_bots)} Telegram bots. The list has been saved to found_bots.txt")
