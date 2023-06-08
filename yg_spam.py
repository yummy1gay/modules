# meta developer: @yummy_gay

import asyncio
from asyncio import gather, sleep
from telethon.events import NewMessage

from .. import loader, utils


def register(cb):
    cb(yg_spamMod())


class yg_spamMod(loader.Module):
    """Спам модуль"""

    strings = {"name": "yg_spam"}
    spamming = False

    async def spamcmd(self, message):
        """<слово>"""
        if self.spamming:
            await utils.answer(
                message,
                "<b>Уже запущен спам.</b> <i>Используй</i> <code>.stopspam</code> <i>для остановки спама</i> <emoji document_id=5348140027698227662>🙀</emoji>",
            )
            await sleep(5)
            await message.delete()
            return

        args = utils.get_args(message)
        if not args:
            await utils.answer(
                message, "<b>Укажи слово для спама <emoji document_id=5348140027698227662>🙀</emoji></b>"
            )
            await sleep(5)
            await message.delete()
            return

        word = " ".join(args)
        self.spamming = True

        async def spam_task():
            while self.spamming:
                await message.client.send_message(message.to_id, word)

        await utils.answer(
            message,
            f"<b>Начинаю спамить словом</b> <code>{word}</code>. <i>Используй</i> <code>.stopspam</code> <i>для остановки</i> <emoji document_id=5348140027698227662>🙀</emoji>",
        )
        await gather(*[spam_task()])
        await sleep(10)
        await message.delete()
        return

    async def stopspamcmd(self, message):
        """остановить спам"""
        if not self.spamming:
            await utils.answer(
                message, "<b>Спам не запущен</b> <emoji document_id=5348140027698227662>🙀</emoji>"
            )
            await sleep(5)
            await message.delete()
            return

        self.spamming = False
        await utils.answer(
            message, "<b>Спам остановлен</b> <emoji document_id=5348140027698227662>🙀</emoji>"
        )
        await sleep(5)
        await message.delete()

    async def client_ready(self, client, db):
        self.client = client