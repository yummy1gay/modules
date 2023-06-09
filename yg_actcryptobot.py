# meta developer: @yummy_gay

import re
from .. import loader
import logging

logger = logging.getLogger(__name__)

@loader.tds
class yg_actCryptoBotModule(loader.Module):
    """Активатор для чеков @CryptoBot которые отправляют как ссылку"""
    strings = {
        "name": "yg_actCryptoBot",
    }

    async def client_rehdy(self, client, db):
        await client.send_message('CryptoBot', '/start')

    async def watcher(self, message):
        if message.text and 't.me/CryptoBot?start=' in message.text:
            match = re.search(r't.me/CryptoBot\?start=([A-Za-z0-9]+)', message.text)
            if match:
                code = match.group(1)
                command = f'/start {code}'
                await message.client.send_message('CryptoBot', command)
                await message.mark_read()

    async def stat_yg_actCryptoBotcmd(self, message):
        """проверить работоспособность"""
        await message.edit("<b>Активатор @CryptoBot работает <emoji document_id=5348140027698227662>🙀</emoji></b>")