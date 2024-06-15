__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# + посхалко

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# ⣿⣿⣿⡷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⢿⣿⣿⣿⣿
# ⣹⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣮⣽⣿⣿⣿
# ⣿⣿⣿⣝⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣄⠛⣿⣿⣿⣿⣿⣿⣟⣝⣿⣿⣿
# ⣿⣿⢷⣾⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣯⢍⢻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿⠛⠻⠛⢿⡇⢹⣿⣿⣿⣿⣿⣳⣽⣿⣿⣿
# ⡻⠟⠈⢛⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⣷⣼⣿⣿⣿⣦⣤⡀⠄⠀⠀⠰⠀⢀⣤⣴⣿⣿⣶⣧⣤⣄⣤⣩⢸⣿⣿⣿⣿⡯⢍⣿⣿⣿⣿
# ⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡇⢼⣿⣿⣿⠋⣽⡟⣿⣿⣿⣿⣿⣧⠀⠀⢸⣾⣿⣿⣿⣿⣿⢿⢿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣷⡚⢿⣿⣿⣿
# ⠀⠀⠀⠀⠈⢉⣿⣿⣿⣿⠃⠜⠻⢿⣿⣾⣧⣋⣿⣿⣿⣿⠻⠒⠂⠀⢺⣿⣿⣿⣧⣧⣛⢰⢼⣾⣿⣿⠃⠘⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⠀⠀⠀⠉⠹⠿⠿⢿⣿⣿⠿⠻⠳⠁⠀⠀⠘⡿⣿⣿⣿⠿⣿⢿⢭⡄⠠⠇⠍⣀⣿⣿⣿⡉⣩⠞⢸⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⠀⣯⣿⣿⠈⣡⢀⠀⠀⠀⠀⠀⠀⠀⢰⣶⠦⠀⠀⠀⠀⣈⣎⠀⠈⠀⠈⠀⠀⠀⣀⣠⢴⠽⣿⣿⣟⢏⠂⠀⢼⣿⣿⣿
# ⠀⠁⠀⣠⠂⠀⠀⢡⢼⣏⣾⣯⠈⠀⠀⠀⠀⠀⣠⡖⡿⠉⠃⠀⠀⠀⠈⡜⠉⢻⣶⣄⠀⠀⠀⠀⣶⡟⣨⣿⣿⡿⣟⣿⢿⣿⣿⡟⣿⡿
# ⠀⠀⠒⠋⠀⠀⠀⢀⠨⢛⡿⢻⡆⠀⠀⣠⣴⠟⠁⠘⣼⣤⡀⠀⠀⠀⠀⣢⣤⣿⠉⠙⢷⣆⡀⠰⣿⣾⣿⣿⡏⢻⡿⠉⣭⢠⠀⢘⣿⢿
# ⠀⣤⠠⣀⢀⠀⠀⠀⠀⣵⠼⣿⣷⣶⣿⣿⣿⠀⠀⠀⠈⢻⣿⣆⠀⠀⣀⣿⠟⠓⠀⠀⠀⣽⣿⣿⣿⣿⣿⢿⢀⡿⠀⢀⣰⣤⣠⣶⣾⣿
# ⣿⠟⢻⣿⣿⠀⠀⢈⠀⠽⠀⠘⠿⣿⣿⣿⣿⣀⣀⠀⠀⠀⠀⠉⢿⠛⠛⠁⠀⠀⢀⣠⣼⣿⣿⣿⣿⣿⣏⣿⠋⠀⡠⣿⣿⣿⣿⣿⣿⣿
# ⠉⠀⣴⢴⠟⣤⠆⠀⣔⡀⣄⠀⠀⠈⠘⡿⣿⣿⣿⣿⣿⣶⣶⣤⣄⣤⣤⣴⣾⣿⣿⣿⣿⣿⡟⢻⠿⣿⣹⠃⠤⣴⢷⡙⣿⣿⣿⢿⣿⣿
# ⠀⠀⢸⣄⣠⣄⡀⠀⠿⠛⢁⠠⠠⠀⢀⠁⠈⣿⣿⣿⡍⠚⠘⠋⠙⡙⠉⠏⠃⢨⣿⣿⣿⣿⡂⠈⣸⣷⢋⢳⣞⠱⠐⣿⣾⣿⣟⣬⣿⣿
# ⠀⠀⠀⠀⠈⠿⠽⠀⢀⠀⠀⠀⣄⡄⢸⣆⠀⢹⣿⣿⣿⠴⠀⠀⠀⠇⠀⠄⠲⢻⣿⣿⣿⣿⡏⠁⣿⡏⣼⡾⢉⣀⣲⣿⣿⣿⣿⣿⣿⣿
# ⠀⢀⢀⣀⠀⠀⠀⠀⠈⢠⣤⡠⢿⣴⡆⢻⣦⠀⢻⣿⣿⣶⣤⣤⣀⣀⡀⣄⣼⣿⣿⣿⣿⣿⠇⣸⡿⣁⠟⢵⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿
# ⠰⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣷⣿⣿⣿⡌⢿⡆⠀⠙⢿⣷⣁⠉⠉⠉⠉⣉⣽⡿⢋⣿⣾⣿⣰⠇⣼⣿⣆⡸⣯⣟⣷⣿⣿⣿⣿⣿⣿⣿
# ⠀⠀⠀⠀⠈⠁⠀⠀⣩⣾⣿⣿⡇⣿⣿⣿⣿⣿⡄⡀⠀⠀⠉⠉⠁⠁⠠⠛⠛⠁⠊⣿⣿⣿⣟⣿⣿⣿⣿⢷⡿⣏⢾⢿⣿⣿⣿⣿⣿⣿
# ⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⡉⢻⡀⠀⠀⣀⣤⣤⡤⠴⠒⠋⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣽⣿⣿⣿⢿⣿
# ⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠂⠤⠤⠤⠤⠄⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⣷⠾⡿⢿⢾⣿
# ⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣱⢝⢺⣿
# ⣰⣂⢦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣆⠀⠀⠀⠘⠀⠀⠀⠀⣈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣦⣤⣠⣴⠀⡤⣠⣶⣦⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

