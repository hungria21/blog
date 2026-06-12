import mistune
import re
from tl_definitions import InputRichMessageHtml

class RichFormatter:
    def __init__(self):
        # Configurar mistune para gerar HTML compatível com Rich Messages
        self.markdown = mistune.create_markdown(
            plugins=['strikethrough', 'table', 'url']
        )

    def to_rich_html(self, text):
        """Converte vários formatos para HTML rico do Telegram."""
        # Pré-processamento simples para alguns formatos comuns

        # 1. LaTeX simples ($...$ -> <tg-math>...</tg-math>)
        text = re.sub(r'\$(.*?)\$', r'<tg-math>\1</tg-math>', text)
        text = re.sub(r'\$\$(.*?)\$\$', r'<tg-math-block>\1</tg-math-block>', text, flags=re.DOTALL)

        # 2. Spoiler estilo Discord (||...|| -> <tg-spoiler>...</tg-spoiler>)
        text = re.sub(r'\|\|(.*?)\|\|', r'<tg-spoiler>\1</tg-spoiler>', text)

        # 3. Markdown convert para HTML usando mistune
        html = self.markdown(text)

        # Ajustes no HTML gerado pelo mistune para bater com as tags do Telegram
        # Mistune gera <strong> e <em>, Telegram prefere <b> e <i> (ou ambos funcionam no Rich)
        # Mas vamos manter o padrão Telegram
        html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
        html = html.replace('<em>', '<i>').replace('</em>', '</i>')

        return html

    def to_rich_message(self, text, photos=None, documents=None):
        html = self.to_rich_html(text)
        return InputRichMessageHtml(
            html=html,
            photos=photos,
            documents=documents
        )

    def format_welcome_message(self):
        return (
            "<h1>Bem-vindo ao Rich Message Bot!</h1>"
            "<p>Eu posso formatar suas mensagens usando o novo sistema de <b>Rich Messages</b> do Telegram (v10.1+).</p>"
            "<p>Envie-me qualquer texto em Markdown, LaTeX ($...$), ou spoilers (||...||).</p>"
            "<p>Use /sintaxe para ver todos os formatos suportados.</p>"
        )

    def get_syntax_catalog(self):
        return {
            "Markdown Original": "https://daringfireball.net/projects/markdown/",
            "CommonMark": "https://commonmark.org/",
            "GitHub Flavored Markdown (GFM)": "https://github.github.com/gfm/",
            "Markdown Extra": "https://michelf.ca/projects/php-markdown/extra/",
            "MultiMarkdown": "https://fletcher.github.io/MultiMarkdown-6/",
            "Pandoc Markdown": "https://pandoc.org/",
            "Markdown-it": "https://github.com/markdown-it/markdown-it",
            "Showdown": "https://github.com/showdownjs/showdown",
            "Marked": "https://github.com/markedjs/marked",
            "Mistune": "https://github.com/lepture/mistune",
            "Python-Markdown": "https://python-markdown.github.io/",
            "Parsedown": "https://github.com/erusev/parsedown",
            "Kramdown": "https://kramdown.gettalong.org/",
            "League CommonMark": "https://commonmark.thephpleague.com/",
            "Remark": "https://remark.js.org/",
            "MDX": "https://mdxjs.com/",
            "R Markdown": "https://rmarkdown.rstudio.com/",
            "Quarto": "https://quarto.org/",
            "Bookdown": "https://bookdown.org/",
            "Jupyter Notebook Markdown": "https://jupyter.org/",
            "Docusaurus": "https://docusaurus.io/",
            "VuePress": "https://vuepress.vuejs.org/",
            "VitePress": "https://vitepress.dev/",
            "Astro": "https://astro.build/",
            "MkDocs": "https://www.mkdocs.org/",
            "Material for MkDocs": "https://squidfunk.github.io/mkdocs-material/",
            "Hugo": "https://gohugo.io/",
            "Jekyll": "https://jekyllrb.com/",
            "Eleventy": "https://www.11ty.dev/",
            "Nuxt Content": "https://content.nuxt.com/",
            "GitBook": "https://www.gitbook.com/",
            "Docsify": "https://docsify.js.org/",
            "Read The Docs": "https://readthedocs.org/",
            "HonKit": "https://honkit.netlify.app/",
            "Slate": "https://github.com/slatedocs/slate",
            "Redocly": "https://redocly.com/",
            "Obsidian": "https://obsidian.md/",
            "Logseq": "https://logseq.com/",
            "Joplin": "https://joplinapp.org/",
            "Zettlr": "https://zettlr.com/",
            "Foam": "https://foambubble.github.io/",
            "Notable": "https://notable.app/",
            "Marp": "https://marp.app/",
            "Reveal.js Markdown": "https://revealjs.com/",
            "Slidev": "https://sli.dev/",
            "Remark.js": "https://remarkjs.com/",
            "Deckset": "https://www.deckset.com/",
            "PptxGenJS": "https://gitbrent.github.io/PptxGenJS/",
            "Telegram MarkdownV2": "https://core.telegram.org/bots/api#markdownv2-style",
            "Telegram Rich Messages": "https://core.telegram.org/bots/api",
            "Discord Markdown": "https://support.discord.com/",
            "Slack Mrkdwn": "https://api.slack.com/reference/surfaces/formatting",
            "Mattermost Markdown": "https://docs.mattermost.com/",
            "Rocket.Chat Markdown": "https://docs.rocket.chat/",
            "Matrix Markdown": "https://matrix.org/",
            "Reddit Markdown": "https://support.reddithelp.com/",
            "AsciiDoc": "https://asciidoc.org/",
            "Asciidoctor": "https://asciidoctor.org/",
            "reStructuredText": "https://docutils.sourceforge.io/rst.html",
            "Textile": "https://textile-lang.com/",
            "Org Mode": "https://orgmode.org/",
            "Typst": "https://typst.app/",
            "LaTeX": "https://www.latex-project.org/",
            "ConTeXt": "https://wiki.contextgarden.net/",
            "TeX": "https://tug.org/",
            "Scribble": "https://docs.racket-lang.org/scribble/",
            "Djot": "https://djot.net/",
            "Gemtext": "https://geminiprotocol.net/docs/gemtext.gmi",
            "Pollen": "https://docs.racket-lang.org/pollen/",
            "Antora": "https://antora.org/",
            "Sphinx": "https://www.sphinx-doc.org/",
            "MyST Markdown": "https://mystmd.org/",
            "Typora Extended Markdown": "https://typora.io/",
            "Markua": "https://markua.com/",
            "Leanpub Markdown": "https://leanpub.com/help/manual",
            "CriticMarkup": "https://criticmarkup.com/",
            "Fountain": "https://fountain.io/"
        }
