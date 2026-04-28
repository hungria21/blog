import os
import json
import markdown
import datetime

# Configurações
ARTICLES_DIR = 'articles'
OUTPUT_DIR = 'posts'
MANIFEST_FILE = 'manifest.json'
TEMPLATE_FILE = 'article_template.html'

# HTML Template para os artigos estáticos
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Moonshot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="../css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0a0a0a; color: #e5e5e5; }}
        .markdown-body details {{
            background-color: #1a1a1a;
            border: 1px solid #333;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }}
        .markdown-body summary {{
            font-weight: 600;
            cursor: pointer;
            outline: none;
            color: #fff;
        }}
        .markdown-body p {{ margin-bottom: 1rem; line-height: 1.6; }}
        .markdown-body h1 {{ font-size: 2.25rem; font-weight: 700; color: white; margin-bottom: 1.5rem; }}
        .markdown-body h2 {{ font-size: 1.5rem; font-weight: 600; color: white; margin-top: 2rem; margin-bottom: 1rem; }}
    </style>
</head>
<body class="min-h-screen">
    <nav class="border-b border-zinc-800 p-4 sticky top-0 bg-[#0a0a0a]/80 backdrop-blur-md z-10">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <a href="../index.html" class="text-xl font-bold tracking-tighter text-white">MOONSHOT BLOG</a>
            <a href="../index.html" class="text-zinc-400 hover:text-white transition-colors">Voltar</a>
        </div>
    </nav>

    <main class="max-w-3xl mx-auto p-6 py-12">
        <article id="article-content" class="markdown-body">
            {content}
        </article>
    </main>

    <footer class="border-t border-zinc-800 p-8 mt-20 text-center text-zinc-500 text-sm">
        &copy; 2023 Moonshot Blog. Suporte total a Instant View.
    </footer>
</body>
</html>
"""

def generate():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(MANIFEST_FILE, 'r') as f:
        articles = json.load(f)

    for article in articles:
        md_path = os.path.join(ARTICLES_DIR, f"{article['id']}.md")
        if not os.path.exists(md_path):
            print(f"Aviso: {md_path} não encontrado.")
            continue

        with open(md_path, 'r') as f:
            md_content = f.read()

        # Converter Markdown para HTML
        # markdown.extensions.extra inclui suporte a tabelas, atributos e HTML bruto
        html_body = markdown.markdown(md_content, extensions=['extra'])

        # Gerar o arquivo final
        final_html = HTML_TEMPLATE.format(
            title=article['title'],
            content=html_body
        )

        output_path = os.path.join(OUTPUT_DIR, f"{article['id']}.html")
        with open(output_path, 'w') as f:
            f.write(final_html)
        print(f"Gerado: {output_path}")

if __name__ == "__main__":
    generate()
