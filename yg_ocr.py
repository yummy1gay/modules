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

from telethon import TelegramClient
from deep_translator import GoogleTranslator
import requests
import os

from .. import loader, utils

class yg_ocr(loader.Module):
    """Модуль для распознавания текста на изображении и перевода"""
    
    strings = {
        "name": "yg_ocr",
        "a": "<emoji document_id=6008090211181923982>📝</emoji> <b>Распознанный текст:</b>\n\n<code>{}</code>",
        "b": "<emoji document_id=5409014875517104495>📝</emoji> <b>Перевод:</b>\n\n<code>{}</code>",
        "c": "<emoji document_id=4949467677086188821>😭</emoji> <b>Ошибка при обработке изображения. Попробуйте еще раз</b>",
        "d": "<emoji document_id=5386367538735104399>⌛</emoji> <b>Обрабатываю изображение...</b>",
        "e": "<emoji document_id=4947293727849710197>🤬</emoji> <b>Ответьте на сообщение изображением</b>",
        "f": "<emoji document_id=4925063363672670983>🤷</emoji> <b>Не удалось распознать текст на изображении. Убедитесь, что изображение четкое и содержит текст</b>",
        "g": "<emoji document_id=4925063363672670983>🤷</emoji> <b>Не удалось перевести текст</b>",
        "h": "<emoji document_id=4949683473423008596>🍌</emoji> <b>На изображении не найден текст для распознавания</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "K86567468188957",
                "API ключ для ocr.space",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )

    async def client_ready(self, client: TelegramClient, db):
        self.client = client

    async def p(self, m):
        """распознать текст на изображении с помощью OCR"""
        r = await m.get_reply_message()
        if not r or not r.photo:
            await utils.answer(m, self.strings["e"])
            return None

        await utils.answer(m, self.strings["d"])

        f = await self.client.download_media(r.photo)
        p = {
            'isOverlayRequired': False,
            'apikey': self.config["api_key"],
            'language': 'eng',
            'scale': True,
            'OCREngine': 2
        }

        try:
            with open(f, 'rb') as file:
                s = requests.post(
                    'https://api.ocr.space/parse/image',
                    data=p,
                    files={'filename': ('image.png', file, 'image/png')}
                )
            s.raise_for_status()
        except requests.RequestException as e:
            print(f"Request Error: {e}")
            await utils.answer(m, self.strings["c"])
            return None
        finally:
            if os.path.exists(f):
                os.remove(f)

        l = s.json()
        if 'ParsedResults' in l and l['ParsedResults']:
            t = l['ParsedResults'][0].get('ParsedText', '').strip()
            if t:
                return t
            else:
                await utils.answer(m, self.strings["h"])
                return None
        else:
            await utils.answer(m, self.strings["f"])
            return None

    async def t(self, text, m):
        try:
            a = GoogleTranslator(source='auto', target='ru')
            i = a.translate(text=text)
            return i
        except Exception as e:
            print(f"Translation Error: {e}")
            await utils.answer(m, self.strings["g"])
            return None

    @loader.command()
    async def ocr(self, m):
        """распознать текст на изображении"""
        t = await self.p(m)
        if t:
            await utils.answer(m, self.strings["a"].format(t))

    @loader.command()
    async def trocr(self, m):
        """распознать и перевести текст на изображении"""
        t = await self.p(m)
        if t:
            n = await self.t(t, m)
            if n:
                await utils.answer(m, self.strings["b"].format(n))