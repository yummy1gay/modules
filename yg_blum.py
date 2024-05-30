__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# + посхалко

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3


# ⣿⣿⣿⡷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⢿⣿⣿⣿⣿
# ⣹⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣮⣽⣿⣿⣿
# ⣿⣿⣿⣝⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣄⠛⣿⣿⣿⣿⣿⣿⣟⣝⣿⣿⣿
# ⣿⣿⢷⣾⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣯⢍⢻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿⠛⠻⠛⢿⡇⢹⣿⣿⣿⣿⣿⣳⣽⣿⣿⣿
# ⡻⠟⠈⢛⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⣷⣼⣿⣿⣿⣦⣤⡀⠄⠀⠀⠰⠀⢀⣤⣴⣿⣿⣶⣧⣤⣄⣤⣩⢸⣿⣿⣿⣿⡯⢍⣿⣿⣿⣿
# ⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡇⢼⣿⣿⣿⠋⣽⡟⣿⣿⣿⣿⣿⣧⠀⠀⢸⣾⣿⣿⣿⣿⣿⢿⢿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣷⡚⢿⣿⣿⣿
# ⠀⠀⠀⠀⠈⢉⣿⣿⣿⣿⠃⠜⠻⢿⣿⣾⣧⣋⣿⣿⣿⣿⠻⠒⠂⠀⢺⣿⣿⣿⣧⣧⣛⢰⢼⣾⣿⣿⠃⠘⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⠀⠀⠀⠉⠹⠿⠿⢿⣿⣿⠿⠻⠳⠁⠀⠀⠘⡿⣿⣿⣿⠿⣿⢿⢭⡄⠠⠇⠍⣀⣿⣿⣿⡉⣩⠞⢸⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⠀⣯⣿⣿⠈⣡⢀⠀⠀⠀⠀⠀⠀⠀⢰⣶⠦⠀⠀⠀⠀⣈⣎⠀⠈⠀⠈⠀⠀⠀⣀⣠⢴⠽⣿⣿⣟⢏⠂⠀⢼⣿⣿⣿
# ⠀⠁⠀⣠⠂⠀⠀⢡⢼⣏⣾⣯⠈⠀⠀⠀⠀⠀⣠⡖⡿⠉⠃⠀⠀⠀⠈⡜⠉⢻⣶⣄⠀⠀⠀⠀⣶⡟⣨⣿⣿⡿⣟⣿⢿⣿⣿⡟⣿⡿
# ⠀⠀⠒⠋⠀⠀⠀⢀⠨⢛⡿⢻⡆⠀⠀⣠⣴⠟⠁⠘⣼⣤⡀⠀⠀⠀⠀⣢⣤⣿⠉⠙⢷⣆⡀⠰⣿⣾⣿⣿⡏⢻⡿⠉⣭⢠⠀⢘⣿⢿
# ⠀⣤⠠⣀⢀⠀⠀⠀⠀⣵⠼⣿⣷⣶⣿⣿⣿⠀⠀⠀⠈⢻⣿⣆⠀⠀⣀⣿⠟⠓⠀⠀⠀⣽⣿⣿⣿⣿⣿⢿⢀⡿⠀⢀⣰⣤⣠⣶⣾⣿
# ⣿⠟⢻⣿⣿⠀⠀⢈⠀⠽⠀⠘⠿⣿⣿⣿⣿⣀⣀⠀⠀⠀⠀⠉⢿⠛⠛⠁⠀⠀⢀⣠⣼⣿⣿⣿⣿⣿⣏⣿⠋⠀⡠⣿⣿⣿⣿⣿⣿⣿
# ⠉⠀⣴⢴⠟⣤⠆⠀⣔⡀⣄⠀⠀⠈⠘⡿⣿⣿⣿⣿⣿⣶⣶⣤⣄⣤⣤⣴⣾⣿⣿⣿⣿⣿⡟⢻⠿⣿⣹⠃⠤⣴⢷⡙⣿⣿⣿⢿⣿⣿
# ⠀⠀⢸⣄⣠⣄⡀⠀⠿⠛⢁⠠⠠⠀⢀⠁⠈⣿⣿⣿⡍⠚⠘⠋⠙⡙⠉⠏⠃⢨⣿⣿⣿⣿⡂⠈⣸⣷⢋⢳⣞⠱⠐⣿⣾⣿⣟⣬⣿⣿
# ⠀⠀⠀⠀⠈⠿⠽⠀⢀⠀⠀⠀⣄⡄⢸⣆⠀⢹⣿⣿⣿⠴⠀⠀⠀⠇⠀⠄⠲⢻⣿⣿⣿⣿⡏⠁⣿⡏⣼⡾⢉⣀⣲⣿⣿⣿⣿⣿⣿⣿
# ⠀⢀⢀⣀⠀⠀⠀⠀⠈⢠⣤⡠⢿⣴⡆⢻⣦⠀⢻⣿⣿⣶⣤⣤⣀⣀⡀⣄⣼⣿⣿⣿⣿⣿⠇⣸⡿⣁⠟⢵⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿
# ⠰⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣷⣿⣿⣿⡌⢿⡆⠀⠙⢿⣷⣁⠉⠉⠉⠉⣉⣽⡿⢋⣿⣾⣿⣰⠇⣼⣿⣆⡸⣯⣟⣷⣿⣿⣿⣿⣿⣿⣿
# ⠀⠀⠀⠀⠈⠁⠀⠀⣩⣾⣿⣿⡇⣿⣿⣿⣿⣿⡄⡀⠀⠀⠉⠉⠁⠁⠠⠛⠛⠁⠊⣿⣿⣿⣟⣿⣿⣿⣿⢷⡿⣏⢾⢿⣿⣿⣿⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⡉⢻⡀⠀⠀⣀⣤⣤⡤⠴⠒⠋⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣽⣿⣿⣿⢿⣿
# ⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠂⠤⠤⠤⠤⠄⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⣷⠾⡿⢿⢾⣿
# ⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣱⢝⢺⣿
# ⣰⣂⢦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣆⠀⠀⠀⠘⠀⠀⠀⠀⣈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣦⣤⣠⣴⠀⡤⣠⣶⣦⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

