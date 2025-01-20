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
import requests
import os

from .. import loader

@loader.tds
class yg_capctha(loader.Module):
    """Решает капчу криптобота (если вы не прем юзер)"""

    strings = {"name": "yg_captcha"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "K86567468188957",
                "API ключ для ocr.space",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "captcha_on",
                True,
                "ляляля",
                validator=loader.validators.Boolean()
            ),
        )

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message):
        if self.config["captcha_on"]:
            if message.text and message.sender_id == 1559501630:
                if message.photo and (re.search(r'Пришлите символы, которые вы видите на картинке.', message.text) or
                                    re.search(r'Enter the characters you see in the image.', message.text)):
                    file = await self.client.download_media(message.photo)
                    payload = {
                        'isOverlayRequired': False,
                        'apikey': self.config["api_key"],
                        'language': 'eng',
                        'scale': True,
                        'OCREngine': 2
                    }

                    try:
                        with open(file, 'rb') as f:
                            response = requests.post(
                                'https://api.ocr.space/parse/image',
                                data=payload,
                                files={'filename': ('image.png', f, 'image/png')}
                            )

                        if response.status_code == 200:
                            result = response.json()
                            if 'ParsedResults' in result and result['ParsedResults']:
                                ocr_text = result['ParsedResults'][0].get('ParsedText', '').replace(" ", "")
                                await message.reply(ocr_text)
                            else:
                                sorry = await message.reply("/cancel")
                                await sorry.edit("/cancel\n\n<emoji document_id=5456337168781810982>😔</emoji> <b>Не удалось решить капчу</b>")
                                
                        else:
                            sorry = await message.reply("/cancel")
                            await sorry.edit("/cancel\n\n<emoji document_id=5456337168781810982>😔</emoji> <b>Не удалось решить капчу</b>")
                    finally:
                        if os.path.exists(file):
                            os.remove(file)

    async def captchacmd(self, message):
        """вкл/выкл решалку капчи"""
        self.config["captcha_on"] = not self.config["captcha_on"]
        await message.edit(f"<emoji document_id=5361836987642815474>🦋</emoji> <b>Решалка капчи @CryptoBot {'включена' if self.config['captcha_on'] else 'выключена'}</b>")