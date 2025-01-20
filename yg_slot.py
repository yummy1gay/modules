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

from telethon.tl.types import InputMediaDice

from .. import loader

@loader.tds
class yg_slot(loader.Module):
    """Модуль для подкрутки игрового автомата (частое использование может вызвать FloodWait)"""

    strings = {
        "name": "yg_slot"
    }
    
    @loader.sudo
    async def yg_stcmd(self, message):
        """подкрутить слот"""
        val = 0
        await message.delete()
        while True:
            ms = await message.client.send_message(message.chat_id, file=InputMediaDice("🎰"))
            if ms.media.value == 64:
                break
            else:
                await ms.delete()
                
    async def floodinfocmd(self, message):
        """что такое FloodWait?"""
        await message.edit("<emoji document_id=5348140027698227662>🙀</emoji> <b>Что такое флудвейт?</b>\n\n"
                        "<emoji document_id=5870609858520158157>ℹ️</emoji><b>Флудвейт</b> <u>(floodwait)</u> <i>— это временный запрет на выполнение каких-то действий для конкретного аккаунта.</i>\n\n"
                        "<emoji document_id=5870609858520158157>ℹ️</emoji><i>Обычно возникает из-за того, что пользователь совершал или пытался совершать однотипные операции слишком часто.</i>\n\n"
                        "<emoji document_id=5870609858520158157>ℹ️</emoji><b>Не используй данный модуль часто дабы избежать floodwait.</b>")