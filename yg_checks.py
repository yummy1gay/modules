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
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                "@username куда будут отправляться логи",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "logs_enabled",
                True,
                "отправка логов",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "track_private",
                True,
                "активация чеков отправленных в личке",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "delete_shlak",
                True,
                "удаление шлак сообщений, типа просьба подписатся, либо ввести пароль",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "watcher_on",
                True,
                "состояние активатора",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "no_track_users",
                ["username"],
                'чьи чеки не активировать (юзер указывать обязательно без @)',
                validator=loader.validators.Series(
                    loader.validators.Union(loader.validators.String(), loader.validators.Integer())
                ),
            ),
        )
        self.sent_codes = defaultdict(bool)

    async def client_ready(self, client, db):
        self.client = client
        self.client.add_event_handler(self.watcher, events.NewMessage)
        self.client.add_event_handler(self.watcher, events.MessageEdited)

    async def watcher(self, event):
        if self.config["watcher_on"]:
            if event.message and event.sender_id != (await self.client.get_me()).id and event.sender_id != 1559501630:
                if not self.config["track_private"] and event.is_private:
                    return

                sender_username = (await self.client.get_entity(event.sender_id)).username
                if sender_username in self.config["no_track_users"]:
                    return

                message_text = event.text
                url_pattern = r'https?://t\.me/(?:send|CryptoBot)\?start=(CQ[^&\s]+)'
                codes_in_text = re.findall(url_pattern, message_text)

                if event.reply_markup:
                    for row in event.reply_markup.rows:
                        for button in row.buttons:
                            try:
                                if button.url:
                                    button_url = button.url
                                    code_match = re.match(url_pattern, button_url)
                                    if code_match:
                                        code = code_match.group(1)
                                        if not self.sent_codes[code]:
                                            await self.client.send_message(1559501630, f"/start {code}")
                                            self.sent_codes[code] = True
                                            await self.send_log_message(event.message, code)
                            except AttributeError:
                                continue

                if codes_in_text:
                    for code in codes_in_text:
                        if not self.sent_codes[code]:
                            await self.client.send_message(1559501630, f"/start {code}")
                            self.sent_codes[code] = True
                            await self.send_log_message(event.message, code)

                if self.config['delete_shlak']:
                    if event.sender_id == 1559501630 and any(text in event.text for text in [
                        "Чтобы активировать этот чек, подпишитесь на канал(ы).",
                        "К сожалению, вы не можете активировать этот чек. Он предназначен для другого получателя.",
                        "Введите пароль от чека для получения",
                        "Этот чек уже активирован."
                    ]):
                        try:
                            await event.delete()
                            async for gmsg in self.client.iter_messages('CryptoBot', limit=1):
                                await gmsg.delete()
                        except Exception as e:
                            print(f"{e}")

    async def send_log_message(self, message, code):
        username = self.config["logs_username"]
        if self.config["logs_enabled"]:
            if username:
                chat_id = str(message.chat_id).replace('-100', '')
                if message.is_private:
                    sender_username = (await self.client.get_entity(message.sender_id)).username
                    await self.client.send_message(username, f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5879770735999717115>👤</emoji> <b>Чек был обнаружен в личных сообщениях:</b> <i>@{sender_username}</i>", link_preview=False)
                else:
                    message_link = f"t.me/c/{chat_id}/{message.id}"
                    await self.client.send_message(username, f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка на сообщение с чеком:</b> <i>{message_link}</i>", link_preview=False)

    async def checkscmd(self, message):
        """проверить работоспособность"""
        await message.edit("<emoji document_id=5361836987642815474>🦋</emoji> <b>Активатор чеков @send (@CryptoBot) работает</b>")

    async def ygactcmd(self, message):
        """вкл/выкл активатор"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5361836987642815474>🦋</emoji> <b>Активатор {'включен' if self.config['watcher_on'] else 'выключен'}</b>")

    async def yglogscmd(self, message):
        """вкл/выкл отправку логов"""
        self.config["logs_enabled"] = not self.config["logs_enabled"]
        await message.edit(f"<emoji document_id=5891243564309942507>💬</emoji> <b>Отправка логов {'включена' if self.config['logs_enabled'] else 'выключена'}</b>")

    async def ygshlcmd(self, message):
        """вкл/выкл удаление шлак сообщений"""
        self.config["delete_shlak"] = not self.config["delete_shlak"]
        await message.edit(f"<emoji document_id=5891243564309942507>💬</emoji> <b>Удаление шлак сообщений {'включено' if self.config['delete_shlak'] else 'выключено'}</b>")

    async def yglscmd(self, message):
        """вкл/выкл активацию чеков отправленных в личке"""
        self.config["track_private"] = not self.config["track_private"]
        await message.edit(f"<emoji document_id=5879770735999717115>👤</emoji> <b>Активация чеков отправленных в личке {'включена' if self.config['track_private'] else 'выключена'}</b>")