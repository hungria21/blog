import json
import re
import uuid
from bot import RichMessageBot
from rich_models import RichMessageBuilder, Heading, RichText, Photo, Slideshow, Table, TableCell, Bold, Italic, Collage

def test_rendering_fix():
    # Testar se Bold(Italic("text")) renderiza corretamente e não como um objeto Python
    nested = Bold(Italic("Texto Aninhado"))
    md = nested.to_markdown()
    print(f"Markdown aninhado: {md}")
    assert md == "**_Texto Aninhado_**"

    html = nested.to_html()
    print(f"HTML aninhado: {html}")
    assert html == "<b><i>Texto Aninhado</i></b>"
    print("Teste de correção de renderização aninhada passou!")

def test_collage_template():
    bot = RichMessageBot("fake")
    query = "https://a.jpg https://b.jpg"
    results = bot.generate_inline(query)

    # Deve conter Slideshow, Collage e Texto Simples (Tabela não aparece se for só links sem texto extra no regex atual,
    # mas o regex \S+ pega tudo, então vamos conferir)
    titles = [r["title"] for r in results]
    print(f"Templates gerados: {titles}")
    assert "🖼️ Criar Colagem" in titles
    assert "🎞️ Criar SlideShow" in titles
    print("Teste de template de colagem passou!")

if __name__ == "__main__":
    test_rendering_fix()
    test_collage_template()
