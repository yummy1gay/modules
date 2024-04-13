#meta developer: @yummy1gay

import re
from telethon import events
from collections import defaultdict
from .. import loader

@loader.tds
class yg_checks(loader.Module):
    """Активатор чеков @send (@CryptoBot)"""

    strings = {"name": "yg_checks"}

    def __init__(self):
        self.sent_codes = defaultdict(bool)

    async def client_ready(self, client, db):
        self.client = client

        @client.on(events.NewMessage)
        @client.on(events.MessageEdited)
        async def watcher(event):
            if event.message and event.sender_id != (await client.get_me()).id and event.sender_id != 1559501630:
                message_text = event.message.message
                url_pattern = r'https?://t\.me/(?:send|CryptoBot)\?start=(CQ[^&\s]+)'
                codes_in_text = re.findall(url_pattern, message_text)

                if event.message.reply_markup:
                    for row in event.message.reply_markup.rows:
                        for button in row.buttons:
                            if button.url:
                                button_url = button.url
                                code_match = re.match(url_pattern, button_url)
                                if code_match:
                                    code = code_match.group(1)
                                    if not self.sent_codes[code]:
                                        await self.client.send_message('CryptoBot', f"/start {code}")
                                        self.sent_codes[code] = True

                if codes_in_text:
                    for code in codes_in_text:
                        if not self.sent_codes[code]:
                            await self.client.send_message('CryptoBot', f"/start {code}")
                            self.sent_codes[code] = True
    
    async def checkscmd(self, message):
        """проверить работоспособность"""
        await message.edit("<emoji document_id=5361836987642815474>🦋</emoji> <b>Активатор чеков @send (@CryptoBot) работает</b>")