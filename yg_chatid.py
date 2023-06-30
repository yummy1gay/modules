#meta developer: @yummy_gay

from .. import loader

@loader.tds
class yg_CHATIDModule(loader.Module):
    """Модуль для отображения ID чата в котором ты находишься"""

    strings = {
        "name": "yg_chatid",
        "group_id": "<b>Chat ID:</b> <code>{group_id}</code>"
    }

    async def chatidcmd(self, message):
        """отображает ID чата"""
        group_id = message.chat_id
        await message.edit(self.strings["group_id"].format(group_id=group_id))