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

import asyncio
from urllib.parse import unquote
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.tl.functions.channels import JoinChannelRequest
import aiohttp
from aiohttp_proxy import ProxyConnector
from aiocfscrape import CloudflareScraper
from yumlib import yummy
import random
import json
import os
from datetime import datetime, timedelta, timezone

from .. import loader

@loader.tds
class yg_whales(loader.Module):
    """AutoTapper and receives daily check-ins in @WheelOfWhalesBot with proxy support!"""

    strings = {"name": "yg_whales"}

    def __init__(self):
        self.file = "WheelOfWhales.json"
        
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                "channel/chat @username for logs (if you want to save logs to favorites, specify 'me' here; do not include @)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "running_on",
                False,
                "script status",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autotap",
                False,
                "autotap status",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "user_agent",
                "",
                "User-Agent string (leave empty to use random User-Agent) | Find out your User-Agent - t.me/YumUserAgentBot/app",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "proxy",
                "",
                "Proxy (http) settings in various formats: ip:port:user:pass, ip:port",
                validator=loader.validators.String()
            )
        )

    def load_user_agent(self):
        if self.config["user_agent"]:
            return self.config["user_agent"]
        
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                data = json.load(f)
                return data.get("user_agent", generate_random_user_agent(self))

        return generate_random_user_agent(self)

    def parse_proxy(self, proxy):
        if not proxy:
            return None
        
        parts = proxy.split(':')
        
        if len(parts) == 2:
            host, port = parts
            return {
                'type': 'http',
                'host': host,
                'port': port,
                'user': None,
                'pass': None
            }
        elif len(parts) == 4:
            host, port, user, password = parts
            return {
                'type': 'http',
                'host': host,
                'port': port,
                'user': user,
                'pass': password
            }
        else:
            return None

    async def check_proxy(self, proxy_config):
        if not proxy_config:
            return False

        proxy_url = f"{proxy_config['type']}://"
        
        if proxy_config['user'] and proxy_config['pass']:
            proxy_url += f"{proxy_config['user']}:{proxy_config['pass']}@"
        
        proxy_url += f"{proxy_config['host']}:{proxy_config['port']}"

        try:
            connector = ProxyConnector().from_url(proxy_url)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get('https://httpbin.org/ip') as response:
                    ip = (await response.json()).get('origin')
                    await self.log(f"<emoji document_id=5251203410396458957>🛡</emoji> <b>Proxy IP:</b> <code>{ip}</code>")
                    return True
        except Exception as e:
            await self.log(f"<emoji document_id=5251203410396458957>🛡</emoji> <b>Proxy:</b> <code>{proxy_url}</code>\n<emoji document_id=5237927129613614048>😡</emoji> <b>Error:</b> <code>{e}</code>")
            return False

        return False

    async def client_ready(self, client, db):
        self.client = client
        proxy = self.parse_proxy(self.config["proxy"])
        
        if proxy:
            if await self.check_proxy(proxy):
                if proxy['user'] and proxy['pass']:
                    connector = ProxyConnector().from_url(proxy['type'] + '://' + f"{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}")
                else:
                    connector = ProxyConnector().from_url(proxy['type'] + '://' + f"{proxy['host']}:{proxy['port']}")
                self.scraper = CloudflareScraper(connector=connector, timeout=aiohttp.ClientTimeout(total=60))
            else:
                self.scraper = CloudflareScraper(timeout=aiohttp.ClientTimeout(total=60))
        else:
            self.scraper = CloudflareScraper(timeout=aiohttp.ClientTimeout(total=60))
        
        me = await self.client.get_me()
        await yummy(client)
        self.user_id = me.id
        self.user_agent = self.load_user_agent()

        asyncio.create_task(self.wheel())
        asyncio.create_task(self.clicker())

    async def data(self) -> str:
        web = await self.client(RequestWebViewRequest(
            peer='WheelOfWhalesBot',
            bot='WheelOfWhalesBot',
            platform='android',
            from_bot_menu=False,
            url='https://clicker.crashgame247.io/'
        ))

        url = web.url
        return unquote(url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

    async def login(self):
        data_check_chain = await self.data()
        
        params = dict(item.split('=') for item in data_check_chain.split('&'))
        user_data = json.loads(unquote(params['user']))

        json_data = {
            "dataCheckChain": data_check_chain,
            "initData": {
                "query_id": params['query_id'],
                "user": user_data,
                "auth_date": params['auth_date'],
                "hash": params['hash']
            }
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "accept-language": "en,en-US;q=0.9",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://clicker.crashgame247.io/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent": self.user_agent
        }

        resp = await self.scraper.post("https://clicker-api.crashgame247.io/user/sync", json=json_data, headers=headers)
        resp_json = await resp.json()

        token = resp_json.get("token")
        whitelisted = resp_json.get("user", {}).get("whitelisted")
        nanoid = resp_json.get("user", {}).get("nanoid")
        balance = resp_json.get("balance", {}).get("amount")
        streak = resp_json.get("meta", {}).get("dailyLoginStreak")
        last_login = resp_json.get("meta", {}).get("lastFirstDailyLoginAt")
        next_spin = resp_json.get("meta", {}).get("nextSpinAt")

        return (token, whitelisted, nanoid, balance, streak, last_login, next_spin)

    async def claim_daily_bonus(self, token):
        headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": f"Bearer {token}",
            "User-Agent": self.user_agent
        }
        try:
            response = await self.scraper.patch("https://clicker-api.crashgame247.io/user/bonus/claim", headers=headers)
            response.raise_for_status()
            return True
        except Exception as e:
            await self.log(f"<emoji document_id=5237927129613614048>😡</emoji> <b>Error when claiming the daily bonus:</b> <code>{e}</code>")
            return False

    async def send_clicks(self, token, click_count):
        if self.config["autotap"]:
            headers = {
                "accept": "application/json, text/plain, */*",
                "authorization": f"Bearer {token}",
                "content-type": "application/json",
                "User-Agent": self.user_agent
            }
            await self.scraper.patch("https://clicker-api.crashgame247.io/meta/clicker", headers=headers, json={"clicks": click_count})

    async def clicker(self):
        if self.config["autotap"]:
            token, whitelisted, nanoid, balance, streak, last_login, next_spin = await self.login()
            if not token:
                return
            click_count = balance + 1

            while True:
                for _ in range(1000):
                    await self.send_clicks(token, click_count)
                    click_count += 1
                    await asyncio.sleep(random.uniform(1, 2))

                sleep_time = random.randint(1100, 2000)
                await self.log(f"<emoji document_id=5454132901371203117>🏖</emoji> <code>+1000</code> <b>clicks, going to sleep for</b> <code>{sleep_time // 60}</code> <b>minutes.</b>")
                await asyncio.sleep(sleep_time)

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    async def wheel(self) -> None:
        while self.config["running_on"]:
            try:
                token, whitelisted, nanoid, balance, streak, last_login, next_spin = await self.login()

                if not whitelisted:
                    await self.log(f"<emoji document_id=5237697597971378782>😢</emoji> <b>You is not whitelisted.</b>")
                    return

                last_login_time = datetime.strptime(last_login, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

                if datetime.now(timezone.utc) - last_login_time > timedelta(hours=24):
                    bonus = await self.claim_daily_bonus(token)
                    if bonus:
                        new_streak = streak + 1
                        await self.log(f"<emoji document_id=5235630748039394997>🥰</emoji> <b>Daily bonus successfully claimed!</b>\n<emoji document_id=5460961680328509338>🏎</emoji> <b>Current streak:</b> <code>{new_streak}</code>")

            except Exception as e:
                await self.log(f"<emoji document_id=5237927129613614048>😡</emoji> <b>Error in the wheel function:</b> <code>{e}</code> <i>(please report this - @yummy1gay)</i>")
            
            await asyncio.sleep(3600)

    async def bwhalescmd(self, message):
        """show your balance, current streak, next whalespin, and time remaining until the next check-in in @WheelOfWhalesBot"""
        await message.edit("<emoji document_id=5215484787325676090>🕐</emoji> <b>Fetching information...</b>")

        token, whitelisted, nanoid, balance, streak, last_login, next_spin = await self.login()

        if not whitelisted:
            await message.edit(f"<emoji document_id=5237697597971378782>😢</emoji> <b>You is not whitelisted.</b>")
            return
        
        if last_login:
            last_login_time = datetime.strptime(last_login, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            
            remaining_time = last_login_time + timedelta(hours=24) - datetime.now(timezone.utc)
            hours_remaining = remaining_time.total_seconds() // 3600
            minutes_remaining = (remaining_time.total_seconds() % 3600) // 60
        else:
            hours_remaining, minutes_remaining = "0", "0"

        await message.edit(f"<emoji document_id=5395643160560948786>✈️</emoji> <b><a href='https://t.me/wheelofwhalesbot?start={nanoid}pub'>Wheel Of Whales 🐳</a></b>\n\n"
                            f"<emoji document_id=5237708627447396243>🤑</emoji> <b>Balance:</b> <code>{balance}</code>\n"
                            f"<emoji document_id=5235630748039394997>🥰</emoji> <b>Current Daily-Streak:</b> <code>{streak}</code>\n"
                            f"<emoji document_id=5449742478427053613>🟡</emoji> <b>Next WhaleSpin at:</b> <code>{next_spin}</code>\n"
                            f"<emoji document_id=5460961680328509338>🏎</emoji> <b>Next check-in available in:</b> <code>{int(hours_remaining)}h {int(minutes_remaining)}m</code>")

    async def whalescmd(self, message):
        """on/off running script"""
        self.config["running_on"] = not self.config["running_on"]
        if self.config["running_on"]:
            asyncio.create_task(self.wheel())
        await message.edit(f"<emoji document_id=5237708627447396243>🤑</emoji> <b>Script for</b> <b><a href='https://t.me/wheelofwhalesbot'>Wheel Of Whales</a></b> {'<b>on</b>' if self.config['running_on'] else '<b>off</b>'}!</b>")

    async def autotapcmd(self, message):
        """on/off AutoTapper"""
        self.config["autotap"] = not self.config["autotap"]
        if self.config["autotap"]:
            asyncio.create_task(self.clicker())
        await message.edit(f"<emoji document_id=5235462501285507881>🐳</emoji> <b>AutoTapper for</b> <b><a href='https://t.me/wheelofwhalesbot'>Wheel Of Whales</a></b> {'<b>on</b>' if self.config['autotap'] else '<b>off</b>'}!</b>")

def generate_random_user_agent(self, device_type='android', browser_type='chrome'):
    chrome_versions = list(range(110, 127))
    firefox_versions = list(range(90, 100))

    if browser_type == 'chrome':
        major_version = random.choice(chrome_versions)
        minor_version = random.randint(0, 9)
        build_version = random.randint(1000, 9999)
        patch_version = random.randint(0, 99)
        browser_version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"
    elif browser_type == 'firefox':
        browser_version = random.choice(firefox_versions)

    if device_type == 'android':
        android_versions = ['10.0', '11.0', '12.0', '13.0']
        android_device = random.choice([
            'SM-G960F', 'Pixel 5', 'SM-A505F', 'Pixel 4a', 'Pixel 6 Pro', 
            'SM-N975F', 'SM-G973F', 'Pixel 3', 'SM-G980F', 'Pixel 5a', 
            'SM-G998B', 'Pixel 4', 'SM-G991B', 'SM-G996B', 'SM-F711B', 
            'SM-F916B', 'SM-G781B', 'SM-N986B', 'SM-N981B', 'Pixel 2', 
            'Pixel 2 XL', 'Pixel 3 XL', 'Pixel 4 XL', 'Pixel 5 XL', 
            'Pixel 6', 'Pixel 6 XL', 'Pixel 6a', 'Pixel 7', 'Pixel 7 Pro',
            'OnePlus 8', 'OnePlus 8 Pro', 'OnePlus 9', 'OnePlus 9 Pro', 
            'OnePlus Nord', 'OnePlus Nord 2', 'OnePlus Nord CE', 
            'OnePlus 10', 'OnePlus 10 Pro', 'OnePlus 10T', 
            'OnePlus 10T Pro', 'Xiaomi Mi 9', 'Xiaomi Mi 10', 
            'Xiaomi Mi 11', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Note 9',
            'Huawei P30', 'Huawei P40', 'Huawei Mate 30', 
            'Huawei Mate 40', 'Sony Xperia 1', 'Sony Xperia 5', 
            'LG G8', 'LG V50', 'LG V60', 'Nokia 8.3', 'Nokia 9 PureView'
        ])
        android_version = random.choice(android_versions)
        user_agent = (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) "
                      f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36")
        
    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0']
        ios_version = random.choice(ios_versions)
        user_agent = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                      f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) "
                      f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36")

    elif device_type == 'ubuntu':
        user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) "
                      f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36")

    else:
        return None

    with open(self.file, 'w') as f:
        json.dump({"user_agent": user_agent}, f)

    return user_agent