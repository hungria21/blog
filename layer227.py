import struct
import random
from telethon import helpers
from telethon.tl.tlobject import TLObject, TLRequest

class InputRichMessageMarkdown(TLObject):
    CONSTRUCTOR_ID = 0x09ac8186
    def __init__(self, markdown, rtl=False, noautolink=False, photos=None, documents=None, users=None):
        self.markdown = markdown
        self.rtl = rtl
        self.noautolink = noautolink
        self.photos = photos or []
        self.documents = documents or []
        self.users = users or []

    def _bytes(self):
        flags = 0
        if self.rtl: flags |= 1
        if self.noautolink: flags |= 2
        if self.photos: flags |= 4
        if self.documents: flags |= 8
        if self.users: flags |= 16

        res = [
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', flags),
            helpers.encode_bytes(self.markdown.encode('utf-8'))
        ]

        if self.photos:
            res.append(b'\x15\xc4\xb5\x1c')
            res.append(struct.pack('<i', len(self.photos)))
            for p in self.photos: res.append(p._bytes())

        if self.documents:
            res.append(b'\x15\xc4\xb5\x1c')
            res.append(struct.pack('<i', len(self.documents)))
            for d in self.documents: res.append(d._bytes())

        if self.users:
            res.append(b'\x15\xc4\xb5\x1c')
            res.append(struct.pack('<i', len(self.users)))
            for u in self.users: res.append(u._bytes())

        return b''.join(res)

class InputBotInlineMessageRichMessage(TLObject):
    CONSTRUCTOR_ID = 0xb43df56c
    def __init__(self, rich_message, reply_markup=None):
        self.rich_message = rich_message
        self.reply_markup = reply_markup
    def _bytes(self):
        flags = 0
        if self.reply_markup: flags |= 4
        return b''.join((
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', flags),
            (self.reply_markup._bytes() if self.reply_markup else b''),
            self.rich_message._bytes(),
        ))

class InputBotInlineResult(TLObject):
    CONSTRUCTOR_ID = 0x88bf9319
    def __init__(self, id, type, send_message, title=None, description=None, url=None, thumb=None, content=None):
        self.id = id
        self.type = type
        self.send_message = send_message
        self.title = title
        self.description = description
        self.url = url
        self.thumb = thumb
        self.content = content
    def _bytes(self):
        flags = 0
        if self.title: flags |= 2
        if self.description: flags |= 4
        if self.url: flags |= 8
        if self.thumb: flags |= 16
        if self.content: flags |= 32
        return b''.join((
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', flags),
            helpers.encode_bytes(self.id.encode('utf-8')),
            helpers.encode_bytes(self.type.encode('utf-8')),
            (helpers.encode_bytes(self.title.encode('utf-8')) if self.title else b''),
            (helpers.encode_bytes(self.description.encode('utf-8')) if self.description else b''),
            (helpers.encode_bytes(self.url.encode('utf-8')) if self.url else b''),
            (self.thumb._bytes() if self.thumb else b''),
            (self.content._bytes() if self.content else b''),
            self.send_message._bytes(),
        ))

class SetInlineBotResultsLayer227Request(TLRequest):
    CONSTRUCTOR_ID = 0xbb12a419
    def __init__(self, query_id, results, cache_time=300, next_offset=None, gallery=False, is_private=False):
        self.query_id = query_id
        self.results = results
        self.cache_time = cache_time
        self.next_offset = next_offset
        self.gallery = gallery
        self.is_private = is_private
    def _bytes(self):
        flags = 0
        if self.gallery: flags |= 1
        if self.is_private: flags |= 2
        if self.next_offset is not None: flags |= 4
        return b''.join((
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', flags),
            struct.pack('<q', self.query_id),
            b'\x15\xc4\xb5\x1c',
            struct.pack('<i', len(self.results)),
            b''.join(r._bytes() for r in self.results),
            struct.pack('<i', self.cache_time),
            (helpers.encode_bytes(self.next_offset.encode('utf-8')) if self.next_offset is not None else b''),
        ))

class SendMessageLayer227Request(TLRequest):
    CONSTRUCTOR_ID = 0xfef48f62
    def __init__(self, peer, message, random_id=None, rich_message=None):
        self.peer = peer
        self.message = message
        self.random_id = random_id or random.getrandbits(63)
        self.rich_message = rich_message
    def _bytes(self):
        flags = 0
        if self.rich_message: flags |= (1 << 23)
        return b''.join((
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', flags),
            self.peer._bytes(),
            helpers.encode_bytes(self.message.encode('utf-8')),
            struct.pack('<q', self.random_id),
            (self.rich_message._bytes() if self.rich_message else b''),
        ))
