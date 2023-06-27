#meta developer: @yummy_gay

from .. import loader, utils

def register(cb):
    cb(SendMsgMod())

class SendMsgMod(loader.Module):
    """Модуль для отправки сообщений на указанный юзернейм"""

    strings = {"name": "yg_sendmsg"}

    async def sendmsgcmd(self, message):
        """<username> <word> oтправляет сообщение на указанный юзернейм"""
        args = utils.get_args(message)
        if len(args) < 2:
            await message.edit("<b>Неверный формат.</b> <i>Используйте</i> <code>.sendmsg username word</code>")
            return
        username = args[0]
        word = " ".join(args[1:])
        await message.client.send_message(username, word)
        await message.edit(f"<b>Сообщение отправлено сюда:</b> <code>{username}</code><b>, слово:</b> <code>{word}</code>")