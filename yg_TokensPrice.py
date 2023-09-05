#meta developer: @yummy_gay
#channel tg: @yg_modules
#st1tl cl0wn

#██╗░░░██╗░██████╗░░░░░███╗░░░███╗░█████╗░██████╗░██╗░░░██╗██╗░░░░░███████╗░██████╗
#╚██╗░██╔╝██╔════╝░░░░░████╗░████║██╔══██╗██╔══██╗██║░░░██║██║░░░░░██╔════╝██╔════╝
#░╚████╔╝░██║░░██╗░░░░░██╔████╔██║██║░░██║██║░░██║██║░░░██║██║░░░░░█████╗░░╚█████╗░
#░░╚██╔╝░░██║░░╚██╗░░░░██║╚██╔╝██║██║░░██║██║░░██║██║░░░██║██║░░░░░██╔══╝░░░╚═══██╗
#░░░██║░░░╚██████╔╝░░░░██║░╚═╝░██║╚█████╔╝██████╔╝╚██████╔╝███████╗███████╗██████╔╝

import re
from .. import loader
import httpx
import asyncio
from telethon.tl.functions.channels import JoinChannelRequest

@loader.sudo
class FCKPricesMod(loader.Module):
    """Модуль для того чтобы узнавать информацию об цене токенов которые числятся в базе данных FCK Analytics"""

    strings = {"name": "yg_TokensPrice"}

    async def pricecmd(self, message):
        """<name> получить информацию о токене"""
        try:
            args = message.raw_text.split(" ", 1)
            if len(args) < 2:
                await message.edit("<emoji document_id=4987934263182623512>😩</emoji> <b>А где имя токена? Использование:</b> <code>.price *name*</code>")
                return
            
            name = args[1].strip().upper()
            await message.edit(f"<b>Получение данных о токене {name}...</b> <emoji document_id=4988080790286894217>🫥</emoji>")

            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.kucoin.com/api/v1/prices?base=USD&currencies=TON")
                api_price = float(response.json().get("data", {}).get("TON"))

            async with message.client.conversation("FCKAnalyticsBot") as conv:
                sent_message = await conv.send_message(f"/price {name}")
                await asyncio.sleep(1)
                await sent_message.delete()

                response = await conv.get_response()

                if "not found!" in response.text:
                    await message.edit(f"<emoji document_id=5870657884844462243>❌</emoji> <b>Токен {name} не найден в базе FCK Analytics!</b>")
                    await response.delete()
                    return
                
                data = response.text

                price_match = re.search(r"⚖️ Price: .*? = (.*?) TON", data)
                change7_match = re.search(r"(🔼|🔽) (.*?) \(7d\)", data)
                volume_match = re.search(r"🛢 Volume \(24h\): (.*?)\n", data)
                totalvolume_match = re.search(r"🏦 Total volume \(24h\): (.*?)\n", data)

                if not (price_match and change7_match and volume_match and totalvolume_match):
                    raise ValueError("Не удалось извлечь данные")

                price = price_match.group(1).strip()
                change7_emoji = change7_match.group(1)
                change7_emoji = "<emoji document_id=5456199025453709307>📊</emoji>" if change7_emoji == "🔽" else "<emoji document_id=5870930636742595124>📊</emoji>"
                change7 = float(change7_match.group(2).replace('%', ''))
                change1 = round(change7 / 7, 2)

                volume_data = volume_match.group(1)
                buy_sell_matches = re.findall(r"(buy|sell) - (.*?) TON", volume_data)
                if buy_sell_matches:
                    buy_sell_data = ", ".join([f"<b>{action}</b> -<code>{volume}</code> <emoji document_id=5188672371648634636>👛</emoji>" for action, volume in buy_sell_matches])
                else:
                    buy_sell_data = volume_data.strip()

                totalvolume = totalvolume_match.group(1)

                calculated_price = round(float(price) * api_price, 4)

                change1_symbol = "+" if change1 >= 0 else ""
                change7_symbol = "+" if change7 >= 0 else ""

                formatted_data = (
                    f"<emoji document_id=5873146865637133757>🎤</emoji> <b>Цена {name}:</b> <code>{price}</code> <b>TON (≈{calculated_price:.4f}$)</b>\n"
                    f"{change7_emoji} <b>Изменение цены (24ч):</b> <code>{change1_symbol}{change1}%</code>\n"
                    f"{change7_emoji} <b>Изменение цены (7д):</b> <code>{change7_symbol}{change7}%</code>\n"
                    f"<emoji document_id=5870921681735781843>📊</emoji> <b>Объем (24ч):</b> {buy_sell_data}\n"
                    f"<emoji document_id=5870921681735781843>📊</emoji> <b>Общий объем (24ч):</b> <code>{totalvolume}</code>\n\n"
                    f"<emoji document_id=5873159368286932298>🔗</emoji> <b>Источники:</code> <b><a href='https://t.me/FCKAnalyticsBot'>FCK Analytics</a></b><b>,</b> <b><a href='https://www.kucoin.com/ru/price/TON'>KuCoin</a></b>"
                )

                await response.delete()

            await message.edit(formatted_data)

        except Exception as e:
            await message.edit(f"<b>Произошла ошибка:</b> <code>{str(e)}</code>")
