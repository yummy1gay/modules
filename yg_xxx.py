__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

from .. import loader, utils

@loader.tds
class yg_xxx(loader.Module):
    """Модуль для копирования сообщений и отправки их по указанному юзернейму (создавался для того, чтобы пиздить сообщения из каналов или чатов, где это запрещено). (@username можно указать в конфиге, и не указывать его каждый раз при вводе команды)"""

    strings = {"name": "yg_xxx"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "@username",
                "",
                "@username куда будет отправлятся медиа (указывать без @)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )

    async def xxxcmd(self, message):
        """<ссылка на сообщение> <@username (без @)> - скопировать сообщение (текст или медиа) и отправить по указаному юзернейму"""
        try:
            args = utils.get_args_raw(message)
            if not args:
                await message.edit("<emoji document_id=5397836737797954832>🤬</emoji> <b>Чёто ты не правильно ввёл. Пример:</b> <code>.xxx <ссылка на сообщение> <@username (без @)></code>")
                return

            args = args.split()
            if len(args) < 1:
                await message.edit("<emoji document_id=5397836737797954832>🤬</emoji> <b>Чёто ты не правильно ввёл. Пример:</b> <code>.xxx <ссылка на сообщение> <@username (без @)></code>")
                return

            link = args[0]
            username = args[1] if len(args) > 1 else self.config["@username"]

            if not link.startswith("https://t.me/"):
                await message.edit("<emoji document_id=5397836737797954832>🤬</emoji> <b>Неправильный формат ссылки. Используй ссылку на сообщение в Telegram</b>")
                return

            await message.edit("<emoji document_id=5215484787325676090>🕐</emoji> <b>Загружаю...</b>")

            x = link
            c = x.split('/')[3]
            i = int(x.split('/')[-1])

            z = message.client
            q = await z.get_messages(c, ids=i)

            if q.media:
                f = await z.download_media(q.media)

                if q.message:
                    if username:
                        await z.send_file(username, f, caption=q.text)
                    else:
                        await z.send_file('me', f, caption=q.text)
                else:
                    if username:
                        await z.send_file(username, f)
                    else:
                        await z.send_file('me', f)

                if username:
                    await message.edit(f"<emoji document_id=5210861495549707686>👍</emoji> <b>Успешно! Было обнаружено медиа, оно отправлено в @{username}</b>")
                else:
                    await message.edit("<emoji document_id=5210861495549707686>👍</emoji> <b>Успешно! Было обнаружено медиа, но так как ты не указал @username оно было отправлено в избранное</b>")
            else:
                if username:
                    await z.send_message(username, q.text)
                    await message.edit(f"<emoji document_id=5210861495549707686>👍</emoji> <b>Успешно! Был обнаружен текст, он отправлен в @{username}</b>")
                else:
                    await z.send_message('me', q.text)
                    await message.edit("<emoji document_id=5210861495549707686>👍</emoji> <b>Успешно! Был обнаружен текст, но так как ты не указал @username он был отправлен в избранное</b>")

        except Exception as e:
            await message.edit(f"<b>Ошибка: {e}</b>")
