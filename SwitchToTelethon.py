__version__ = (1, 0, 0, 1)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.4

# thx to @codrago for the inspiration
# this module may lead to unstable operation of the userbot

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
import aiofiles
import aiohttp
from telethon.extensions.html import parse
import inspect

from .. import loader, utils

@loader.tds
class SwitchToTelethon(loader.Module):
    """Auto switch from Hikka-TL to Telethon"""

    strings = {"name": "SwitchToTelethon"}

    async def client_ready(self, client, db):
        self.client = client
        # step1
        if self.get("switch1"):
            await self._switch_to_telethon(ignore=False)
            await self._change_files()
        else:
            pass
        # step2
        if self.get("switch2"):
            chat_id = self.get("switch2")
            await self.client.send_message(
                chat_id,
                f"<emoji document_id=5996898247963055513>🖤</emoji> <b>Switch to Telethon is completed successfully! (this module has been automatically unloaded)</b>\n\n"
                f"<emoji document_id=5325547803936572038>✨</emoji> <i>To restore everything to its original state, use the command</i> <code>{self.get_prefix()}terminal git checkout -- .</code><i>, and restart</i>"
            )
            self.set("switch2", None)
            await self.invoke('unloadmod', 'SwitchToTelethon', self.inline.bot_id)

    @loader.command()
    async def switch(self, message):
        """Automatically switch to Telethon"""

        chat_id = utils.get_chat_id(message)
        await utils.answer(message, "<emoji document_id=5461117441612462242>🙂</emoji> <i>Starting the first stage of switching to Telethon...</i>")

        await self._switch_to_telethon(ignore=True)

        self.set("switch1", chat_id)
        await utils.answer(message, "<emoji document_id=5456140674028019486>⚡️</emoji> <b>First stage completed. Restarting...</b>")
        await self._restart()

    async def _restart(self):
        await self.invoke('restart', '-f', self.inline.bot_id)

    async def _switch_to_telethon(self, ignore):
        for root, _, files in os.walk("."):
            for file in files:
                # conflict bypass
                if 'SwitchToTelethon' in file:
                    continue

                if file.endswith('.py') or file.endswith('.yml'):
                    await self._process_file(os.path.join(root, file), ignore)

    async def _process_file(self, file_path, ignore):
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                original = await f.readlines()

            updated = False
            switched = []

            for line in original:
                # conflict bypass x2
                if ignore and "CUSTOM_EMOJIS" in line:
                    switched.append(line)
                    continue
                # conflict bypass x3
                if file_path.endswith('main.py') and ignore and line.strip() == "import hikkatl":
                    switched.append(line)
                    continue
                # change references from "hikkatl" to "telethon" for switch
                if file_path.endswith('.py'):
                    if "hikkatl" in line:
                        line = line.replace("hikkatl", "telethon")
                        updated = True
                    # conflict bypass x4
                    if "(2, 0, 8)" in line:
                        line = line.replace("(2, 0, 8)", "(1, 35, 0)")
                        updated = True
                    # change references from "Hikka-TL-New" to "telethon" for switch
                    if "Hikka-TL-New" in line:
                        line = line.replace("Hikka-TL-New", "telethon")
                        updated = True
                # for HikkaInfo
                elif file_path.endswith('.yml'):
                    if '<emoji document_id=5377437404078546699>💜</emoji> <b>Hikka-TL:</b>' in line:
                        line = line.replace(
                            "<emoji document_id=5377437404078546699>💜</emoji> <b>Hikka-TL:</b>",
                            "<emoji document_id=5204453279790033300>❤️‍🔥</emoji> <b><a href='https://github.com/LonamiWebs/Telethon.git'>Telethon</a></b>:"
                        )
                        updated = True

                switched.append(line)

            if updated:
                async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                    await f.writelines(switched)
                print(f"Switched to Telethon: {file_path}")

        except Exception as e:
            print(f"Error: {file_path}: {e}")

    async def _change_files(self):
        chat_id = self.get("switch1")
        if not chat_id:
            print("No chat ID found for logging.")
            return

        try:
            async with aiohttp.ClientSession() as session:
                # update html.py
                async with session.get("https://raw.githubusercontent.com/yummy1gay/hikariatama-libs/main/html.py") as r_html:
                    if r_html.status == 200:
                        html_code = await r_html.text()

                        async with aiofiles.open(inspect.getfile(parse), 'w', encoding='utf-8') as f_html:
                            await f_html.write(html_code)

                        html_message = f"👍 <i>Updated Telethon parser file (for sending spoilers, custom emojis, etc.):</i> <code>{inspect.getfile(parse)}</code>"
                    else:
                        html_message = f"⚠️ <b>Failed to update HTML parse file:</b> <code>{r_html.status}</code> (please, use <code>{self.get_prefix()}terminal git checkout -- .</code>, and restart)"

                # update translate.py
                async with session.get("https://raw.githubusercontent.com/yummy1gay/hikariatama-libs/main/translate.py") as r_translate:
                    if r_translate.status == 200:
                        translate_code = await r_translate.text()

                        async with aiofiles.open("./hikka/modules/translate.py", 'w', encoding='utf-8') as f_translate:
                            await f_translate.write(translate_code)

                        translate_message = f"👍 <i>Updated translation module:</i> <code>./hikka/modules/translate.py</code> <i>(for compatibility)</i>"
                    else:
                        translate_message = f"⚠️ <b>Failed to update translation module:</b> <code>{r_translate.status}</code> (please, use <code>{self.get_prefix()}terminal git checkout -- .</code>, and restart)"

                await self.client.send_message(
                    chat_id,
                    f"{html_message}\n{translate_message}\n\n⏳ <b>Restarting...</b>"
                )

                self.set("switch1", None)
                self.set("switch2", chat_id)
                await self._restart()

        except Exception as e:
            print(f"Error updating files: {e}")
            if chat_id:
                await self.client.send_message(
                    chat_id, f"⚠️ <b>Error updating files:</b> <code>{e}</code> (please, use <code>{self.get_prefix()}terminal git checkout -- .</code>, and restart)"
                )

# окей