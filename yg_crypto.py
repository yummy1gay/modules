# meta developer: @yummy_gay

import random as r
import requests
import time
from telethon.tl.types import Message
from .. import loader, utils


class MeowCryptoManagerMod(loader.Module):
    """Крутой модуль для того чтобы чекать курс в реальном времени🕶"""

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
            self.db.set("defaultvalute", "update", True)

    async def монетаcmd(self, message: Message):
        """<название> выбрать крипту по умолчанию"""

        args = utils.get_args_raw(message)
        self.db.set("defaultvalute", "val", args)
        await utils.answer(message, self.strings("okey").format(args))

    async def вклвыклcmd(self, message: Message):
        """Включить/выключить автообновление курса (каждые 11 сек)"""
        current_state = self.db.get("defaultvalute", "update", True)
        new_state = not current_state
        self.db.set("defaultvalute", "update", new_state)

        if new_state:
            await utils.answer(message, "<b>Автообновление курса: вкл</b>")
        else:
            await utils.answer(message, "<b>Автообновление курса: выкл</b>")

    async def курсcmd(self, message: Message):
        "<кол-во> <название монеты> смотерть курс"
        args = utils.get_args_raw(message)
        tray = self.db.get("defaultvalute", "val", args)
        if tray == "":
            tray = "btc"
        if not args:
            args = "1" + " " + str(tray)
        args_list = args.split(" ")
        try:
            if len(args_list) == 1 and isinstance(float(args_list[0]), float) == True:
                args_list.append(str(tray))
        except Exception:
            args_list = ["1", args_list[0]]
        coin = args_list[1].upper()

        while True:
            api = requests.get(
                f"https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms=USD,RUB,UAH,PLN,KZT,BTC,ETH,TONCOIN"
            ).json()
            smiles = r.choice(
                [
                    "<emoji document_id=5348140027698227662>🙀</emoji>"
                ]
            )

            try:
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
                        " document_id=5465465383035083768>💰</emoji> <b>{}"
                        " BTC</b>\n<emoji document_id=5465198785825087352>💰</emoji>"
                        " <b>{} ETH</b>\n<emoji"
                        " document_id=5197515039296200279>💰</emoji> <b>{} TON</b>"
                    ).format(
                        smiles,
                        count,
                        coin,
                        round(api["USD"] * count, 2),
                        round(api["UAH"] * count, 2),
                        round(api["PLN"] * count, 2),
                        round(api["RUB"] * count, 2),
                        round(api["KZT"] * count, 2),
                        round(api["BTC"] * count, 4),
                        round(api["ETH"] * count, 4),
                        round(api["TONCOIN"] * count, 4),
                    )

                    current_time = time.strftime("%H:%M:%S")
                    form += f"\n\n<b><i>Последнее Обновление:</i></b> <b>{current_time}</b>"

                    await utils.answer(message, form)
                except KeyError:
                    await utils.answer(message, self.strings["keyerror"])
            except ValueError:
                await utils.answer(message, self.strings["inc_args"])

            update_state = self.db.get("defaultvalute", "update", True)

            if not update_state:
                break

            time.sleep(11)