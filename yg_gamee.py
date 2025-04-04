__version__ = (1, 5, 0, 0)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.
# thx to github.com/IvbcI for most of the code in the GameeHacker class.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import re
import json
import requests
from hashlib import md5
from random import randint
from uuid import uuid4
from datetime import datetime, timezone, timedelta

from .. import loader, utils

class GameeHacker:
    SALT = "crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen"

    def __init__(self, url, score, play_time, uuid):
        self.url = url
        self.score = score
        self.play_time = play_time
        self.game_url = self._extract_game_url()
        self.game_uuid = uuid
        self.checksum = self._create_checksum(uuid)
        self.uuid = self._create_uuid()
        self.user_creds = self._get_user_credentials()
        self.user_auth_token = self.get_user_auth_token()
        self.user_id = self.get_user_id()
        self.user_personal = self.get_user_personal()
        self.game_data = self._get_game_data()
        self.game_id = self.get_game_id()
        self.release_number = self.get_release_number()
        self.response_data = None

    def _create_checksum(self, uuid):
        raw_data = f"{self.score}:{self.play_time}:{self.game_url}::{str(uuid)}:{__class__.SALT}"
        hash = md5(raw_data.encode()).hexdigest()
        return hash

    def _extract_game_url(self):
        groups = re.search(r"prizes\.gamee\.com\/game-bot\/(.*)", self.url)
        assert groups is not None, "Invalid Url."
        game_url = f"/game-bot/{groups.group(1)}"
        return game_url

    def _create_uuid(self):
        return str(uuid4())

    def _get_user_credentials(self):
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                   "Accept": "*/*",
                   "Accept-Language": "en-US,en;q=0.5",
                   "Accept-Encoding": "gzip, deflate",
                   "Client-Language": "en",
                   "Content-Type": "text/plain;charset=UTF-8",
                   "Origin": "https://prizes.gamee.com",
                   "Priority": "u=1, i",
                   "Referer": "https://prizes.gamee.com/",
                   "Sec-Fetch-Dest": "empty",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Site": "same-site",
                   "X-Bot-Header": "gamee",
                   "X-Install-Uuid": self.uuid}

        data = {"jsonrpc": "2.0",
                "id": "user.authentication.botLogin",
                "method": "user.authentication.botLogin",
                "params": {"botName": "telegram", "botGameUrl": self.game_url, "botUserIdentifier": None}}

        json_data = json.dumps(data)
        response = requests.post("https://api.gamee.com/",
                                 headers=headers, data=json_data).json()

        assert self.validate_token(response), "Invalid Token)"
        user_creds = response["result"]
        return user_creds

    def validate_token(self, response):
        if response.get('result'):
            return True
        return False

    def get_user_auth_token(self):
        return self.user_creds["tokens"]["authenticate"]

    def get_user_id(self):
        return self.user_creds["user"]["id"]

    def get_user_personal(self):
        return self.user_creds["user"]["personal"]

    def _get_game_data(self):
        headers = {"X-Install-Uuid": self.uuid,
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"}

        data = {"jsonrpc": "2.0",
                "id": "game.getWebGameplayDetails",
                "method": "game.getWebGameplayDetails",
                "params": {"gameUrl": self.game_url}}

        json_data = json.dumps(data)
        response = requests.post("https://api.gamee.com/",
                                 headers=headers, data=json_data).json()
        game_data = response["result"]["game"]
        return game_data

    def get_game_id(self):
        return self.game_data["id"]

    def get_release_number(self):
        return self.game_data["release"]["number"]

    def check_ban_status(self):
        data = self.response_data
        status = data.get("error", {}).get("message", None)
        if status:
            return True
        return False

    def send_score(self):
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                   "Accept": "*/*",
                   "Accept-Language": "en-US,en;q=0.5",
                   "Accept-Encoding": "gzip, deflate",
                   "Client-Language": "en",
                   "Content-Type": "text/plain;charset=UTF-8",
                   "Origin": "https://prizes.gamee.com",
                   "Priority": "u=1, i",
                   "Referer": "https://prizes.gamee.com/",
                   "Sec-Fetch-Dest": "empty",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Site": "same-site",
                   "Authorization": f"Bearer {self.user_auth_token}",
                   "X-Bot-Header": "gamee",
                   "X-Install-Uuid": self.uuid}

        data = {"jsonrpc": "2.0",
                "id": "game.saveWebGameplay",
                "method": "game.saveWebGameplay",
                "params": {"gameplayData": {
                    "gameId": self.game_id, "score": self.score,
                    "playTime": self.play_time, "gameUrl": self.game_url,
                    "metadata": {"gameplayId": randint(1, 500)},
                    "isSaveState": False, "gameStateData": None,
                    "gameplayOrigin": "game", "replayData": None,
                    "replayVariant": None, "replayDataChecksum": None,
                    "releaseNumber": self.release_number,
                    "createdTime": datetime.now(timezone(timedelta(hours=2))).replace(microsecond=0).isoformat(),
                    "uuid": self.game_uuid, "checksum": self.checksum}}}
        
        json_data = json.dumps(data)
        response = requests.post("https://api.gamee.com/",
                                 headers=headers, data=json_data).json()
        self.response_data = response
        return response

