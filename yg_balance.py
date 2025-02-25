__version__ = (1, 5)

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
import urllib.parse, json
from telethon import TelegramClient
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName

from .. import loader, utils

@loader.tds
class yg_balance(loader.Module):
    """Модуль для просмотра балансов в @CryptoBot и @wallet"""

    strings = {
        "name": "yg_balance",
        "cryptobot": (
            "<emoji document_id=5217705010539812022>☺️</emoji> <b>My balance in @CryptoBot:</b>\n\n{}"
        ),
        "wallet": (
            "<emoji document_id=5438394062434485433>💎</emoji> <b>My balance in @wallet:</b>\n\n{}"
        ),
    }

    strings_ru = {
        "name": "yg_balance",
        "cryptobot": (
            "<emoji document_id=5217705010539812022>☺️</emoji> <b>Мой баланс в @CryptoBot:</b>\n\n{}"
        ),
        "wallet": (
            "<emoji document_id=5438394062434485433>💎</emoji> <b>Мой баланс в @wallet:</b>\n\n{}"
        ),
    }

    strings_ua = {
        "name": "yg_balance",
        "cryptobot": (
            "<emoji document_id=5217705010539812022>☺️</emoji> <b>Мій баланс у @CryptoBot:</b>\n\n{}"
        ),
        "wallet": (
            "<emoji document_id=5438394062434485433>💎</emoji> <b>Мій баланс у @wallet:</b>\n\n{}"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "hide_0_balances",
                True,
                "hiding zero balances",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.scraper = cloudscraper.create_scraper()

    async def check(self, bot, message):
        async with message.client.conversation(bot) as conv:
            request = await conv.send_message("/wallet")
            answer = await conv.get_response()

            await request.delete()
            await answer.delete()

        return answer.text

    def cryptobot(self, text):
        hide_zeros = self.config["hide_0_balances"]
        
        lines = [line.strip() for line in text.split('\n') if line.strip() and 'Кошелёк' not in line]
        total_line = next((line for line in lines if line.startswith('≈')), '')
        balance_lines = [line for line in lines if not line.startswith('≈')]

        if hide_zeros:
            balance_lines = [line for line in balance_lines if not re.search(r':\s?0(?:\.0+)?\s\w+', line)]

        return '\n'.join(balance_lines) + (f"\n\n{total_line}" if total_line else '')

    async def auth(self):
        bot = await self.client.get_input_entity(1985737506)
        app = InputBotAppShortName(bot_id=bot, short_name="start")

        web_view = await self.client(RequestAppWebViewRequest(
            peer='me',
            app=app,
            platform='android'
        ))

        return web_view.url
    
    async def login(self):
        url = await self.auth()
        fragment = urllib.parse.unquote(urllib.parse.unquote(urllib.parse.urlparse(url).fragment[13:]))
        params = dict(urllib.parse.parse_qsl(fragment))
        params["user"] = json.loads(params.get("user", "{}"))

        data = {
            **params,
            "web_view_init_data_raw": urllib.parse.unquote(url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        }

        resp = self.scraper.post(
            f"https://walletbot.me/api/v1/users/auth/",
            json=data
        )

        return resp.json().get('value', {})
    
    async def get_balances(self):
        resp = self.scraper.get(
            "https://walletbot.me/api/v1/accounts/",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Authorization": await self.login(),
            },
        )

        hide_zeros = self.config["hide_0_balances"]
        balances = [
            f"<b>{account['currency']}:</b> {account['available_balance']} ({account['available_balance_usd_amount']}$)"
            for account in resp.json().get("accounts", [])
            if not (hide_zeros and account['available_balance'] == 0 and account['available_balance_usd_amount'] == 0.0)
        ]
        
        return balances
    
    @loader.command(ru_doc="проверить баланс в @CryptoBot",
                    ua_doc="перевірити баланс у @CryptoBot")
    async def bc(self, message):
        """check balance in @CryptoBot"""
        text = await self.check(1559501630, message)
        balance = self.cryptobot(text)
        await utils.answer(message, self.strings["cryptobot"].format(balance))

    @loader.command(ru_doc="проверить баланс в @wallet",
                    ua_doc="перевірити баланс у @wallet")
    async def bw(self, message):
        """check balance in @wallet"""
        balances = await self.get_balances()
        balance = "\n".join(balances) if balances else "-"
        await utils.answer(message, self.strings["wallet"].format(balance))

    @loader.command(ru_doc="вкл/выкл скрытие нулевых балансов",
                    ua_doc="увімк/вимк приховування нульових балансів")
    async def hide0(self, message):
        "on/off hiding zero balances"
        self.config["hide_0_balances"] = not self.config["hide_0_balances"]

        status = 'включено' if self.config["hide_0_balances"] else 'выключено'
        await utils.answer(
            message,
            f"<emoji document_id=5278611606756942667>❤️</emoji> <b>Скрытие нулевых балансов {status}</b>"
        )