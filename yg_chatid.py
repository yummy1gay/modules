__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

from telethon.tl.types import User, Chat, Channel
from yumlib import yummy

from .. import loader, utils

@loader.tds
class yg_chatid(loader.Module):
    """Модуль для отображения ID чатов, каналов или пользователей"""

    strings = {
        "name": "yg_chatid",
        "chat_id": "<b>Chat ID:</b> <code>{}</code>",
        "user_id": "<b>User ID:</b> <code>{}</code>",
        "not_found": "<b>Not Found</b>"
    }

    async def client_ready(self, client, db):
        await yummy(client)

    async def chatidcmd(self, message):
        """<reply>/@username - узнать ID юзера (на сообщение которого вы ответили), указанного юзера или текущего чата"""
        args = utils.get_args_raw(message)

        if message.is_reply:
            reply_msg = await message.get_reply_message()
            entity = await message.client.get_entity(reply_msg.sender_id)
            await self.who(message, entity)
            return
        
        if args:
            try:
                entity = await message.client.get_entity(args)
                await self.who(message, entity)
            except Exception:
                await message.edit(self.strings["not_found"])
            return
        
        id = message.chat_id
        await message.edit(self.strings["chat_id"].format(id))

    async def who(self, message, entity):
        if isinstance(entity, User):
            await message.edit(self.strings["user_id"].format(entity.id))
        elif isinstance(entity, (Chat, Channel)):
            await message.edit(self.strings["chat_id"].format(entity.id))
        else:
            await message.edit(self.strings["not_found"])
