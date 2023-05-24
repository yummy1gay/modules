# meta developer: @yummy_gay

import asyncio
import logging

from telethon.tl.types import InputMediaDice

from telethon import events

from .. import loader, security, utils
from telethon.errors import ChatSendMediaForbiddenError

logger = logging.getLogger(__name__)

@loader.tds
class DiceMod(loader.Module):
    """yg_dice"""

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

from telethon.errors import PeerIdInvalidError

@loader.tds
class DiceMod(loader.Module):
    """Подкрутить кубики теперь можно незаметно, ты можешь написать команду куда угодно, кубики бросятся в тот чат чье ChatID ты указал🕶"""

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

    @loader.unrestricted
    async def dicecmd(self, message):
        """<айди чата> <эмодзи> <цифра> <кол-во>"""
        args = utils.get_args(message)
        if await self.allmodules.check_security(message, security.OWNER):
            try:
                chat_id = int(args[0])
                chat = await message.client.get_input_entity(chat_id)
            except (ValueError, IndexError, TypeError):
                await message.edit("Либо ты не ввёл айди чата, либо он неправильный.")
                return

            try:
                emoji = args[1]
            except IndexError:
                emoji = "🎲"

            possible = self.config["POSSIBLE_VALUES"].get(emoji, None)
            if possible is None:
                emoji = "🎲"
                possible = self.config["POSSIBLE_VALUES"][emoji]

            values = set()
            try:
                for val in args[2].split(","):
                    value = int(val)
                    if value in possible:
                        values.add(value)
            except (ValueError, IndexError):
                values.clear()

            try:
                count = int(args[3])
            except (ValueError, IndexError):
                count = 1

            rolled = -1
            done = 0
            client = message.client
            while True:
                task = client.send_message(chat, file=InputMediaDice(emoji))
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
                await message.edit("Либо ты не ввёл айди чата, либо он неправильный.")
                return

            try:
                emoji = args[1]
            except IndexError:
                emoji = "🎲"

            await message.client.send_message(chat, file=InputMediaDice(emoji))

    @loader.unrestricted
    async def ygchatidcmd(self, message):
        """<юзернейм чата> (показывает чат айди)"""
        args = utils.get_args(message)
        if len(args) != 1:
            await message.edit("Ты не ввёл юзернейм или ссылку чата.")
            return

        chat_link = args[0]
        try:
            chat = await message.client.get_entity(chat_link)
        except (ValueError, PeerIdInvalidError):
            await message.edit("Неправильный юзернейм или ссылка на чат.")
            return

        chat_id = chat.id
        await message.edit(f"Айди чата {chat_link}: -100{chat_id}.")