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
class SpamPonMod(loader.Module):
    """Модуль для спама, в конфиге нужно все указать"""

    strings = {"name": "yg_spampon"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "word", "yg", "Слово, которое будет использоваться для спама",
            "count", "100", "Количество повторений слова для спама",
            "username", "username", "Идентификатор пользователя бота"
        )

    async def spmcmd(self, message):
        """запустить спам"""
        word = self.config["word"]
        count = self.config["count"]
        username = self.config["username"]
        await message.delete()
        for _ in range(count):
            await message.client.send_message(username, word)
