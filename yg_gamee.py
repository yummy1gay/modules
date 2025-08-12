__version__ = (1, 7, 0, 0)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# Changelog v1.7.0:
# - Добавлена поддержка веб аппа
# - Обновлен класс GameeHacker, теперь работает с новым API
# - кок

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import json
import base64
from hashlib import md5
from random import randint
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from urllib.parse import unquote, urlparse, parse_qs

import requests
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName

from .. import loader, utils

class GameeHacker:
    API_URL = "https://api.gamee.com/"
    SALT = "crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen"

    def __init__(self, client, score: int, play_time: int):
        self.client = client
        self.score = score
        self.play_time = play_time
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Client-Language": "en",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://prizes.gamee.com",
            "Referer": "https://prizes.gamee.com/",
            "X-Bot-Header": "gamee",
            "X-Install-Uuid": str(uuid4()),
        })

    async def _get_init_data(self, chat, start_param: str):
        bot = await self.client.get_input_entity("gamee")
        app = InputBotAppShortName(bot_id=bot, short_name="game")

        web_view = await self.client(RequestAppWebViewRequest(
            peer=chat,
            app=app,
            platform='android',
            start_param=start_param,
        ))
        
        auth_url = web_view.url
        return unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

    def _login(self, init_data: str):
        payload = [{"jsonrpc": "2.0",
                    "id": "user.authentication.loginUsingTelegram",
                    "method": "user.authentication.loginUsingTelegram",
                    "params": {"initData": init_data}}]
        
        res = self.session.post(self.API_URL, data=json.dumps(payload)).json()
        
        for item in res:
            if item.get("id") == "user.authentication.loginUsingTelegram":
                if "error" in item:
                    raise RuntimeError(f"Login error: {item['error'].get('message', 'Unknown error')}")
                
                token = item["result"]["tokens"]["authenticate"]
                self.session.headers["Authorization"] = f"Bearer {token}"
                return
        
        raise RuntimeError("Authentication token not found in login response.")

    def _get_game_details(self, game_slug: str):
        payload = [{"jsonrpc": "2.0",
                    "id": "game.get",
                    "method": "game.get",
                    "params": {"slug": game_slug}}]

        res = self.session.post(self.API_URL, data=json.dumps(payload)).json()
        
        for item in res:
            if item.get("id") == "game.get":
                if "error" in item:
                    raise RuntimeError(f"Get game details error: {item['error'].get('message', 'Unknown error')}")
                
                game_data = item["result"]["game"]
                return game_data["id"], game_data["release"]["number"]

        raise RuntimeError("Game details not found in response.")

    def _create_checksum(self, game_id: int, game_uuid: str) -> str:
        raw_data = f"{self.score}:{self.play_time}:{game_id}::{game_uuid}:{__class__.SALT}"
        return md5(raw_data.encode()).hexdigest()

    def _send_score(
        self,
        game_id: int,
        release_number: int,
        chat_instance: str,
        chat_type: str,
    ):
        game_uuid = str(uuid4())
        checksum = self._create_checksum(game_id, game_uuid)

        payload = {
            "jsonrpc": "2.0",
            "id": "game.saveTelegramGameplay",
            "method": "game.saveTelegramGameplay",
            "params": {
                "gameplayData": {
                    "gameId": game_id,
                    "score": self.score,
                    "playTime": self.play_time,
                    "releaseNumber": release_number,
                    "createdTime": datetime.now(timezone(timedelta(hours=2))).replace(microsecond=0).isoformat(),
                    "metadata": {"gameplayId": randint(1, 500)},
                    "isSaveState": False,
                    "gameStateData": None,
                    "gameplayOrigin": "game",
                    "replayData": None,
                    "replayVariant": None,
                    "replayDataChecksum": None,
                    "checksum": checksum,
                    "uuid": game_uuid,
                },
                "chatInstance": chat_instance,
                "chatType": chat_type,
            }
        }
        
        response = self.session.post(self.API_URL, data=json.dumps(payload)).json()
        return response

    async def kok(self, chat, msg):
        try:
            btn = msg.reply_markup.rows[0].buttons[0]
            parsed_url = urlparse(btn.url)
            start_param = parse_qs(parsed_url.query).get('startapp', [None])[0]
            if not start_param:
                raise ValueError("startapp param not found in button URL")
        except Exception:
            raise ValueError("Failed to get game button from the message. Make sure it's a message with a game.")

        game_slug = json.loads(base64.b64decode(start_param))['game']['slug']
        
        init_data = await self._get_init_data(chat, start_param)
        self._login(init_data)
        
        chat_params = {q.split("=")[0]: q.split("=")[1] for q in init_data.split("&")}
        chat_instance = chat_params.get("chat_instance")
        chat_type = chat_params.get("chat_type")
        
        if not chat_instance or not chat_type:
            raise ValueError("Could not parse chat_instance or chat_type from init_data")
            
        game_id, release_number = self._get_game_details(game_slug)
        
        return self._send_score(game_id, release_number, chat_instance, chat_type)

