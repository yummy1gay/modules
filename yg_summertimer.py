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
from datetime import datetime
import pytz
from telethon.tl.types import Message
from telethon.tl import types
from telethon import events

from .. import loader

class SummerModule(loader.Module):
    """Модуль для обратного отсчета до начала лета"""

    strings = {
        "name": "yg_summertimer",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "default_year", 2024, "Год по умолчанию для обратного отсчета до лета"
        )

    def config_complete(self):
        self.name = self.strings["name"]
    
    async def summercmd(self, message: Message):
        """отправить обратный отсчет до лета"""

        await message.delete()

        summer_start = datetime(datetime.now().year, 6, 1).replace(year=self.config["default_year"]).astimezone(
            pytz.timezone('Europe/Kyiv')
        )

        countdown_message = None

        while True:
            now = datetime.now().astimezone(pytz.timezone('Europe/Kyiv'))
            remaining_time = summer_start - now

            days, hours, minutes, seconds = (
                remaining_time.days,
                remaining_time.seconds // 3600,
                (remaining_time.seconds // 60) % 60,
                remaining_time.seconds % 60,
            )
            time_str = (
                f"<b><emoji document_id=5348312457750260828>🙀</emoji> Дней:</b> <code>{days}</code>\n\n"
                f"<b><emoji document_id=5348179601526892213>🙀</emoji> Часов:</b> <code>{hours:02d}</code>\n\n"
                f"<b><emoji document_id=5348175255019988816>🙀</emoji> Минут:</b> <code>{minutes:02d}</code>\n\n"
                f"<b><emoji document_id=5348140027698227662>🙀</emoji> Секунд:</b> <code>{seconds:02d}</code>\n\n"
                "<b>*Таймер обновляется каждые <i>11</i> секунд</b>"
            )

            if countdown_message:
                await countdown_message.edit(f"<emoji document_id=5368797338628271445>🙀</emoji> <b>До лета осталось:</b>\n\n{time_str}")
            else:
                countdown_message = await message.respond(
                    file='https://i.imgur.com/WlIx35i.jpg',
                    message=f"<b><emoji document_id=5368797338628271445>🙀</emoji> До лета осталось:</b>\n\n{time_str}",
                )

            await asyncio.sleep(11)

    async def summerstopcmd(self, message: Message):
        """выключить обновление таймера"""

        await message.delete()

        current_task = getattr(self, '_summer_task', None)
        if current_task and not current_task.done():
            current_task.cancel()
            setattr(self, '_summer_task', None)

        await message.respond("<b>Обновление таймера остановлено.</b>")
