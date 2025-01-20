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

from .. import loader

@loader.tds
class GreetingModule(loader.Module):
    """Модуль для отправки сообщения о том как можно пополнить твой кошелек (все настраивается в конфиге)"""
    strings = {"name": "yg_wallet",
                      "config_wallet": "Твой TON-адрес",
                      "config_crypto_link": "Ссылка на счет с помощью которого можно пополнить твой @CryptoBot",
                      "config_xrocket_link": "Ссылка на счет с помощью которого можно пополнить твой @tonRocketBot"}

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "wallet",
            "укажи свой TON-адрес в конфиге (команда - .cfg yg_wallet)",
            lambda: self.strings("config_wallet")
            ),
            loader.ConfigValue(
            "crypto_link",
            "https://example.com",
            lambda: self.strings("config_crypto_link")
            ),
            loader.ConfigValue(
            "xrocket_link",
            "https://example.com",
            lambda: self.strings("config_xrocket_link")
            )
        )

    async def wcmd(self, message):
        """показать всю информацию для пополнения кошельков"""
        wallet = self.config["wallet"]
        crypto_link = self.config["crypto_link"]
        xrocket_link = self.config["xrocket_link"]

        TON = f"<emoji document_id=5472055112702629499>👋</emoji> <b>Привет!</b>\n\n<emoji document_id=5471952986970267163>💎</emoji> <i>Мой баланс легко пополнить с помощью TON-адреса ниже</i>\n\n<code>{wallet}</code>\n\n"
        TON += f"<b><emoji document_id=5217705010539812022>☺️</emoji> <a href='{crypto_link}'>Пополнить мой CryptoBot</a></b>\n\n"
        TON += f"<b><emoji document_id=5235575317191474172>🚀</emoji> <a href='{xrocket_link}'>Пополнить мой xRocket</a></b>"

        await message.edit(TON)