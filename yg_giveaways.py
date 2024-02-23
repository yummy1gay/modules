#meta developer: @yummy1gay

import re
from telethon.tl.functions.messages import ImportChatInviteRequest
from .. import loader
import asyncio

@loader.tds
class yg_giveaways(loader.Module):
    """Модуль для автоматического участия в розыгрышах @CryptoBot"""

    strings = {"name": "yg_giveaways"}

    async def client_ready(self, client, db):
        await client.send_message('CryptoBot', '/start')

    async def watcher(self, message):
        if message.sender_id == 1559501630 and message.reply_markup and "Crypto Bot" in message.text:
            chat_invites = []
            url_regex = re.compile(r"https://t\.me/\+(\w{12,})")
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        channel_match = url_regex.search(button.url)
                        if channel_match:
                            chat_invites.append(channel_match.group(1))
                    except:
                        pass
            if chat_invites:
                await self.send_invites(chat_invites)
                await asyncio.sleep(1)
                await message.click(data=b'join-giveaway')
                
        if message.reply_markup:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if button.url and button.url.startswith("https://t.me/send?start=G"):
                        code = self.q(button.url)
                        if code:
                            await self.x(code)

    async def send_invites(self, chat_invites):
        invite_message = "<b>Было обнаружено {} канала(-ов) для обязательной подписки:</b>\n\n".format(len(chat_invites))
        for index, invite_link in enumerate(chat_invites, start=1):
            invite_message += "<b>{}.</b> <i>t.me/+{}</i>\n".format(index, invite_link)
        await self.client.send_message("CryptoBot", invite_message, link_preview=False)
        await self.subscribe_to_chats(chat_invites)

    async def subscribe_to_chats(self, chat_invites):
        for invite_link in chat_invites:
            try:
                await self.client(ImportChatInviteRequest(invite_link))
            except Exception as e:
                print("Failed to join chat with invite link {}: {}".format(invite_link, e))

    @staticmethod
    def q(url):
        match = re.search(r'https://t.me/send\?start=G([A-Za-z0-9_]+)', url)
        if match:
            return match.group(1)
        return None

    async def x(self, code):
        await self.client.send_message("CryptoBot", f"/start G{code}")

    async def gwscmd(self, message):
        """проверить работоспособность"""
        await message.edit("<emoji document_id=5361836987642815474>🦋</emoji> <b>Модуль для автоматического участия в розыгрышах @CryptoBot работает</b>")
