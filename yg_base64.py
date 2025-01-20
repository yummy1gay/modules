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

import base64

from .. import loader, utils

@loader.tds
class yg_base64(loader.Module):
    """Encode and decode text using Base64"""

    strings = {"name": "yg_base64"}

    async def encodecmd(self, message):
        """<text> encode the provided text using Base64"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "<b>No text provided to encode.</b>")
            return

        encoded_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        await utils.answer(message, f"<b>Encoded text:</b> <code>{encoded_text}</code>")

    async def decodecmd(self, message):
        """<text> decode the provided Base64 encoded text"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "<b>No encoded text provided to decode</b>")
            return

        try:
            decoded_text = base64.b64decode(text).decode("utf-8")
            await utils.answer(message, f"<b>Decoded text:</b> <code>{decoded_text}</code>")
        except Exception as e:
            await utils.answer(message, f"<b>Error decoding text:</b> <code>{str(e)}</code>")