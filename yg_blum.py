__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# c - claim/create/check

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

from telethon import TelegramClient
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName
from urllib.parse import unquote
import asyncio
import random
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from yumlib import yummy
import aiohttp
import json
from datetime import datetime, timedelta
import os
from aiohttp import ClientSession, ClientConnectorError
from asyncio.exceptions import TimeoutError

from .. import loader

@loader.tds
class yg_blum(loader.Module):
    """Играет в игры @blum, автоматически забирает ежедневные награды и токены с рефки, а также автофарминг токенов"""

    strings = {"name": "yg_blum"}

    def __init__(self):
        self.file = "blum.json"

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "random_points",
                "150, 250",
                "Рандомное кол-во поинтов за одну игру, вводить в формате: 0, 0. Макс. кол-во 280",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "logs_username",
                "",
                "@username канала/чята для логов (если вы хотите сохранять логи в избранном, укажите здесь 'me'; без @)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "running_on",
                False,
                "script status",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "auto_claim",
                False,
                "забирать ли автоматически ежедневную награду? (True - да, False - нет)",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "auto_play",
                False,
                "играть ли в игры автоматически когда появляются билеты? (True - да, False - нет)",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "auto_farm",
                False,
                "фармить ли токены автоматически? (True - да, False - нет)",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "ref_claim",
                False,
                "забирать ли периодически награду с рефки? (True - да, False - нет)",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "user_agent",
                "",
                "Строка User-Agent (оставьте поле пустым, чтобы использовать случайный User-Agent, который будет сгенерирован один раз и затем использоваться постоянно) | Узнай свой User-Agent - t.me/YumUserAgentBot/app",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "proxy",
                "",
                "Proxy (http), указывать в одном из форматов: ip:port:user:pass, ip:port",
                validator=loader.validators.String()
            )
        )

    def load_user_agent(self):
        if self.config.get("user_agent"):
            return self.config["user_agent"]

        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    data = json.load(f)
                    return data.get("user_agent", self.generate_random_user_agent())
            except (IOError, json.JSONDecodeError) as e:
                self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred while loading user agent from file:</b> <code>{e}</code>")

        return self.generate_random_user_agent()
    
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
            await self.log(f"<emoji document_id=5251203410396458957>🛡</emoji> <b>Proxy:</b> <code>{proxy_url}</code>\n<emoji document_id=5240241223632954241>🚫</emoji> <b>Error:</b> <code>{e}</code>")
            return False

        return False

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.user_agent = self.load_user_agent()
        self.game_url = "https://game-domain.blum.codes"
        self.user_url = "https://user-domain.blum.codes"
        proxy = self.parse_proxy(self.config["proxy"])

        headers = {'User-Agent': self.user_agent}

        if proxy:
            if await self.check_proxy(proxy):
                if proxy['user'] and proxy['pass']:
                    connector = ProxyConnector().from_url(proxy['type'] + '://' + f"{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}")
                else:
                    connector = ProxyConnector().from_url(proxy['type'] + '://' + f"{proxy['host']}:{proxy['port']}")
                self.scraper = CloudflareScraper(headers=headers, connector=connector, timeout=aiohttp.ClientTimeout(total=60))
            else:
                self.scraper = CloudflareScraper(headers=headers, timeout=aiohttp.ClientTimeout(total=60))
        else:
            self.scraper = CloudflareScraper(headers=headers, timeout=aiohttp.ClientTimeout(total=60))

        me = await self.client.get_me()
        self.user_id = me.id

        await yummy(client)

        asyncio.create_task(self.blum())

    async def web(self):
        try:
            bot = await self.client.get_input_entity(6865543862)
            app = InputBotAppShortName(bot_id=bot, short_name="app")

            web_view = await self.client(RequestAppWebViewRequest(
                peer='me',
                app=app,
                platform='android'
            ))

            auth_url = web_view.url
            web_data = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            return web_data

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred while getting TG web data:</b> <code>{e}</code>")
            raise

    async def login(self):
        json_data = {"query": await self.web()}

        try:
            response = await self.scraper.post(
                f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP",
                json=json_data
            )
            
            response.raise_for_status()
            
            response_json = await response.json()
            token = response_json.get("token", {}).get("access")

            if not token:
                raise ValueError("Access token not found in the response.")

            return "Bearer " + token

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during login:</b> <code>{e}</code>")
            raise

    async def claim(self, token):
        try:
            headers = {
                'Authorization': token,
                'Accept': 'application/json',
                'User-Agent': self.user_agent
            }

            response = await self.scraper.post(
                f"{self.game_url}/api/v1/daily-reward?offset=-180",
                headers=headers
            )
            
            response_text = await response.text()

            return True if response_text == 'OK' else response_text

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during claim daily reward:</b> <code>{e}</code>")

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    async def dogs(self, t):
        u = f'{self.game_url}/api/v2/game/eligibility/dogs_drop'
        h = {
            'Authorization': f'Bearer {t}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://telegram.blum.codes',
            'user-agent': self.user_agent,
        }
        try:
            async with self.scraper.get(u, headers=h) as r:
                if r is not None:
                    j = await r.json()
                    e = j.get('eligible', False)
                    return e
        except Exception as ex:
            pass
        
        return None

    async def cserver(self):
        url = f"https://ямме.рф/api/status"
        
        async with ClientSession() as session:
            try:
                async with session.get(url, timeout=3) as response:
                    if response.status == 200 and (await response.json()).get("status") == "ok":
                        test = "yyyy1488-uuuu-1488-mmmm-mmmm1488yyyy"
                        points = {"BP": {"amount": 150 + 300 * 5}}
                        assets = {
                            "BOMB": {"clicks": 0},
                            "CLOVER": {"clicks": 150},
                            "FREEZE": {"clicks": 0}
                        }
                        payload = await self.cpayload(test, points, assets)
                        if len(payload) == 684:
                            return True
                    return False
            except (TimeoutError, ClientConnectorError):
                pass
        return False

    async def cpayload(self, game, points, assets):
        url = f'https://ямме.рф/api/blum'
        payload = {
            'id': game,
            'points': points,
            'assets': assets
        }

        async with ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=10) as res:
                    if res.status == 200:
                        res_data = await res.json()
                        return res_data.get("payload")
                    else:
                        return None
            except Exception as e:
                await self.log(f"<b>Exception occurred:</b> <code>{e}</code>")

        return None

    async def play(self):
        """play all games 😈😈"""
        server = await self.cserver()
        if not server:
            await self.log("<emoji document_id=5460972181523537679>😞</emoji> <b>Сервер недоступен, попробую потом..</b>")
            return

        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Priority': 'u=1, i'
        }

        async with self.scraper.get(f'{self.game_url}/api/v1/user/balance', headers=head) as resp:
            count = (await resp.json())['playPasses']
        
        total_point = 0

        if count > 0:
            if self.config["logs_username"]:
                log = await self.client.send_message(self.config["logs_username"], "<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")
            
            for i in range(count):
                async with self.scraper.post(f'{self.game_url}/api/v2/game/play', headers=head) as post:
                    try:
                        response = await post.json()
                        game_id = response['gameId']
                    except KeyError:
                        await log.edit("<emoji document_id=5371035398841571673>💩</emoji> <b>Серверам <a href='https://t.me/blum'><b>Blum</b></a> сейчас очень плохо. Попробуйте позже!</b>")
                        return

                min_points, max_points = map(int, self.config["random_points"].strip('[]').split(','))

                sleep = random.uniform(30, 42)

                await asyncio.sleep(sleep)

                freezes = int((sleep - 30) / 3)
                clover = random.randint(min_points, max_points)

                amount = clover
                points = {"BP": {"amount": amount}}
                assets = {
                    "BOMB": {"clicks": 0},
                    "CLOVER": {"clicks": clover},
                    "FREEZE": {"clicks": freezes}
                }

                payload = await self.cpayload(game_id, points, assets)

                data = {'payload': payload}

                await self.scraper.post(
                    f'{self.game_url}/api/v2/game/claim',
                    headers=head,
                    data=json.dumps(data)
                )

                await log.edit(f'<emoji document_id=5852496924870971453>🐾</emoji> <b>{i + 1} / {count} игр</b>')
                await asyncio.sleep(random.randint(1, 5))
                total_point += amount

            await log.edit(f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Всего зафармлено $BLUM:</b> <code>{total_point}</code>")
        else:
            await log.edit("<emoji document_id=5460972181523537679>😞</emoji> <b>Нет билетов для игры :(</b>")

    async def balance(self, token):
        headers = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': self.user_agent
        }

        async with self.scraper.get(f"{self.game_url}/api/v1/user/balance", headers=headers) as response:
            response_data = await response.json()

        balance = response_data.get("availableBalance")
        play_passes = response_data.get("playPasses")
        timestamp = response_data.get("timestamp")

        start = None
        end = None
        if response_data.get("farming"):
            start = response_data["farming"].get("startTime")
            end = response_data["farming"].get("endTime")

        return (
            int(timestamp / 1000) if timestamp is not None else None,
            int(start / 1000) if start is not None else None,
            int(end / 1000) if end is not None else None,
            balance,
            play_passes
        )

    async def start(self, token):
        try:
            headers = {
                'Authorization': token,
                'Accept': 'application/json',
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Priority': 'u=1, i'
            }

            response = await self.scraper.post(
                f"{self.game_url}/api/v1/farming/start",
                headers=headers
            )

            if response.status != 200:
                response = await self.scraper.post(
                    f"{self.game_url}/api/v1/farming/start",
                    headers=headers
                )

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during start farming:</b> <code>{e}</code>")

    async def cfarm(self, token):
        try:
            while True:
                headers = {
                    'Authorization': token,
                    'Accept': 'application/json',
                    'User-Agent': self.user_agent,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json, text/plain, */*',
                    'Priority': 'u=1, i'
                }
                resp = await self.scraper.post(
                    f"{self.game_url}/api/v1/farming/claim",
                    headers=headers
                )
                if resp.status not in [200, 201]:
                    return None, None
                else:
                    break

            resp_json = await resp.json()

            return int(resp_json.get("timestamp") / 1000), resp_json.get("availableBalance")
        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during claim:</b> <code>{e}</code>")

    async def friend(self, token):
        try:
            headers = {
                'Authorization': token,
                'Accept': 'application/json',
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Priority': 'u=1, i'
            }

            while True:
                response = await self.scraper.get(
                    f"{self.user_url}/api/v1/friends/balance", 
                    headers=headers
                )

                if response.status not in [200, 201]:
                    return 0, False
                else:
                    break
            
            response_data = await response.json()
            claim_amount = response_data.get("amountForClaim")
            is_available = response_data.get("canClaim")

            return claim_amount, is_available

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during friend balance:</b> <code>{e}</code>")

    async def cfriend(self, token):
        try:
            headers = {
                'Authorization': token,
                'Accept': 'application/json',
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                'Priority': 'u=1, i'
            }

            response = await self.scraper.post(
                f"{self.user_url}/api/v1/friends/claim",
                headers=headers
            )

            response_data = await response.json()
            amount = response_data.get("claimBalance")

            if response.status != 200:
                response = await self.scraper.post(
                    f"{self.user_url}/api/v1/friends/claim",
                    headers=headers
                )
                response_data = await response.json()
                amount = response_data.get("claimBalance")

            return amount

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during friends claim:</b> <code>{e}</code>")

    async def playcmd(self, message):
        """<кол-во> - играет на указанное кол-во игр или на все билеты, если кол-во не указано"""
        kok = message.text.split()

        await message.edit("<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Проверяю доступность сервера...</b>")

        server = await self.cserver()
        if not server:
            await message.edit("<emoji document_id=5460972181523537679>😞</emoji> <b>Сервер недоступен, попробуйте позже (возможно он отключен потому-что API опять обновилось)</b>")
            return

        if len(kok) > 1:
            try:
                games = int(kok[1])
            except ValueError:
                await message.edit(
                    "<emoji document_id=5371035398841571673>💩</emoji> <b>Команда введена неправильно! "
                    "Количество игр должно быть числом. Например:</b> <code>.blum 5</code>"
                )
                return
        else:
            games = None

        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Priority': 'u=1, i'
        }

        async with self.scraper.get(f'{self.game_url}/api/v1/user/balance', headers=head) as resp:
            count = (await resp.json())['playPasses']

        if games is None or games > count:
            games = count

        total_point = 0

        if games > 0:
            await message.edit("<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")

            for i in range(games):
                async with self.scraper.post(f'{self.game_url}/api/v2/game/play', headers=head) as post:
                    try:
                        response = await post.json()
                        game_id = response['gameId']
                    except KeyError:
                        await message.edit(
                            "<emoji document_id=5371035398841571673>💩</emoji> <b>Серверам <a href='https://t.me/blum'>"
                            "<b>Blum</b></a> <b>сейчас очень плохо. Попробуйте позже!</b>"
                        )
                        return

                min_points, max_points = map(int, self.config["random_points"].strip('[]').split(','))

                sleep = random.uniform(30, 42)

                await asyncio.sleep(sleep)

                freezes = int((sleep - 30) / 3)
                clover = random.randint(min_points, max_points)

                amount = clover
                points = {"BP": {"amount": amount}}
                assets = {
                    "BOMB": {"clicks": 0},
                    "CLOVER": {"clicks": clover},
                    "FREEZE": {"clicks": freezes}
                }

                payload = await self.cpayload(game_id, points, assets)

                data = {'payload' : payload}

                await self.scraper.post(
                    f'{self.game_url}/api/v2/game/claim',
                    headers=head,
                    data=json.dumps(data)
                )

                await message.edit(f'<emoji document_id=5852496924870971453>🐾</emoji> <b>{i + 1} / {games} игр</b>')

                await asyncio.sleep(random.randint(1, 5))
                total_point += amount

            await message.edit(
                f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Всего зафармлено $BLUM:</b> <code>{total_point}</code>"
            )
        else:
            await message.edit("<emoji document_id=5460972181523537679>😞</emoji> <b>Нет билетов для игры :(</b>")

    async def balancecmd(self, message):
        """показывает баланс из @blum"""
        await message.edit("<emoji document_id=5215484787325676090>🕐</emoji> <b>Получаю информацию...</b>")

        last_run = self.get()
        if last_run:
            next_check_in = last_run + timedelta(hours=12)
            remaining_time = next_check_in - datetime.now()
            hours_remaining = remaining_time.total_seconds() // 3600
            minutes_remaining = (remaining_time.total_seconds() % 3600) // 60
        else:
            hours_remaining, minutes_remaining = "Unknown", "Unknown"
        
        token = await self.login()

        timestamp, start_time, end_time, balance, play_passes = await self.balance(token)

        balance_message = (
            f"<emoji document_id=5375296873982604963>💰</emoji> <b>Баланс:</b>\n\n"
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>$BLUM:</b> <code>{balance}</code>\n"
            f"<emoji document_id=5377599075237502153>🎟</emoji> <b>Билеты:</b> <code>{play_passes}</code>\n"
            f"<emoji document_id=5451732530048802485>⏳</emoji> <b>Следующий чек-ин будет доступен через:</b> <code>{int(hours_remaining)}ч {int(minutes_remaining)}м</code>"
        )

        await message.edit(balance_message)

    async def blumcmd(self, message):
        """вкл/выкл скрипт"""
        self.config["running_on"] = not self.config["running_on"]
        
        if self.config["running_on"]:
            asyncio.create_task(self.blum())

        status = 'включен' if self.config["running_on"] else 'выключен'
        await message.edit(
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Скрипт для <a href='https://t.me/blum'>Blum</a> {status}</b>"
        )

    async def autoplaycmd(self, message):
        """вкл/выкл автоматическую игру на все билеты"""
        self.config["auto_play"] = not self.config["auto_play"]

        status = 'включена' if self.config["auto_play"] else 'выключена'
        await message.edit(
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Автоматическая игра на все билеты <b>{status}</b></b>"
        )

    async def autofarmcmd(self, message):
        """вкл/выкл автоматический фарм токенов"""
        self.config["auto_farm"] = not self.config["auto_farm"]

        status = 'включен' if self.config["auto_farm"] else 'выключен'
        await message.edit(
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Автоматический фарм токенов <b>{status}</b></b>"
        )

    async def autoclaimcmd(self, message):
        """вкл/выкл автоматический клейм ежедневной награды"""
        self.config["auto_claim"] = not self.config["auto_claim"]

        status = 'включен' if self.config["auto_claim"] else 'выключен'
        await message.edit(
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Автоматический клейм ежедневной награды <b>{status}</b></b>"
        )

    async def brefcmd(self, message):
        """вкл/выкл автоматический клейм токенов с рефки"""
        self.config["ref_claim"] = not self.config["ref_claim"]

        status = 'включен' if self.config["ref_claim"] else 'выключен'
        await message.edit(
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Автоматический клейм токенов с рефки <b>{status}</b></b>"
        )

    async def farm(self, token):
        try:
            timestamp, start_time, end_time, balance, play_passes = await self.balance(token)

            if start_time is None and end_time is None:
                await self.start(token)
                await self.log("<emoji document_id=5438496463044752972>⭐️</emoji> <b>Начал фарминг!</b>")

            elif (start_time is not None and end_time is not None and timestamp is not None and
                    timestamp >= end_time):
                timestamp, balance = await self.cfarm(token)
                await self.log(f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Забрал награду с фарминга! Баланс:</b> <code>{balance}</code>")

            elif end_time is not None and timestamp is not None:
                return

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error in farming:</b> <code>{e}</code>")

    async def blum(self) -> None:
        while self.config["running_on"]:
            if self.config["running_on"]:
                try:
                    token = await self.login()
                    timestamp, start_time, end_time, balance, play_passes = await self.balance(token)

                    if self.config["auto_claim"]:
                        last_run = self.get()
                        if not last_run or (datetime.now() - last_run) > timedelta(hours=12):
                            attempt = await self.claim(token)
                            if isinstance(attempt, bool) and attempt:
                                await self.log(f"<emoji document_id=5307973935927663936>✅</emoji> <b>Успешно забрал ежедневную награду (наверное)</b>")
                    
                    if self.config["auto_play"]:
                        if play_passes > 0:
                            await self.play()

                    if self.config["auto_farm"]:
                        await self.farm(token)

                    if self.config["ref_claim"]:
                        claim_amount, is_available = await self.friend(token)
                        
                        if claim_amount != 0 and is_available:
                            amount = await self.cfriend(token)
                            
                            await self.log(
                                f"<emoji document_id=5382026293166489702>👌</emoji> <b>Награда с рефки успешно получена!</b>\n"
                                f"<emoji document_id=5375296873982604963>💰</emoji> <b>Сумма:</b> <code>{amount}</code>"
                            )

                    self.save()

                except Exception as e:
                    await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error in def blum:</b> <code>{e}</code> <i>(please report this - @yummy1gay)</i>")

            sleep_time = random.uniform(3600, 5400)
            await asyncio.sleep(sleep_time)

    def save(self):
        """Save the current time and user agent."""
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                user_agent = data.get("user_agent")
        else:
            user_agent = self.generate_random_user_agent()

        data = {
            "user_agent": user_agent,
            "last_run": datetime.now().isoformat()
        }

        with open(self.file, "w") as f:
            json.dump(data, f)

    def get(self):
        """Get the last run time."""
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                if "last_run" in data:
                    return datetime.fromisoformat(data["last_run"])
                else:
                    pass
        return None

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

        self.save()

        return user_agent