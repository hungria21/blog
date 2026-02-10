import re
import os
import random
import requests
from bs4 import BeautifulSoup
import argparse
import time

def extract_keywords(filepath):
    """
    Extrai palavras-chave de hashtags e nomes de usuário de um arquivo.
    """
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return set(), set()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extrai hashtags
    hashtags = re.findall(r'#(\w+)', content)

    # Extrai nomes de usuário (sem o @)
    usernames = re.findall(r'@(\w+)', content)

    keywords = set()

    # Adiciona hashtags como palavras-chave
    for h in hashtags:
        if len(h) > 2:
            keywords.add(h)

    # Processa nomes de usuário para extrair palavras-chave
    for u in usernames:
        # Remove caracteres inválidos antes de processar
        u_clean = re.sub(r'[^a-zA-Z0-9_]', '', u)

        # Regex para separar por CamelCase ou números
        # Exemplo: TwitterXMediaDownloaderbot -> Twitter, X, Media, Downloaderbot
        # TorrentDxBot -> Torrent, Dx, Bot
        parts = re.findall(r'[A-Z][a-z0-9]*|[a-z0-9]+', u_clean)

        if not parts:
            parts = [u_clean]

        # Se a última parte for 'bot' ou 'Bot' e houver mais partes,
        # podemos opcionalmente anexar ao anterior para seguir o exemplo do usuário
        # "Downloaderbot" (4 palavras chave em TwitterXMediaDownloaderbot)
        if len(parts) > 1:
            last = parts[-1].lower()
            if last == 'bot' and not parts[-1].startswith('Bot'):
                # Anexa ao anterior se o 'bot' estiver em minúsculo e for o fim
                # Mas no exemplo do usuário 'TwitterXMediaDownloaderbot'
                # se fatiarmos por Capitalized, 'Downloaderbot' seria a última parte
                # se 'Downloader' fosse capitalizado.
                pass

        for p in parts:
            # Apenas palavras-chave alfanuméricas sem acentos
            p_clean = re.sub(r'[^a-zA-Z0-9]', '', p)
            if len(p_clean) > 1:
                keywords.add(p_clean)

    return keywords, set(usernames)

def generate_username(keywords, existing_usernames):
    """
    Gera um novo username de bot combinando palavras-chave.
    """
    # Tenta gerar um username único
    while True:
        # Escolhe entre 2 a 4 palavras-chave para combinar
        num_parts = random.randint(2, 4)
        chosen = random.sample(list(keywords), num_parts)

        # Formata o username (Capitalizado)
        username = "".join([p.capitalize() for p in chosen])

        # Garante que termina com 'Bot' se ainda não terminar
        if not username.lower().endswith('bot'):
            username += "Bot"

        # Limpeza final (apenas por segurança)
        username = re.sub(r'[^a-zA-Z0-9_]', '', username)

        # Verifica se já existe na lista e se tem tamanho mínimo
        if len(username) >= 5 and username not in existing_usernames and username.lower() not in [e.lower() for e in existing_usernames]:
            return username

def validate_username(username):
    """
    Valida um username no Telegram raspando a página t.me/username.
    Retorna o status: 'VÁLIDO', 'INVÁLIDO (DISPONÍVEL)', ou 'BOT SEM QUALIDADE'.
    """
    url = f"https://t.me/{username}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "ERRO DE CONEXÃO"

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ""

        # Procura por imagem de perfil
        og_image = soup.find("meta", property="og:image")
        image_url = og_image["content"] if og_image else ""
        is_default_img = "t_logo_2x.png" in image_url or not image_url

        # Procura pelo botão de ação
        action_button = soup.find("a", class_="tgme_action_button_new")
        button_text = action_button.get_text() if action_button else ""

        if "Launch" in title or "Start Bot" in button_text:
            if is_default_img:
                return "BOT SEM QUALIDADE (SEM FOTO)"
            else:
                return "BOT VÁLIDO (EXISTENTE)"
        elif "Contact" in title or "Send Message" in button_text:
            return "DISPONÍVEL / USUÁRIO"
        else:
            return "DESCONHECIDO"

    except Exception as e:
        return f"ERRO: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Gerador de Usernames de Bots do Telegram")
    parser.add_argument("--limit", type=int, help="Quantidade de usernames a serem gerados (deixe vazio para contínuo)")
    parser.add_argument("--file", type=str, default="usernames_BotNews.txt", help="Arquivo de base para palavras-chave")

    args = parser.parse_args()

    print("--- Telegram Bot Username Generator ---")
    keywords, existing = extract_keywords(args.file)

    if not keywords:
        print("Erro: Nenhuma palavra-chave extraída. Verifique o arquivo de entrada.")
        return

    print(f"Palavras-chave: {len(keywords)}")
    print(f"Existentes: {len(existing)}")
    print("Iniciando geração...\n")

    count = 0
    try:
        while True:
            if args.limit and count >= args.limit:
                break

            username = generate_username(keywords, existing)
            status = validate_username(username)

            print(f"[{count+1}] @{username:30} | Status: {status}")

            count += 1
            # Pequeno delay para evitar rate limit do Telegram
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nProcesso interrompido pelo usuário.")

    print(f"\nConcluído. {count} usernames processados.")

if __name__ == "__main__":
    main()
