__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.4

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

from telethon import events, functions
from telethon.tl.types import MessageMediaGiveaway, DialogFilter
from telethon.tl.functions.channels import JoinChannelRequest
from yumlib import yummy
from datetime import datetime, timezone

from .. import loader

class yg_prem(loader.Module):
    """Модуль для автоматического участия в розыгрышах премиум-подписок"""

    strings = {"name": "yg_prem"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                "@username куда будут отправляться логи",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "watcher_on",
                True,
                "состояние активатора",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "folder",
                True,
                "добавляет папку под названием yg_prem, в которую добавляются все каналы на которые подписался модуль",
                validator=loader.validators.Boolean()
            )
        )
        
    async def client_ready(self, client, db):
        self.folder_name = "yg_prem"
        self.client = client
        self.client.add_event_handler(self.prem, events.NewMessage)
        await yummy(client)

    async def premcmd(self, message):
        """вкл/выкл автоматическое участие в розыгрышах на премиум-подписки"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5217822164362739968>👑</emoji> <b>Автоматическое участие в розыгрышах на премиум-подписки {'включено' if self.config['watcher_on'] else 'выключено'}</b>")

    async def foldercmd(self, message):
        """вкл/выкл добавление каналов на которые подписался модуль в папку"""
        self.config["folder"] = not self.config["folder"]
        await message.edit(f"<emoji document_id=5325547803936572038>✨</emoji> <b>Добавление каналов на которые подписался модуль в папку {'включено' if self.config['folder'] else 'выключено'}</b>")

    async def get_giveaway_info(self, message):
        channels_info = []
        for channel_id in message.media.channels:
            entity = await message.client.get_entity(channel_id)
            username = entity.username
            if username is None:
                usernames = [u.username for u in entity.usernames if u.active]
                username = usernames[0] if usernames else "нету"

            channels_info.append({
                'title': entity.title,
                'username': username
            })
        
        quantity = message.media.quantity
        months = message.media.months
        until_date = message.media.until_date.strftime("%H:%M %d.%m.%Y")

        result = {
            'channels': channels_info,
            'quantity': quantity,
            'months': months,
            'until_date': until_date
        }

        return result

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message)

    async def create_or_get_folder(self):
        """проверка на наличие папки yg_prem и создание новой при необходимости"""
        if self.config["folder"]:
            dialog_filters = await self.client(functions.messages.GetDialogFiltersRequest())

            for dialog_filter in dialog_filters:
                if hasattr(dialog_filter, "id") and hasattr(dialog_filter, "title") and dialog_filter.title == self.folder_name:
                    return dialog_filter.id

            chan = "yg_modules"
            peers = [await self.client.get_input_entity(chan)]

            folder_id = len(dialog_filters) + 1
            new_folder = DialogFilter(
                id=folder_id,
                title=self.folder_name,
                include_peers=peers,
                exclude_peers=[],
                pinned_peers=[]
            )
            await self.client(functions.messages.UpdateDialogFilterRequest(id=folder_id, filter=new_folder))

            return folder_id

    async def add_channel_to_folder(self, folder_id, channel):
        """добавление канала в папку"""
        if self.config["folder"]:
            dialog_filters = await self.client(functions.messages.GetDialogFiltersRequest())
            
            folder = next((f for f in dialog_filters if hasattr(f, "id") and f.id == folder_id), None)
            
            if folder is None:
                await self.log("<emoji document_id=5210952531676504517>❌</emoji> <b>Папка не найдена.</b>")
                return
            
            updated_peers = folder.include_peers + [channel]

            updated_folder = DialogFilter(
                id=folder_id,
                title=self.folder_name,
                include_peers=updated_peers,
                exclude_peers=[],
                pinned_peers=[]
            )
            await self.client(functions.messages.UpdateDialogFilterRequest(id=folder_id, filter=updated_folder))

    async def prem(self, event):
        """watcher for new giveaway messages"""
        if self.config["watcher_on"]:
            if event.message.media and isinstance(event.message.media, MessageMediaGiveaway):
                giveaway_message = await self.client.get_messages(event.chat_id, ids=event.message.id)
                giveaway_info = await self.get_giveaway_info(giveaway_message)
                channels = giveaway_info['channels']
                until_date = event.message.media.until_date

                if until_date < datetime.now(timezone.utc):
                    return

                folder_id = await self.create_or_get_folder()

                for channel in channels:
                    username = channel['username']
                    if username != "нету":
                        try:
                            await self.client(JoinChannelRequest(username))
                            await self.add_channel_to_folder(folder_id, await self.client.get_input_entity(username))
                        except Exception as e:
                            await self.log(f"<emoji document_id=5210952531676504517>❌</emoji> <b>Не смог подписаться на @{username}, из-за ошибки:</b> <code>{str(e)}</code>")

                channels_info = "\n".join([f"• {channel['title']} (@{channel['username']})" for channel in giveaway_info['channels']])
                quantity = giveaway_info['quantity']
                months = giveaway_info['months']
                until_date = giveaway_info['until_date']

                m = self.count(months)
                t = f"на <code>{months}</code> {m}"
                log = (f"<emoji document_id=5456140674028019486>⚡️</emoji> <b>Участвую в новом розыгрыше! Информация:</b>\n\n"
                       f"<emoji document_id=5282843764451195532>🖥</emoji> <b>Каналы:</b>\n{channels_info}\n\n"
                       f"<emoji document_id=5438496463044752972>⭐️</emoji> <b>Количество премок:</b> <code>{quantity}</code> ({t})\n"
                       f"<emoji document_id=5413879192267805083>🗓</emoji> <b>Дата окончания розыгрыша:</b> <code>{until_date}</code> (UTC)\n")
                
                await self.log(log)

    def count(self, months):
        if 11 <= months % 100 <= 14:
            return "месяцев"
        kok = months % 10
        if kok == 1:
            return "месяц"
        elif 2 <= kok <= 4:
            return "месяца"
        else:
            return "месяцев"