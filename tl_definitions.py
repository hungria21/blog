from telethon import types, functions
from telethon.tl.tlobject import TLObject, TLRequest
import struct
import random

class InputRichMessageMarkdown(TLObject):
    CONSTRUCTOR_ID = 0x09ac8186
    SUBCLASS_OF_ID = 0x5198eb53

    def __init__(self, markdown, photos=None, documents=None, rtl=False):
        self.markdown = markdown
        self.photos = photos or []
        self.documents = documents or []
        self.rtl = rtl

    def _bytes(self):
        flags = 0
        if self.photos:
            flags |= 1
        if self.documents:
            flags |= 2
        if self.rtl:
            flags |= 4

        res = [struct.pack('<I', self.CONSTRUCTOR_ID), struct.pack('<I', flags)]
        res.append(self.serialize_bytes(self.markdown))
        if self.photos:
            res.append(struct.pack('<I', 0x1cb5c415)) # Vector
            res.append(struct.pack('<i', len(self.photos)))
            for p in self.photos:
                res.append(p._bytes())
        if self.documents:
            res.append(struct.pack('<I', 0x1cb5c415)) # Vector
            res.append(struct.pack('<i', len(self.documents)))
            for d in self.documents:
                res.append(d._bytes())
        return b''.join(res)

class SendMessageLayer227Request(TLRequest):
    CONSTRUCTOR_ID = 0xfef48f62
    METHOD_NAME = 'messages.sendMessage'

    def __init__(self, peer, rich_message, reply_to=None, random_id=None, reply_markup=None):
        self.peer = peer
        self.rich_message = rich_message
        self.reply_to = reply_to
        self.random_id = random_id or random.getrandbits(64) - (1 << 63)
        self.reply_markup = reply_markup

    def _bytes(self):
        flags = 0x4000000 # Rich message flag
        if self.reply_to:
            flags |= 1
        if self.reply_markup:
            flags |= 64

        res = [struct.pack('<I', self.CONSTRUCTOR_ID), struct.pack('<I', flags)]
        res.append(self.peer._bytes())
        if self.reply_to:
            res.append(self.reply_to._bytes())
        res.append(struct.pack('<Q', self.random_id))
        res.append(self.serialize_bytes("")) # message is empty when rich_message is present
        if self.reply_markup:
            res.append(self.reply_markup._bytes())
        res.append(self.rich_message._bytes())
        return b''.join(res)

class InputBotInlineMessageRichMessage(TLObject):
    CONSTRUCTOR_ID = 0xb43df56c
    SUBCLASS_OF_ID = 0x892bed5e

    def __init__(self, rich_message, reply_markup=None):
        self.rich_message = rich_message
        self.reply_markup = reply_markup

    def _bytes(self):
        flags = 1
        if self.reply_markup:
            flags |= 4
        res = [struct.pack('<I', self.CONSTRUCTOR_ID), struct.pack('<I', flags)]
        res.append(self.rich_message._bytes())
        if self.reply_markup:
            res.append(self.reply_markup._bytes())
        return b''.join(res)

class SetInlineBotResultsLayer227Request(TLRequest):
    CONSTRUCTOR_ID = 0x69931754
    METHOD_NAME = 'messages.setInlineBotResults'

    def __init__(self, query_id, results, cache_time=0, gallery=False, private=False, next_offset=None, switch_pm=None):
        self.query_id = query_id
        self.results = results
        self.cache_time = cache_time
        self.gallery = gallery
        self.private = private
        self.next_offset = next_offset
        self.switch_pm = switch_pm

    def _bytes(self):
        flags = 0
        if self.gallery: flags |= 1
        if self.private: flags |= 2
        if self.next_offset: flags |= 4
        if self.switch_pm: flags |= 8

        res = [struct.pack('<I', self.CONSTRUCTOR_ID), struct.pack('<I', flags)]
        res.append(struct.pack('<Q', self.query_id))
        res.append(struct.pack('<i', self.cache_time))
        res.append(struct.pack('<I', 0x1cb5c415)) # Vector
        res.append(struct.pack('<i', len(self.results)))
        for r in self.results:
            res.append(r._bytes())
        if self.next_offset:
            res.append(self.serialize_bytes(self.next_offset))
        if self.switch_pm:
            res.append(self.switch_pm._bytes())
        return b''.join(res)
