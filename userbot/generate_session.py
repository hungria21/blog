"""
Script para gerar string de sessão do Telegram
Execute: python generate_session.py
"""

import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("=" * 50)
print("GERADOR DE STRING DE SESSÃO - TELEGRAM USERBOT")
print("=" * 50)
print()

# Obter credenciais
api_id = input("Digite seu API_ID: ").strip()
api_hash = input("Digite seu API_HASH: ").strip()

if not api_id or not api_hash:
    print("❌ API_ID e API_HASH são obrigatórios!")
    exit(1)

try:
    api_id = int(api_id)
except ValueError:
    print("❌ API_ID deve ser um número!")
    exit(1)

print()
print("📱 Conectando ao Telegram...")
print("Você receberá um código de confirmação no Telegram.")
print()

# Criar cliente com StringSession
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print()
    print("✅ Login realizado com sucesso!")
    print()
    print("=" * 50)
    print("SUA STRING DE SESSÃO:")
    print("=" * 50)
    print()
    print(client.session.save())
    print()
    print("=" * 50)
    print()
    print("⚠️  ATENÇÃO:")
    print("1. Copie essa string e cole no arquivo .env")
    print("2. NUNCA compartilhe essa string com ninguém!")
    print("3. Com ela, qualquer pessoa pode acessar sua conta")
    print()
    print("💾 Salve em .env como:")
    print("STRING_SESSION=<sua_string_aqui>")
    print()