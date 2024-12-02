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

import re
from telethon import events
from collections import defaultdict
from yumlib import yummy
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl, MessageMediaWebPage
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from urlextract import URLExtract
import asyncio
import ast

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
                "watcher_on",
                True,
                "состояние активатора",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "subscribe",
                True,
                "подписываться ли на каналы чтобы активировать чеки которые этого требуют",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "unsubscribe",
                True,
                "отписываться ли от каналов после активации чека",
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
        await yummy(client)
        self.me = await self.client.get_me()
        self.me_id = self.me.id
        self.extractor = URLExtract()
        self.cache = set()
        handlers = [
            (self.cb, [events.NewMessage, events.MessageEdited]),
            (self.channels, [events.NewMessage, events.MessageEdited]),
            (self.passwords, [events.NewMessage, events.MessageEdited]),
        ]

        for handler_func, event_list in handlers:
            for event in event_list:
                self.client.add_event_handler(handler_func, event)

    async def get_codes(self, text, entities, markup):
        urls_in_message = set()
        finded_codes = set()

        url_pattern = r'https?://t\.me/(?:send|CryptoBot)\?start=([A-Za-z0-9_-]+)'

        if entities:
            for entity in entities:
                if isinstance(entity, MessageEntityUrl):
                    urls_in_text = self.extractor.find_urls(text)
                    for found_url in urls_in_text:
                        urls_in_message.add(found_url.strip())

                elif isinstance(entity, MessageEntityTextUrl):
                    url = entity.url.strip()
                    urls_in_message.add(url)

                elif isinstance(entity, MessageMediaWebPage):
                    url = entity.url.strip()
                    urls_in_message.add(url)

        if markup:
            for button_row in markup.rows:
                for button in button_row.buttons:
                    if hasattr(button, "url") and button.url:
                        urls_in_message.add(button.url.strip())

        for found_url in urls_in_message:
            clean_url = re.sub(r'[^\w:/?&=.-]', '', found_url)
            code_match = re.match(url_pattern, clean_url)
            if code_match:
                code = code_match.group(1)
                finded_codes.add(code)

        return list(finded_codes)

    async def password(self, pasw):

        def safeeval(expr):
            try:
                return int(eval(compile(ast.parse(expr, mode="eval"), '', 'eval')))
            except Exception:
                pass

        if pasw in self.cache:
            return None

        self.cache.add(pasw)

        try:
            return str(safeeval(pasw))
        except ValueError:
            pass

        if pasw.endswith("=?"):
            try:
                return str(safeeval(pasw[:-2]))
            except ValueError:
                pass

        if pasw.endswith("="):
            try:
                return str(safeeval(pasw[:-1]))
            except ValueError:
                pass

        lines = pasw.strip().split("\n")
        for line in lines:
            for sep in [": ", " - ", " — ", " = "]:
                if sep in line:
                    part = line.split(sep, 1)[1]
                    try:
                        return str(safeeval(part))
                    except ValueError:
                        return part

            if line.lower().startswith("пароль "):
                part = line[7:]
                try:
                    return str(safeeval(part))
                except ValueError:
                    return part

        return None

    async def cb(self, message):
        if self.config["watcher_on"]:
            if message.id in self.sent_codes:
                return

            if message and message.sender_id not in [self.me_id, 1559501630]:
                if not self.config["track_private"] and message.is_private:
                    return

                sender_username = getattr(message.sender, 'username', None) if message.sender else None
                if sender_username in self.config["no_track_users"]:
                    return

                codes = await self.get_codes(message.text, message.entities, message.reply_markup)

                if codes:
                    for code in codes:
                        if not self.sent_codes[code]:
                            if code.startswith('CQ'):
                                await self.client.send_message(1559501630, f"/start {code}")
                                self.sent_codes[code] = True
                                await self.send_log_message(message, code)

            self.sent_codes[message.id] = True

    async def channels(self, event):
        if not self.config["subscribe"]:
            return

        if not self.config["watcher_on"]:
            return

        if event.sender_id == 1559501630 and event.text.startswith('Чтобы активировать этот чек, подпишитесь на канал'):
            subscribed = []
            try:
                rows = event.reply_markup.rows if event.reply_markup else None
                if rows:
                    for row in rows:
                        for button in row.buttons:
                            if button.url:
                                invite_code = button.url.split('+', 1)[1]
                                await self.client(ImportChatInviteRequest(invite_code))
                                subscribed.append(invite_code)
            except Exception:
                pass

            await asyncio.sleep(1)
            await event.click(data=b'check-subscribe')
            await asyncio.sleep(1)

            if self.config["unsubscribe"]:
                for invite_code in subscribed:
                    channel_info = await self.client(CheckChatInviteRequest(hash=invite_code))
                    channel = channel_info.chat
                    await self.client(LeaveChannelRequest(channel))

    async def passwords(self, message):
        if not self.config["watcher_on"]:
            return

        if message.sender_id == 1559501630 and message.text.startswith('Введите пароль от чека для получения'):
            password = " ".join("\n".join(message.raw_text.split("\n")[2:]).split(" ")[1:])
            r = await self.password(password)
            if r !=None:
                await self.client.send_message(1559501630, r)

    async def send_log_message(self, message, code):
        username = self.config["logs_username"]
        if self.config["logs_enabled"]:
            if username:
                chat_id = str(message.chat_id).replace('-100', '')
                if message.is_private:
                    sender_username = getattr(message.sender, 'username', None) if message.sender else None
                    await self.client.send_message(username, f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5879770735999717115>👤</emoji> <b>Чек был обнаружен в личных сообщениях:</b> <i>@{sender_username}</i>", link_preview=False)
                else:
                    message_link = f"t.me/c/{chat_id}/{message.id}"
                    await self.client.send_message(username, f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка на сообщение с чеком:</b> <i>{message_link}</i>", link_preview=False)

    async def checkscmd(self, message):
        """вкл/выкл активатор"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5361836987642815474>🦋</emoji> <b>Активатор {'включен' if self.config['watcher_on'] else 'выключен'}</b>")

    async def yglogscmd(self, message):
        """вкл/выкл отправку логов"""
        self.config["logs_enabled"] = not self.config["logs_enabled"]
        await message.edit(f"<emoji document_id=5204396521797205590>💬</emoji> <b>Отправка логов {'включена' if self.config['logs_enabled'] else 'выключена'}</b>")

    async def yglscmd(self, message):
        """вкл/выкл активацию чеков отправленных в личке"""
        self.config["track_private"] = not self.config["track_private"]
        await message.edit(f"<emoji document_id=5393127508021365476>🔐</emoji> <b>Активация чеков отправленных в личке {'включена' if self.config['track_private'] else 'выключена'}</b>")

    async def subscribecmd(self, message):
        """вкл/выкл авто-подписку"""
        self.config["subscribe"] = not self.config["subscribe"]
        await message.edit(f"<emoji document_id=5436118876523865146>🍑</emoji> <b>Авто-подписка {'включена' if self.config['subscribe'] else 'выключена'}</b>")

    async def unsubscribecmd(self, message):
        """вкл/выкл авто-отписку"""
        self.config["unsubscribe"] = not self.config["unsubscribe"]
        await message.edit(f"<emoji document_id=5436118876523865146>🍑</emoji> <b>Авто-отписка {'включена' if self.config['unsubscribe'] else 'выключена'}</b>")