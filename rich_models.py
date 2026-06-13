from typing import List, Optional, Union, Dict, Any

class RichText:
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

class RichTextPlain(RichText):
    def __init__(self, text: str):
        self.text = text
    def to_dict(self):
        return {"_": "richTextPlain", "text": self.text}

class RichTextBold(RichText):
    def __init__(self, text: RichText):
        self.text = text
    def to_dict(self):
        return {"_": "richTextBold", "text": self.text.to_dict()}

class RichTextItalic(RichText):
    def __init__(self, text: RichText):
        self.text = text
    def to_dict(self):
        return {"_": "richTextItalic", "text": self.text.to_dict()}

class RichTextUnderline(RichText):
    def __init__(self, text: RichText):
        self.text = text
    def to_dict(self):
        return {"_": "richTextUnderline", "text": self.text.to_dict()}

class RichTextStrikethrough(RichText):
    def __init__(self, text: RichText):
        self.text = text
    def to_dict(self):
        return {"_": "richTextStrikethrough", "text": self.text.to_dict()}

class RichTextUrl(RichText):
    def __init__(self, text: RichText, url: str):
        self.text = text
        self.url = url
    def to_dict(self):
        return {"_": "richTextUrl", "text": self.text.to_dict(), "url": self.url}

class RichTextMath(RichText):
    def __init__(self, text: str):
        self.text = text
    def to_dict(self):
        return {"_": "richTextMath", "text": self.text}

class RichTextList(RichText):
    def __init__(self, texts: List[RichText]):
        self.texts = texts
    def to_dict(self):
        return [t.to_dict() for t in self.texts]

# To handle concatenations of rich text
class RichTextConcat(RichText):
    def __init__(self, texts: List[RichText]):
        self.texts = texts
    def to_dict(self):
        # In some contexts, a list of RichText is expected
        return [t.to_dict() for t in self.texts]

class PageBlock:
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

class PageBlockParagraph(PageBlock):
    def __init__(self, text: RichText):
        self.text = text
    def to_dict(self):
        return {"_": "pageBlockParagraph", "text": self.text.to_dict()}

class PageBlockHeading(PageBlock):
    def __init__(self, text: RichText, level: int):
        self.level = level
        self.text = text
    def to_dict(self):
        return {"_": f"pageBlockHeading{self.level}", "text": self.text.to_dict()}

class PageBlockPreformatted(PageBlock):
    def __init__(self, text: RichText, language: str = ""):
        self.text = text
        self.language = language
    def to_dict(self):
        return {"_": "pageBlockPreformatted", "text": self.text.to_dict(), "language": self.language}

class PageBlockMath(PageBlock):
    def __init__(self, text: str):
        self.text = text
    def to_dict(self):
        return {"_": "pageBlockMath", "text": self.text}

class PageBlockDivider(PageBlock):
    def to_dict(self):
        return {"_": "pageBlockDivider"}

class PageBlockTable(PageBlock):
    def __init__(self, rows: List[List[RichText]], caption: Optional[RichText] = None):
        self.rows = rows
        self.caption = caption
    def to_dict(self):
        table_rows = []
        for row in self.rows:
            cells = [{"_": "pageBlockTableCell", "text": cell.to_dict()} for cell in row]
            table_rows.append({"_": "pageBlockTableRow", "cells": cells})
        res = {"_": "pageBlockTable", "rows": table_rows}
        if self.caption:
            res["caption"] = self.caption.to_dict()
        return res

class PageBlockList(PageBlock):
    def __init__(self, items: List[RichText], ordered: bool = False):
        self.items = items
        self.ordered = ordered
    def to_dict(self):
        block_type = "pageBlockOrderedList" if self.ordered else "pageBlockUnorderedList"
        list_items = [{"_": "pageListItem", "text": item.to_dict()} for item in self.items]
        return {"_": block_type, "items": list_items}

class InputRichMessage:
    def __init__(self, blocks: List[PageBlock], photos: List[str] = None, documents: List[str] = None):
        self.blocks = blocks
        self.photos = photos or []
        self.documents = documents or []
    def to_dict(self):
        return {
            "blocks": [b.to_dict() for b in self.blocks],
            "photos": self.photos,
            "documents": self.documents
        }
