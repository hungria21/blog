# Gerador de Usernames para Bots do Telegram

Este projeto gera sugestões de nomes de usuário (usernames) para bots do Telegram baseando-se em palavras-chave extraídas de listas existentes. Ele também valida se o nome gerado já está em uso, se é um bot ativo ou se o nome parece estar disponível.

## Funcionalidades

- **Extração Inteligente**: Analisa o arquivo `usernames_BotNews.txt` para extrair palavras-chave de hashtags e usernames (usando CamelCase).
- **Geração Aleatória**: Combina de 2 a 4 palavras-chave para criar nomes únicos.
- **Evita Duplicatas**: Garante que os nomes gerados não estejam na lista inicial de bots conhecidos.
- **Validação em Tempo Real**: Verifica o status do username no Telegram (t.me) identificando:
  - **BOT VÁLIDO (EXISTENTE)**: Já é um bot com foto de perfil.
  - **BOT SEM QUALIDADE (SEM FOTO)**: Username ocupado por um bot mas sem personalização.
  - **DISPONÍVEL / USUÁRIO**: Username que não parece ser um bot (pode estar disponível para registro).
- **Modos de Execução**: Suporta geração contínua ou uma quantidade específica definida pelo usuário.

## Pré-requisitos

- Python 3.x
- Bibliotecas: `requests`, `beautifulsoup4`

## Instalação

```bash
pip install -r requirements.txt
```

## Como Usar

Para gerar uma quantidade específica de nomes (ex: 10):
```bash
python3 bot_gen.py --limit 10
```

Para gerar continuamente:
```bash
python3 bot_gen.py
```

Você também pode especificar um arquivo de base diferente:
```bash
python3 bot_gen.py --file meus_usernames.txt
```

## Estrutura do Projeto

- `bot_gen.py`: Script principal com toda a lógica.
- `requirements.txt`: Dependências do projeto.
- `usernames_BotNews.txt`: Base de dados de exemplo.
- `sourcecode.txt`: Referência de análise de HTML do Telegram.
