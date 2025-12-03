import random
import string
import sys
import time
import inquirer
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)


def generate_random_string(length=12):
    """Gera uma string aleatória para ser usada como hash no link."""
    characters = string.ascii_letters + string.digits + '_-'
    return ''.join(random.choice(characters) for _ in range(length))


def check_telegram_link(hash_code):
    """Verifica se um link do Telegram com um determinado hash é válido."""
    url = f"https://t.me/+{hash_code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Procurar por elementos que indiquem um convite válido
            join_button = soup.find('a', class_='tgme_action_button_new')
            channel_title = soup.find('div', class_='tgme_page_title')

            if join_button and channel_title:
                print(f"{Fore.GREEN}Link Válido Encontrado: {url} - {channel_title.text.strip()}")
                return url, channel_title.text.strip()
            else:
                return None, None
    except requests.RequestException as e:
        print(f"{Fore.RED}Erro ao verificar o link {url}: {e}")
        return None, None
    return None, None


VALID_LINKS_FILE = "valid_telegram_links.txt"

def save_valid_link(link, title):
    """Salva um link válido no arquivo."""
    with open(VALID_LINKS_FILE, "a") as f:
        f.write(f"{link} - {title}\n")


def main():
    """Função principal que executa o menu interativo ou um modo de teste."""
    if not sys.stdout.isatty():
        # Modo não interativo para testes
        print(f"{Fore.YELLOW}Executando em modo de teste não interativo.")
        for _ in tqdm(range(5), desc="Links Verificados"):
            hash_code = generate_random_string()
            link, title = check_telegram_link(hash_code)
            if link:
                save_valid_link(link, title)
            time.sleep(1)
        return

    stop_checking = False
    questions = [
        inquirer.List(
            'action',
            message="O que você gostaria de fazer?",
            choices=['Iniciar Verificação', 'Sair'],
        ),
    ]

    while True:
        answers = inquirer.prompt(questions)
        if not answers or answers['action'] == 'Sair':
            break

        if answers['action'] == 'Iniciar Verificação':
            stop_checking = False
            print(f"{Fore.YELLOW}Iniciando a verificação de links... Pressione Ctrl+C para parar.")

            try:
                with tqdm(desc="Links Verificados", unit="link") as pbar:
                    while not stop_checking:
                        hash_code = generate_random_string()
                        link, title = check_telegram_link(hash_code)
                        if link:
                            save_valid_link(link, title)
                        pbar.update(1)
                        time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Verificação parada pelo usuário.")
                stop_checking = True


if __name__ == "__main__":
    main()
