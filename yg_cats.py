# meta developer: @yummy_gay

import asyncio

from telethon.tl.types import Message

from .. import loader, utils


class YGCatsMod(loader.Module):
    """Модуль для вывода эмодзи кота по порядку (частоту обновления эмодзи можно изменить в конфиге)"""

    strings = {
        "name": "yg_cats",
    }

    emojis = [
        "<emoji document_id=5348312457750260828>🙀</emoji>",
        "<emoji document_id=5348179601526892213>🙀</emoji>",
        "<emoji document_id=5348175255019988816>🙀</emoji>",
        "<emoji document_id=5348140027698227662>🙀</emoji>",
    ]

    def __init__(self):
        self.config = loader.ModuleConfig("sleep_time", 10, lambda m: self.strings("sleep_time_config", m))

    task = None

    async def ygcatscmd(self, message: Message):
        """родить меняющийся эмодзи"""
        if self.task and not self.task.done():
            await utils.answer(message, "вкл")
            return

        self.task = asyncio.create_task(self._run_ygcats(message))

    async def ygstopcmd(self, message: Message):
        """вкл/выкл"""
        if self.task and not self.task.done():
            self.task.cancel()
            self.task = None
            await utils.answer(message, "выкл")
        else:
            await utils.answer(message, "и так уже выкл ало")

    async def _run_ygcats(self, message: Message):
        sleep_time = self.config["sleep_time"]
        while True:
            for emoji in self.emojis:
                await utils.answer(message, emoji)
                await asyncio.sleep(sleep_time)