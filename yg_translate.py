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

from deep_translator import GoogleTranslator
from langdetect import detect

from .. import loader, utils

@loader.tds
class переводMod(loader.Module):
    """Модуль для перевода текста на различные языки"""

    strings = {"name": "yg_translate"}
    
    @loader.command("перевод", aliases=["tr"])
    async def пcmd(self, message):
        """перевести текст на несколько языков"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Что переводить то?")
            return

        phrase = args.strip()

        translations = []
        languages = {
            "ru": "<emoji document_id=6323139226418284334>🇷🇺</emoji> <b>Русский</b>",
            "uk": "<emoji document_id=6323289850921354919>🇺🇦</emoji> <b>Украинский</b>",
            "en": "<emoji document_id=6321193412959668105>🇺🇲</emoji> <b>Английский</b>",
            "de": "<emoji document_id=6320817337033295141>🇩🇪</emoji> <b>Немецкий</b>",
            "zh-CN": "<emoji document_id=6323453751168337485>🇨🇳</emoji> <b>Китайский</b>",
        }

        source_lang = detect(phrase)
        if source_lang not in languages:
            source_lang = "auto"

        for lang, lang_name in languages.items():
            translation = GoogleTranslator(source=source_lang, target=lang).translate(phrase)
            translations.append(f"{lang_name}: <code>{translation}</code>")

        response = f"<emoji document_id=5443038326535759644>💬</emoji> <b>Текст:</b> <i>{phrase}</i>\n\n" + "\n\n".join(translations)
        await utils.answer(message, response)
