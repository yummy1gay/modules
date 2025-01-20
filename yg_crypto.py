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

import random as r
import requests
from telethon.tl.types import Message

from .. import loader, utils

class yg_crypto(loader.Module):
    """Модуль для того чтобы узнать курс крипты/фиата"""

    strings = {
        "name": "yg_crypto",
        "inc_args": "<b>🐳 Incorrect args</b>",
        "keyerror": (
            "🗿 <b>Maybe the coin is not in the site database or you typed the wrong"
            " name.</b>"
        ),
        "okey": "<b>👯 Successfully. Current default valute: {}</b>",
    }
    strings_ru = {
        "inc_args": "<b><emoji document_id=5348140027698227662>🙀</emoji> Неккоректные аргументы</b>",
        "keyerror": (
            "<b><emoji document_id=5348140027698227662>🙀</emoji> Возможно монеты нету в базе данных сайта, или вы ввели неккоректное"
            " название.</b>"
        ),
        "okey": "<b><emoji document_id=5348140027698227662>🙀</emoji> Успешно. Текущая стандартная валюта: {}</b>",
    }

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

        if "defaultvalute" not in self.db:
            self.db.set("defaultvalute", "val", "btc")

    async def монетаcmd(self, message: Message):
        """<название> выбрать крипту по умолчанию"""

        args = utils.get_args_raw(message)
        self.db.set("defaultvalute", "val", args)
        await utils.answer(message, self.strings["okey"].format(args))

    async def курсcmd(self, message: Message):
        """<кол-во> <название монеты> смотреть курс"""
        args = utils.get_args_raw(message)
        tray = self.db.get("defaultvalute", "val", args)
        if tray == "":
            tray = "btc"
        if not args:
            args = "1" + " " + str(tray)
        args_list = args.split(" ")
        try:
            if len(args_list) == 1 and isinstance(float(args_list[0]), float):
                args_list.append(str(tray))
        except Exception:
            args_list = ["1", args_list[0]]
        coin = args_list[1].upper()

        if coin == "ТОН":
            coin = "TON"
        if coin == "ЮСД":
            coin = "USD"
        if coin == "РУБ":
            coin = "RUB"
        if coin == "ГРН":
            coin = "UAH"
        if coin == "ЗЛ":
            coin = "PLN"

        api = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms=USD,RUB,UAH,PLN,KZT,BTC,ETH,TON"
        ).json()
        smiles = r.choice(
            [
                "<emoji document_id=5348140027698227662>🙀</emoji>",
                "<emoji document_id=5348175255019988816>🙀</emoji>",
                "<emoji document_id=5348179601526892213>🙀</emoji>",
                "<emoji document_id=5348312457750260828>🙀</emoji>"
            ]
        )

        try:
            count = float(args_list[0])
            form = (
                "{} <b><i>{} {} is:</i></b>\n\n<emoji"
                " document_id=6323374027985389586>🇺🇸</emoji>"
                " <b>{}$</b>\n<emoji"
                " document_id=6323289850921354919>🇺🇦</emoji>"
                " <b>{}₴</b>\n<emoji"
                " document_id=6323602387101550101>🇵🇱</emoji>"
                " <b>{}zł.</b>\n<emoji"
                " document_id=6323139226418284334>🇷🇺</emoji>"
                " <b>{}₽</b>\n<emoji"
                " document_id=6323135275048371614>🇰🇿</emoji>"
                " <b>{}₸</b>\n<emoji"
                " document_id=5215590800003451651>🪙</emoji> <b>{}"
                " BTC</b>\n<emoji document_id=5217867240044512715>🪙</emoji>"
                " <b>{} ETH</b>\n<emoji"
                " document_id=5215276644620586569>🪙</emoji> <b>{} TON</b>"
            ).format(
                smiles,
                count,
                coin,
                round(api.get("USD", 0) * count, 2),
                round(api.get("UAH", 0) * count, 2),
                round(api.get("PLN", 0) * count, 2),
                round(api.get("RUB", 0) * count, 2),
                round(api.get("KZT", 0) * count, 2),
                round(api.get("BTC", 0) * count, 4),
                round(api.get("ETH", 0) * count, 4),
                round(api.get("TON", 0) * count, 4),
            )

            await utils.answer(message, form)
        except KeyError:
            await utils.answer(message, self.strings["keyerror"])
        except ValueError:
            await utils.answer(message, self.strings["inc_args"])