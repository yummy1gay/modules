# meta developer: @yummy_gay
# скитл даун

from .. import loader
import logging

logger = logging.getLogger(__name__)

@loader.tds
class yg_actTonRocketModule(loader.Module):
    """Активатор для чеков @tonRocketBot которые отправляют как ссылку"""

    strings = {
        "name": "yg_actTonRocket",
    }

    async def client_ready(self, client, db):
        await client.send_message('tonRocketBot', '/start')
    
    async def watcher(self, message):
        if message.text and 'https://t.me/tonRocketBot?start=' in message.text:
            code = message.raw_text.split('=')[1]
            
            command = f'/start {code}'
            await message.client.send_message('tonRocketBot', command)
            await message.mark_read()

    async def stat_yg_actTonRocketcmd(self, message):
        """проверить работоспособность"""
        await message.edit("<b>Активатор @tonRocketBot работает <emoji document_id=5348140027698227662>🙀</emoji></b>")