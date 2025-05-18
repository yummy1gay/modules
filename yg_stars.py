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

import re
import struct
import asyncio
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from telethon.tl.tlobject import TLObject, TLRequest
from telethon.tl.types import TypeInputUser

from .. import loader, utils

class YRates:
    currencies = 'USD EUR UAH RUB PLN'.split()

    def __init__(self, stars: int, base: str, cents: int):
        self.stars = stars
        self.base = base.upper()
        self.amount = cents / 100
        self.rates: dict[str, float] = {}
        self._client = httpx.AsyncClient(timeout=10)

    async def _fetch(self) -> None:
        resp = await self._client.get(f'https://open.er-api.com/v6/latest/{self.base}')
        resp.raise_for_status()
        all_rates = resp.json().get('rates', {})
        self.rates = {c: all_rates.get(c, 1) for c in self.currencies}

    async def _prem(self) -> float:
        return self.amount / self.stars

    async def _frag(self) -> float:
        res = await self._client.get('https://fragment.com/')
        res.raise_for_status()
        cookies = res.cookies
        m = re.search(r'ajInit\({"version":\d+,"apiUrl":"([^"}]+)"', res.text)
        y = re.search(r'"tonRate":\s*([0-9.]+)', res.text)
        ton = float(y.group(1))
        api = m.group(1).replace('\\/', '/')
        post = await self._client.post(f'https://fragment.com{api}',
                                       data={'stars': '0',
                                             'quantity': '100',
                                             'method': 'updateStarsPrices'},
                                       headers={'cookie': f"stel_ssid={cookies.get('stel_ssid')}"})
        post.raise_for_status()
        price_raw = post.json().get('cur_price', '')
        p = float(re.search(r'~.*?(\d+\.\d+)', price_raw).group(1))
        return p / 100, ton

    async def _app(self) -> float:
        res = await self._client.get('https://apps.apple.com/ua/app/telegram-messenger/id686449807')
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        for li in soup.select('li.list-with-numbers__item'):
            title = li.select_one('span.truncate-single-line--block')
            if title and title.text.strip() == '100 Telegram Stars':
                price = li.select_one('span.list-with-numbers__item__price').text
                clean = price.replace('\u00A0', ' ').replace(',', '.')
                amt = float(re.search(r"([\d]+(?:\.\d+)?)", clean).group(1))
                return amt / 100
        raise ValueError('App Store price not found!')

    async def get(self) -> dict[str, dict[str, float]]:
        await self._fetch()
        (prem,
        (frag_usd, ton),
        app_usd) = await asyncio.gather(self._prem(),
                                        self._frag(),
                                        self._app())
        await self._client.aclose()

        to_base = 1 / self.rates.get('USD', 1)
        def conv(x: float) -> dict[str, float]:
            out = {c: round(x * self.rates[c], 6) for c in self.currencies}
            out['TON'] = round(out['USD'] / ton, 6)
            return out

        return {'<emoji document_id=5859721575258921535>🏴</emoji> <b><a href="https://fragment.com/">Fragment</a></b>': conv(frag_usd * to_base),
                '<emoji document_id=5859742513224489071>🌟</emoji> <b>@PremiumBot</b>': conv(prem),
                '<emoji document_id=5859347509377244022>🍏</emoji> <b><a href="https://apps.apple.com/">App Store</a></b>': conv(app_usd * to_base)}

