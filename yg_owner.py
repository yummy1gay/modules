
__version__ = (1, 0, 0, 1)

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

import re
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.types import DocumentAttributeSticker
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import GetCustomEmojiDocumentsRequest
from telethon.tl.functions.messages import GetInlineBotResultsRequest

from .. import loader

@loader.tds
class yg_owner(loader.Module):
	"""Получить информацию о владельце стикер/эмодзи пака"""

	strings = {"name": "yg_owner"}

	async def ownercmd(self, msg):
		"""<reply to sticker/premium emoji> - узнать овнера пака"""
		if not msg.reply_to_msg_id:
			await msg.edit("<emoji document_id=5210952531676504517>❌</emoji> <i>Ответь на стикер или эмодзи, чтобы получить информацию</i>")
			return
		
		await msg.edit("<emoji document_id=4988080790286894217>🫥</emoji> <b>Получаю информацию...</b>")

		reply = await msg.get_reply_message()

		if reply.sticker:
			if reply.media and reply.media.document and isinstance(reply.media.document.attributes[1], DocumentAttributeSticker):
				await self.sticker(reply, msg)
				return

		elif reply.entities:
			if isinstance(reply.entities[0], MessageEntityCustomEmoji):
				await self.emoji(reply, msg)
				return

		await msg.edit("<emoji document_id=5210952531676504517>❌</emoji> <i>Ответь на стикер или эмодзи, чтобы получить информацию</i>")

	async def sticker(self, reply, msg):
		id = reply.media.document.attributes[1].stickerset.id >> 32
		set = await msg.client(GetStickerSetRequest(
			stickerset=reply.media.document.attributes[1].stickerset,
			hash=0
		))

		link = f"t.me/addemoji/{set.set.short_name}"
		await self.info(id, link, msg)

	async def emoji(self, reply, msg):
		id = reply.entities[0].document_id
		data = await msg.client(GetCustomEmojiDocumentsRequest(
			document_id=[id]
		))

		set = data[0].attributes[1].stickerset
		pack = await msg.client(GetStickerSetRequest(stickerset=set, hash=0))
		link = f"t.me/addemoji/{pack.set.short_name}"
		set_id = set.id >> 32
		await self.info(set_id, link, msg)

	async def info(self, id, link, msg):
		call = await msg.client(GetInlineBotResultsRequest(
			peer='me',
			offset='0',
			bot='usinfobot',
			query=str(id)
		))

		if call.results:
			result = call.results[0]
			name, username = self.extract(result)

			if name and username:
				await msg.edit(f"<b>Пак: {link}</b>\n"
				               f"<b>Информация об владельце:</b>\n\n"
						       f"• <b>UserID:</b> <code>⁣{id}</code>\n"
							   f"• <b>⁣Name:</b> <code>{name}</code>\n"
							   f"• <b>⁣Username:</b> <b>@{username}</b>")
			else:
				await msg.edit(f"<b>Пак: {link}</b>\n"
				               f"<b>Информация об владельце:</b>\n\n"
						       f"• <b>UserID:</b> <code>⁣{id}</code>\n"
							   f"• <b>⁣Name:</b> <code>не найдено</code>\n"
							   f"• <b>⁣Username:</b> <code>не найдено</code>")
		else:
			await msg.edit("<emoji document_id=5210952531676504517>❌</emoji> <b>Не удалось найти информацию о владельце</b>")

	def extract(self, result):
		name, username = None, None

		name_match = re.search(r"👦🏻\s*(.*?)\n", result.send_message.message)
		username_match = re.search(r"🌐\s*@([\w_]+)\n", result.send_message.message)

		if name_match:
			name = name_match.group(1).strip()

		if username_match:
			username = username_match.group(1).strip()

		return name, username