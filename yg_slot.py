# meta developer: @yummy_gay
# ститл даун
from .. import loader
from telethon.tl.types import InputMediaDice

@loader.tds
class DiceRollModule(loader.Module):
    """Модуль для подкрутки игрового автомата (частое использование может вызвать FloodWait)"""

    strings = {
        "name": "yg_slot"
    }

    @loader.sudo
    async def yg_stcmd(self, message):
        """подкрутить слот"""
        val = 0
        await message.delete()
        while True:
            ms = await message.client.send_message(message.chat_id, file=InputMediaDice("🎰"))
            if ms.media.value == 64:
                break
            else:
                await ms.delete()
                
    async def floodinfocmd(self, message):
    	"""что такое FloodWait?"""
    	await message.edit("<emoji document_id=5348140027698227662>🙀</emoji> <b>Что такое флудвейт?</b>\n\n<emoji document_id=5870609858520158157>ℹ️</emoji><b>Флудвейт</b> <u>(floodwait)</u> <i>— это временный запрет на выполнение каких-то действий для конкретного аккаунта.</i>\n\n<emoji document_id=5870609858520158157>ℹ️</emoji><i>Обычно возникает из-за того, что пользователь совершал или пытался совершать однотипные операции слишком часто.</i>\n\n<emoji document_id=5870609858520158157>ℹ️</emoji><b>Не используй данный модуль часто дабы избежать floodwait.</b>")