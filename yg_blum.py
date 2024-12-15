__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# c - claim/create/check

# thx to github.com/sanjithacks for generating payload

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
import time
import json
import base64
import random
from urllib.parse import unquote
from datetime import datetime, timedelta
import hashlib

import aiohttp
from aiohttp_proxy import ProxyConnector
import asyncio
import cloudscraper
from yumlib import yummy

from telethon import TelegramClient
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

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

        if proxy:
            if await self.check_proxy(proxy):
                if proxy['user'] and proxy['pass']:
                    scraper = cloudscraper.create_scraper()
                    proxies = {
                        'http': f"{proxy['type']}://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}",
                        'https': f"{proxy['type']}://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}",
                        'socks5': f"{proxy['type']}://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"
                    }
                    scraper.proxies.update(proxies)
                else:
                    scraper = cloudscraper.create_scraper()
                    proxies = {
                        'http': f"{proxy['type']}://{proxy['host']}:{proxy['port']}",
                        'https': f"{proxy['type']}://{proxy['host']}:{proxy['port']}",
                        'socks5': f"{proxy['type']}://{proxy['host']}:{proxy['port']}"
                    }
                    scraper.proxies.update(proxies)
            else:
                scraper = cloudscraper.create_scraper()
        else:
            scraper = cloudscraper.create_scraper()

        self.scraper = scraper
        self.game = {
            "version": 1.2,
            "gameId": "",
            "challenge": {
                "nonce": 0,
                "hash": "",
            },
            "earnedPoints": {"BP": {"amount": 100}},
            "assetClicks": {
                "BOMB": {"clicks": 0},
                "CLOVER": {"clicks": 100},
                "FREEZE": {
                    "clicks": 2
                },
            },
            "isNode": False,
        }

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
            response = self.scraper.post(
                f"{self.user_url}/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP",
                json=json_data
            )
            
            response.raise_for_status()
            
            response_json = response.json()
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

            response = self.scraper.post(
                f"{self.game_url}/api/v1/daily-reward?offset=-180",
                headers=headers
            )
            
            response_text = response.text()

            return True if response_text == 'OK' else response_text

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during claim daily reward:</b> <code>{e}</code>")

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    def generate_challenge(self, game_id: str, difficulty: int = 4) -> dict:
        nonce = 0
        target = "0" * difficulty
        start_time = time.time()

        while True:
            data = game_id + str(nonce)

            hash_object = hashlib.sha256(data.encode())
            hash_hex = hash_object.hexdigest()

            if hash_hex.startswith(target):
                break

            nonce += 1

        time_taken = time.time() - start_time
        return {
            "nonce": nonce,
            "hash": hash_hex,
            "iterations": nonce + 1,
            "time_taken": time_taken,
        }
    
    async def encrypt_payload(self, payload: str):
        try:
            load_public_key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUF6NXM0cnRzZkxiRmxoZnRoNFJ1OQpZZFdzaU45eVpJc2RtdUE4U2lOaTIrU1pSZlplQVRIMUh2ZVc5OUQyc3JxbkloOFVpUlR4dEpiWFdGSDFCTEQ2CkUvZ09RdjBMdy9Ld1VHZWhScjc3Zm5PT05QbkJBTnF3dEppOFRvWDZDL2hFeW9JMFlFaU5JUzdiY21JczVVNmkKRm9heTF0UFlmRzFkSEJXVGxxU2NidG5lSUthTTJxL3JtRXlQaHlRcDhTcHlTc0x5WTE1WGxERGM4SE5zNVhMNQpNU2hZTllQRWUrVG9hTTNsMDRMSDR6UmRxTEJLZ0ZJMFpqRWxVWlh0T24vTS81em1WamFwd1Q2Ymk0cldOTnZKCmM3TTdabkQ5RXJGWFFxemRLR0x0cHA4Q1hPdXZnUncxRGdPdFpITWwxRzVzY0p1TFZmYjJYRnBKaFNHUmYyQkkKMFFxbmhJc1VWNW03M1JWWE9Ma214dzZOcWpsbnI0TmNpR3F4MzMzWjFSa2o0U09odHJCbitiVXg3SzFIUVNveApDWVgycmlsRlFsdWdDNXd4NmxVU0lRRlQvU010anQ0S20remszYWFiQjlPQUQvWjgzOWVqVzM5MEpLbzA3MVg3CnVITkNhM2dIMjUvV2Rzc0Yra0NybDR3ZmhlUUhUcDhwck9qTjMrTXNNUTRBdzNBOFBvR1ZYdytMK3E1dmVuK0IKcndqanJyYmQzZ0pGMzdkYURydjRrWEFycGNFdHkxNVV4TTB0YzZZUXV5TzR3UDVwTG9BSmNOTFNtc1VGNzBOMwp4a3dqT05BYlByWURqc0x5c1dpUmRUWCsxaGx4NndqL2xWRVNmVjV2U0RvTytENmZUTjd2ZXRqZE5MSWRFeG9hClRmTzBkNzUrc2NGdGdtellvM2NxK1pNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=="
            public_key_bytes = base64.b64decode(load_public_key)
            public_key = serialization.load_pem_public_key(public_key_bytes)
            payload_bytes = payload.encode("utf-8")

            encrypted_payload = public_key.encrypt(
                payload_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=SHA256()),
                    algorithm=SHA256(),
                    label=None,
                ),
            )
            return base64.b64encode(encrypted_payload).decode("utf-8")

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error encrypting payload:</b> <code>{e}</code>")
            return None

    async def cpayload(self, game, assets):
        challenge = self.generate_challenge(game)

        self.game["gameId"] = game
        self.game["challenge"]["nonce"] = challenge["nonce"]
        self.game["challenge"]["hash"] = challenge["hash"]
        self.game["earnedPoints"]["BP"]["amount"] = assets["CLOVER"]["clicks"]
        self.game["assetClicks"]["CLOVER"]["clicks"] = assets["CLOVER"]["clicks"]
        self.game["assetClicks"]["FREEZE"]["clicks"] = assets["FREEZE"]["clicks"]

        encrypted_payload = await self.encrypt_payload(json.dumps(self.game, separators=(",", ":")))

        return encrypted_payload

    async def play(self):
        """play all games 😈😈"""
        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Priority': 'u=1, i'
        }

        with self.scraper.get(f'{self.game_url}/api/v1/user/balance', headers=head) as resp:
            count = (resp.json())['playPasses']
        
        total_point = 0

        if count > 0:
            if self.config["logs_username"]:
                log = await self.client.send_message(self.config["logs_username"], "<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")
            
            for i in range(count):
                with self.scraper.post(f'{self.game_url}/api/v2/game/play', headers=head) as post:
                    try:
                        response = post.json()
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
                assets = {
                    "BOMB": {"clicks": 0},
                    "CLOVER": {"clicks": clover},
                    "FREEZE": {"clicks": freezes}
                }

                payload = await self.cpayload(game_id, assets)

                data = {'payload': payload}

                self.scraper.post(
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

        with self.scraper.get(f"{self.game_url}/api/v1/user/balance", headers=headers) as response:
            response_data = response.json()

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

            response = self.scraper.post(
                f"{self.game_url}/api/v1/farming/start",
                headers=headers
            )

            if response.status_code != 200:
                response = self.scraper.post(
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
                resp = self.scraper.post(
                    f"{self.game_url}/api/v1/farming/claim",
                    headers=headers
                )
                if resp.status_code not in [200, 201]:
                    return None, None
                else:
                    break

            resp_json = resp.json()

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
                response = self.scraper.get(
                    f"{self.user_url}/api/v1/friends/balance", 
                    headers=headers
                )

                if response.status_code not in [200, 201]:
                    return 0, False
                else:
                    break
            
            response_data = response.json()
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

            response = self.scraper.post(
                f"{self.user_url}/api/v1/friends/claim",
                headers=headers
            )

            response_data = response.json()
            amount = response_data.get("claimBalance")

            if response.status_code != 200:
                response = self.scraper.post(
                    f"{self.user_url}/api/v1/friends/claim",
                    headers=headers
                )
                response_data = response.json()
                amount = response_data.get("claimBalance")

            return amount

        except Exception as e:
            await self.log(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred during friends claim:</b> <code>{e}</code>")

    async def playcmd(self, message):
        """<кол-во> - играет на указанное кол-во игр или на все билеты, если кол-во не указано"""
        kok = message.text.split()

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

        with self.scraper.get(f'{self.game_url}/api/v1/user/balance', headers=head) as resp:
            count = (resp.json())['playPasses']

        if games is None or games > count:
            games = count

        total_point = 0

        if games > 0:
            await message.edit("<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")

            for i in range(games):
                with self.scraper.post(f'{self.game_url}/api/v2/game/play', headers=head) as post:
                    try:
                        response = post.json()
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
                assets = {
                    "BOMB": {"clicks": 0},
                    "CLOVER": {"clicks": clover},
                    "FREEZE": {"clicks": freezes}
                }

                payload = await self.cpayload(game_id, assets)

                data = {'payload' : payload}

                self.scraper.post(
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
            hours_remaining, minutes_remaining = 0, 0
        
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

    async def update_useragentcmd(self, message):
        """обновить User-Agent"""
        try:
            if os.path.exists(self.file):
                os.remove(self.file)

            new_user_agent = self.generate_random_user_agent()

            with open(self.file, 'w') as f:
                json.dump({"user_agent": new_user_agent}, f)

            self.config["user_agent"] = new_user_agent

            await message.edit(f"<emoji document_id=5345863488872916640>✅</emoji> <b>User agent updated successfully!</b>")
        except (IOError, json.JSONDecodeError) as e:
            await message.edit(f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occurred while updating user agent:</b> <code>{e}</code>")

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

        with open(self.file, 'w') as f:
            json.dump({"user_agent": user_agent}, f)

        self.save()

        return user_agent