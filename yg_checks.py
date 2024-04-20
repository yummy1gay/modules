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

        @client.on(events.NewMessage)
        @client.on(events.MessageEdited)
        async def watcher(event):
            if event.message and event.sender_id != (await client.get_me()).id and event.sender_id != 1559501630:
                if not self.config["track_private"] and event.is_private:
                    return

                sender_username = (await self.client.get_entity(event.sender_id)).username
                if sender_username in self.config["no_track_users"]:
                    return

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
                                        await self.send_log_message(event.message, code)

                if codes_in_text:
                    for code in codes_in_text:
                        if not self.sent_codes[code]:
                            await self.client.send_message('CryptoBot', f"/start {code}")
                            self.sent_codes[code] = True
                            await self.send_log_message(event.message, code)
    
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

    async def yglogscmd(self, message):
        """вкл/выкл отправку логов"""
        self.config["logs_enabled"] = not self.config["logs_enabled"]
        await message.edit(f"<emoji document_id=5891243564309942507>💬</emoji> <b>Отправка логов {'включена' if self.config['logs_enabled'] else 'выключена'}</b>")

    async def yglscmd(self, message):
        """вкл/выкл активацию чеков отправленных в личке"""
        self.config["track_private"] = not self.config["track_private"]
        await message.edit(f"<emoji document_id=5879770735999717115>👤</emoji> <b>Активация чеков отправленных в личке {'включена' if self.config['track_private'] else 'выключена'}</b>")