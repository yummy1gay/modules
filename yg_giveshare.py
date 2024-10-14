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
import cloudscraper
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import KeyboardButtonUrl, InputBotAppShortName
from telethon.tl.functions.messages import RequestAppWebViewRequest
from yumlib import yummy
from telethon import errors
from urllib.parse import unquote

from .. import loader

@loader.tds
class yg_giveshare(loader.Module):
    """Модуль для автоматического участия в розыгрышах @GiveShareBot"""

    strings = {"name": "yg_giveshare"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                "@username канала/чята для логов (если вы хотите сохранять логи в избранном, укажите здесь 'me'; без @)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "watcher_on",
                True,
                "состояние активатора",
                validator=loader.validators.Boolean()
            )
        )
        self.client = None
        self.scraper = cloudscraper.create_scraper()
        self.processed_codes = set()

    async def client_ready(self, client, db):
        self.client = client
        await yummy(client)
        self.client.add_event_handler(self.giveshare, events.NewMessage)
        self.client.add_event_handler(self.giveshare, events.MessageEdited)

    async def giveshare(self, event):
        if not self.config["watcher_on"]:
            return

        message_text = event.message.message
        url_pattern = r'https?://t\.me/GiveShareBot/app\?startapp=([A-Za-z0-9]+)'
        codes_in_text = re.findall(url_pattern, message_text)

        if event.message.reply_markup:
            for row in event.message.reply_markup.rows:
                for button in row.buttons:
                    if isinstance(button, KeyboardButtonUrl) and button.url:
                        code_match = re.match(url_pattern, button.url)
                        if code_match:
                            code = code_match.group(1)
                            if code not in self.processed_codes:
                                await self.participate(code)
                            return

        if codes_in_text:
            for code in codes_in_text:
                if code not in self.processed_codes:
                    await self.participate(code)
    
    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message, link_preview=False)

    async def participate(self, code):
        giveaway_url = f"https://t.me/GiveShareBot/app?startapp={code}"

        init_data = await self.data()
        
        response = self.scraper.post(
            'https://api.giveshare.ru/index',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*'
            },
            json={
                "initData": init_data,
                "param": code
            }
        )
        
        raffle_data = response.json()
        
        if 'raffle' in raffle_data:
            raffle = raffle_data['raffle']
            log_info = (
                f"<emoji document_id=5456140674028019486>⚡️</emoji> <b>Участвую в новом <a href='{giveaway_url}'>GiveShare розыгрыше</a>!</b>\n\n"
                f"<emoji document_id=5467538555158943525>💭</emoji> <b>Название:</b> <code>{raffle['title']}</code>\n"
                f"<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Текущее кол-во участников:</b> <code>{raffle['members_count']}</code>\n"
                f"<emoji document_id=5440621591387980068>🔜</emoji> <b>Дата окончания:</b> <code>{raffle['date_end']}</code>\n\n"
                f"<emoji document_id=5282843764451195532>🖥</emoji> <i>Так же подписался на данные каналы для участия в розыгрыше:</i>\n"
            )
            
            for channel in raffle['channels']:
                channel_link = channel['link']
                channel_name = channel['name']
                log_info += f'• <b><a href="{channel_link}">{channel_name}</a></b>\n'
                await self.subscribe(channel_link)
            
            self.scraper.post(
                'https://api.giveshare.ru/member/check',
                headers={'Content-Type': 'application/json'},
                json={
                    "initData": init_data,
                    "raffle": raffle['id']
                }
            )

            self.processed_codes.add(code)
            await self.log(log_info)
        else:
            return

    async def data(self):
        bot = await self.client.get_input_entity(1618805558)
        app = InputBotAppShortName(bot_id=bot, short_name="app")
        web_view = await self.client(RequestAppWebViewRequest(peer='me', app=app, platform='android'))
        auth_url = web_view.url
        init_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        return init_data

    async def subscribe(self, channel_link):
        invite_code = channel_link.split('+')[1]
        try:
            await self.client(ImportChatInviteRequest(invite_code))
        except errors.rpcerrorlist.UserAlreadyParticipantError:
            pass
        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Произошла ошибка при подписке на канал {channel_link}</b>: {e}")

    async def givesharecmd(self, message):
        """вкл/выкл автоматическое участие в розыгрышах"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5352746955648813465>🤓</emoji> <b>Автоматическое участие в розыгрышах {'включено' if self.config['watcher_on'] else 'выключено'}</b>")