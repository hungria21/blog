from pyrogram import raw
from pyrogram.raw.core import TLObject
from pyrogram.raw.core.primitives import Int, Long, String, Vector

def to_signed_int(n):
    import struct
    return struct.unpack('<i', struct.pack('<I', n))[0]

# Implementação manual dos tipos Layer 227 no PyroTGFork
class InputRichMessageMarkdown(TLObject):
    ID = 0x09ac8186
    QUALIFIED_NAME = "raw.types.InputRichMessageMarkdown"

    def __init__(self, markdown: str, rtl: bool = None, noautolink: bool = None,
                 photos: list = None, documents: list = None, users: list = None):
        self.markdown = markdown
        self.rtl = rtl
        self.noautolink = noautolink
        self.photos = photos
        self.documents = documents
        self.users = users

    def write(self):
        flags = 0
        if self.rtl: flags |= (1 << 0)
        if self.noautolink: flags |= (1 << 1)
        if self.photos: flags |= (1 << 2)
        if self.documents: flags |= (1 << 3)
        if self.users: flags |= (1 << 4)

        b = Int(self.ID, signed=False)
        b += Int(flags)
        b += String(self.markdown)
        if self.photos: b += Vector(self.photos)
        if self.documents: b += Vector(self.documents)
        if self.users: b += Vector(self.users)
        return b

class SendMessageLayer227(raw.functions.messages.SendMessage):
    ID = 0xfef48f62

    def __init__(self, peer, message, random_id,
                 no_webpage=None, silent=None, background=None, clear_draft=None,
                 noforwards=None, update_stickersets_order=None, invert_media=None,
                 allow_paid_floodskip=None, reply_to=None, reply_markup=None,
                 entities=None, schedule_date=None, schedule_repeat_period=None,
                 send_as=None, quick_reply_shortcut=None, effect=None,
                 allow_paid_stars=None, suggested_post=None, rich_message=None):
        super().__init__(peer=peer, message=message, random_id=random_id)
        self.no_webpage = no_webpage
        self.silent = silent
        self.background = background
        self.clear_draft = clear_draft
        self.noforwards = noforwards
        self.update_stickersets_order = update_stickersets_order
        self.invert_media = invert_media
        self.allow_paid_floodskip = allow_paid_floodskip
        self.reply_to = reply_to
        self.reply_markup = reply_markup
        self.entities = entities
        self.schedule_date = schedule_date
        self.schedule_repeat_period = schedule_repeat_period
        self.send_as = send_as
        self.quick_reply_shortcut = quick_reply_shortcut
        self.effect = effect
        self.allow_paid_stars = allow_paid_stars
        self.suggested_post = suggested_post
        self.rich_message = rich_message

    def write(self):
        flags = 0
        if self.reply_to: flags |= (1 << 0)
        if self.no_webpage: flags |= (1 << 1)
        if self.reply_markup: flags |= (1 << 2)
        if self.entities: flags |= (1 << 3)
        if self.silent: flags |= (1 << 5)
        if self.background: flags |= (1 << 6)
        if self.clear_draft: flags |= (1 << 7)
        if self.schedule_date: flags |= (1 << 10)
        if self.send_as: flags |= (1 << 13)
        if self.noforwards: flags |= (1 << 14)
        if self.update_stickersets_order: flags |= (1 << 15)
        if self.invert_media: flags |= (1 << 16)
        if self.quick_reply_shortcut: flags |= (1 << 17)
        if self.effect: flags |= (1 << 18)
        if self.allow_paid_floodskip: flags |= (1 << 19)
        if self.allow_paid_stars: flags |= (1 << 21)
        if self.suggested_post: flags |= (1 << 22)
        if self.rich_message: flags |= (1 << 23)
        if self.schedule_repeat_period: flags |= (1 << 24)

        b = Int(self.ID, signed=False)
        b += Int(flags)
        b += self.peer.write()
        if self.reply_to: b += self.reply_to.write()
        b += String(self.message)
        b += Long(self.random_id)
        if self.reply_markup: b += self.reply_markup.write()
        if self.entities: b += Vector(self.entities)
        if self.schedule_date: b += Int(self.schedule_date)
        if self.send_as: b += self.send_as.write()
        if self.quick_reply_shortcut: b += self.quick_reply_shortcut.write()
        if self.effect: b += Long(self.effect)
        if self.allow_paid_stars: b += Long(self.allow_paid_stars)
        if self.suggested_post: b += self.suggested_post.write()
        if self.rich_message: b += self.rich_message.write()
        if self.schedule_repeat_period: b += Int(self.schedule_repeat_period)
        return b
