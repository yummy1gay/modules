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

from datetime import datetime

from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    MessageActionChannelMigrateFrom,
    UserStatusOnline,
)

from .. import loader, utils

@loader.tds
class ChatInfoMod(loader.Module):
    """Посмотреть информацию о чате."""

    strings = {"name": "yg_chatinfo"}

    async def chatinfocmd(self, chatinfo):
        """<юзернейм чата> или <айди чата> или просто команда в том чате где ты находишься"""
        if chatinfo.chat:
            await chatinfo.edit("<b><emoji document_id=5451732530048802485>⏳</emoji> Загрузка...</b>")
            chat = await get_chatinfo(chatinfo)
            caption = await fetch_info(chat, chatinfo)
            try:
                await chatinfo.client.send_message(
                    chatinfo.to_id,
                    str(caption),
                )
            except Exception:
                await chatinfo.edit(f"<b><emoji document_id=5472267631979405211>🚫</emoji> Произошла ошибка.</b>")
            await chatinfo.delete()
        else:
            await chatinfo.edit("<b><emoji document_id=5472267631979405211>🚫</emoji> Это не чат!</b>")


async def get_chatinfo(event):
    chat = utils.get_args_raw(event)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChannelRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("<b><emoji document_id=5472267631979405211>🚫</emoji> Недействительный канал/группа.</b>")
            return None
        except ChannelPrivateError:
            await event.reply(
                "<b><emoji document_id=5472267631979405211>🚫</emoji> Этот канал/группа приватная, либо я заблокирован там.</b>"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("<b><emoji document_id=5472267631979405211>🚫</emoji> Такой канал/группа не существует.</b>")
            return None
        except:
            chat = event.input_chat
            chat_info = await event.client(GetFullChannelRequest(chat))
            return chat_info
    return chat_info


async def fetch_info(chat, event):
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    chat_title = chat_obj_info.title
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception:
        msg_info = None
        await event.edit("<b><emoji document_id=5472267631979405211>🚫</emoji> Произошла ошибка.</b>")
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Удалённый аккаунт"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and type(msg_info.messages[0].action) is MessageActionChannelMigrateFrom
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    users_online = 0
    async for i in event.client.iter_participants(event.chat_id):
        if isinstance(i.status, UserStatusOnline):
            users_online = users_online + 1
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info
    bots = 0
    slowmode = (
        "Да"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "Нет"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "Да"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "Нет"
    )
    verified = (
        "Да" if hasattr(chat_obj_info, "verified") and chat_obj_info.verified else "Нет"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception:
            await event.edit("<b><emoji document_id=5472267631979405211>🚫</emoji> Произошла ошибка.</b>")
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b><emoji document_id=5348140027698227662>🙀</emoji> Информация о чате:</b>\n\n"
    caption += f"<b><emoji document_id=5370900820336319679>🥰</emoji> ChatID:</b> {chat_obj_info.id}\n\n"
    if messages_viewable is not None:
        caption += f"<b><emoji document_id=5424885441100782420>👀</emoji> Видимые сообщения:</b> <i>{messages_viewable}</i>\n\n"
    if messages_sent:
        caption += f"<b><emoji document_id=5465300082628763143>💬</emoji> Всего сообщений:</b> <i>{messages_sent}</i>\n\n"
    elif messages_sent_alt:
        caption += f"<b><emoji document_id=5465300082628763143>💬</emoji> Всего сообщений:</b> <i>{messages_sent_alt}</i>\n\n"
    if members is not None:
        caption += f"<b><emoji document_id=5372926953978341366>👥</emoji> Участников:</b> <i>{members}</i>\n\n"
    if banned_users is not None:
        caption += f"<b><emoji document_id=5472267631979405211>🚫</emoji> Пользователей в бане:</b> <i>{banned_users}</i>\n\n"
    if admins is not None:
        caption += f"<b><emoji document_id=5190498849440931467>👨‍💻</emoji> Админов:</b> <i>{admins}</i>\n\n"
    if bots_list:
        caption += f"<b><emoji document_id=5372981976804366741>🤖</emoji> Ботов:</b> <i>{bots}</i>\n"
    if description:
        caption
    return caption