# Userbot Telegram com Telethon

Este é um userbot para Telegram construído com a biblioteca Telethon, projetado para ser executado no Termux.

## Configuração

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Crie o arquivo `.env`:**
    Copie o arquivo `.env.example` para `.env` e preencha as variáveis de ambiente:
    - `API_ID`: Seu API ID do Telegram.
    - `API_HASH`: Seu API Hash do Telegram.
    - `SESSION_NAME`: (Opcional) Nome do arquivo de sessão.
    - `COMMAND_PREFIX`: (Opcional) Prefixo para os comandos (padrão: `.`)

3.  **Execute o userbot:**
    ```bash
    python main.py
    ```
    Na primeira execução, você será solicitado a fornecer seu número de telefone, código de login e senha de autenticação de dois fatores (se houver).

## Comandos

- `.alive`: Verifica se o bot está online.
- `.stats`: Mostra estatísticas de uso.
- `.ytdl <url>`: Baixa vídeos do YouTube e outras plataformas.
- `.ytaudio <url>`: Baixa o áudio de vídeos.
- `.gallery <url>`: Baixa galerias de imagens.
- `.help`: Mostra a lista de comandos.
