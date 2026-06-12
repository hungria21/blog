import sys
import os

def validate():
    print("Iniciando validação do código...")

    try:
        import telethon
        print(f"Telethon instalado: {telethon.__version__}")
    except ImportError:
        print("Erro: Telethon não instalado.")
        return False

    try:
        import mistune
        print(f"Mistune instalado: {mistune.__version__}")
    except ImportError:
        print("Erro: Mistune não instalado.")
        return False

    files = ['config.py', 'tl_definitions.py', 'formatter.py', 'bot.py', 'requirements.txt']
    for f in files:
        if os.path.exists(f):
            print(f"Arquivo {f} encontrado.")
        else:
            print(f"Erro: Arquivo {f} não encontrado.")
            return False

    print("Verificando sintaxe dos arquivos Python...")
    for f in files:
        if f.endswith('.py'):
            try:
                with open(f, 'r') as file:
                    compile(file.read(), f, 'exec')
                print(f"Sintaxe de {f} OK.")
            except Exception as e:
                print(f"Erro de sintaxe em {f}: {e}")
                return False

    print("Validação concluída com sucesso!")
    return True

if __name__ == '__main__':
    if validate():
        sys.exit(0)
    else:
        sys.exit(1)
