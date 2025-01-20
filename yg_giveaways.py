__version__ = (1, 4, 9, 0)

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

import asyncio
import random
import re
from collections import defaultdict
from urllib.parse import unquote

import cloudscraper
from urlextract import URLExtract
from twocaptcha import TwoCaptcha
from telethon import events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import (
    ImportChatInviteRequest,
    RequestWebViewRequest
)
from telethon.tl.types import (
    MessageEntityUrl,
    MessageEntityTextUrl,
    MessageMediaWebPage
)

from .. import loader

@loader.tds
class yg_giveaways(loader.Module):
    """Модуль для автоматического участия в розыгрышах @CryptoBot"""

    strings = {"name": "yg_giveaways"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "48fa7d95329caadf367fff4cc5d15a80",
                "2captcha.com API Key (для прохождения Cloudflare Turnstile)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "logs_username",
                "",
                "@username куда будут отправляться логи",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "watcher_on",
                True,
                "состояние активатора",
                validator=loader.validators.Boolean()
            )
        )
        self.codes = defaultdict(bool)

    async def client_ready(self, client, db):
        self.scraper = cloudscraper.create_scraper()
        self.client = client
        self.solver = TwoCaptcha(self.config["api_key"])
        self.me = await self.client.get_me()
        self.me_id = self.me.id
        self.extractor = URLExtract()
        handlers = [
            (self.gw, [events.NewMessage, events.MessageEdited])
        ]

        for handler_func, event_list in handlers:
            for event in event_list:
                self.client.add_event_handler(handler_func, event)

    async def claim(self, url, bot_username):
        web_view = await self.client(RequestWebViewRequest(
            peer=bot_username,
            bot=bot_username,
            platform='android',
            from_bot_menu=False,
            url=url
        ))

        auth_url = web_view.url
        params = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        access_token = await self.get_token('https://api.send.tg/internal/v1/authentication/webapp', params)

        if access_token:
            code = url.split('/')[-1]
            giveaway_info = await self.get_giveaway_info(code, access_token)

            if giveaway_info:
                chats = giveaway_info.get('chats', [])
                join = giveaway_info.get("can_join")
                status = giveaway_info.get("member_status")
                if join and status == "not_member":
                    await self.join_channels(chats)
                    await self.participate_in_giveaway(code, access_token)

    async def get_giveaway_info(self, code, access_token):
        url = f'https://api.send.tg/internal/v1/giveaway/{code}'
        UserAgent = self.generate_random_user_agent()
        headers = {
            'Accept': 'application/json',
            'Cookie': f'access_token={access_token}',
            'User-Agent': UserAgent
        }

        response = self.scraper.get(url, headers=headers)
        if response.status_code == 200:
            giveaway_data = response.json()
            return giveaway_data
        else:
            await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Failed to fetch giveaway info. Status code:</b> <code>{response.status_code}</code>")
            return None

    async def join_channels(self, chats):
        for chat in chats:
            link = chat['link']
            try:
                if link.startswith('https://t.me/+'):
                    username = link.split('+')[-1]
                    try:
                        await self.client(ImportChatInviteRequest(username))
                        await asyncio.sleep(1)
                    except Exception as e:
                        await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Error joining invite link</b> <code>{username}</code><b>:</b> <code>{e}</code>")
                else:
                    try:
                        await self.client(JoinChannelRequest(link))
                        await asyncio.sleep(1)
                    except Exception as e:
                        await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Error joining channel<b> <code>{link}<code><b>:</b> <code>{e}</code>")

            except Exception as e:
                await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Failed to join channel</b> <code>{link}<code><b>:</b> <code>{e}</code>")

    async def solve_turnstile(self, url):
        sitekey = "0x4AAAAAAActoBfh_En8yr3T"
        solved = self.solver.turnstile(sitekey=sitekey, url=url)
        token = solved.get('code')
        return token

    async def get_token(self, url, params):
        json_data = {
            "initData": params
        }
        UserAgent = self.generate_random_user_agent()
        headers = {
            'Accept': 'application/json',
            'User-Agent': UserAgent
        }

        response = self.scraper.post(url, json=json_data, headers=headers)
        
        if response.status_code == 200:
            headers = response.headers
            set_cookie = headers.get('Set-Cookie')
            if set_cookie:
                access_token = set_cookie.split('access_token=')[1].split(';')[0]
                return access_token
            else:
                return None
        else:
            return None

    async def participate_in_giveaway(self, code, access_token):
        url = f'https://api.send.tg/internal/v1/giveaway/{code}/participate'
        UserAgent = self.generate_random_user_agent()
        headers = {
            'Accept': 'application/json',
            'Cookie': f'access_token={access_token}',
            'User-Agent': UserAgent
        }
        challenge_url = f"https://app.send.tg/giveaways/{code}"
        challenge_token = await self.solve_turnstile(challenge_url)
        json_data = {
            "challenge_token": challenge_token
        }

        response = self.scraper.post(url, json=json_data, headers=headers)
        if response.status_code == 200:
            pass
        else:
            await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Failed to participate in the giveaway. Status code:</b> <code>{response.status_code}</code>")

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    async def get_codes(self, text, entities, markup):
        urls_in_message = set()
        finded_codes = set()

        url_pattern = r'https?://t\.me/(?:send|CryptoBot)/app\?startapp=[a-zA-Z0-9_-]+?-([A-Za-z0-9]+)(?:-|$)'

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

    async def gw(self, message):
        if self.config["watcher_on"]:
            if message and message.sender_id not in [self.me_id, 1559501630]:
                try:
                    codes = await self.get_codes(message.text, message.entities, message.reply_markup)

                    if codes:
                        for code in codes:
                            if not self.codes[code]:
                                await self.claim(f"https://app.crypt.bot/giveaways/{code}", "send")
                                self.codes[code] = True
                except AttributeError:
                    pass

    async def giveawayscmd(self, message):
        """вкл/выкл активатор"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5361836987642815474>🦋</emoji> <b>Активатор {'включен' if self.config['watcher_on'] else 'выключен'}</b>")

    def generate_random_user_agent(self, device_type='android', browser_type='chrome'):
        existing_versions = {
            110: [
                '110.0.5481.154',
                '110.0.5481.153',
                '110.0.5481.65',
                '110.0.5481.64',
                '110.0.5481.63',
                '110.0.5481.61'
            ],
            111: [
                "111.0.5563.116",
                '111.0.5563.115',
                '111.0.5563.58',
                '111.0.5563.49'
            ],
            112: [
                '112.0.5615.136',
                '112.0.5615.136',
                '112.0.5615.101',
                '112.0.5615.100',
                '112.0.5615.48'
            ],
            113: [
                '113.0.5672.77',
                '113.0.5672.76'
            ],
            114: [
                '114.0.5735.60',
                '114.0.5735.53'
            ],
            115: [
                '115.0.5790.136'
            ],
            116: [
                '116.0.5845.172',
                '116.0.5845.164',
                '116.0.5845.163',
                '116.0.5845.114',
                '116.0.5845.92'
            ],
            117: [
                '117.0.5938.154',
                '117.0.5938.141',
                '117.0.5938.140',
                '117.0.5938.61',
                '117.0.5938.61',
                '117.0.5938.60'
            ],
            118: [
                '118.0.5993.112',
                '118.0.5993.111',
                '118.0.5993.80',
                '118.0.5993.65',
                '118.0.5993.48'
            ],
            119: [
                '119.0.6045.194',
                '119.0.6045.193',
                '119.0.6045.164',
                '119.0.6045.163',
                '119.0.6045.134',
                '119.0.6045.134',
                '119.0.6045.66',
                '119.0.6045.53'
            ],
            120: [
                '120.0.6099.230',
                '120.0.6099.210',
                '120.0.6099.194',
                '120.0.6099.193',
                '120.0.6099.145',
                '120.0.6099.144',
                '120.0.6099.144',
                '120.0.6099.116',
                '120.0.6099.116',
                '120.0.6099.115',
                '120.0.6099.44',
                '120.0.6099.43'
            ],
            121: [
                '121.0.6167.178',
                '121.0.6167.165',
                '121.0.6167.164',
                '121.0.6167.164',
                '121.0.6167.144',
                '121.0.6167.143',
                '121.0.6167.101'
            ],
            122: [
                '122.0.6261.119',
                '122.0.6261.106',
                '122.0.6261.105',
                '122.0.6261.91',
                '122.0.6261.90',
                '122.0.6261.64',
                '122.0.6261.43'
            ],
            123: [
                '123.0.6312.121',
                '123.0.6312.120',
                '123.0.6312.119',
                '123.0.6312.118',
                '123.0.6312.99',
                '123.0.6312.80',
                '123.0.6312.41',
                '123.0.6312.40'
            ],
            124: [
                '124.0.6367.179',
                '124.0.6367.172',
                '124.0.6367.171',
                '124.0.6367.114',
                '124.0.6367.113',
                '124.0.6367.83',
                '124.0.6367.82',
                '124.0.6367.54'
            ],
            125: [
                '125.0.6422.165',
                '125.0.6422.164',
                '125.0.6422.147',
                '125.0.6422.146',
                '125.0.6422.113',
                '125.0.6422.72',
                '125.0.6422.72',
                '125.0.6422.53',
                '125.0.6422.52'
            ],
            126: [
                '126.0.6478.122',
                '126.0.6478.72',
                '126.0.6478.71',
                '126.0.6478.50'
            ]
        }

        devices = [
            ('Samsung', 'SM-G980F', 'AVERAGE', 10),
            ('Samsung', 'SM-G973F', 'AVERAGE', 9),
            ('Samsung', 'SM-G973U', 'AVERAGE', 9),
            ('Samsung', 'SM-N986B', 'AVERAGE', 11),
            ('Samsung', 'SM-N981B', 'AVERAGE', 11),
            ('Samsung', 'SM-F916B', 'AVERAGE', 11),
            ('Samsung', 'SM-G998B', 'HIGH', 12),
            ('Samsung', 'SM-G991B', 'HIGH', 12),
            ('Samsung', 'SM-G996B', 'HIGH', 12),
            ('Samsung', 'SM-G990E', 'HIGH', 12),
            ('Samsung', 'SM-G990B', 'HIGH', 12),
            ('Samsung', 'SM-G990B2', 'HIGH', 12),
            ('Samsung', 'SM-G990U', 'HIGH', 12),
            ('Google', 'Pixel 5', 'AVERAGE', 11),
            ('Google', 'Pixel 5a', 'AVERAGE', 11),
            ('Google', 'Pixel 6', 'AVERAGE', 12),
            ('Google', 'Pixel 6 Pro', 'AVERAGE', 12),
            ('Google', 'Pixel 6 XL', 'AVERAGE', 12),
            ('Google', 'Pixel 6a', 'AVERAGE', 12),
            ('Google', 'Pixel 7', 'HIGH', 13),
            ('Google', 'Pixel 7a', 'AVERAGE', 13),
            ('Google', 'Pixel 7 Pro', 'HIGH', 13),
            ('Google', 'Pixel 8', 'HIGH', 14),
            ('Google', 'Pixel 8a', 'HIGH', 14),
            ('Google', 'Pixel 8 Pro', 'HIGH', 14),
            ('Google', 'Pixel 9', 'HIGH', 14),
            ('Google', 'Pixel 9 Pro', 'HIGH', 14),
            ('Google', 'Pixel 9 Pro XL', 'HIGH', 14),
            ('Xiaomi', 'Mi 10', 'AVERAGE', 10),
            ('Xiaomi', 'Mi 11', 'AVERAGE', 11),
            ('Xiaomi', 'Mi 12', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 10', 'HIGH', 11),
            ('Xiaomi', 'Redmi Note 10 Pro', 'HIGH', 11),
            ('Xiaomi', 'Redmi Note 11', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 11 Pro', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 12', 'HIGH', 13),
            ('Xiaomi', 'Redmi Note 12 Pro', 'HIGH', 13),
            ('Xiaomi', 'POCO M3 Pro', 'HIGH', 11),
            ('Xiaomi', 'POCO X5', 'HIGH', 12),
            ('Xiaomi', 'POCO X5 Pro', 'HIGH', 12),
            ('Xiaomi', 'POCO X6 Pro', 'HIGH', 13),
            ('Xiaomi', 'POCO F4', 'HIGH', 12),
            ('Xiaomi', 'POCO F4 GT', 'HIGH', 12),
            ('Xiaomi', 'POCO F3', 'HIGH', 11),
            ('OnePlus', 'NE2215', 'AVERAGE', 12),
            ('OnePlus', 'NE2210', 'AVERAGE', 12),
            ('OnePlus', 'IN2010', 'AVERAGE', 10),
            ('OnePlus', 'IN2023', 'AVERAGE', 11),
            ('OnePlus', 'LE2117', 'AVERAGE', 11),
            ('OnePlus', 'LE2123', 'AVERAGE', 11),
            ('OnePlus', 'CPH2423', 'AVERAGE', 12),
            ('Huawei', 'VOG-AL00', 'AVERAGE', 9),
            ('Huawei', 'ANA-AL00', 'AVERAGE', 10),
            ('Huawei', 'TAS-AL00', 'AVERAGE', 10),
            ('Huawei', 'OCE-AN10', 'AVERAGE', 11),
            ('Sony', 'J9150', 'AVERAGE', 9),
            ('Sony', 'J9210', 'AVERAGE', 10)
        ]

        firefox_versions = list(range(100, 127))

        if browser_type == 'chrome':
            major_version = random.choice(list(existing_versions.keys()))
            browser_version = random.choice(existing_versions[major_version])
        elif browser_type == 'firefox':
            browser_version = random.choice(firefox_versions)

        user_agent = ""

        if device_type == 'android':
            android_versions = {
                '10': 29,
                '11': 30,
                '12': 31,
                '13': 33,
                '14': 34
            }

            manufacturer, model, performance_class, min_android_version = random.choice(devices)
            android_version = str(random.choice([v for v in android_versions.keys() if int(v) >= min_android_version]))
            sdk_version = android_versions[android_version]

            if browser_type == 'chrome':
                major_version = random.choice(list(existing_versions.keys()))
                browser_version = random.choice(existing_versions[major_version])
                user_agent = (f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 "
                              f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 "
                              f"Telegram-Android/11.4.2 ({manufacturer} {model}; Android {android_version}; "
                              f"SDK {sdk_version}; {performance_class})")
            elif browser_type == 'firefox':
                browser_version = random.choice(firefox_versions)
                user_agent = (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                              f"Gecko/{browser_version}.0 Firefox/{browser_version}.0 "
                              f"Telegram-Android/11.4.2 ({manufacturer} {model}; Android {android_version}; "
                              f"SDK {sdk_version}; {performance_class})")

        elif device_type == 'ios':
            ios_versions = ['13.0', '14.0', '15.0', '16.0', '17.0', '18.0']
            ios_version = random.choice(ios_versions)
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                              f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                              f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version}.0 Mobile/15E148 Safari/605.1.15")

        elif device_type == 'windows':
            windows_versions = ['10.0', '11.0']
            windows_version = random.choice(windows_versions)
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              f"Chrome/{browser_version} Safari/537.36")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                              f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

        elif device_type == 'ubuntu':
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                              f"Chrome/{browser_version} Safari/537.36")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) Gecko/{browser_version}.0 "
                              f"Firefox/{browser_version}.0")

        return user_agent