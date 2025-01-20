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

from telethon import TelegramClient

from .. import loader, utils

class yg_balance(loader.Module):
    """Модуль для просмотра балансов в @CryptoBot и @wallet"""

    strings = {
        "name": "yg_balance",
        "cryptobot": (
            "<emoji document_id=5217705010539812022>☺️</emoji> <b>Мой баланс в @CryptoBot:</b>\n\n{}"
        ),
        "wallet": (
            "<emoji document_id=5438394062434485433>💎</emoji> <b>Мой баланс в @wallet:</b>\n\n{}"
        ),
    }

    emoji_map = {
        "Bitcoin": "<emoji document_id=5215590800003451651>🪙</emoji>",
        "Toncoin": "<emoji document_id=5215276644620586569>🪙</emoji>",
        "USDT": "<emoji document_id=5215699136258524363>🪙</emoji>",
        "NOT": "<emoji document_id=5215699170618263097>🪙</emoji>",
        "DOGS": "<emoji document_id=5341347975006280049>🪙</emoji>"
    }

    @staticmethod
    async def check(bot, message):
        async with message.client.conversation(bot) as conv:
            request = await conv.send_message("/wallet")
            answer = await conv.get_response()

            await request.delete()
            await answer.delete()

        return answer.text

    @staticmethod
    def cryptobot(text):
        lines = [line.strip() for line in text.split('\n') if line.strip() and not 'Кошелёк' in line]
        balance_lines = [line for line in lines if not line.startswith('≈')]
        total_line = next((line for line in lines if line.startswith('≈')), '')
        return '\n'.join(balance_lines) + (f"\n\n{total_line}" if total_line else '')

    @staticmethod
    def wallet(text):
        lines = [line.strip() for line in text.split('\n') if line.strip() and not 'Мой кошелёк' in line]
        formatted_lines = []
        for line in lines:
            for crypto, emoji in yg_balance.emoji_map.items():
                if crypto in line:
                    formatted_lines.append(f"{emoji} {line}")
                    break
            else:
                formatted_lines.append(line)
        return '\n'.join(formatted_lines)

    @loader.command()
    async def bc(self, message):
        """проверить баланс в @CryptoBot"""
        text = await self.check(1559501630, message)
        balance = self.cryptobot(text)
        await utils.answer(message, self.strings["cryptobot"].format(balance))

    @loader.command()
    async def bw(self, message):
        """проверить баланс в @wallet"""
        text = await self.check(1985737506, message)
        balance = self.wallet(text)
        await utils.answer(message, self.strings["wallet"].format(balance))