from telethon.tl.functions.messages import RequestWebViewRequest
from urllib.parse import unquote
import requests as req
import json
import time
import random
from fake_useragent import UserAgent
import aiohttp

from .. import loader

@loader.tds
class yg_blum(loader.Module):
    """Играет в игры в @BlumCryptoBot (За 1 игру выдаёт 230 - 240 $BLUM)"""

    strings = {"name": "yg_blum"}

    async def client_ready(self, client, db):
        self.client = client
        headers = {'User-Agent': UserAgent(os='android').random}
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True)

    async def get_tg_web_data(self):
        web_view = await self.client(RequestWebViewRequest(
            peer='BlumCryptoBot',
            bot='BlumCryptoBot',
            platform='android',
            from_bot_menu=False,
            url='https://telegram.blum.codes/'
        ))

        auth_url = web_view.url
        return unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

    async def login(self):
        json_data = {"query": await self.get_tg_web_data()}

        resp = await self.session.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
        resp_json = await resp.json()

        token = resp_json.get("token").get("access")
        return "Bearer" + token

    async def blumcmd(self, message):
        """играет на все ваши билеты, и в конце показывает сколько в итоге вышло"""
        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        }
        resp = req.get('https://game-domain.blum.codes/api/v1/user/balance', headers=head)
        count = json.loads(resp.text)['playPasses']
        total_point = 0
        if count != 0:
            await message.edit("<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")
            for i in range(count):
                post_id = req.post('https://game-domain.blum.codes/api/v1/game/play', headers=head)
                game_id = json.loads(post_id.text)['gameId']
                time.sleep(random.randrange(30, 60, 5))
                points = random.randint(150, 250)
                req.post('https://game-domain.blum.codes/api/v1/game/claim', headers=head, json={
                    "gameId": game_id, "points": points})
                await message.edit(f'<emoji document_id=5852496924870971453>🐾</emoji> <b>{i + 1} / {count} игр</b>')
                time.sleep(random.randint(1, 5))
                total_point += points
            await message.edit(f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Всего зафармленно $BLUM:</b> <code>{total_point}</code>")
        else:
            await message.edit("<emoji document_id=5460972181523537679>😞</emoji> <b>Нету билетов для игры :(</b>")