@loader.tds
class yg_gamee(loader.Module):
    """Module to cheat score in @gamee"""

    strings = {
        "name": "yg_gamee",
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Specify a link or reply to the message with the game!</i>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Failed to click the button.. Make sure this is a message with a game!</i>",
        "reply": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Use:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>in a reply to the message with the game!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Error:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Score boosted!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>New record:</b> <code>{score}</code>",
    }

    strings_ru = {
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Укажи ссылку или сделай реплай на сообщение с игрой!</i>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Не удалось кликнуть по кнопке.. Убедись, что это сообщение с игрой!</i>",
        "reply": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Используй:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>в реплае на сообщение с игрой!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Ошибка:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Рекорд накручен!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Новый рекорд:</b> <code>{score}</code>",
    }

    strings_ua = {
        "args": "<emoji document_id=5447644880824181073>⚠️</emoji> <i>Вкажи посилання або зроби реплай на повідомлення з грою!</i>",
        "button": "<emoji document_id=5436113877181941026>❓</emoji> <i>Не вдалося натиснути на кнопку.. Переконайся, що це повідомлення з грою!</i>",
        "reply": "<emoji document_id=5461117441612462242>🙂</emoji> <i>Використовуй:</i> <code>{prefix}gamee &lt;score&gt; &lt;time in seconds&gt;</code> <i>у відповіді на повідомлення з грою!</i>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Помилка:</b> <code>{error}</code>",
        "success": "<emoji document_id=5325547803936572038>✨</emoji> <b>Рекорд накручено!</b>\n<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Новий рекорд:</b> <code>{score}</code>",
    }

    @loader.command(ru_doc="<reply/link to message with game> <score> <time in seconds> - накрутить рекорд",
                    ua_doc="<reply/link to message with game> <score> <time in seconds> - накрутити рекорд")
    async def gameecmd(self, m):
        """<reply/link to message with game> <score> <time in seconds> - cheat score"""
        await utils.answer(m, "<emoji document_id=5386367538735104399>⌛️</emoji>")
        
        args = utils.get_args_raw(m)
        r = await m.get_reply_message()

        if not args and not r:
            await utils.answer(m, self.strings["args"])
            return

        game_url = None
        score = None
        play_time = None

        if r:
            try:
                btn = await r.click(0)
                game_url = btn.url
            except Exception:
                await utils.answer(m, self.strings["button"])
                return
            try:
                score, play_time = map(int, args.strip().split())
            except Exception:
                await utils.answer(m, self.strings["reply"].format(prefix=self.get_prefix()))
                return
        else:
            try:
                parts = args.strip().split()
                if len(parts) != 3:
                    raise ValueError("invalid number of arguments")
                link, score_str, time_str = parts
                score = int(score_str)
                play_time = int(time_str)

                msg_id = int(link.split("/")[-1])
                if "/c/" in link:
                    peer_id = int("-100" + link.split("/c/")[1].split("/")[0])
                else:
                    peer = link.split("/")[-2]
                    peer_id = (await m.client.get_entity(peer)).id

                msg = await m.client.get_messages(peer_id, ids=msg_id)
                btn = await msg.click(0)
                game_url = btn.url
            except Exception as e:
                await utils.answer(m, self.strings["error"].format(error=str(e)))
                return
        try:
            hacker = GameeHacker(game_url, score, play_time, str(uuid4()))
            result = hacker.send_score()
            banned = hacker.check_ban_status()
            if banned:
                await m.delete()
                await m.client.send_file(m.chat_id, "https://t.me/forhikka/2")
            elif "error" in result:
                await utils.answer(m, self.strings["error"].format(error=result['error'].get('message', '🤷‍♂️')))
            else:
                await utils.answer(m, self.strings["success"].format(score=score))
        except Exception as e:
            await utils.answer(m, self.strings["error"].format(error=str(e)))