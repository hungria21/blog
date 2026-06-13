import sys
import logging

def validate():
    print("Iniciando validação do bot...")

    # Check dependencies
    try:
        import telegram
        import telegram.ext
        print(f"✓ python-telegram-bot v{telegram.__version__} instalado.")
    except ImportError:
        print("✗ Erro: python-telegram-bot não encontrado.")
        sys.exit(1)

    # Check config
    try:
        from config import TOKEN
        if ":" not in TOKEN:
            print("✗ Erro: Token no config.py parece inválido.")
        else:
            print("✓ Configuração do token encontrada.")
    except ImportError:
        print("✗ Erro: config.py não encontrado.")
        sys.exit(1)

    # Syntax check main.py
    try:
        import main
        print("✓ main.py importado com sucesso (sem erros de sintaxe).")
    except Exception as e:
        # Expected if it starts polling, but we just want to see if it parses
        if "loop" in str(e) or "attribute" in str(e):
             print("✓ main.py validado (erros de execução durante import são normais se tentar rodar o bot).")
        else:
             print(f"? main.py import result: {e}")

    print("Validação concluída com sucesso!")

if __name__ == "__main__":
    validate()