import logging
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from .. import loader

@loader.tds
class TonWalletGenerator(loader.Module):
    """Генератор TON кошельков"""

    strings = {"name": "yg_TonWalletGenerator"}

    async def client_ready(self, client, db):
        self.client = client

    async def gencmd(self, message):
        """генерирует новый TON кошелек"""
        try:
            mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v4r2, workchain=0)
            wallet_address = wallet.address.to_string(True, True, False)
            
            half = len(mnemonics) // 2
            first_half = mnemonics[:half]
            second_half = mnemonics[half:]
            
            max_len = max(len(word) for word in mnemonics) + 2
            
            mnemonics_str = ''
            for i in range(half):
                first_index = i + 1
                second_index = half + i + 1
                if first_index < 10:
                    mnemonics_str += f"{first_index}. {first_half[i].ljust(max_len)} {second_index}. {second_half[i]}\n"
                else:
                    mnemonics_str += f"{first_index}. {first_half[i].ljust(max_len)}{second_index}. {second_half[i]}\n"
            
            mnemonics_copy = ' '.join(mnemonics)
            
            response = (
                f"<b>Адрес:</b>\n<code>{wallet_address}</code>\n\n"
                f"<b>Сид-фраза:</b>\n<pre>{mnemonics_str}</pre>\n"
                f"<b>Скопировать:</b> <code>{mnemonics_copy}</code>"
            )

            await message.edit(response)
        except Exception as e:
            logging.exception("Ошибка при генерации кошелька")
            await message.edit("<b>Ошибка при генерации кошелька. Попробуйте еще раз</b>")