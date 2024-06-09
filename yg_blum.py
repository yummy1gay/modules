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
import asyncio
import random
from aiocfscrape import CloudflareScraper
import aiohttp

from .. import loader

@loader.tds
class yg_blum(loader.Module):
    """Играет в игры в @BlumCryptoBot (За 1 игру выдаёт 150 - 250 $BLUM)"""

    strings = {"name": "yg_blum"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "random_points",
                "150, 250",
                "Рандомное кол-во поинтов за одну игру, вводить в формате: 0, 0. Макс. кол-во 280",
                validator=loader.validators.Hidden(loader.validators.String()),
            )
        )

    async def client_ready(self, client, db):
        self.client = client
        headers = {'User-Agent': generate_random_user_agent(device_type='android', browser_type='chrome')}
        self.scraper = CloudflareScraper(headers=headers, timeout=aiohttp.ClientTimeout(total=60))

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

        resp = await self.scraper.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
        resp_json = await resp.json()

        token = resp_json.get("token").get("access")
        return "Bearer " + token

    async def blumcmd(self, message):
        """играет на все ваши билеты, и в конце показывает сколько в итоге вышло"""
        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': generate_random_user_agent(device_type='android', browser_type='chrome')
        }
        async with self.scraper.get('https://game-domain.blum.codes/api/v1/user/balance', headers=head) as resp:
            count = (await resp.json())['playPasses']
        total_point = 0
        if count != 0:
            await message.edit("<emoji document_id=5371057462088570593>😋</emoji> <b>Начал играть...</b>")
            for i in range(count):
                async with self.scraper.post('https://game-domain.blum.codes/api/v1/game/play', headers=head) as post_id:
                    try:
                        game_id = (await post_id.json())['gameId']
                    except KeyError:
                        await message.edit("<emoji document_id=5371035398841571673>💩</emoji> Серверам <a href='https://t.me/BlumCryptoBot'><b>Blum</b></a> сейчас очень плохо. Попробуйте позже!")
                        return
                await asyncio.sleep(random.randrange(30, 60, 5))
                min_points, max_points = map(int, self.config["random_points"].strip('[]').split(','))
                points = random.randint(min_points, max_points)
                await self.scraper.post('https://game-domain.blum.codes/api/v1/game/claim', headers=head, json={
                    "gameId": game_id, "points": points})
                await message.edit(f'<emoji document_id=5852496924870971453>🐾</emoji> <b>{i + 1} / {count} игр</b>')
                await asyncio.sleep(random.randint(1, 5))
                total_point += points
            await message.edit(f"<emoji document_id=5350746136544037083>🤑</emoji> <b>Всего зафармленно $BLUM:</b> <code>{total_point}</code>")
        else:
            await message.edit("<emoji document_id=5460972181523537679>😞</emoji> <b>Нету билетов для игры :(</b>")

    async def balancecmd(self, message):
        """показывает баланс из @BlumCryptoBot"""
        token = await self.login()
        head = {
            'Authorization': token,
            'Accept': 'application/json',
            'User-Agent': generate_random_user_agent(device_type='android', browser_type='chrome')
        }
        async with self.scraper.get("https://game-domain.blum.codes/api/v1/user/balance", headers=head) as resp:
            resp_json = await resp.json()
        
        balance = resp_json.get("availableBalance")
        play_passes = resp_json.get("playPasses")

        balance_message = (
            f"<emoji document_id=5375296873982604963>💰</emoji> <b>Баланс:</b>\n\n"
            f"<emoji document_id=5350746136544037083>🤑</emoji> <b>$BLUM:</b> <code>{balance}</code>\n"
            f"<emoji document_id=5377599075237502153>🎟</emoji> <b>Билеты:</b> <code>{play_passes}</code>"
        )

        await message.edit(balance_message)

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