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

import os
import requests
import matplotlib.pyplot as plt
from yumlib import yummy

from .. import loader

class TonGraphMod(loader.Module):
    """Модуль для графика курса TON"""

    strings = {"name": "yg_ton"}

    async def client_ready(self, client, db):
        await yummy(client)

    async def toncmd(self, message):
        """Отправить график курса TON/USD"""
        try:
            await message.edit("<b>Получение данных... <emoji document_id=4988080790286894217>🫥</emoji></b>")
            ton_price = self.get_ton_price()
            ton_data = self.get_ton_data(ton_price)
            ton_price_change_str = self.get_ton_price_change()

            if not ton_data:
                await message.edit("<b>Не удалось получить данные о курсе TON.</b>")
            
            graph_image = self.generate_graph(ton_data)
            
            caption = self.generate_caption(ton_price, ton_price_change_str)
            
            await message.client.send_file(message.to_id, graph_image, caption=caption)
            
            await message.delete()
            
            if os.path.exists(graph_image):
                os.remove(graph_image)
        except Exception as e:
            await message.edit(f"<b>Произошла ошибка: {str(e)}</b>")
    
    def get_ton_price(self):
        try:
            response = requests.get("https://min-api.cryptocompare.com/data/price", params={
                "fsym": "TON",
                "tsyms": "USD"
            })
            data = response.json()
            
            ton_price = data.get("USD", 0)
            return ton_price
        except Exception as e:
            return 0
    
    def get_ton_data(self, ton_price):
        try:
            response = requests.get("https://min-api.cryptocompare.com/data/v2/histoday", params={
                "fsym": "TON",
                "tsym": "USD",
                "limit": 40,
                "aggregate": 1
            })
            data = response.json()
            
            ton_prices = [entry['close'] for entry in data['Data']['Data']]
            ton_prices.append(ton_price)
            return {"prices": ton_prices}
        except Exception as e:
            return None
    
    def generate_graph(self, ton_data):
        try:
            prices = ton_data.get("prices", [])
            time_intervals = list(range(1, len(prices) + 1))
            
            plt.figure(figsize=(12, 6))
            plt.plot(time_intervals, prices, marker='o', color='white', alpha=0.7, lw=3, mec='white', mew=2, ms=6)
            
            plt.title("TON/USD Price Chart (Last 24 hours)", color='white')
            plt.grid(True, alpha=0.3)
            
            plt.xticks(time_intervals[::len(prices)//6], rotation=45)
            plt.tight_layout()
            
            plt.gca().set_facecolor('black')
            plt.gca().spines['top'].set_color('none')
            plt.gca().spines['right'].set_color('none')
            plt.gca().xaxis.set_ticks_position('bottom')
            plt.gca().yaxis.set_ticks_position('left')
            plt.gca().spines['left'].set_position(('outward', 10))
            plt.gca().spines['bottom'].set_position(('outward', 10))
            
            
            graph_image_path = "ton_graph.png"
            plt.savefig(graph_image_path, facecolor='black')
            plt.close()
            
            return graph_image_path
        except Exception as e:
            return None
    
    def generate_caption(self, ton_price, ton_price_change_str):
        ton_usd_price = self.get_ton_usd_sell()
        ton_prices = self.get_ton_prices()
        caption = f"<b><emoji document_id=5215276644620586569>☺️</emoji> Текущий курс TON:</b>\n\n"
        caption += f"<b><emoji document_id=6323374027985389586>🇺🇸</emoji> USD:</b> <code>{ton_usd_price}</code>\n"
        
        for currency, price in ton_prices.items():
            caption += f"<b>{currency}:</b> <code>{price}</code>\n"
        
        caption += f"\n<emoji document_id=5451882707875276247>🕯</emoji> <b>Изменение цены (24ч):</b> <code>{ton_price_change_str}</code>\n\n"
        caption += "<emoji document_id=5873159368286932298>🔗</emoji> <b>Источники:</b> <b><a href='https://www.kucoin.com/ru/price/TON'>KuCoin</a></b><b>,</b> <b><a href='https://coingate.com/'>CoinGate</a></b>"
        
        return caption

    def get_ton_prices(self):
        try:
            ton_usd_sell = self.get_ton_usd_sell()

            if ton_usd_sell is None:
                return None

            base_url = "https://api.coingate.com/v2/rates/merchant/USD/"
            currencies = {
                "<emoji document_id=6323289850921354919>🇺🇦</emoji> UAH": "UAH",
                "<emoji document_id=6323602387101550101>🇵🇱</emoji> PLN": "PLN",
                "<emoji document_id=6323139226418284334>🇷🇺</emoji> RUB": "RUB"
            }
            
            ton_prices = {}
            for currency, currency_code in currencies.items():
                response = requests.get(base_url + currency_code)
                rate = float(response.text.strip())
                
                if rate:
                    ton_price_in_currency = ton_usd_sell * rate
                    ton_price_in_currency_rounded = round(ton_price_in_currency, 2)
                    ton_prices[currency] = f"{ton_price_in_currency_rounded:.2f}"
                else:
                    ton_prices[currency] = "N/A"
            
            return ton_prices
        except Exception as e:
            return None

    def get_ton_usd_sell(self):
        try:
            response = requests.get("https://api.kucoin.com/api/v1/market/stats?symbol=TON-USDT")
            data = response.json()
            
            ton_usd_sell = float(data["data"]["sell"])
            return ton_usd_sell
        except Exception as e:
            return None

    def get_ton_price_change(self):
        try:
            ton_data = requests.get(
                "https://api.kucoin.com/api/v1/market/stats?symbol=TON-USDT"
            ).json()
            
            ton_price_change = float(ton_data["data"]["changeRate"]) * 100
            ton_price_change_str = "+" if ton_price_change > 0 else ""
            ton_price_change_str += "{:.2f}%".format(ton_price_change)
            
            return ton_price_change_str
        except Exception as e:
            return "N/A"