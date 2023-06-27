#meta developer: @yummy_gay
import asyncio
import re
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from .. import loader
import logging

logger = logging.getLogger(__name__)

@loader.tds
class yg_actTonRocketModule(loader.Module):
    """Активатор для чеков @tonRocketBot, которые отправляются как ссылки"""

    strings = {
        "name": "yg_actTonRocket",
        "unsubscribe_enabled": "<b>Функция отписки от каналов включена <emoji document_id=5348140027698227662>🙀</emoji></b>",
        "unsubscribe_disabled": "<b>Функция отписки от каналов выключена <emoji document_id=5348140027698227662>🙀</emoji></b>",
    }

    def __init__(self):
        self.unsubscribe_enabled = False

    async def client_ready(self, client, db):
        await client.send_message('tonRocketBot', '/start')

    async def watcher(self, message):
        if message.text and 'https://t.me/tonRocketBot?start=' in message.text:
            match = re.search(r'https://t.me/tonRocketBot\?start=([A-Za-z0-9_/]+)', message.raw_text)
            if match:
                code = match.group(1)
                command = f'/start {code}'
                await message.client.send_message('tonRocketBot', command)
                await message.mark_read()
                await asyncio.sleep(2)
                await message.client.send_message('tonRocketBot', command)

        if message.from_id == 5014831088 and message.reply_markup:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if hasattr(button, 'url'):
                        url = button.url
                        if url.startswith('https://t.me/'):
                            channel_username = url.split('https://t.me/')[1]
                            await self.client(JoinChannelRequest(channel_username))
                            if self.unsubscribe_enabled:
                                await asyncio.sleep(5)
                                await self.client(LeaveChannelRequest(channel_username))

        if message.reply_markup and message.reply_markup.rows:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if button.url and button.url.startswith("https://t.me/tonRocketBot?start="):
                        text = self.extract_text_from_button_url(button.url)
                        if text:
                            await self.send_text_to_tonRocketBot(text)

    @staticmethod
    def extract_text_from_button_url(url):
        pattern = r"https://t.me/tonRocketBot\?start=([A-Za-z0-9_/]+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    async def send_text_to_tonRocketBot(self, text):
        await self.client.send_message("tonRocketBot", f"/start {text}")

    async def stat_ygcmd(self, message):
        """проверить работоспособность"""
        await message.edit("<b>Активатор чеков @tonRocketBot работает <emoji document_id=5348140027698227662>🙀</emoji></b>")

    async def unsubscribecmd(self, message):
        """включить/выключить функцию отписки от каналов"""
        self.unsubscribe_enabled = not self.unsubscribe_enabled
        if self.unsubscribe_enabled:
            await message.edit(self.strings["unsubscribe_enabled"])
        else:
            await message.edit(self.strings["unsubscribe_disabled"])