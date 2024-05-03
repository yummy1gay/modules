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
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                "@username куда будут отправляться логи",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "logs_enabled",
                True,
                "отправка логов",
                validator=loader.validators.Boolean()
            )
        )
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
                await self.subscribe_to_chats(chat_invites)
                await asyncio.sleep(1)
                await message.click(data=b'join-giveaway')
                await asyncio.sleep(0.1)
                await message.delete()
                
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

        if message.sender_id == 1559501630 and message.reply_markup:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if button.url.startswith("https://app.crypt.bot/giveaways"):
                        giw_link = button.url
                        if not "Поздравляем!" in message.text:
                            await self.send_log_message(giw_link)
                            await asyncio.sleep(0.1)
                            await message.delete()
            
    async def send_log_message(self, giw_link):
        username = self.config["logs_username"]
        if self.config["logs_enabled"]:
            if username:
                await self.client.send_message(username, f"<b><emoji document_id=5195366520561092628>🎁</emoji> Зарегистрировался в новом розыгрыше!\n\n<emoji document_id=5870527201874546272>🔗</emoji> Все подробности: <a href='{giw_link}'>click</a></b>", link_preview=False)

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
        msg = await self.client.send_message("CryptoBot", f"/start G{code}")
        await asyncio.sleep(0.1)
        await msg.delete()

    async def gwscmd(self, message):
        """проверить работоспособность"""
        await message.edit("<emoji document_id=5361836987642815474>🦋</emoji> <b>Модуль для автоматического участия в розыгрышах @CryptoBot работает</b>")

    async def gwslogscmd(self, message):
        """вкл/выкл отправку логов"""
        self.config["logs_enabled"] = not self.config["logs_enabled"]
        await message.edit(f"<emoji document_id=5891243564309942507>💬</emoji> <b>Отправка логов {'включена' if self.config['logs_enabled'] else 'выключена'}</b>")