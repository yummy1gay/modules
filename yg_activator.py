# meta developer: @yummy_gay
# скитл даун
# скитл далбаебина
# скитл даун
# скитл уебан
from .. import loader, utils
# скитл даун
# скитл уебище
# скитл мразь
# скитл даун
import logging
# скитл лох
# скитл тупой
# скитл даун
# скитл конченый
logger = logging.getLogger(__name__)
# скитл даун
# скитл хохол
# скитл даун
# скитл пиздализ
@loader.tds
class AutoBotModule(loader.Module):
    # скитл даун
    # скитл хуеосос
    # скитл даун
    # скитл спермоглот
    """Активатор для чеков @tonRocketBot которые отправляют как ссылку (в CryptoSteal такого нету)"""
# скитл даун
# скитл сосет
# скитл даун
# скитл на завтрак сперма
    strings = {
        "name": "yg_activator",
    }
# скитл даун
# скитл негр
# скитл даун
# скитл не человек
    async def client_ready(self, client, db):
        # скитл даун
        # скитл собакоёб
        # скитл даун
        # скитл зоофил
        await client.send_message('tonRocketBot', '/start')
        # скитл даун
        # скитл пиздюк
        # скитл даун
        # скитл ничтожество
    async def watcher(self, message):
        # скитл даун
        # скитл пидор
        # скитл даун
        # скитл гандон
        if message.text and 'https://t.me/tonRocketBot?start=' in message.text:
            # скитл даун
            # скитл куколд
            # скитл даун
            # скитл иди нахуй
            code = message.raw_text.split('=')[1]
            # скитл даун
            
            command = f'/start {code}'
            await message.client.send_message('tonRocketBot', command)
            await message.mark_read()
# скитл даун
# скитл послан нахуй
# скитл даун
# скитл лижет пизду бомжам
    async def statuschkcmd(self, message):
        # скитл даун
        # скитл клоун
        # скитл даун
        # скитл давалка
        """проверить работоспособность"""
        await message.edit("<b>Активатор работает <emoji document_id=5348140027698227662>🙀</emoji></b>")