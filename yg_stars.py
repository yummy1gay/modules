__version__ = (1, 1, 1, 1)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# ported classes from telethon that are not in Hikka-TL

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

from .. import loader, utils

@loader.tds
class yg_stars(loader.Module):
    """Get current prices for stars in different currencies!"""

    strings = {"name": "yg_stars",
               "hint": ("<i><emoji document_id=5857158158388041525>💡</emoji> The course is calculated at the price of a 100 star package.\n"
                        "<emoji document_id=5246762912428603768>📉</emoji> When you buy more, the price per star will be slightly lower!</i>\n\n"),
               "loading": "<emoji document_id=5402186569006210455>💱</emoji> <b>Fetching information...</b>",
               "phrase": "Rate for",
               "1": "stars",
               "2": "star",
               "3": "stars"}
    
    strings_ru = {"name": "yg_stars",
                  "hint": ("<i><emoji document_id=5857158158388041525>💡</emoji> Курс рассчитан по цене пакета в 100 звёзд.\n"
                           "<emoji document_id=5246762912428603768>📉</emoji> При покупке большего количества цена за звезду будет немного ниже!</i>\n\n"),
                  "loading": "<emoji document_id=5402186569006210455>💱</emoji> <b>Получаю информацию...</b>",
                  "phrase": "Курс за",
                  "1": "звёзд",
                  "2": "звезду",
                  "3": "звезды"}
    
    strings_ua = {"name": "yg_stars",
                  "hint": ("<i><emoji document_id=5857158158388041525>💡</emoji> Курс розрахований за ціною пакета 100 зірок.\n"
                           "<emoji document_id=5246762912428603768>📉</emoji> При покупці більшої кількості ціна за зірку буде трохи нижчою!</i>\n\n"),
                  "loading": "<emoji document_id=5402186569006210455>💱</emoji> <b>Отримую інформацію...</b>",
                  "phrase": "Курс за",
                  "1": "зірок",
                  "2": "зірку",
                  "3": "зірки"}

    async def client_ready(self, *_):
        self.lib = await self.import_lib("https://mods.kok.gay/lib",
                                         suspend_on_error=True)

    @loader.command(ru_doc="<amount> - получить курс звезд", ua_doc="<amount> - отримати курс зірок")
    async def starscmd(self, msg):
        """<amount> - get the rate of stars"""
        args = utils.get_args_raw(msg)
        try:
            amount = int(args) if args else 1
        except ValueError:
            await utils.answer(msg, "<b>Enter the number of stars!</b>")
            return
        
        await utils.answer(msg, self.strings("loading"))

        result = await msg.client(self.lib.GetStarsGiftOptionsRequest(user_id="me"))
        rates = await self.lib.YRates(result[0].stars, result[0].currency, result[0].amount).get()

        text = (f"<emoji document_id=5956159800260695086>⭐️</emoji> <b>{self.phrase(amount)}</b>\n\n"
                f"{self.strings('hint')}")

        for source, values in rates.items():
            text += self.format(source, values, amount) + "\n"

        await utils.answer(msg, text, parse_mode=self.lib.YummyHtml)

    def phrase(self, amount):
        last_two = amount % 100
        last = amount % 10

        suffix = ("1" if 11 <= last_two <= 14 else
                  "2" if last == 1 else
                  "3" if 2 <= last <= 4 else "1")

        return f"{self.strings('phrase')} <code>{amount}</code> {self.strings(suffix)}"
    
    def format(self, name, data, amount):
        return (f"{name}:\n"
                f"<blockquote>├─ <emoji document_id=6321193412959668105>🇺🇲</emoji> <b>USD:</b> <code>{data['USD'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323217102765295143>🇪🇺</emoji> <b>EUR:</b> <code>{data['EUR'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323289850921354919>🇺🇦</emoji> <b>UAH:</b> <code>{data['UAH'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323139226418284334>🇷🇺</emoji> <b>RUB:</b> <code>{data['RUB'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323602387101550101>🇵🇱</emoji> <b>PLN:</b> <code>{data['PLN'] * amount:.2f}</code>\n"
                f"└─ <emoji document_id=5859542041330981468>👛</emoji> <b>TON:</b> <code>{data['TON'] * amount:.2f}</code></blockquote>\n")