class StarsGiftOption(TLObject): # это куда легче чем угадывать сидит ли чел на форке блядь!
    CONSTRUCTOR_ID = 0x5e0589f1
    SUBCLASS_OF_ID = 0xa9cd4bb7

    def __init__(self, stars: int, currency: str, amount: int, extended: Optional[bool]=None, store_product: Optional[str]=None):
        self.stars = stars
        self.currency = currency
        self.amount = amount
        self.extended = extended
        self.store_product = store_product

    def to_dict(self):
        return {
            '_': 'StarsGiftOption',
            'stars': self.stars,
            'currency': self.currency,
            'amount': self.amount,
            'extended': self.extended,
            'store_product': self.store_product
        }

    def _bytes(self):
        return b''.join((
            b'\xf1\x89\x05^',
            struct.pack('<I', (0 if self.extended is None or self.extended is False else 2) | (0 if self.store_product is None or self.store_product is False else 1)),
            struct.pack('<q', self.stars),
            b'' if self.store_product is None or self.store_product is False else (self.serialize_bytes(self.store_product)),
            self.serialize_bytes(self.currency),
            struct.pack('<q', self.amount),
        ))

    @classmethod
    def from_reader(cls, reader):
        constructor_id = reader.read_int()
        if constructor_id != cls.CONSTRUCTOR_ID:
            raise ValueError(f"Invalid constructor_id: expected {cls.CONSTRUCTOR_ID}, got {constructor_id}")

        flags = reader.read_int()
        _extended = bool(flags & 2)
        _stars = reader.read_long()

        if flags & 1:
            _store_product = reader.tgread_string()
        else:
            _store_product = None

        _currency = reader.tgread_string()
        _amount = reader.read_long()

        return cls(stars=_stars, currency=_currency, amount=_amount, extended=_extended, store_product=_store_product)

class GetStarsGiftOptionsRequest(TLRequest): #обожаю телетон :3
    CONSTRUCTOR_ID = 0xd3c96bc8
    SUBCLASS_OF_ID = 0xe9a3b7d5  # Vector<StarsGiftOption>

    def __init__(self, user_id: Optional['TypeInputUser'] = None):
        self.user_id = user_id

    async def resolve(self, client, utils):
        if self.user_id:
            self.user_id = utils.get_input_user(await client.get_input_entity(self.user_id))

    def _bytes(self):
        return b''.join((
            struct.pack('<I', self.CONSTRUCTOR_ID),
            struct.pack('<I', 1 if self.user_id else 0),
            b'' if self.user_id is None else self.user_id._bytes(),
        ))

    def read_result(self, reader):
        vector_constructor = reader.read_int()
        if vector_constructor != 0x1cb5c415:
            raise ValueError(f"Invalid vector constructor_id: expected 0x1cb5c415, got {vector_constructor:#x}")
        count = reader.read_int()
        return [StarsGiftOption.from_reader(reader) for _ in range(count)]

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

        result = await msg.client(GetStarsGiftOptionsRequest(user_id="me"))
        rates = await YRates(result[0].stars, result[0].currency, result[0].amount).get()

        text = (f"<emoji document_id=5956159800260695086>⭐️</emoji> <b>{self.phrase(amount)}</b>\n\n"
                f"{self.strings('hint')}")

        for source, values in rates.items():
            text += self.format(source, values, amount) + "\n"

        await utils.answer(msg, text)

    def phrase(self, amount):
        last_two = amount % 100
        last = amount % 10

        suffix = ("1" if 11 <= last_two <= 14 else
                  "2" if last == 1 else
                  "3" if 2 <= last <= 4 else "1")

        return f"{self.strings('phrase')} <code>{amount}</code> {self.strings(suffix)}"
    
    def format(self, name, data, amount):
        return (f"{name}:\n"
                f"├─ <emoji document_id=6321193412959668105>🇺🇲</emoji> <b>USD:</b> <code>{data['USD'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323217102765295143>🇪🇺</emoji> <b>EUR:</b> <code>{data['EUR'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323289850921354919>🇺🇦</emoji> <b>UAH:</b> <code>{data['UAH'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323139226418284334>🇷🇺</emoji> <b>RUB:</b> <code>{data['RUB'] * amount:.2f}</code>\n"
                f"├─ <emoji document_id=6323602387101550101>🇵🇱</emoji> <b>PLN:</b> <code>{data['PLN'] * amount:.2f}</code>\n"
                f"└─ <emoji document_id=5859542041330981468>👛</emoji> <b>TON:</b> <code>{data['TON'] * amount:.2f}</code>\n")