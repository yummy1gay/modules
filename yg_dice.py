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

import asyncio
import logging

from telethon.tl.types import InputMediaDice
import emoji

from .. import loader, security, utils

logger = logging.getLogger(__name__)

@loader.tds
class yg_dice(loader.Module):
    """Модуль для подкрутки эмодзи игр"""

    strings = {"name": "yg_dice"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "POSSIBLE_VALUES",
            {
                "": [1, 2, 3, 4, 5, 6],
                "🎲": [1, 2, 3, 4, 5, 6],
                "🎯": [1, 2, 3, 4, 5, 6],
                "🏀": [1, 2, 3, 4, 5],
            },
            "Mapping of emoji to possible values",
        )

    async def count(self, message, emoji_arg):
        if emoji.emoji_count(emoji_arg) == 0:
            await message.edit("<emoji document_id=5274099962655816924>❗️</emoji> <b>Убедись, что ты ввел корректное эмодзи</b>")
            return False
        return True

    @loader.unrestricted
    async def dicecmd(self, message):
        """<айди чата> <эмодзи> <цифра> <кол-во>"""
        args = utils.get_args(message)

        if await self.allmodules.check_security(message, security.OWNER):
            if len(args) == 0:
                await message.edit("<emoji document_id=5210952531676504517>❌</emoji> <b>Не указаны аргументы. Используй:</b> <code>.dice <айди чата> <эмодзи> <цифра> <кол-во></code>\n\n<i>Пример:<i> <code>.dice -1006093001819 🎲 6 2</code> <i>или</i> <code>.dice 🎲 6 2</code> <i>или</i> <code>.dice 🎲 6</code>")
                return

            if args[0].lstrip('-').isdigit():
                try:
                    chat_id = int(args[0])
                    chat = await message.client.get_input_entity(chat_id)
                    emoji_arg = args[1] if len(args) > 1 else "🎲"
                    values_index = 2
                    count_index = 3
                except (ValueError, IndexError, TypeError):
                    await message.edit("<emoji document_id=5314504236132747481>⁉️</emoji> <b>Либо ты не ввёл айди чата, либо он неправильный</b>")
                    return
            else:
                chat = message.to_id
                emoji_arg = args[0]
                values_index = 1
                count_index = 2

            if await self.count(message, emoji_arg):
                possible = self.config["POSSIBLE_VALUES"].get(emoji_arg, None)
                if possible is None:
                    emoji_arg = "🎲"
                    possible = self.config["POSSIBLE_VALUES"][emoji_arg]

                values = set()
                try:
                    for val in args[values_index].split(","):
                        value = int(val)
                        if value in possible:
                            values.add(value)
                except (ValueError, IndexError):
                    values.clear()

                try:
                    count = int(args[count_index])
                except (ValueError, IndexError):
                    count = 1

                rolled = -1
                done = 0
                client = message.client
                while True:
                    task = client.send_message(chat, file=InputMediaDice(emoji_arg))
                    if message:
                        message = (await asyncio.gather(message.delete(), task))[1]
                    else:
                        message = await task
                    rolled = message.media.value
                    logger.debug("Rolled %d", rolled)
                    if rolled in values or not values:
                        done += 1
                        message = None
                        if done == count:
                            break
            else:
                try:
                    chat_id = int(args[0])
                    chat = await message.client.get_input_entity(chat_id)
                except (ValueError, IndexError, TypeError):
                    await message.edit("<emoji document_id=5314504236132747481>⁉️</emoji> <b>Либо ты не ввёл айди чата, либо он неправильный</b>")
                    return

                try:
                    emoji_arg = args[1]
                except IndexError:
                    emoji_arg = "🎲"

                await message.client.send_message(chat, file=InputMediaDice(emoji_arg))