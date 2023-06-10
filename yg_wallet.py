# meta developer: @yummy_gay

from .. import loader
from telethon.tl import types

@loader.tds
class GreetingModule(loader.Module):
    """Модуль для отправки сообщения о том как можно пополнить твой кошелек (все настраивается в конфиге)"""
    strings = {"name": "yg_wallet",
                      "config_wallet": "Твой TON-адрес",
                      "config_crypto_link": "Ссылка на счет с помощью которого можно пополнить твой @CryptoBot",
                      "config_tonrocket_link": "Ссылка на счет с помощью которого можно пополнить твой @tonRocketBot"}

    def __init__(self):
        self.config = loader.ModuleConfig(
        loader.ConfigValue(
            "wallet",
            "укажи свой TON-адрес в конфиге",
            lambda: self.strings("config_wallet")
            ),
            loader.ConfigValue(
            "crypto_link",
            "https://example.com",
            lambda: self.strings("config_crypto_link")
            ),
            loader.ConfigValue(
            "tonrocket_link",
            "https://example.com",
            lambda: self.strings("config_tonrocket_link")
            )
        )

    async def wcmd(self, message):
        """показать всю информацию для пополнения кошельков"""
        wallet = self.config["wallet"]
        crypto_link = self.config["crypto_link"]
        tonrocket_link = self.config["tonrocket_link"]

        TON = f"<emoji document_id=5472055112702629499>👋</emoji> <b>Привет!</b>\n\n<emoji document_id=5471952986970267163>💎</emoji> <i>Мой баланс легко пополнить с помощью TON-адреса ниже</i>\n\n<code>{wallet}</code>\n\n"
        TON += f"<b><emoji document_id=5361836987642815474>🦋</emoji> <a href='{crypto_link}'>Пополнить мой CryptoBot</a></b>\n\n"
        TON += f"<b><emoji document_id=5388963434148667202>👛</emoji> <a href='{tonrocket_link}'>Пополнить мой TonRocket</a></b>"

        await message.edit(TON)