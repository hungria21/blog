from abc import ABC, abstractmethod
from typing import List, Union, Optional

class RichElement(ABC):
    @abstractmethod
    def to_markdown(self) -> str:
        pass

    @abstractmethod
    def to_html(self) -> str:
        pass

class RichText(RichElement):
    def __init__(self, content: Union[str, List['RichText']]):
        self.content = content

    def _render(self, mode: str) -> str:
        if isinstance(self.content, list):
            res = []
            for c in self.content:
                if isinstance(c, RichText):
                    res.append(c._render(mode))
                else:
                    res.append(str(c))
            return "".join(res)
        return str(self.content)

    def to_markdown(self) -> str: return self._render("md")
    def to_html(self) -> str: return self._render("html")

class Bold(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"**{content}**" if mode == "md" else f"<b>{content}</b>"

class Italic(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"_{content}_" if mode == "md" else f"<i>{content}</i>"

class Underline(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"<u>{content}</u>"

class Strikethrough(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"~~{content}~~" if mode == "md" else f"<s>{content}</s>"

class Spoiler(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"||{content}||" if mode == "md" else f"<tg-spoiler>{content}</tg-spoiler>"

class Code(RichText):
    def _render(self, mode: str) -> str:
        content = super()._render(mode)
        return f"`{content}`" if mode == "md" else f"<code>{content}</code>"

class TableCell(RichElement):
    def __init__(self, text: RichText, is_header: bool = False, align: str = "left"):
        self.text = text
        self.is_header = is_header
        self.align = align

    def to_markdown(self) -> str: return self.text.to_markdown()
    def to_html(self) -> str:
        tag = "th" if self.is_header else "td"
        return f'<{tag} align="{self.align}">{self.text.to_html()}</{tag}>'

class Table(RichElement):
    def __init__(self, rows: List[List[TableCell]], caption: Optional[str] = None):
        self.rows = rows
        self.caption = caption

    def to_markdown(self) -> str:
        # Simplificação: assume que a primeira linha é o cabeçalho se houver mais de uma
        if not self.rows: return ""
        res = []
        for i, row in enumerate(self.rows):
            line = "| " + " | ".join([c.to_markdown() for c in row]) + " |"
            res.append(line)
            if i == 0 and len(self.rows) > 1:
                # Separador de cabeçalho Markdown
                sep = "| " + " | ".join([":---" if c.align == "left" else ":---:" if c.align == "center" else "---:" for c in row]) + " |"
                res.append(sep)
        return "\n".join(res)

    def to_html(self) -> str:
        cap = f"<caption>{self.caption}</caption>" if self.caption else ""
        rows_html = ""
        for row in self.rows:
            rows_html += "<tr>" + "".join([c.to_html() for c in row]) + "</tr>"
        return f'<table bordered>{cap}{rows_html}</table>'

class Math(RichElement):
    def __init__(self, expression: str, block: bool = False):
        self.expression = expression
        self.block = block

    def to_markdown(self) -> str:
        return f"$${self.expression}$$" if self.block else f"${self.expression}$"

    def to_html(self) -> str:
        tag = "tg-math-block" if self.block else "tg-math"
        return f"<{tag}>{self.expression}</{tag}>"

class Heading(RichElement):
    def __init__(self, text: RichText, level: int = 1):
        self.text = text
        self.level = max(1, min(6, level))

    def to_markdown(self) -> str:
        return f"{'#' * self.level} {self.text.to_markdown()}"

    def to_html(self) -> str:
        return f"<h{self.level}>{self.text.to_html()}</h{self.level}>"

class Divider(RichElement):
    def to_markdown(self) -> str: return "---"
    def to_html(self) -> str: return "<hr/>"

class Link(RichText):
    def __init__(self, text: RichText, url: str):
        super().__init__(text.content)
        self.url = url

    def to_markdown(self) -> str: return f"[{super().to_markdown()}]({self.url})"
    def to_html(self) -> str: return f'<a href="{self.url}">{super().to_html()}</a>'

class ChecklistItem(RichElement):
    def __init__(self, text: RichText, checked: bool = False):
        self.text = text
        self.checked = checked

    def to_markdown(self) -> str:
        mark = "x" if self.checked else " "
        return f"- [{mark}] {self.text.to_markdown()}"

    def to_html(self) -> str:
        # Checklists no Rich HTML são simulados via listas ou atributos nativos se suportado
        # Usando emoji para maior compatibilidade visual se a tag não for clara
        mark = "✅ " if self.checked else "⬜ "
        return f"<li>{mark}{self.text.to_html()}</li>"

class RichMessageBuilder:
    def __init__(self):
        self.elements: List[RichElement] = []

    def add(self, element: RichElement):
        self.elements.append(element)
        return self

    def build_markdown(self) -> str:
        return "\n\n".join([e.to_markdown() for e in self.elements])

    def build_html(self) -> str:
        return "".join([e.to_html() for e in self.elements])
