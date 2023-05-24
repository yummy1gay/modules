# meta developer: @yummy_gay

import asyncio
import random
from telethon.tl.types import Message
from .. import loader, utils

class YGCatsMod(loader.Module):
    """Модуль для вывода случайных эмодзи кота (only prem users)"""

    strings = {
        "name": "yg_cat"}

    emojis = [
        "<emoji document_id=5348140027698227662>🙀</emoji>",
        "<emoji document_id=5348175255019988816>🙀</emoji>",
        "<emoji document_id=5348179601526892213>🙀</emoji>",
        "<emoji document_id=5348312457750260828>🙀</emoji>"
    ]

    async def ygcatscmd(self, message: Message):
        """выводит случайное эмодзи котика каждые 10 секунд"""
        used_emojis = []
        while True:
            available_emojis = [emoji for emoji in self.emojis if emoji not in used_emojis]
            if not available_emojis:
                used_emojis = []
                available_emojis = self.emojis

            random_emoji = random.choice(available_emojis)
            used_emojis.append(random_emoji)

            await utils.answer(message, random_emoji)
            await asyncio.sleep(10)