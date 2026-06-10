from telethon import types, functions
from telethon.tl import TLObject, TLRequest
import struct

class InputRichMessageMarkdown(TLObject):
    CONSTRUCTOR_ID = 0x09ac8186

    def __init__(self, markdown, rtl=None, noautolink=None, photos=None, documents=None, users=None):
        self.markdown = markdown
        self.rtl = rtl
        self.noautolink = noautolink
        self.photos = photos
        self.documents = documents
        self.users = users

    def to_dict(self):
        return {
            '_': 'InputRichMessageMarkdown',
            'markdown': self.markdown,
            'rtl': self.rtl,
            'noautolink': self.noautolink,
            'photos': self.photos,
            'documents': self.documents,
            'users': self.users
        }

    def _bytes(self):
        flags = 0
        if self.rtl: flags |= 1
        if self.noautolink: flags |= 2
        if self.photos: flags |= 4
        if self.documents: flags |= 8
        if self.users: flags |= 16

        return (
            struct.pack('<I', self.CONSTRUCTOR_ID) +
            struct.pack('<I', flags) +
            TLObject.serialize_bytes(self.markdown) +
            (TLObject.serialize_bytes(self.photos) if self.photos else b'') +
            (TLObject.serialize_bytes(self.documents) if self.documents else b'') +
            (TLObject.serialize_bytes(self.users) if self.users else b'')
        )

class SendMessageLayer227Request(TLRequest):
    CONSTRUCTOR_ID = 0xfef48f62
    METHOD_NAME = 'messages.sendMessage'

    def __init__(self, peer, message, random_id,
                 no_webpage=None, silent=None, background=None, clear_draft=None,
                 noforwards=None, update_stickersets_order=None, invert_media=None,
                 allow_paid_floodskip=None, reply_to=None, reply_markup=None,
                 entities=None, schedule_date=None, schedule_repeat_period=None,
                 send_as=None, quick_reply_shortcut=None, effect=None,
                 allow_paid_stars=None, suggested_post=None, rich_message=None):
        self.peer = peer
        self.message = message
        self.random_id = random_id
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

    def _bytes(self):
        flags = 0
        if self.reply_to: flags |= 1
        if self.no_webpage: flags |= 2
        if self.reply_markup: flags |= 4
        if self.entities: flags |= 8
        if self.silent: flags |= 32
        if self.background: flags |= 64
        if self.clear_draft: flags |= 128
        if self.schedule_date: flags |= 1024
        if self.send_as: flags |= 8192
        if self.noforwards: flags |= 16384
        if self.update_stickersets_order: flags |= 32768
        if self.invert_media: flags |= 65536
        if self.quick_reply_shortcut: flags |= 131072
        if self.effect: flags |= 262144
        if self.allow_paid_floodskip: flags |= 524288
        if self.allow_paid_stars: flags |= 2097152
        if self.suggested_post: flags |= 4194304
        if self.rich_message: flags |= 8388608
        if self.schedule_repeat_period: flags |= 16777216

        return (
            struct.pack('<I', self.CONSTRUCTOR_ID) +
            struct.pack('<I', flags) +
            self.peer._bytes() +
            (self.reply_to._bytes() if self.reply_to else b'') +
            TLObject.serialize_bytes(self.message) +
            struct.pack('<q', self.random_id) +
            (self.reply_markup._bytes() if self.reply_markup else b'') +
            (TLObject.serialize_bytes(self.entities) if self.entities else b'') +
            (struct.pack('<I', self.schedule_date) if self.schedule_date else b'') +
            (struct.pack('<I', self.schedule_repeat_period) if self.schedule_repeat_period else b'') +
            (self.send_as._bytes() if self.send_as else b'') +
            (self.quick_reply_shortcut._bytes() if self.quick_reply_shortcut else b'') +
            (struct.pack('<q', self.effect) if self.effect else b'') +
            (struct.pack('<q', self.allow_paid_stars) if self.allow_paid_stars else b'') +
            (self.suggested_post._bytes() if self.suggested_post else b'') +
            (self.rich_message._bytes() if self.rich_message else b'')
        )
