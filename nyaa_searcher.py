# Requer: requests, beautifulsoup4
# Instalação: pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import quote_plus

def search_nyaa(query):
    """
    Busca por arquivos no nyaa.si, filtra os resultados e os exibe de forma organizada.
    """
    encoded_query = quote_plus(query)
    url = f"https://nyaa.si/?f=0&c=0_0&q={encoded_query}"
    print(f"Buscando por '{query}' em nyaa.si...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        table_body = soup.find('tbody')
        if not table_body:
            print("\nNenhum resultado encontrado na página ou a estrutura do site mudou.")
            return

        rows = table_body.find_all('tr')

        results = []
        for row in rows:
            if not row.find('td'):
                continue

            cols = row.find_all('td')

            title_cell = cols[1]
            # Encontra todos os links, mas filtra aquele que leva aos comentários
            title_links = title_cell.find_all('a')

            # O título é geralmente o último link que não é um link de comentário
            title = ""
            if len(title_links) > 1 and "comments" in title_links[-1].get('href', ''):
                title = title_links[-2].get_text(strip=True)
            elif title_links:
                title = title_links[-1].get_text(strip=True)
            else:
                title = title_cell.get_text(strip=True)

            # Lógica de filtragem aprimorada
            language_keywords = ['pt-br', 'pt', 'legendado', 'português']
            has_language = any(keyword in title.lower() for keyword in language_keywords)

            if '1080p' in title.lower() and has_language:

                magnet_cell = cols[2]
                magnet_link = magnet_cell.find('a', href=lambda href: href and href.startswith('magnet:'))
                if magnet_link:
                    magnet = magnet_link['href']
                else:
                    magnet = "Não encontrado"

                size = cols[3].get_text(strip=True)

                results.append({'title': title, 'size': size, 'magnet': magnet})

        if results:
            print("\n--- Resultados Encontrados ---")
            for result in results:
                print(f"Título: {result['title']}")
                print(f"Tamanho: {result['size']}")
                print(f"Magnet Link: {result['magnet']}")
                print("---------------------------------")
        else:
            print("\nNenhum resultado encontrado com os filtros '1080p' e 'português'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}", file=sys.stderr)
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Erro de Conexão: {conn_err}", file=sys.stderr)
    except requests.exceptions.Timeout as timeout_err:
        print(f"Tempo de requisição esgotado: {timeout_err}", file=sys.stderr)
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição: {req_err}", file=sys.stderr)

if __name__ == "__main__":
    try:
        search_term = input("Digite o que você deseja buscar: ")
        if search_term:
            search_nyaa(search_term)
        else:
            print("Termo de busca não pode ser vazio.")
    except KeyboardInterrupt:
        print("\nBusca interrompida pelo usuário.")
        sys.exit(0)
