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


from .. import loader, utils

@loader.tds
class yg_sendmsg(loader.Module):
    """Модуль для отправки сообщений на указанный юзернейм"""

    strings = {"name": "yg_sendmsg"}
    
    async def sendmsgcmd(self, message):
        """<username> <word> oтправляет сообщение на указанный юзернейм"""
        args = utils.get_args(message)
        if len(args) < 2:
            await message.edit("<b>Неверный формат.</b> <i>Используйте</i> <code>.sendmsg username word</code>")
            return
        username = args[0]
        word = " ".join(args[1:])
        await message.client.send_message(username, word)
        await message.edit(f"<b>Сообщение отправлено сюда:</b> <code>{username}</code><b>, слово:</b> <code>{word}</code>")
