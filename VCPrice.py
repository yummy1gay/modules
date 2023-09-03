#meta developer: @yummy_gay

from .. import loader
import re
import asyncio

class VCPriceMod(loader.Module):
    """Получение цены VC"""

    strings = {"name": "VCPrice"}

    async def vccmd(self, message):
        """Получить цену VC"""
        try:
            await message.edit("<b>Получение данных...</b> <emoji document_id=4988080790286894217>🫥</emoji>")
            
            async with message.client.conversation("FCKAnalyticsBot") as conv:
                sent_message = await conv.send_message("/price vc")
                await asyncio.sleep(0.5)
                await sent_message.delete()
                response = await conv.get_response()
                
                data = response.text
                
                price_match = re.search(r"⚖️ Price: .*? = (.*?) TON", data)
                change7_match = re.search(r"🔼 (.*?) \(7d\)", data)
                volume_match = re.search(r"🛢 Volume \(24h\): (.*?)\n", data)
                totalvolume_match = re.search(r"🏦 Total volume \(24h\): (.*?)\n", data)
                
                if not (price_match and change7_match and volume_match and totalvolume_match):
                    raise ValueError("Не удалось извлечь данные")
                
                price = price_match.group(1).strip()
                change7 = float(change7_match.group(1).replace('%', ''))
                
                change1 = round(change7 / 7, 2)
                
                volume_data = volume_match.group(1)
                buy_sell_matches = re.findall(r"(buy|sell) - (.*?) TON", volume_data)
                if buy_sell_matches:
                    buy_sell_data = ", ".join([f"<b>{action}</b> -<code>{volume}</code> <emoji document_id=5188672371648634636>👛</emoji>" for action, volume in buy_sell_matches])
                else:
                    buy_sell_data = volume_data.strip()
                
                totalvolume = totalvolume_match.group(1)
                
                formatted_data = (
                    f"<emoji document_id=5449632342580672565>📈</emoji> <b>Цена VC:</b> <code>{price}</code> <b>TON</b>\n"
                    f"<emoji document_id=5870930636742595124>📊</emoji> <b>Изменение цены (1д):</b> <code>≈ {change1}%</code>\n"  # Добавляем новую колонку
                    f"<emoji document_id=5870930636742595124>📊</emoji> <b>Изменение цены (7д):</b> <code>{change7}%</code>\n"
                    f"<emoji document_id=5870921681735781843>📊</emoji> <b>Объем (24ч):</b> {buy_sell_data}\n"
                    f"<emoji document_id=5870921681735781843>📊</emoji> <b>Общий объем (24ч):</b> <code>{totalvolume}</code>"
                )
                
                await response.delete()
            
            await message.edit(formatted_data + "\n\n<emoji document_id=5873159368286932298>🔗</emoji> <b>Источник:</code> <b><a href='https://t.me/FCKAnalyticsBot'>FCKAnalytics</a></b>")
            
        except Exception as e:
            await message.edit(f"<b>Произошла ошибка:</b> <code>{str(e)}</code>")