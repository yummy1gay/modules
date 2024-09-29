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

import logging
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from yumlib import yummy

from .. import loader, utils

@loader.tds
class TonWalletGenerator(loader.Module):
    """Генератор TON кошельков"""

    strings = {"name": "yg_TonWalletGenerator"}

    async def client_ready(self, client, db):
        self.client = client
        await yummy(client)

    async def gencmd(self, message):
        """<count> генерирует один или несколько TON кошельков"""
        try:
            args = utils.get_args_raw(message).strip()
            if args:
                try:
                    count = int(args)
                    chozabretto = self.gcd(count)
                    tmp = await message.edit(f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Генерирую {count} {chozabretto}...</b>")
                    if count < 2 or count > 200:
                        raise ValueError
                except ValueError:
                    await message.edit("<emoji document_id=5465665476971471368>❌</emoji> <b>Некорректное количество кошельков. Допустимый диапазон: от 2 до 200.</b>\n\n<emoji document_id=5472164874886846699>✨</emoji> <i>Если вы хотите сгенерировать один кошелек то просто напишите</i> <code>.gen</code>")
                    return
            else:
                kok = await message.edit("<emoji document_id=5431449001532594346>⚡️</emoji> <b>Генерирую...</b>")
                count = 1

            wallets_info = []
            for _ in range(count):
                mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v4r2, workchain=0)
                wallet_address = wallet.address.to_string(True, True, False)
                wallets_info.append((wallet_address, ' '.join(mnemonics)))

            if count == 1:
                half = len(wallets_info[0][1].split()) // 2
                first_half = wallets_info[0][1].split()[:half]
                second_half = wallets_info[0][1].split()[half:]

                max_len = max(len(word) for word in wallets_info[0][1].split()) + 2

                mnemonics_str = ''
                for i in range(half):
                    first_index = i + 1
                    second_index = half + i + 1
                    if first_index < 10:
                        mnemonics_str += f"{first_index}. {first_half[i].ljust(max_len)} {second_index}. {second_half[i]}\n"
                    else:
                        mnemonics_str += f"{first_index}. {first_half[i].ljust(max_len)}{second_index}. {second_half[i]}\n"

                response = (
                    f"<b>Адрес:</b>\n<code>{wallets_info[0][0]}</code>\n\n"
                    f"<b>Сид-фраза:</b>\n<pre>{mnemonics_str}</pre>\n"
                    f"\n<b>Скопировать:</b> <code>{wallets_info[0][1]}</code>"
                )
                await kok.edit(response)
            else:
                wallet_info = "\n\n".join(f"{i+1}. Адрес: {addr}\n   Сид-фраза: {seed}" for i, (addr, seed) in enumerate(wallets_info))
                with open("wallets.txt", "w", encoding="utf-8") as f:
                    f.write(wallet_info)

                chozabretto = self.gcd(count)
                caption = f"<emoji document_id=5370869711888194012>👾</emoji> <b>Сгенерировано {count} {chozabretto}</b>"
                await self.client.send_file(message.peer_id, "wallets.txt", caption=caption)
                await tmp.delete()
        except Exception as e:
            logging.exception("Ошибка при генерации кошелька")
            await message.edit("<emoji document_id=5465665476971471368>❌</emoji> <b>Ошибка при генерации кошелька. Попробуйте еще раз</b>")

    def gcd(self, count):
        if 11 <= count % 100 <= 14:
            return "кошельков"
        last_digit = count % 10
        if last_digit == 1:
            return "кошелек"
        elif 2 <= last_digit <= 4:
            return "кошелька"
        else:
            return "кошельков"