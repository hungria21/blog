# Guia de Instalação (Pydroid 3 & Termux) 📱

Este bot foi otimizado para rodar diretamente no seu celular através do **Pydroid 3** ou **Termux**.

## 1. Obtendo as Credenciais do Telegram 🔑

Antes de começar, você precisa de:
1. **API ID** e **API Hash**: Obtenha em [my.telegram.org](https://my.telegram.org).
2. **Bot Token**: Obtenha com o [@BotFather](https://t.me/BotFather) no Telegram.

---

## 2. Rodando no Pydroid 3 (Android) 🐍

1. Instale o **Pydroid 3** na Play Store.
2. Abra o app e vá no menu lateral -> **Pip**.
3. Na aba "INSTALL", digite: `pyrogram tgcrypto` e clique em Install.
4. Copie o código do `main.py` deste repositório.
5. No Pydroid 3, crie um novo arquivo, cole o código e salve como `main.py`.
6. Clique no botão de **Play** (ícone amarelo).
7. Na primeira execução, o bot pedirá seu API_ID, API_HASH e BOT_TOKEN diretamente no terminal. Digite-os e ele salvará automaticamente.

---

## 3. Rodando no Termux (Android) 💻

1. Instale o **Termux** (preferencialmente via F-Droid).
2. Execute os seguintes comandos para preparar o ambiente:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   ```
3. Clone este repositório:
   ```bash
   git clone https://github.com/yitzhak050/MarkdownRichBot.git
   cd MarkdownRichBot
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Inicie o bot:
   ```bash
   python main.py
   ```
6. Insira suas credenciais quando solicitado.

---

## Configurações Adicionais no BotFather ⚠️

Para que o modo **Inline** funcione corretamente:
1. Vá ao [@BotFather](https://t.me/BotFather).
2. Use o comando `/setinline`.
3. Escolha seu bot e envie uma mensagem de exemplo.
4. Use o comando `/setinlinefeedback`.
5. Selecione seu bot -> **Enabled** -> **100%**.

---

**Nota:** O arquivo `.env` será criado automaticamente na primeira vez que você rodar o bot com as suas credenciais. Nunca compartilhe esse arquivo!
