#meta developer: @yummy1gay

import re
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from .. import loader
import asyncio

@loader.tds
class yg_giveaways(loader.Module):
    """Модуль для автоматического участия в розыгрышах @CryptoBot"""

    strings = {"name": "yg_giveaways"}

    def __init__(self):
        self.codes = {}

    async def client_ready(self, client, db):
        await client.send_message('CryptoBot', '/start')

    async def watcher(self, message):
        if message.sender_id == 1559501630 and message.reply_markup and "Crypto Bot" in message.text:
            chat_invites = []
            url_regex_private = re.compile(r"https?://t\.me/(\w{4,})")
            url_regex_public = re.compile(r"https?://t\.me/\+(\w{12,})")
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    try:
                        if url_regex_private.match(button.url):
                            channel_match = url_regex_private.match(button.url)
                            chat_invites.append((channel_match.group(1), True))
                        elif url_regex_public.match(button.url):
                            channel_match = url_regex_public.match(button.url)
                            chat_invites.append((channel_match.group(1), False))
                    except:
                        pass
            if chat_invites:
                await self.send_invites(chat_invites)
                await asyncio.sleep(1)
                await message.click(data=b'join-giveaway')
                
        if message.reply_markup:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if button.url and button.url.startswith("https://t.me/send?start=G") or button.url.startswith("https://t.me/CryptoBot/app?startapp=giveaway-G"):
                        code = self.q(button.url)
                        if code and code not in self.codes:
                            await self.x(code)
                            self.codes[code] = True

        if message.text:
            urls = re.findall(r'https://t.me/send\?start=G([^\s]+)|https://t.me/CryptoBot/app\?startapp=giveaway-G([^\s]+)', message.text)
            for url_tuple in urls:
                for url in url_tuple:
                    if url:
                        code = self.q(url)
                        if code and code not in self.codes:
                            await self.x(code)
                            self.codes[code] = True

    async def send_invites(self, chat_invites):
        invite_message = "<b>Было обнаружено {} канала(-ов) для обязательной подписки:</b>\n\n".format(len(chat_invites))
        for index, (invite_link, is_public) in enumerate(chat_invites, start=1):
            if is_public:
                invite_message += "<b>{}.</b> <i>t.me/{}</i>\n".format(index, invite_link)
            else:
                invite_message += "<b>{}.</b> <i>t.me/+{}</i>\n".format(index, invite_link)
        await self.client.send_message("CryptoBot", invite_message, link_preview=False)
        await self.subscribe_to_chats(chat_invites)

    async def subscribe_to_chats(self, chat_invites):
        for invite_link, is_public in chat_invites:
            try:
                if is_public:
                    await self.client(JoinChannelRequest(invite_link))
                else:
                    await self.client(ImportChatInviteRequest(invite_link))
            except Exception as e:
                print(f"Failed to join chat with invite link {invite_link}: {e}")

    @staticmethod
    def q(url):
        match = re.search(r'https://t.me/send\?start=G([^\s]+)', url)
        if match:
            return match.group(1)
        else:
            match = re.search(r'https://t.me/CryptoBot/app\?startapp=giveaway-G([^\s]+)', url)
            if match:
                return match.group(1)
        return None

    async def x(self, code):
        await self.client.send_message("CryptoBot", f"/start G{code}")

    async def gwscmd(self, message):
        """проверить работоспособность"""
        await message.edit("<emoji document_id=5361836987642815474>🦋</emoji> <b>Модуль для автоматического участия в розыгрышах @CryptoBot работает</b>")