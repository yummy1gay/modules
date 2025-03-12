__version__ = (1, 0, 0, 1)

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

import re
from .. import loader, utils
from telethon import events
import os

@loader.tds
class yg_trigger(loader.Module):
    """Триггер-модуль. Документация: kok.gay/trigger"""

    strings = {"name": "yg_trigger"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "watcher_on",
                True,
                "состояние вотчера",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        self.db = db
        self.triggers = self.db.get("triggers", "list", [])
        self.client = client
        handlers = [
            (self.trigger, [events.NewMessage, events.MessageEdited])
        ]

        for handler_func, event_list in handlers:
            for event in event_list:
                self.client.add_event_handler(handler_func, event)

    async def save_triggers(self):
        self.db.set("triggers", "list", self.triggers)

    async def validate(self, entity_value, target_entity):
        entity_k = entity_value.replace("@", "")

        entity_id = getattr(target_entity, "id", None)
        entity_usernames = await self.get_usernames(target_entity)

        if entity_k.isdigit():
            return int(entity_value) == entity_id

        return entity_k.lower() in entity_usernames

    async def add_trigger(self, conditions: dict, response: str):
        self.triggers.append({"conditions": conditions, "response": response})
        await self.save_triggers()

    async def triggercmd(self, message):
        """вкл/выкл вотчер"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        await message.edit(f"<emoji document_id=5361741454685256344>🎮</emoji> <b>Триггер-мод {'включен' if self.config['watcher_on'] else 'выключен'}</b>")

    async def remove_trigger(self, index: int):
        try:
            del self.triggers[index]
            await self.save_triggers()
            return True
        except IndexError:
            return False

    async def clear_triggers(self):
        self.triggers = []
        await self.save_triggers()

    async def get_usernames(self, entity):
        usernames = []

        if entity.username:
            username = entity.username
            if username:
                usernames.append(username.lower())

        if entity.usernames:
            additional_usernames = [
                u.username.lower() for u in (getattr(entity, "usernames", []) or [])
            ]
            usernames.extend(additional_usernames)

        return usernames

    async def list_triggerscmd(self, message):
        """показать все существующие триггеры"""
        if not self.triggers:
            await utils.answer(message, "<emoji document_id=5461117441612462242>🙂</emoji> <b>Нет активных триггеров</b>")
            return

        reply_with_html = "<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Список триггеров:</b>\n\n"
        
        reply_plain_text = "Список триггеров:\n\n"
        
        for i, trigger in enumerate(self.triggers):
            conditions = "\n".join([f"<b>-</b> {k}: <code>{v}</code>" for k, v in trigger["conditions"].items()])
            if not conditions:
                conditions = "<b>Нет условий (all=true)</b>"
            reply_with_html += f"<b>{i}.</b> Условия:\n{conditions}\n\n<emoji document_id=5443038326535759644>💬</emoji> <b>Ответ:</b> <code>{trigger['response']}</code>\n\n"
            
            reply_plain_text += f"{i}.\nУсловия:\n{conditions}\nОтвет: {trigger['response']}\n\n"

        if len(reply_with_html) > 4096:
            file_path = "triggers_list.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(reply_plain_text)

            await message.delete()
            await self.client.send_file(message.chat, caption="<emoji document_id=5433653135799228968>📁</emoji> <i>Вывод команды слишком длинный, поэтому он отправлен в файле.</i>", file=file_path)
            os.remove(file_path)
        else:
            await utils.answer(message, reply_with_html)

    async def split(self, input_str):
        is_in_quotes = False
        split_index = -1

        for i, char in enumerate(input_str):
            if char == '"':
                is_in_quotes = not is_in_quotes
            elif char == '|' and not is_in_quotes:
                split_index = i
                break

        if split_index == -1:
            raise ValueError("Некорректный формат: отсутствует разделитель '|'")

        return input_str[:split_index].strip(), input_str[split_index + 1:].strip()

    async def add_triggercmd(self, message):
        """<условия> | <ответ> - добавить новый триггер"""
        args = utils.get_args_raw(message)
        if not args or "|" not in args:
            await utils.answer(
                message,
                "<emoji document_id=5240241223632954241>🚫</emoji> <b>Формат: <условия> | <ответ></b>\n<emoji document_id=5325547803936572038>✨</emoji> Пример: <code>text=\"Привет\" | Здравствуй!</code>"
            )
            return

        try:
            conditions_raw, response = await self.split(args)

            valid_keys = {
                "text", "user", "chat", "starts_with", "ends_with", "contains",
                "regex", "is_command", "word_count", "char_count", "is_reply", "is_forwarded",
                "media_type", "message_length", "time_range", "date", "weekday", "all"
            }

            conditions = {}

            pattern = r'(\w+)=((?:\"(?:[^\"]|\\\")*\"|[^,\s]+))'
            matches = re.finditer(pattern, conditions_raw)

            for match in matches:
                key, value = match.group(1), match.group(2)

                if key not in valid_keys:
                    raise ValueError(f"Некорректное условие: {key}")

                if key in {"text", "regex", "contains", "starts_with", "ends_with"}:
                    if not (value.startswith('"') and value.endswith('"')):
                        raise ValueError(f"Значение для условия {key} должно быть в кавычках")
                    value = value[1:-1].replace('\\"', '"')

                if key == "all" and value.lower() == "true":
                    conditions = {"all": True}
                    break

                conditions[key] = value

            if not conditions:
                raise ValueError(
                    "😨 Ты не указал никаких условий.. Если ты такой смелый, укажи all=true в условиях!"
                )

            if conditions.get("all"):
                conditions = {}

            await self.add_trigger(conditions, response)

            conditions_str = "\n".join([f"<b>-</b> {k}: <code>{v}</code>" for k, v in conditions.items()])
            if not conditions_str:
                conditions_str = "<b>Нет условий (all=true)</b>"

            await utils.answer(
                message,
                f"<emoji document_id=5456140674028019486>⚡️</emoji> <b>Триггер добавлен!</b>\n\nУсловия:\n{conditions_str}\n\n<emoji document_id=5443038326535759644>💬</emoji> <b>Ответ:</b> <code>{response}</code>"
            )

        except ValueError as e:
            await utils.answer(message, f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Ошибка:</b> <code>{e}</code>")
        except Exception as e:
            await utils.answer(message, f"<emoji document_id=5240241223632954241>🚫</emoji> <b>Непредвиденная ошибка:</b> <code>{e}</code>")

    async def remove_triggercmd(self, message):
        """<номер> - удалить триггер"""
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await utils.answer(
                message,
                "<emoji document_id=5240241223632954241>🚫</emoji> <b>Укажи номер триггера для удаления</b>"
            )
            return

        index = int(args)
        if await self.remove_trigger(index):
            await utils.answer(message, "<emoji document_id=5445267414562389170>🗑</emoji> <b>Триггер удалён!</b>")
        else:
            await utils.answer(message, "<emoji document_id=5240241223632954241>🚫</emoji> <b> Неверный номер триггера</b>")

    async def clear_triggerscmd(self, message):
        """удалить все триггеры"""
        await self.clear_triggers()
        await utils.answer(message, "<emoji document_id=5445267414562389170>🗑</emoji> <b>Все триггеры удалены!</b>")

    async def trigger(self, message):
        if not self.config["watcher_on"]:
            return
        
        responses = []

        for trigger in self.triggers:
            conditions = trigger["conditions"]
            match = True

            for key, value in conditions.items():
                value = value.strip('"')
                if key == "text" and value.lower() != message.raw_text.lower():
                    match = False
                    break
                elif key == "user" and not await self.validate(value, message.sender):
                    match = False
                    break
                elif key == "chat" and not await self.validate(value, message.chat):
                    match = False
                    break
                elif key == "starts_with" and not message.raw_text.lower().startswith(value.lower()):
                    match = False
                    break
                elif key == "ends_with" and not message.raw_text.lower().endswith(value.lower()):
                    match = False
                    break
                elif key == "contains" and value.lower() not in message.raw_text.lower():
                    match = False
                    break
                elif key == "regex" and not re.search(value, message.raw_text):
                    match = False
                    break
                elif key == "is_command" and value.lower() == "true" and not message.raw_text.startswith("/"):
                    match = False
                    break
                elif key == "word_count" and len(message.raw_text.split()) != int(value):
                    match = False
                    break
                elif key == "char_count" and len(message.raw_text) != int(value):
                    match = False
                    break
                elif key == "is_reply" and value.lower() == "true" and not message.is_reply:
                    match = False
                    break
                elif key == "is_forwarded" and value.lower() == "true" and not message.fwd_from:
                    match = False
                    break
                elif key == "media_type":
                    media_types = {"photo": message.photo, "video": message.video, "sticker": message.sticker, "voice": message.voice, "audio": message.audio}
                    if not media_types.get(value.lower()):
                        match = False
                        break
                elif key == "message_length" and not (int(value.split("-", 1)[0]) <= len(message.raw_text) <= int(value.split("-", 1)[1])):
                    match = False
                    break
                elif key == "time_range" and not (int(value.split("-", 1)[0]) <= message.date.hour <= int(value.split("-", 1)[1])):
                    match = False
                    break
                elif key == "date" and value != message.date.strftime("%Y-%m-%d"):
                    match = False
                    break
                elif key == "weekday" and value.lower() != message.date.strftime("%A").lower():
                    match = False
                    break

            if match:
                responses.append(trigger["response"])

        for response in responses:
            await message.reply(response)
