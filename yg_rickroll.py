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

import re
from pytube import YouTube
from telethon.tl.types import MessageEntityTextUrl

from .. import loader, utils

@loader.tds
class yg_rickroll(loader.Module):
    """Модуль чтобы проверить есть ли ссылка на рикролл в сообщении"""

    strings = {
        "name": "yg_rickroll",
        "no_reply": "<emoji document_id=5240241223632954241>🚫</emoji> <b>You did not reply to the message</b>",
        "no_youtube_link": "<emoji document_id=5240241223632954241>🚫</emoji> <b>No YouTube link found in the reply message</b>",
        "is_rick_roll": "<emoji document_id=5440660757194744323>‼️</emoji> <b>A RickRoll link was found in the message</b>",
        "is_not_rick_roll": "<emoji document_id=5206607081334906820>✔️</emoji> <b>No RickRoll link was found in the message</b>",
        "error": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Error retrieving video information:</b> <code>{}</code>",
        "loading": "<emoji document_id=5386367538735104399>⌛️</emoji> <b>Loading...</b>",
        "link_arg": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>You need to reply to the message with a YouTube video link</b>",
        "not_found": "<emoji document_id=5240241223632954241>🚫</emoji> <b>YouTube video link not found</b>"
    }

    strings_ru = {
        "no_reply": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Вы не ответили на сообщение</b>",
        "no_youtube_link": "<emoji document_id=5240241223632954241>🚫</emoji> <b>В сообщении не найдено ссылки на YouTube</b>",
        "is_rick_roll": "<emoji document_id=5440660757194744323>‼️</emoji> <b>В сообщении обнаружена ссылка на RickRoll</b>",
        "is_not_rick_roll": "<emoji document_id=5206607081334906820>✔️</emoji> <b>В сообщении не найдено ссылки на RickRoll</b>",
        "error": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Ошибка при получении информации об видео:</b> <code>{}</code>",
        "loading": "<emoji document_id=5386367538735104399>⌛️</emoji> <b>Загрузка...</b>",
        "link_arg": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Вам нужно ответить на сообщение с ссылкой на YouTube ролик</b>",
        "not_found": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Не найдено ссылки на YouTube ролик</b>"
    }
    
    async def rickcmd(self, message):
        """<reply> - проверить есть ли ссылка на рикролл в сообщении"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return
        
        url = self.extract_youtube_url(reply)
        if not url:
            await utils.answer(message, self.strings("no_youtube_link"))
            return
        
        try:
            video = YouTube(url)
            if "Never Gonna Give You Up" in video.title:
                await utils.answer(message, self.strings("is_rick_roll"))
            else:
                await utils.answer(message, self.strings("is_not_rick_roll"))
        except Exception as e:
            await utils.answer(message, self.strings("error").format(str(e)))

    def extract_youtube_url(self, message):
        """Extract YouTube URL from the message entities or text"""
        youtube_regex = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+|https?://youtu\.be/[\w-]+|https?://m\.youtube\.com/watch\?v=[\w-]+|https?://youtube\.tv/watch\?v=[\w-]+)'
        
        if message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityTextUrl):
                    if re.match(youtube_regex, entity.url):
                        return entity.url
        
        match = re.search(youtube_regex, message.raw_text)
        if match:
            return match.group(0)
        
        return None
