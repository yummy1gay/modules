#meta developer: @yummy_gay
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader, utils

def register(cb):
    cb(SpamPonMod())

class SpamPonMod(loader.Module):
    """Модуль для спама, в конфиге нужно все указать"""

    strings = {"name": "yg_spampon"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "word", "yg", "Слово, которое будет использоваться для спама",
            "count", "100", "Количество повторений слова для спама",
            "username", "username", "Идентификатор пользователя бота"
        )

    async def spmcmd(self, message):
        """запустить спам"""
        word = self.config["word"]
        count = self.config["count"]
        username = self.config["username"]
        await message.delete()
        for _ in range(count):
            await message.client.send_message(username, word)