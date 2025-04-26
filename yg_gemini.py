__version__ = (1, 5, 0, 0)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# requires: google-generativeai pillow

# Changelog v1.5.0:
# - Чаты с контекстом: Новые команды (.gcreate, .gask, .gchats) для диалогов с Gemini, сохраняющих историю.
# - Регенерация ответов: Кнопка "🔄" под каждым ответом для получения другого варианта.
# - Расширенная поддержка медиа: Работает с фото, видео, аудио и голосовыми сообщениями.
# - Пагинация: Длинные ответы теперь разбиваются на страницы.
# - Гибкая конфигурация: Поддержка нескольких API-ключей, команда .gset для инструкции, команда .gmodels для просмотра моделей.
# - Улучшения интерфейса: Локализация (RU/UA), улучшенное форматирование, обработка цитат.

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
import re
import asyncio
import logging
import random
import secrets
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from telethon.extensions import html
from telethon.tl.types import Message
from telethon.utils import split_text

from .. import loader, utils
from ..inline.types import InlineCall
from ..inline.utils import Utils

logger = logging.getLogger(__name__)

@loader.tds
class yg_gemini(loader.Module):
    """Gemini AI module with media support, regeneration, and chat context!"""

    strings = {
        "name": "yg_gemini",

        "no_keys": "<emoji document_id=5274099962655816924>❗️</emoji> <b>API key not specified. You can get it here: aistudio.google.com/apikey (free), then specify it in the config (<code>{self.get_prefix()}cfg yg_gemini</code>)</b>",
        "api_error": "Gemini API Error: {error}",
        "unknown_error": "An unknown error occurred: {error}",
        "list_models_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Failed to retrieve list of models:</b> {error}",
        "pagination_error": "[Pagination Error]",
        "media_dl_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Failed to download media ({media_type}):</b> {error}",
        "media_unsupported": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Media type <code>{mime_type}</code> is not supported by the module!</b>",
        "media_upload_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Failed to upload media ({media_type}) to Google server:</b> {error}",

        "loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query:</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini is thinking...</b>",
        "loading_media_query": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query regarding media ({media_type}):</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini is thinking...</b>",
        "loading_media_only": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query about media ({media_type})...</b>\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini is thinking...</b>",
        "regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query:</b> {prompt}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Regenerating response...</b>",
        "regenerating_media_query": "💬 <b>Query regarding media ({media_type}):</b> {prompt}\n\n🔄 <b>Regenerating response...</b>",
        "regenerating_media_only": "💬 <b>Query about media ({media_type})...</b>\n\n🔄 <b>Regenerating response...</b>",
        "media_dl": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Downloading media ({media_type})...</b>",
        "media_upload": "<b><emoji document_id=5447410659077661506>🌐</emoji> Uploading media ({media_type}) to Google server...</b>",

        "resp_base": "💬 <b>Query:</b> {prompt}\n\n✨ <b>Response from Gemini:</b>",
        "resp_base_media": "💬 <b>Query regarding media ({media_type}):</b> {prompt}\n\n✨ <b>Response from Gemini:</b>",
        "resp_base_media_only": "✨ <b>Response from Gemini (about media {media_type}):</b>",

        "gemini_no_prompt": "<emoji document_id=5274099962655816924>❗️</emoji> <i>Enter a query or reply to media!</i>",
        "gask_usage": "<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Usage:</b> <code>{prefix}gask &lt;chat_id&gt; &lt;question&gt;</code>",
        "models_title": "<b>✨ Available Gemini Models:</b>\n\n",
        "model_entry": "🔹 <b>{name}</b>\n    ▫️ <i>{desc}</i>\n",
        "models_fetch": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Retrieving list of models...</b>",
        "models_not_found": "<emoji document_id=5416081784641168838>🟢</emoji> No available models found (straaaange)",

        "chat_create_ok": "<emoji document_id=5325547803936572038>✅</emoji> <b>Chat created!</b>\n<b>ID:</b> <code>{chat_id}</code>\n<b>Name:</b> {name}",
        "chat_not_found": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Chat with ID <code>{chat_id}</code> not found</b>",
        "chat_no_chats": "😕 <b>You don't have any Gemini chats yet. Use <code>{prefix}gcreate</code>!</b>",
        "chat_list_title": "💾 <b>Your Gemini Chats:</b>",
        "chat_menu_title": "🔧 <b>Chat {chat_id} ({name}):</b>",
        "chat_menu_history": "📜 History",
        "chat_menu_delete": "🗑 Delete",
        "chat_menu_back": "🔙 Back",
        "chat_hist_title": "📜 <b>Chat History {chat_id} ({name})</b> (Page {current_page}/{total_pages}):",
        "chat_hist_entry": "<b>{role}:</b> <blockquote expandable>{text}</blockquote>",
        "chat_hist_empty": "<i>Chat history is empty!</i>",
        "chat_del_confirm": "❓ <b>Delete chat {chat_id} ({name})? This is irreversible.</b>",
        "chat_del_yes": "✅ Yes",
        "chat_del_no": "❌ No",
        "chat_del_ok": "✅ Chat {chat_id} deleted!",

        "gask_loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query to chat <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini is thinking...</b>",
        "gask_resp_base": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query to chat <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=5325547803936572038>✨</emoji> <b>Response from Gemini:</b>",
        "gask_regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Query to chat <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Regenerating response...</b>",

        "btn_regenerate": "🔄 Regenerate",
        "btn_prev": "⬅️",
        "btn_next": "➡️",
        "btn_chat": "{name} ({chat_id})",

        "photo": "photo",
        "video": "video",
        "audio": "audio",
        "voice": "voice message",
        "no_args": "<emoji document_id=5461117441612462242>🙂</emoji> <b>You need to specify the text of the instruction!</b>",
        "success": "<emoji document_id=5206607081334906820>✔️</emoji> <b>The instruction has been successfully installed!</b>",

        "config_api_key": "Gemini API keys (aistudio.google.com/apikey). One will be chosen randomly for each request.",
        "config_model": "Gemini model. {prefix}gmodels will show available ones. Example: gemini-1.5-pro-latest",
        "config_system_instruction": "System instruction for Gemini. Can be set using the {prefix}gset command if you encounter limits!",
        "config_proxy": "Proxy: http://user:pass@host:port or socks5://user:pass@host:port (needed if Gemini is not available for your server's geo location)",
    }

    strings_ru = {
        "no_keys": "<emoji document_id=5274099962655816924>❗️</emoji> <b>API ключ не указан. Получить его можно тут: aistudio.google.com/apikey (бесплатно), затем укажи его в конфиге (<code>{self.get_prefix()}cfg yg_gemini</code>)</b>",
        "api_error": "Ошибка API Gemini: {error}",
        "unknown_error": "Произошла неизвестная ошибка: {error}",
        "list_models_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не удалось получить список моделей:</b> {error}",
        "pagination_error": "[Ошибка пагинации]",
        "media_dl_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не удалось скачать медиа ({media_type}):</b> {error}",
        "media_unsupported": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Тип медиа <code>{mime_type}</code> не поддерживается модулем!</b>",
        "media_upload_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не удалось загрузить медиа ({media_type}) на сервер Google:</b> {error}",

        "loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос:</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думает...</b>",
        "loading_media_query": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос к медиа ({media_type}):</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думает...</b>",
        "loading_media_only": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос по медиа ({media_type})...</b>\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думает...</b>",
        "regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос:</b> {prompt}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Регенерация ответа...</b>",
        "regenerating_media_query": "💬 <b>Запрос к медиа ({media_type}):</b> {prompt}\n\n🔄 <b>Регенерация ответа...</b>",
        "regenerating_media_only": "💬 <b>Запрос по медиа ({media_type})...</b>\n\n🔄 <b>Регенерация ответа...</b>",
        "media_dl": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Загрузка медиа ({media_type})...</b>",
        "media_upload": "<b><emoji document_id=5447410659077661506>🌐</emoji> Загрузка медиа ({media_type}) на сервер Google...</b>",

        "resp_base": "💬 <b>Запрос:</b> {prompt}\n\n✨ <b>Ответ от Gemini:</b>",
        "resp_base_media": "💬 <b>Запрос к медиа ({media_type}):</b> {prompt}\n\n✨ <b>Ответ от Gemini:</b>",
        "resp_base_media_only": "✨ <b>Ответ от Gemini (по медиа {media_type}):</b>",

        "gemini_no_prompt": "<emoji document_id=5274099962655816924>❗️</emoji> <i>Введи запрос или ответь на медиа!</i>",
        "gask_usage": "<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Использование:</b> <code>{prefix}gask &lt;id_чата&gt; &lt;вопрос&gt;</code>",
        "models_title": "<b>✨ Доступные модели Gemini:</b>\n\n",
        "model_entry": "🔹 <b>{name}</b>\n    ▫️ <i>{desc}</i>\n",
        "models_fetch": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Получение списка моделей...</b>",
        "models_not_found": "<emoji document_id=5416081784641168838>🟢</emoji> Не найдено доступных моделей (страннааа)",

        "chat_create_ok": "<emoji document_id=5325547803936572038>✅</emoji> <b>Чат создан!</b>\n<b>ID:</b> <code>{chat_id}</code>\n<b>Имя:</b> {name}",
        "chat_not_found": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Чат с ID <code>{chat_id}</code> не найден</b>",
        "chat_no_chats": "😕 <b>У вас пока нет чатов Gemini. Используйте <code>{prefix}gcreate</code>!</b>",
        "chat_list_title": "💾 <b>Ваши чаты Gemini:</b>",
        "chat_menu_title": "🔧 <b>Чат {chat_id} ({name}):</b>",
        "chat_menu_history": "📜 История",
        "chat_menu_delete": "🗑 Удалить",
        "chat_menu_back": "🔙 Назад",
        "chat_hist_title": "📜 <b>История чата {chat_id} ({name})</b> (Стр. {current_page}/{total_pages}):",
        "chat_hist_entry": "<b>{role}:</b> <blockquote expandable>{text}</blockquote>",
        "chat_hist_empty": "<i>История чата пуста!</i>",
        "chat_del_confirm": "❓ <b>Удалить чат {chat_id} ({name})? Это необратимо.</b>",
        "chat_del_yes": "✅ Да",
        "chat_del_no": "❌ Нет",
        "chat_del_ok": "✅ Чат {chat_id} удален!",

        "gask_loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос в чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думает...</b>",
        "gask_resp_base": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос в чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=5325547803936572038>✨</emoji> <b>Ответ от Gemini:</b>",
        "gask_regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запрос в чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Регенерация ответа...</b>",

        "btn_regenerate": "🔄 Регенерировать",
        "btn_prev": "⬅️",
        "btn_next": "➡️",
        "btn_chat": "{name} ({chat_id})",

        "photo": "фото",
        "video": "видео",
        "audio": "аудио",
        "voice": "голосовое сообщение",
        "no_args": "<emoji document_id=5461117441612462242>🙂</emoji> <b>Тебе нужно указать текст инструкции!</b>",
        "success": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Инструкция успешно установлена!</b>",

        "config_api_key": "Ключи API Gemini (aistudio.google.com/apikey). Для каждого запроса будет выбиратся один на рандом.",
        "config_model_name": "Модель Gemini. {prefix}gmodels покажет доступные. Пример: gemini-1.5-pro-latest",
        "config_system_instruction": "Системная инструкция для Gemini, можно указать с помощью команды {prefix}gset если сталкиваетесь с лимитом!",
        "config_proxy": "Прокси: http://user:pass@host:port или socks5://user:pass@host:port (нужен если gemini не доступен для гео вашего сервера)",
    }

    strings_ua = {
        "no_keys": "<emoji document_id=5274099962655816924>❗️</emoji> <b>API ключ не вказано. Отримати його можна тут: aistudio.google.com/apikey (безкоштовно), потім вкажи його в конфігу (<code>{self.get_prefix()}cfg yg_gemini</code>)</b>",
        "api_error": "Помилка API Gemini: {error}",
        "unknown_error": "Сталася невідома помилка: {error}",
        "list_models_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не вдалося отримати список моделей:</b> {error}",
        "pagination_error": "[Помилка пагінації]",
        "media_dl_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не вдалося завантажити медіа ({media_type}):</b> {error}",
        "media_unsupported": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Тип медіа <code>{mime_type}</code> не підтримується модулем!</b>",
        "media_upload_error": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Не вдалося завантажити медіа ({media_type}) на сервер Google:</b> {error}",

        "loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит:</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думає...</b>",
        "loading_media_query": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит до медіа ({media_type}):</b> {prompt}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думає...</b>",
        "loading_media_only": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит щодо медіа ({media_type})...</b>\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думає...</b>",
        "regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит:</b> {prompt}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Регенерація відповіді...</b>",
        "regenerating_media_query": "💬 <b>Запит до медіа ({media_type}):</b> {prompt}\n\n🔄 <b>Регенерація відповіді...</b>",
        "regenerating_media_only": "💬 <b>Запит щодо медіа ({media_type})...</b>\n\n🔄 <b>Регенерація відповіді...</b>",
        "media_dl": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Завантаження медіа ({media_type})...</b>",
        "media_upload": "<b><emoji document_id=5447410659077661506>🌐</emoji> Завантаження медіа ({media_type}) на сервер Google...</b>",

        "resp_base": "💬 <b>Запит:</b> {prompt}\n\n✨ <b>Відповідь від Gemini:</b>",
        "resp_base_media": "💬 <b>Запит до медіа ({media_type}):</b> {prompt}\n\n✨ <b>Відповідь від Gemini:</b>",
        "resp_base_media_only": "✨ <b>Відповідь від Gemini (щодо медіа {media_type}):</b>",

        "gemini_no_prompt": "<emoji document_id=5274099962655816924>❗️</emoji> <i>Введіть запит або дайте відповідь на медіа!</i>",
        "gask_usage": "<emoji document_id=5334544901428229844>ℹ️</emoji> <b>Використання:</b> <code>{prefix}gask &lt;id_чату&gt; &lt;питання&gt;</code>",
        "models_title": "<b>✨ Доступні моделі Gemini:</b>\n\n",
        "model_entry": "🔹 <b>{name}</b>\n    ▫️ <i>{desc}</i>\n",
        "models_fetch": "<b><emoji document_id=5386367538735104399>⌛️</emoji> Отримання списку моделей...</b>",
        "models_not_found": "<emoji document_id=5416081784641168838>🟢</emoji> Не знайдено доступних моделей (дииивно)",

        "chat_create_ok": "<emoji document_id=5325547803936572038>✅</emoji> <b>Чат створено!</b>\n<b>ID:</b> <code>{chat_id}</code>\n<b>Ім'я:</b> {name}",
        "chat_not_found": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Чат з ID <code>{chat_id}</code> не знайдено</b>",
        "chat_no_chats": "😕 <b>У вас ще немає чатів Gemini. Використовуйте <code>{prefix}gcreate</code>!</b>",
        "chat_list_title": "💾 <b>Ваші чати Gemini:</b>",
        "chat_menu_title": "🔧 <b>Чат {chat_id} ({name}):</b>",
        "chat_menu_history": "📜 Історія",
        "chat_menu_delete": "🗑 Видалити",
        "chat_menu_back": "🔙 Назад",
        "chat_hist_title": "📜 <b>Історія чату {chat_id} ({name})</b> (Стор. {current_page}/{total_pages}):",
        "chat_hist_entry": "<b>{role}:</b> <blockquote expandable>{text}</blockquote>",
        "chat_hist_empty": "<i>Історія чату порожня!</i>",
        "chat_del_confirm": "❓ <b>Видалити чат {chat_id} ({name})? Це незворотно.</b>",
        "chat_del_yes": "✅ Так",
        "chat_del_no": "❌ Ні",
        "chat_del_ok": "✅ Чат {chat_id} видалено!",

        "gask_loading": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит у чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>⏳</emoji> <b>Gemini думає...</b>",
        "gask_resp_base": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит у чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=5325547803936572038>✨</emoji> <b>Відповідь від Gemini:</b>",
        "gask_regenerating": "<emoji document_id=5443038326535759644>💬</emoji> <b>Запит у чат <code>{chat_id}</code>:</b> {question}\n\n<emoji document_id=4988080790286894217>🔄</emoji> <b>Регенерація відповіді...</b>",

        "btn_regenerate": "🔄 Регенерувати",
        "btn_prev": "⬅️",
        "btn_next": "➡️",
        "btn_chat": "{name} ({chat_id})",

        "photo": "фото",
        "video": "відео",
        "audio": "аудіо",
        "voice": "голосове повідомлення",
        "no_args": "<emoji document_id=5461117441612462242>🙂</emoji> <b>Вам потрібно вказати текст інструкції!</b>",
        "success": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Інструкцію успішно встановлено!</b>",

        "config_api_key": "Ключі API Gemini (aistudio.google.com/apikey). Для кожного запиту буде вибиратися один навмання.",
        "config_model_name": "Модель Gemini. {prefix}gmodels покаже доступні. Приклад: gemini-1.5-pro-latest",
        "config_system_instruction": "Системна інструкція для Gemini. Можна вказати за допомогою команди {prefix}gset, якщо ви стикаєтеся з лімітом!",
        "config_proxy": "Проксі: http://user:pass@host:port або socks5://user:pass@host:port (потрібен, якщо Gemini недоступний для географічного розташування вашого сервера)",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                [],
                lambda: self.strings("config_api_key"),
                validator=loader.validators.Series(loader.validators.Hidden(loader.validators.String())),
            ),
            loader.ConfigValue(
                "model_name",
                "gemini-1.5-flash-latest",
                lambda: self.strings("config_model_name").format(prefix=self.get_prefix()),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "system_instruction",
                "",
                lambda: self.strings("config_system_instruction").format(prefix=self.get_prefix()),
                validator=loader.validators.String(),
            ),
             loader.ConfigValue(
                "proxy",
                "",
                lambda: self.strings("config_proxy"),
                validator=loader.validators.String(),
            )
        )

    def sanitise_text(self, text: str) -> str:
        return re.sub(r"</?emoji.*?>", "", text)

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        Utils.sanitise_text = self.sanitise_text
        self.safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

        proxy = self.config["proxy"]
        if proxy:
            os.environ["http_proxy"] = proxy
            os.environ["https_proxy"] = proxy
            os.environ["HTTP_PROXY"] = proxy
            os.environ["HTTPS_PROXY"] = proxy

    @loader.command(ru_doc="[имя] - создать чат Gemini с контекстом", ua_doc="[ім'я] — створити чат Gemini з контекстом")
    async def gcreate(self, msg: Message):
        """[name] - create a new Gemini chat session with context"""
        args = utils.get_args_raw(msg)
        chat_id = secrets.token_hex(3)
        chat_name = args.strip() if args else f"Chat-{chat_id[:4]}"

        chats = self._get_chats()
        while chat_id in chats:
            chat_id = secrets.token_hex(4)

        chats[chat_id] = {"history": [], "name": chat_name}
        self._save_chats(chats)

        await utils.answer(
            msg,
            self.strings("chat_create_ok").format(
                chat_id=chat_id,
                name=utils.escape_html(chat_name)
            )
        )

    @loader.command(ru_doc="<id_чата> <вопрос> - задать вопрос в чат Gemini", ua_doc="<id_чату> <питання> — поставити питання в чаті Gemini")
    async def gask(self, msg: Message):
        """<chat_id> <question> - ask a question in a Gemini chat session"""
        if not self.config["api_key"]:
            await utils.answer(msg, self.strings("no_keys").format(prefix=self.get_prefix()))
            return

        args = utils.get_args(msg)
        if len(args) < 2:
            await utils.answer(msg, self.strings("gask_usage").format(prefix=self.get_prefix()))
            return

        chat_id = args[0].lower()
        user_question = " ".join(args[1:]).strip()

        if not user_question:
            await utils.answer(msg, "<emoji document_id=5436113877181941026>❓</emoji> <b>What question?</b>")
            return

        await self._process_chat_request(msg, chat_id, user_question)

    @loader.command(ru_doc="<реплай на медиа / текст> — запрос к Gemini (фото/видео/аудио), без контекста", ua_doc="<реплай на медіа / текст> — запит до Gemini (фото/відео/аудіо), без контексту")
    async def geminicmd(self, message: Message):
        """<reply to media / text> — send stateless request to Gemini (photo/video/audio)"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings("no_keys").format(prefix=self.get_prefix()))
            return

        await self._process_stateless_request(message)

    @loader.command(ru_doc="показать/управлять чатами Gemini", ua_doc="показати/керувати чатами Gemini")
    async def gchats(self, message: Message):
        """show and manage Gemini chat sessions"""
        await self._display_chats_list(message)

    @loader.command(ru_doc="<текст> - установить инструкцию для Gemini", ua_doc="<текст> - встановити інструкцію для Gemini")
    async def gset(self, message: Message):
        "<text> - set instruction for Gemini"
        if not (args := utils.get_args_html(message)):
            return await utils.answer(message, self.strings("no_args"))

        self.config["system_instruction"] = args
        await utils.answer(message, self.strings("success"))

    @loader.command(ru_doc="показывает доступные модели Gemini", ua_doc="показує доступні моделі Gemini")
    async def gmodels(self, msg: Message):
        status = await utils.answer(msg, self.strings("models_fetch"))
        try:
            models = await utils.run_sync(genai.list_models)
            found = []
            for m in models:
                if any(x in m.supported_generation_methods for x in ['generateContent', 'startChat']) and 'embed' not in m.name.lower():
                    found.append({"name": m.name.replace('models/', ''), "desc": m.description})
            found.sort(key=lambda x: x["name"])
            if not found:
                out = self.strings("models_not_found")
            else:
                out = self.strings("models_title") + "".join(
                    self.strings("model_entry").format(
                        name=f"<code>{utils.escape_html(m['name'])}</code>",
                        desc=utils.escape_html(m['desc'])
                    ) for m in found
                )
            await utils.answer(status, out)
        except Exception as e:
            err = self.strings("list_models_error").format(error=utils.escape_html(str(e)))
            await utils.answer(status, err)

    async def _call_gemini_api(
        self,
        api_key: str,
        content: Optional[Union[str, List[Union[str, genai.types.File]]]] = None,
        chat_mode: bool = False,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        if not api_key:
            raise ValueError("API Key is required!")

        try:
            genai.configure(api_key=api_key)

            system_instruction = self.config["system_instruction"] if self.config["system_instruction"] else None
            model = genai.GenerativeModel(model_name=self.config["model_name"],
                                          system_instruction=system_instruction,
                                          safety_settings=self.safety_settings)

            if chat_mode:
                if history is None: raise ValueError("Chat mode requires history")
                chat = model.start_chat(history=history)
                last_prompt_content = history[-1]['parts']
                response = await chat.send_message_async(
                                     last_prompt_content,
                        safety_settings=self.safety_settings)
            else:
                if content is None: raise ValueError("Stateless mode requires content")
                if isinstance(content, str): content = [content]
                response = await model.generate_content_async(content, 
                                safety_settings=self.safety_settings)

            if not response.parts: return f"⚠️ The answer is blocked by Gemini or empty"
            return response.text.strip()

        except Exception as e:
            err_info = getattr(e, 'message', str(e))
            raise RuntimeError(f"{err_info}") from e

    async def _regenerate_stateless_callback(
        self,
        call: InlineCall,
        prompt_text: str,
        file_name: Optional[str],
        media_type: Optional[str],
        user_prompt: str,
        key: str,
    ):
        if not key:
            await call.answer(self.strings("unknown_error").format(error="Missing API key"), show_alert=True)
            return

        escaped = utils.escape_html(user_prompt)
        loading = ""
        args = {}
        if user_prompt:
            loading = "regenerating_media_query" if media_type else "regenerating"
            args = {"prompt": escaped, "media_type": media_type}
        elif media_type:
            loading = "regenerating_media_only"
            args = {"media_type": media_type}

        text = self.strings(loading).format(**args) if loading else "🔄 Regeneration..."
        await call.edit(text=text)

        try:
            content = []
            if file_name:
                try:
                    genai.configure(api_key=key)
                    file = await utils.run_sync(genai.get_file, name=file_name)
                    content.append(file)
                except Exception as e:
                    await call.answer(f"⚠️ Media not found ({file_name}). Text only.", show_alert=False)
                    media_type = file_name = None

            if prompt_text:
                content.append(prompt_text)

            if not content:
                await call.edit(text=self.strings("unknown_error").format(error="No content"), reply_markup=None)
                return

            raw = await self._call_gemini_api(key, content=content, chat_mode=False)
            html = self.markdown2html(raw)
            response = self.make_expandable(html)

            base = ""
            if user_prompt:
                base = self.strings("resp_base_media").format(media_type=media_type, prompt=escaped) if media_type else self.strings("resp_base").format(prompt=escaped)
            elif media_type:
                base = self.strings("resp_base_media_only").format(media_type=media_type)

            final = f"{base}\n{response}"
            args = (prompt_text, file_name, media_type, user_prompt, key)

            if len(final.encode()) > 3996:
                pages = await utils.run_sync(self._get_pages, response)
                if pages:
                    await self._paginate_response_callback(
                        call=call,
                        message=None,
                        pages=pages,
                        current_page_index=0,
                        constructed_base_text=base,
                        regenerate_callback=self._regenerate_stateless_callback,
                        regenerate_args=args,
                    )
                else:
                    btns = [[{"text": self.strings("btn_regenerate"), "callback": self._regenerate_stateless_callback, "args": args}]]
                    await call.edit(text=f"{base}\n{self.strings('pagination_error')}", reply_markup=btns)
            else:
                btns = [[{"text": self.strings("btn_regenerate"), "callback": self._regenerate_stateless_callback, "args": args}]]
                await call.edit(text=final, reply_markup=btns)

        except (RuntimeError, ValueError) as e:
            await call.edit(text=self.strings("api_error").format(error=utils.escape_html(str(e))), reply_markup=None)
        except Exception as e:
            await call.edit(text=self.strings("unknown_error").format(error=utils.escape_html(str(e))), reply_markup=None)

    def _get_chats(self) -> Dict[str, Dict[str, Any]]:
        chats = self.db.get("yg_gemini", "chats", {})
        return chats if isinstance(chats, dict) else {}

    def _save_chats(self, chats: Dict[str, Dict[str, Any]]):
        self.db.set("yg_gemini", "chats", chats)

    async def _process_chat_request(self, msg: Message, chat_id: str, question: str):
        chats = self._get_chats()
        if chat_id not in chats:
            await utils.answer(msg, self.strings("chat_not_found").format(chat_id=chat_id))
            return

        chat = chats[chat_id]
        hist = chat.get("history")
        if not isinstance(hist, list):
            logger.warning(f"Invalid history for {chat_id}, resetting.")
            hist = []
            chat["history"] = hist

        quote = self._format_quote(msg)
        final_q = f"{quote}\n\n{question}" if quote else question
        hist.append({"role": "user", "parts": [final_q]})

        status = await utils.answer(
            msg,
            self.strings("gask_loading").format(
                chat_id=chat_id,
                question=utils.escape_html(question)
            )
        )
        if not isinstance(status, Message):
            if hist and hist[-1]["role"] == "user":
                hist.pop()
            await self.client.send_message(msg.chat_id, self.strings("unknown_error").format(error="No status message"))
            return

        key = self._get_api_key()
        if not key:
            if hist and hist[-1]["role"] == "user":
                hist.pop()
            await utils.answer(status, self.strings("no_keys").format(prefix=self.get_prefix()))
            return

        await self._generate_and_display_chat(
            msg=status,
            key=key,
            chat_id=chat_id,
            last_question=question
        )

    async def _generate_and_display_chat(self, msg: Message, key: str, chat_id: str, last_question: str):
        chats = self._get_chats()
        if chat_id not in chats or not isinstance(chats[chat_id].get("history"), list):
            await utils.answer(msg, self.strings("chat_not_found").format(chat_id=chat_id))
            return

        hist = chats[chat_id]["history"]

        try:
            raw = await self._call_gemini_api(key, history=hist, chat_mode=True)
            hist.append({"role": "model", "parts": [raw]})
            chats[chat_id]["history"] = hist
            self._save_chats(chats)

            html = self.markdown2html(raw)
            final = self.make_expandable(html)

            base = self.strings("gask_resp_base").format(
                chat_id=chat_id, question=utils.escape_html(last_question))
            text = f"{base}\n{final}"
            regen_args = (chat_id, last_question)

            if len(text.encode("utf-8")) > 3996:
                pages = await utils.run_sync(self._get_pages, final)
                if pages:
                    await self._paginate_response_callback(
                        call=None, message=msg, pages=pages, current_page_index=0,
                        constructed_base_text=base,
                        regenerate_callback=self._regenerate_chat_callback,
                        regenerate_args=regen_args,
                    )
                else:
                    buttons = [[{"text": self.strings("btn_regenerate"),
                                "callback": self._regenerate_chat_callback,
                                "args": regen_args}]]
                    await self.inline.form(
                        message=msg, text=f"{base}\n{self.strings('pagination_error')}",
                        reply_markup=buttons, silent=True,
                    )
            else:
                buttons = [[{"text": self.strings("btn_regenerate"),
                            "callback": self._regenerate_chat_callback,
                            "args": regen_args}]]
                await self.inline.form(message=msg, text=text, reply_markup=buttons, silent=True)

        except (RuntimeError, ValueError) as e:
            if hist and hist[-1].get("role") == "user":
                hist.pop()
                chats[chat_id]["history"] = hist
                self._save_chats(chats)
                logger.info(f"Removed last user msg from {chat_id} after API error")
            err = self.strings("api_error").format(error=utils.escape_html(str(e)))
            await utils.answer(msg, err)

        except Exception as e:
            if hist and hist[-1].get("role") == "user":
                hist.pop()
                chats[chat_id]["history"] = hist
                self._save_chats(chats)
                logger.info(f"Removed last user msg from {chat_id} after unexpected error")
            err = self.strings("unknown_error").format(error=utils.escape_html(str(e)))
            await utils.answer(msg, err)

    async def _regenerate_chat_callback(self, call: InlineCall, chat_id: str, last_question_display: str):
        api_key = self._get_api_key()
        if not api_key:
            await call.answer(self.strings("no_keys").format(prefix=self.get_prefix()), show_alert=True)
            return

        chats = self._get_chats()
        if chat_id not in chats or not isinstance(chats[chat_id].get("history"), list):
            await call.answer(self.strings("chat_not_found").format(chat_id=chat_id), show_alert=True)
            return

        history = chats[chat_id]["history"]
        regen_text = self.strings("gask_regenerating").format(chat_id=chat_id, question=utils.escape_html(last_question_display))
        if not await call.edit(text=regen_text, reply_markup=None):
            return

        try:
            if history and history[-1].get("role") == "model":
                history.pop()
            elif not history or history[-1].get("role") != "user":
                await call.edit(text=self.strings("unknown_error").format(error="Corrupted history"), reply_markup=None)
                return

            new_resp = await self._call_gemini_api(api_key, history=history, chat_mode=True)
            history.append({'role': 'model', 'parts': [new_resp]})
            chats[chat_id]["history"] = history
            self._save_chats(chats)

            html = self.markdown2html(new_resp)
            part = self.make_expandable(html)
            q = utils.escape_html(last_question_display)
            base = self.strings("gask_resp_base").format(chat_id=chat_id, question=q)
            text = f"{base}\n{part}"
            args = (chat_id, last_question_display)

            if len(text.encode()) > 3996:
                pages = await utils.run_sync(self._get_pages, part)
                if pages:
                    await self._paginate_response_callback(
                        call=call, message=None, pages=pages, current_page_index=0,
                        constructed_base_text=base,
                        regenerate_callback=self._regenerate_chat_callback,
                        regenerate_args=args,
                    )
                else:
                    btns = [[{"text": self.strings("btn_regenerate"), "callback": self._regenerate_chat_callback, "args": args}]]
                    await call.edit(text=f"{base}\n{self.strings('pagination_error')}", reply_markup=btns)
            else:
                btns = [[{"text": self.strings("btn_regenerate"), "callback": self._regenerate_chat_callback, "args": args}]]
                await call.edit(text=text, reply_markup=btns)

        except (RuntimeError, ValueError) as e:
            err = self.strings("api_error").format(error=utils.escape_html(str(e)))
            await call.edit(text=err, reply_markup=None)
        except Exception as e:
            err = self.strings("unknown_error").format(error=utils.escape_html(str(e)))
            await call.edit(text=err, reply_markup=None)

    async def _process_stateless_request(self, msg: Message):
        args = utils.get_args_raw(msg)
        prompt = args.strip() if args else ""
        quote = self._format_quote(msg)
        full_prompt = f"{quote}\n\n{prompt}" if prompt else quote

        reply = await msg.get_reply_message()
        parts, uploaded, mime, mtype, api_key = [], None, None, None, None
        status = msg
        loading_key = None

        if reply and reply.media:
            try:
                media_info = self._get_media_info(reply)
                if media_info:
                    dl_func, mime, mtype = media_info
                    uploaded, api_key = await self._upload_media(status, dl_func, mime, mtype)
                    if uploaded:
                        parts.append(uploaded)
                    else:
                        return
                else:
                    mime_display = (getattr(reply.media.document, 'mime_type', "N/A")
                                    if hasattr(reply.media, 'document') else
                                    "image/jpeg" if reply.photo else "N/A")
                    await utils.answer(status, self.strings("media_unsupported").format(
                        mime_type=utils.escape_html(mime_display)))
                    return
            except Exception as e:
                await utils.answer(status, self.strings("media_dl_error").format(
                    media_type=mtype or "media",
                    error=utils.escape_html(str(e))
                ))
                return

        if full_prompt:
            parts.append(full_prompt)
        elif not parts:
            await utils.answer(msg, self.strings("gemini_no_prompt"))
            return

        api_key = api_key or self._get_api_key()
        if not api_key:
            await utils.answer(status, self.strings("no_keys").format(prefix=self.get_prefix()))
            return

        escaped = utils.escape_html(prompt)
        if prompt:
            loading_key = "loading_media_query" if mtype else "loading"
        elif mtype:
            loading_key = "loading_media_only"

        if loading_key:
            args = {"prompt": escaped, "media_type": mtype} if prompt else {"media_type": mtype}
            await utils.answer(status, self.strings(loading_key).format(**args))

        await self._generate_and_display_stateless(
            status_msg=status,
            api_key=api_key,
            content_parts=parts,
            user_prompt_display=prompt,
            uploaded_file=uploaded,
            media_type_str=mtype
        )

    async def _generate_and_display_stateless(
        self,
        status_msg: Message,
        api_key: str,
        content_parts: list,
        user_prompt_display: str,
        uploaded_file: Optional[genai.types.File],
        media_type_str: Optional[str],
    ):
        try:
            raw = await self._call_gemini_api(api_key, content=content_parts, chat_mode=False)
            html = self.markdown2html(raw)
            response = self.make_expandable(html)

            escaped = utils.escape_html(user_prompt_display)
            base = ""
            if user_prompt_display:
                base = self.strings("resp_base_media").format(
                    media_type=media_type_str, prompt=escaped
                ) if media_type_str else self.strings("resp_base").format(prompt=escaped)
            elif media_type_str:
                base = self.strings("resp_base_media_only").format(media_type=media_type_str)

            final = f"{base}\n{response}"

            uploaded_name = uploaded_file.name if uploaded_file else None
            prompt_text = content_parts[-1] if content_parts and isinstance(content_parts[-1], str) else ""
            regen_args = (prompt_text, uploaded_name, media_type_str, user_prompt_display, api_key)

            if len(final.encode('utf-8')) > 3996:
                pages = await utils.run_sync(self._get_pages, html)
                if pages:
                    await self._paginate_response_callback(
                        call=None,
                        message=status_msg,
                        pages=pages,
                        current_page_index=0,
                        constructed_base_text=base,
                        regenerate_callback=self._regenerate_stateless_callback,
                        regenerate_args=regen_args
                    )
                else:
                    buttons = [[{
                        "text": self.strings("btn_regenerate"),
                        "callback": self._regenerate_stateless_callback,
                        "args": regen_args,
                    }]]
                    await self.inline.form(
                        message=status_msg,
                        text=f"{base}\n{self.strings('pagination_error')}",
                        reply_markup=buttons,
                        silent=True,
                    )
            else:
                buttons = [[{
                    "text": self.strings("btn_regenerate"),
                    "callback": self._regenerate_stateless_callback,
                    "args": regen_args,
                }]]
                await self.inline.form(
                    message=status_msg,
                    text=final,
                    reply_markup=buttons,
                    silent=True,
                )

        except (RuntimeError, ValueError) as e:
            err = self.strings("api_error").format(error=utils.escape_html(str(e)))
            await utils.answer(status_msg, err)
        except Exception as e:
            err = self.strings("unknown_error").format(error=utils.escape_html(str(e)))
            await utils.answer(status_msg, err)

    def _get_pages(self, html_text: str) -> List[str]:
        text_content, entities = html.parse(html_text)
        parts = split_text(text_content, entities, limit=3000)
        pages = [html.unparse(part_text, part_entities) for part_text, part_entities in parts]
        pages = [p.replace("<blockquote>", "<blockquote expandable>") for p in pages] #love telethonn👹
        return pages

    async def _paginate_response_callback(
        self,
        call: Optional[InlineCall],
        message: Optional[Message],
        pages: List[str],
        current_page_index: int,
        constructed_base_text: str,
        regenerate_callback: callable,
        regenerate_args: tuple,
    ):
        total = len(pages)
        idx = max(0, min(total - 1, current_page_index))

        page = pages[idx]
        text = f"{constructed_base_text}\n{page}"

        buttons = []
        nav = []
        if idx > 0:
            nav.append({
                "text": self.strings("btn_prev"),
                "callback": self._paginate_response_callback,
                "args": (None, pages, idx - 1, constructed_base_text, regenerate_callback, regenerate_args),
            })
        if idx < total - 1:
            nav.append({
                "text": self.strings("btn_next"),
                "callback": self._paginate_response_callback,
                "args": (None, pages, idx + 1, constructed_base_text, regenerate_callback, regenerate_args),
            })
        if nav: buttons.append(nav)
        buttons.append([{
            "text": self.strings("btn_regenerate"),
            "callback": regenerate_callback,
            "args": regenerate_args,
        }])

        if call:
            await call.edit(text=text, reply_markup=buttons)
        elif message:
            await self.inline.form(
                message=message,
                text=text,
                reply_markup=buttons,
                silent=True
            )
        else:
            logger.error("Pagination callback received neither call nor message")

    async def _display_chats_list(self, target: Union[Message, InlineCall]):
        chats = self._get_chats()
        is_call = isinstance(target, InlineCall)

        if not chats:
            text = self.strings("chat_no_chats").format(prefix=self.get_prefix())
            if is_call:
                await target.edit(text=text, reply_markup=None)
            else:
                await utils.answer(target, text)
            return

        text = self.strings("chat_list_title")
        buttons = []
        sorted_ids = sorted(chats.keys(), key=lambda k: chats[k].get("name", "").lower())
        for chat_id in sorted_ids:
             chat = chats[chat_id]
             name = chat.get("name", f"Chat-{chat_id[:4]}")
             buttons.append([{
                 "text": self.strings("btn_chat").format(name=utils.escape_html(name), chat_id=chat_id),
                 "callback": self._chat_manage_menu, "args": (chat_id,),
             }])

        if is_call:
            await target.edit(text=text, reply_markup=buttons)
        else:
            await self.inline.form(message=target, text=text, reply_markup=buttons, silent=True)

    async def _chat_manage_menu(self, call: InlineCall, chat_id: str):
        chats = self._get_chats()
        if chat_id not in chats:
            await call.answer(self.strings("chat_not_found").format(chat_id=chat_id), show_alert=True)
            await self._display_chats_list(call)
            return

        name = chats[chat_id].get("name", f"Chat-{chat_id[:4]}")
        buttons = [
            [{"text": self.strings("chat_menu_history"), "callback": self._chat_view_history, "args": (chat_id, 0)}],
            [{"text": self.strings("chat_menu_delete"), "callback": self._chat_delete_confirm, "args": (chat_id,)}],
            [{"text": self.strings("chat_menu_back"), "callback": self._display_chats_list}],
        ]
        text = self.strings("chat_menu_title").format(chat_id=chat_id, name=utils.escape_html(name))
        await call.edit(text=text, reply_markup=buttons)

    async def _chat_view_history(self, call: InlineCall, chat_id: str, page_index: int):
        chats = self._get_chats()
        if chat_id not in chats or not isinstance(chats[chat_id].get("history"), list):
            await call.answer(self.strings("chat_not_found").format(chat_id=chat_id), show_alert=True)
            await self._display_chats_list(call)
            return

        chat = chats[chat_id]
        name = chat.get("name", f"Chat-{chat_id[:4]}")
        history = chat.get("history", [])

        if not history:
            btns = [[{"text": self.strings("chat_menu_back"), "callback": self._chat_manage_menu, "args": (chat_id,)}]]
            await call.edit(text=self.strings("chat_hist_empty"), reply_markup=btns)
            return

        entries = []
        for e in history:
            role = "👤 User" if e.get("role") == "user" else "✨ Gemini"
            parts = e.get("parts", [])
            if not isinstance(parts, list): parts = [str(parts)]
            text = utils.escape_html(" ".join(str(p) for p in parts)).strip() or "[empty]"
            entries.append(self.strings("chat_hist_entry").format(role=role, text=text))

        html = "\n\n".join(entries)
        pages = await utils.run_sync(self._get_pages, html)
        total = len(pages)
        idx = max(0, min(total - 1, page_index))

        if not pages:
            err = self.strings("chat_hist_empty")
            if history: err += f"\n{self.strings('pagination_error')}"
            btns = [[{"text": self.strings("chat_menu_back"), "callback": self._chat_manage_menu, "args": (chat_id)}]]
            await call.edit(text=err, reply_markup=btns)
            return

        page = pages[idx]
        title = self.strings("chat_hist_title").format(
            chat_id=chat_id, name=utils.escape_html(name),
            current_page=idx + 1, total_pages=total
        )
        text = f"{title}\n\n{page}"

        nav = []
        if idx > 0: nav.append({"text": self.strings("btn_prev"), "callback": self._chat_view_history, "args": (chat_id, idx - 1)})
        if idx < total - 1: nav.append({"text": self.strings("btn_next"), "callback": self._chat_view_history, "args": (chat_id, idx + 1)})

        btns = []
        if nav: btns.append(nav)
        btns.append([{"text": self.strings("chat_menu_back"), "callback": self._chat_manage_menu, "args": (chat_id)}])

        await call.edit(text=text, reply_markup=btns)

    async def _chat_delete_confirm(self, call: InlineCall, chat_id: str):
        chats = self._get_chats()
        if chat_id not in chats:
            await call.answer(self.strings("chat_not_found").format(chat_id=chat_id), show_alert=True)
            await self._display_chats_list(call)
            return

        name = chats[chat_id].get("name", f"Chat-{chat_id[:4]}")
        buttons = [[
            {"text": self.strings("chat_del_yes"), "callback": self._chat_delete_execute, "args": (chat_id,)},
            {"text": self.strings("chat_del_no"), "callback": self._chat_manage_menu, "args": (chat_id,)}, # Back to chat menu
        ]]
        text = self.strings("chat_del_confirm").format(chat_id=chat_id, name=utils.escape_html(name))
        await call.edit(text=text, reply_markup=buttons)

    async def _chat_delete_execute(self, call: InlineCall, chat_id: str):
        chats = self._get_chats()
        if chat_id in chats:
            del chats[chat_id]
            self._save_chats(chats)
            await call.answer(self.strings("chat_del_ok").format(chat_id=chat_id), show_alert=True)
            await self._display_chats_list(call)
        else:
            await call.answer(self.strings("chat_not_found").format(chat_id=chat_id), show_alert=True)
            await self._display_chats_list(call)

    async def _upload_media(
        self,
        status_msg: Message,
        dl_func: callable,
        mime_type: str,
        media_type_str: str
    ) -> Tuple[Optional[genai.types.File], Optional[str]]:
        api_key = self._get_api_key()
        if not api_key:
            await utils.answer(status_msg, self.strings("no_keys").format(prefix=self.get_prefix()))
            return None, None

        uploaded_file = None
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{mime_type.split('/')[-1]}") as temp_file:
                temp_file_path = temp_file.name

            await utils.answer(status_msg, self.strings("media_dl").format(media_type=media_type_str))
            await dl_func(temp_file_path)

            await utils.answer(status_msg, self.strings("media_upload").format(media_type=media_type_str))

            genai.configure(api_key=api_key)
            uploaded_file = await utils.run_sync(
                genai.upload_file,
                path=temp_file_path,
                display_name=f"hikka_{media_type_str}_{secrets.token_hex(3)}",
                mime_type=mime_type
            )

            await self._wait_for_file_active(uploaded_file, api_key)

        except Exception as e:
            err_key = "media_upload_error" if 'upload' in str(e).lower() or 'state' in str(e).lower() else "media_dl_error"
            await utils.answer(status_msg, self.strings(err_key).format(media_type=media_type_str, error=utils.escape_html(str(e))))
            uploaded_file = None
            api_key = None

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as e_rm:
                    logger.error(f"Failed to remove temp file {temp_file_path}: {e_rm}")

        return uploaded_file, api_key

    def _get_api_key(self) -> Optional[str]:
        keys = self.config["api_key"]
        return random.choice(keys) if keys else None

    @staticmethod
    def markdown2html(text: str) -> str:
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
        text = re.sub(r"```(?:\w*\n)?(.*?)```", r"<code>\1</code>", text, flags=re.DOTALL)
        text = re.sub(r"``(.*?)``", r"<code>\1</code>", text)
        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"^\s*[\*\-]\s+(.*)", r"• \1", text, flags=re.MULTILINE)
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)

        allowed_tags = ['b', 'strong', 'i', 'em',
        'u', 'ins', 's', 'strike', 'del', 'span', 'tg-spoiler',
        'a', 'code','pre', 'blockquote']

        def filter_tags(match):
            tag = match.group(1).lower()
            attrs = match.group(2) or ''
            if tag.strip('/').split()[0] in allowed_tags:
                if 'span' in tag and 'tg-spoiler' not in attrs: return ''
                if 'code' in tag and 'language-' in attrs: return f"<{tag}{attrs}>"
                elif tag.startswith('/'): return f"<{tag}>"
                elif any(attr in attrs for attr in ['href=', 'class=', 'emoji-id=']): return f"<{tag}{attrs}>"
                else: return f"<{tag}>"
            return ''

        text = re.sub(r"<(/?\w+)([^>]*)>", filter_tags, text)

        return text

    def make_expandable(self, html_content: str) -> str:
        if len(html_content) > 500:
             return f"<blockquote expandable>{html_content}</blockquote>"
        return html_content
    
    def _format_quote(self, message: Message) -> str:
        if message.reply_to and message.reply_to.quote_text:
            quote = f'"{message.reply_to.quote_text}"'
            return quote
        else:
            return None

    def _get_media_info(self, message: Message) -> Optional[Tuple[callable, str, str]]:
        if not message or not message.media:
            return None

        doc = getattr(message.media, 'document', None)
        if doc and getattr(doc, 'mime_type', None):
            mt = doc.mime_type
            if mt in ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]:
                t = self.strings("photo")
            elif mt in ["video/mp4", "video/mpeg", "video/mov", "video/avi", "video/x-flv", "video/mpg", "video/webm", "video/wmv", "video/3gpp"]:
                t = self.strings("video")
            elif mt in ["audio/wav", "audio/mp3", "audio/aiff", "audio/aac", "audio/ogg", "audio/flac"]:
                t = self.strings("audio")
            else:
                t = None
            if t:
                return lambda f: self.client.download_media(doc, file=f), mt, t

        photo = getattr(message.media, 'photo', None)
        if photo:
            return lambda f: self.client.download_media(photo, file=f), "image/jpeg", self.strings("photo")

        for attr, types, label in [
            ('video', ["video/mp4", "video/mpeg", "video/mov", "video/avi", "video/x-flv", "video/mpg", "video/webm", "video/wmv", "video/3gpp"], self.strings("video")),
            ('voice', ["audio/wav", "audio/mp3", "audio/aiff", "audio/aac", "audio/ogg", "audio/flac"], self.strings("voice")),
            ('audio', ["audio/wav", "audio/mp3", "audio/aiff", "audio/aac", "audio/ogg", "audio/flac"], self.strings("audio")),
        ]:
            media = getattr(message.media, attr, None)
            if media:
                mt = getattr(media, 'mime_type', None)
                if mt and mt in types:
                    return lambda f, m=media: self.client.download_media(m, file=f), mt, label
                if attr == 'video':
                    return lambda f, m=media: self.client.download_media(m, file=f), 'video/mp4', self.strings("video")
                if attr == 'voice':
                    return lambda f, m=media: self.client.download_media(m, file=f), 'audio/ogg', self.strings("voice")
                if attr == 'audio':
                    return lambda f, m=media: self.client.download_media(m, file=f), 'audio/mpeg', self.strings("audio")

        return None

    async def _wait_for_file_active(self, file_object: genai.types.File, api_key: str):
        genai.configure(api_key=api_key)
        while True:
            try:
                updated = await utils.run_sync(genai.get_file, name=file_object.name)
                if updated.state.name == "ACTIVE":
                    return True
                elif updated.state.name == "FAILED":
                    raise RuntimeError(f"File {file_object.name} processing failed on Google's side.")
                await asyncio.sleep(0.4)
            except Exception as e:
                 raise RuntimeError(f"Error checking file {file_object.name} status: {e}")