@loader.tds
class yg_gamee(loader.Module):
    """Module to cheat score in @gamee"""

    strings = {
        "name": "yg_gamee",
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Specify a link or reply to the message with the game!</i>",
        "processing": "<emoji document_id=5386367538735104399>⌛</emoji>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Failed to click the button.. Make sure this is a message with a game!</i>",
        "usage": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Use:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>in a reply to the message with the game!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Error:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Score boosted!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>New record:</b> <code>{score}</code>",
    }

    strings_ru = {
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Укажи ссылку или сделай реплай на сообщение с игрой!</i>",
        "processing": "<emoji document_id=5386367538735104399>⌛</emoji>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Не удалось кликнуть по кнопке.. Убедись, что это сообщение с игрой!</i>",
        "usage": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Используй:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>в реплае на сообщение с игрой!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Ошибка:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Рекорд накручен!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Новый рекорд:</b> <code>{score}</code>",
    }

    strings_ua = {
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Вкажи посилання або зроби реплай на повідомлення з грою!</i>",
        "processing": "<emoji document_id=5386367538735104399>⌛</emoji>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Не вдалося натиснути на кнопку.. Переконайся, що це повідомлення з грою!</i>",
        "usage": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Використовуй:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>у відповіді на повідомлення з грою!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Помилка:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Рекорд накручено!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Новий рекорд:</b> <code>{score}</code>",
    }

    @loader.command(
        ru_doc="<reply/link to message with game> <score> <time in seconds> - накрутить рекорд",
        ua_doc="<reply/link to message with game> <score> <time in seconds> - накрутити рекорд"
    )
    async def gameecmd(self, m):
        """<reply/link to message with game> <score> <time in seconds> - cheat score"""
        args = utils.get_args_raw(m).strip()
        if not args:
            return await utils.answer(m, self.strings["usage"].format(prefix=self.get_prefix()))
        
        await utils.answer(m, self.strings["processing"])

        r = await m.get_reply_message()

        try:
            if r:
                score, play_time = map(int, args.split())
            else:
                parts = args.split()
                if len(parts) != 3:
                    raise ValueError("invalid number of arguments")

                link, score_str, time_str = parts
                score, play_time = int(score_str), int(time_str)
                link_parts = link.strip("/").split("/")
                msg_id = int(link_parts[-1])

                if "/c/" in link:
                    peer = int("-100" + link_parts[link_parts.index("c") + 1])
                else:
                    peer = link_parts[-2]

                r = await m.client.get_messages(peer, ids=msg_id)

        except Exception:
            return await utils.answer(m, self.strings["usage"].format(prefix=self.get_prefix()))

        try:
            hacker = GameeHacker(self._client, score, play_time)
            result = await hacker.kok(m.chat, r)

            if isinstance(result, dict):
                if "error" in result:
                    error_msg = str(result["error"].get("message", "Unknown error"))
                    if "banned" in error_msg.lower():
                        await m.delete()
                        await m.client.send_file(m.chat_id, "https://t.me/forhikka/2")
                    return await utils.answer(m, self.strings["error"].format(error=error_msg))

                if "result" in result:
                    return await utils.answer(m, self.strings["success"].format(score=score))

            await utils.answer(m, self.strings["error"].format(error=f"Unexpected response: {result}"))

        except Exception as e:
            await utils.answer(m, self.strings["error"].format(error=str(e)))
