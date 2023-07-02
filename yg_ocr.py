#meta developer: @yummy_gay

import io
import easyocr
from telethon import types
from telethon.tl import types as tl_types
from .. import loader

@loader.tds
class OCRModule(loader.Module):
    """Модуль для распознавания текста на фотографии"""
    strings = {
        "name": "yg_ocr",
    }

    async def client_ready(self, client, db):
        self.client = client

    async def check_photo(self, reply_message: types.Message):
        if reply_message and reply_message.media:
            if isinstance(reply_message.media, tl_types.MessageMediaPhoto):
                return reply_message.media.photo

    async def ocrcmd(self, message):
        """<reply> распознать текст на фото"""
        reply = await message.get_reply_message()
        photo = await self.check_photo(reply)
        if not photo:
            await message.edit("<b>Ответьте на фотографию, чтобы распознать текст</b>")
            return

        await message.edit("<b><emoji document_id=4988080790286894217>🫥</emoji> Распознавание текста...</b>")

        try:
            photo_data = await self.client.download_media(photo, bytes)
            reader = easyocr.Reader(["en"])
            result = reader.readtext(photo_data, detail=0, paragraph=True)
        except Exception as e:
            await message.edit(f"<b>Ошибка при распознавании текста: {e}</b>")
            return

        if result:
            text = "\n\n".join(result)
            await message.edit(f"<b><emoji document_id=5873146865637133757>🎤</emoji> Результат распознавания текста:</b>\n\n<emoji document_id=5471978009449731768>👉</emoji> {text} <emoji document_id=5469735272017043817>👈</emoji>")
        else:
            await message.edit("<b>На фото не удалось распознать текст</b>")

    async def stat_ocrcmd(self, message):
        """Проверить работоспособность модуля"""
        await message.edit("<b>Модуль OCRModule работает</b>")















