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
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest
import aiohttp
from aiocfscrape import CloudflareScraper
import random
import json
import os
from datetime import datetime, timedelta

from .. import loader

@loader.tds
class yg_dogs(loader.Module):
    """Completes tasks and receives daily check-ins in @dogshouse_bot"""

    strings = {"name": "yg_dogs"}

    def __init__(self):
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
        )

    async def client_ready(self, client, db):
        self.client = client
        headers = {'User-Agent': generate_random_user_agent(device_type='android', browser_type='chrome')}
        self.scraper = CloudflareScraper(headers=headers, timeout=aiohttp.ClientTimeout(total=60))
        me = await self.client.get_me()
        self.user_id = me.id
        self.file = "dogs.json"

        asyncio.create_task(self.dogs())

    async def data(self) -> str:
        web = await self.client(RequestWebViewRequest(
            peer='dogshouse_bot',
            bot='dogshouse_bot',
            platform='android',
            from_bot_menu=False,
            url='https://onetime.dog'
        ))

        url = web.url
        data = unquote(
            string=unquote(
                string=url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

        return data

    async def join(self, init):
        try:
            response = await self.scraper.post(
                url=f'https://api.onetime.dog/join',
                data=init
            )
            if response.status not in (200, 201):
                return (False, None, None, None)
            json = await response.json()
            balance = json.get('balance')
            reference = json.get('reference')
            streak = json.get('streak')
            return (True, balance, reference, streak)
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Join request error -</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")
            return (False, None, None, None)

    async def get_tasks(self, reference):
        try:
            response = await self.scraper.get(
                url=f'https://api.onetime.dog/tasks?user_id={self.user_id}&reference={reference}'
            )
            json = await response.json()
            return json
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Get tasks request error -</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")
            return None

    async def complete_tasks(self, tasks, reference):
        if not tasks:
            await self.log("<emoji document_id=5801007040155358213>😵</emoji> <b>No tasks found or error occurred</b> <i>(please report this - @yummy1gay)</i>")
            return

        methods = {
            'good-dog': self.verify,
            'send-bone-okx': self.verify,
            'send-bone-binance': self.verify,
            'send-bone-bybit': self.verify,
            'follow-dogs-x': self.verify,
            'subscribe-dogs': self.subscribe,
            'subscribe-blum': self.subscribe,
            'subscribe-notcoin': self.subscribe,
            'invite-frens': self.friends,
            'add-bone-telegram': self.bone,
        }

        no = [
            (task['slug'], task['reward'])
            for task in tasks if not task['complete']
        ]

        for slug, reward in no:
            if slug in methods:
                await methods[slug](slug, reference, reward)

    async def verify(self, task, reference, reward):
        try:
            url = f'https://api.onetime.dog/tasks/verify?task={task}&user_id={self.user_id}&reference={reference}'
            async with self.scraper.post(url) as response:
                if response.status == 200:
                    await self.log(f"<emoji document_id=5803416422319135133>😎</emoji> <b>Task</b> <b>'</b><code>{task}</code><b>'</b> <b>completed successfully. Reward:</b> <code>{reward}</code>")
                else:
                    await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Failed to verify task</b> <b>'</b><code>{task}</code><b>', status code:</b> <code>{response.status}</code> <i>(please report this - @yummy1gay)</i>")
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Error verifying task</b> <b>'</b><code>{task}</code><b>':</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")

    async def friends(self, slug, reference, reward):
        try:
            url = f'https://api.onetime.dog/frens?user_id={self.user_id}&reference={reference}'
            async with self.scraper.get(url) as response:
                json = await response.json()
                count = json.get('count', 0)
                if count >= 5:
                    await self.verify(slug, reference, reward)
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Error checking friends count:</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")

    async def subscribe(self, slug, reference, reward):
        try:
            if slug == 'subscribe-dogs':
                await self.client(JoinChannelRequest('dogs_community'))
            elif slug == 'subscribe-blum':
                await self.client(JoinChannelRequest('blumcrypto'))
            elif slug == 'subscribe-notcoin':
                await self.client(JoinChannelRequest('notcoin'))

            await self.verify(slug, reference, reward)
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Error subscribing to channel in task '</b><code>{slug}</code><b>':</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")

    async def bone(self, slug, reference, reward):
        try:
            me = await self.client.get_me()
            name = me.first_name

            await self.client(UpdateProfileRequest(first_name=f"{name} 🦴"))
            await asyncio.sleep(5)

            await self.verify(slug, reference, reward)
            await asyncio.sleep(3)
            
            await self.client(UpdateProfileRequest(first_name=name))
        except Exception as error:
            await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Error updating profile and verifying task:</b> <code>{error}</code> <i>(please report this - @yummy1gay)</i>")

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    async def dogs(self) -> None:
        first_run = True
        daily_streak = 0
        while self.config["running_on"]:
            if self.config["running_on"]:
                last_run = self.get()
                if not last_run or (datetime.now() - last_run) > timedelta(hours=12):
                    try:
                        init = await self.data()

                        status, balance, reference, streak = await self.join(init)

                        if daily_streak != streak:
                            daily_streak = streak
                            if first_run:
                                await self.log(f"<emoji document_id=5803416422319135133>😎</emoji> <b>Successfully remembered streak and maybe get it (first run)</b>")
                            else:
                                await self.log(f"<emoji document_id=5803416422319135133>😎</emoji> <b>Successfully got new streak, now</b> <code>{daily_streak}</code>")

                        tasks = await self.get_tasks(reference=reference)
                        if tasks:
                            await self.complete_tasks(tasks, reference=reference)

                        self.save()

                    except Exception as e:
                        await self.log(f"<emoji document_id=5801007040155358213>😵</emoji> <b>Error in def dogs:</b> <code>{e}</code> <i>(please report this - @yummy1gay)</i>")
            await asyncio.sleep(3600)

    def save(self):
        """Save the current time."""
        with open(self.file, "w") as f:
            json.dump({"last_run": datetime.now().isoformat()}, f)

    def get(self):
        """Get the last run time."""
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data["last_run"])
        return None

    async def bdogcmd(self, message):
        """show your balance, streak, and time remaining until the next check-in in @dogshouse_bot"""
        init = await self.data()
        status, balance, reference, streak = await self.join(init)

        if status:
            last_run = self.get()
            if last_run:
                next_check_in = last_run + timedelta(hours=12)
                remaining_time = next_check_in - datetime.now()
                hours_remaining = remaining_time.total_seconds() // 3600
                minutes_remaining = (remaining_time.total_seconds() % 3600) // 60
            else:
                hours_remaining, minutes_remaining = "Unknown", "Unknown"

            await message.edit(f"<emoji document_id=4978900228972217627>🐶</emoji> <b><a href='https://t.me/dogshouse_bot'>Dogs 🦴</a></b>\n\n"
                            f"<emoji document_id=5803416422319135133>😎</emoji> <b>Balance:</b> <code>{balance}</code>\n"
                            f"<emoji document_id=5803083266000951243>🔥</emoji> <b>Daily-Streak:</b> <code>{streak}</code>\n"
                            f"<emoji document_id=5803006063963804158>🤑</emoji> <b>Next check-in available in:</b> <code>{int(hours_remaining)}h {int(minutes_remaining)}m</code>")
        else:
            await message.edit("<emoji document_id=5801007040155358213>😵</emoji> <b>Failed to retrieve balance and streak</b>")

    async def dogscmd(self, message):
        """on/off running script"""
        self.config["running_on"] = not self.config["running_on"]
        if self.config["running_on"]:
            asyncio.create_task(self.dogs())
        await message.edit(f"<emoji document_id=4978900228972217627>🐶</emoji> <b>Script for <b><a href='https://t.me/dogshouse_bot'>Dogs 🦴</a></b> {'<b>on</b>' if self.config['running_on'] else '<b>off</b>'}</b>")

def generate_random_user_agent(device_type='android', browser_type='chrome'):
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
            'SM-G960F', 'Pixel 5', 'SM-A505F', 'Pixel 4a', 'Pixel 6 Pro', 'SM-N975F',
            'SM-G973F', 'Pixel 3', 'SM-G980F', 'Pixel 5a', 'SM-G998B', 'Pixel 4',
            'SM-G991B', 'SM-G996B', 'SM-F711B', 'SM-F916B', 'SM-G781B', 'SM-N986B',
            'SM-N981B', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3 XL', 'Pixel 4 XL',
            'Pixel 5 XL', 'Pixel 6', 'Pixel 6 XL', 'Pixel 6a', 'Pixel 7', 'Pixel 7 Pro',
            'OnePlus 8', 'OnePlus 8 Pro', 'OnePlus 9', 'OnePlus 9 Pro', 'OnePlus Nord', 'OnePlus Nord 2',
            'OnePlus Nord CE', 'OnePlus 10', 'OnePlus 10 Pro', 'OnePlus 10T', 'OnePlus 10T Pro',
            'Xiaomi Mi 9', 'Xiaomi Mi 10', 'Xiaomi Mi 11', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Note 9',
            'Huawei P30', 'Huawei P40', 'Huawei Mate 30', 'Huawei Mate 40', 'Sony Xperia 1',
            'Sony Xperia 5', 'LG G8', 'LG V50', 'LG V60', 'Nokia 8.3', 'Nokia 9 PureView'
        ])
        android_version = random.choice(android_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0']
        ios_version = random.choice(ios_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version}.0 Mobile/15E148 Safari/605.1.15")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

    elif device_type == 'ubuntu':
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) Gecko/{browser_version}.0 "
                    f"Firefox/{browser_version}.0")

    return None