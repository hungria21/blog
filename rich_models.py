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
    def __init__(self, content: Union[str, List[Union[str, 'RichText']], 'RichText']):
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
        elif isinstance(self.content, RichText):
            return self.content._render(mode)
        return str(self.content)

    def to_markdown(self) -> str: return self._render("md")
    def to_html(self) -> str: return self._render("html")

class Bold(RichText):
    def _render(self, mode: str) -> str:
        c = super()._render(mode)
        return f"**{c}**" if mode == "md" else f"<b>{c}</b>"

class Italic(RichText):
    def _render(self, mode: str) -> str:
        c = super()._render(mode)
        return f"_{c}_" if mode == "md" else f"<i>{c}</i>"

class Underline(RichText):
    def _render(self, mode: str) -> str:
        return f"<u>{super()._render(mode)}</u>"

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
        if not self.rows: return ""
        res = []
        for i, row in enumerate(self.rows):
            line = "| " + " | ".join([c.to_markdown() for c in row]) + " |"
            res.append(line)
            if i == 0 and len(self.rows) > 1:
                sep = "| " + " | ".join([":---" if c.align == "left" else ":---:" if c.align == "center" else "---:" for c in row]) + " |"
                res.append(sep)
        return "\n".join(res)

    def to_html(self) -> str:
        cap = f"<caption>{self.caption}</caption>" if self.caption else ""
        rows_html = "".join(["<tr>" + "".join([c.to_html() for c in row]) + "</tr>" for row in self.rows])
        return f'<table bordered>{cap}{rows_html}</table>'

class Heading(RichElement):
    def __init__(self, text: RichText, level: int = 1):
        self.text = text
        self.level = max(1, min(6, level))

    def to_markdown(self) -> str:
        return f"{'#' * self.level} {self.text.to_markdown()}"

    def to_html(self) -> str:
        return f"<h{self.level}>{self.text.to_html()}</h{self.level}>"

class Math(RichElement):
    def __init__(self, expression: str, block: bool = False):
        self.expression = expression
        self.block = block

    def to_markdown(self) -> str:
        return f"$${self.expression}$$" if self.block else f"${self.expression}$"

    def to_html(self) -> str:
        tag = "tg-math-block" if self.block else "tg-math"
        return f"<{tag}>{self.expression}</{tag}>"

class Photo(RichElement):
    def __init__(self, url: str, caption: Optional[str] = None):
        self.url = url
        self.caption = caption

    def to_markdown(self) -> str:
        cap = f' "{self.caption}"' if self.caption else ""
        return f"![{self.caption or ''}]({self.url}{cap})"

    def to_html(self) -> str:
        if self.caption:
            return f'<figure><img src="{self.url}"/><figcaption>{self.caption}</figcaption></figure>'
        return f'<img src="{self.url}"/>'

class Slideshow(RichElement):
    def __init__(self, elements: List[Photo], caption: Optional[str] = None):
        self.elements = elements
        self.caption = caption

    def to_markdown(self) -> str:
        items = "\n".join([e.to_markdown() for e in self.elements])
        cap = f"<figcaption>{self.caption}</figcaption>" if self.caption else ""
        return f"<tg-slideshow>\n{items}\n{cap}\n</tg-slideshow>"

    def to_html(self) -> str:
        items = "".join([e.to_html() for e in self.elements])
        cap = f"<figcaption>{self.caption}</figcaption>" if self.caption else ""
        return f"<tg-slideshow>{items}{cap}</tg-slideshow>"

class Collage(RichElement):
    def __init__(self, elements: List[Photo], caption: Optional[str] = None):
        self.elements = elements
        self.caption = caption

    def to_markdown(self) -> str:
        items = "\n".join([e.to_markdown() for e in self.elements])
        cap = f"<figcaption>{self.caption}</figcaption>" if self.caption else ""
        return f"<tg-collage>\n{items}\n{cap}\n</tg-collage>"

    def to_html(self) -> str:
        items = "".join([e.to_html() for e in self.elements])
        cap = f"<figcaption>{self.caption}</figcaption>" if self.caption else ""
        return f"<tg-collage>{items}{cap}</tg-collage>"

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
