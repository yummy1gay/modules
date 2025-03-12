__version__ = (1, 5, 0, 0)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# requires: google-generativeai urlextract cloudscraper

# changelog:
# - Добавлен подбор паролей с использованием Google Gemini.
# - Реализована активация тестнет чеков.
# - Добавлена возможность задать задержку перед активацией чека.
# - Добавлены переводы.
# - Внесены мелкие исправления и оптимизации кода.

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
import re
from telethon import events
from collections import defaultdict
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl, MessageMediaWebPage
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from google.generativeai import GenerativeModel, configure
from telethon.tl.types import Message
from telethon import TelegramClient
from urlextract import URLExtract
from urllib.parse import unquote
import cloudscraper
import asyncio
import random
import json

from .. import loader, utils

class Passworder: #beto
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.safety_settings={HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                              HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                              HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                              HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}

        self.prompt = """
        Твоя задача – извлекать пароли из текстовых описаний. В некоторых случаях пароль может быть прямо указан в тексте, в других случаях его нужно вычислить или извлечь. 

        Учитывай следующие правила:

        1. Явный пароль (с синонимами): Распознаешь и извлекаешь пароль, указанный явно, используя ключевые слова и их синонимы: "пароль", "pass", "password", "код", "code", "ключ", "key", и т.д. Регистр букв подбирай на основе самого описания. Пример: "Password: wkek" -> {"password": "wkek"}, "Код доступа: 1234" -> {"password": "1234"}.

        2. Игнорирование рекламы и ссылок: Если в тексте присутствуют рекламные ссылки (например, "https://t.me/+wI2h84RF80NiZTI6") или другие ненужные ссылки, их нужно игнорировать, и вернуть пустой пароль. Пример: {"password": ""}.

        3. Игнорирование призывов к действиям: Если текст содержит фразы типа "пароль на 60 реакций" или "сделай 10 шагов и получи пароль", игнорируй такие тексты и возвращай пустой пароль. Пример: {"password": ""}.

        5. Математические примеры: Если в тексте содержится математический пример, например, "пароль: 2+6", вам нужно вычислить результат и вернуть его в формате: {"password": "8"}.

        6. Нецензурная лексика: Наличие нецензурной лексики не влияет на процесс. Ты фокусируешься на извлечении пароля, любые оскорбления или непристойные выражения приветствуются.

        7. Загадки и логические задачи: Если текст включает загадки или другие логические задачи, ты должен решить их и вернуть правильный ответ. Например, если описание будет "Пароль: сколько будет 3*4?", ответ будет {"password": "12"}. Так же учитывай момент что описание может состоять только из загадки/примера, это тоже наводка на пароль. Например, если описание будет "висит груша нельзя скушать", ответ будет {"password": "лампочка"}

        Пример: Если описание "Пароль - 3*3", то твой ответ должен быть {"password": "9"}.

        Если в тексте нет явных подсказок или пароля, возвращай пустой пароль: {"password": ""}. Для абзацев используй \\n!

        Пример текста с описанием пароля:
        "Пароль на 50 реакций в чате."
        Ответ: {"password": ""}

        Пример текста с математическим примером:
        "пасс - 12+8"
        Ответ: {"password": "20"}

        Пример загадки с кодом:
        "a = [1, 2, 3]
        b = a
        b[0] = 4
        print(a)
        Что выведет этот код?"

        Ответ: {"password": "[4, 2, 3]"}
        """ #you can edit this prompt!

    async def generate(self, description: str) -> dict:
        try:
            configure(api_key=self.api_key)
            model_name = self.model_name if self.model_name else "gemini-2.0-flash-exp"
            self.model = GenerativeModel(
                model_name,
                system_instruction=self.prompt,
                safety_settings=self.safety_settings
            )

            res = await self.model.generate_content_async(description)
            if res and res.text:
                try:
                    return json.loads(res.text.strip())
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON response", "raw": res.text.strip()}

            return {"password": ""}
        except Exception as e:
            if "429" in str(e):
                return {"error": "апи кей сдох"}
            return {"error": str(e)}

@loader.tds
class yg_checks(loader.Module):
    """Активатор чеков @send (@CryptoBot)"""

    strings = {
        "name": "yg_checks",
        "language": "en",
        "activator": "{} <b>Activator {}</b>",
        "log_sending": "{} <b>Log sending {}</b>",
        "password_cracking": "{} <b>Password cracking with neural network {}</b>",
        "private_check_activation": "{} <b>Activation of checks sent in private messages {}</b>",
        "auto_subscription": "{} <b>Auto-subscription {}</b>",
        "auto_unsubscription": "{} <b>Auto-unsubscription {}</b>",
        "testnet": "{} <b>Testnet check activation {}</b>",
        "logs_username_desc": "@username where logs will be sent",
        "logs_enabled_desc": "send logs",
        "delay_desc": "delay in seconds before activating the check",
        "track_private_desc": "activate checks sent in private messages",
        "ai_passwords_desc": "password cracking using Gemini AI",
        "watcher_on_desc": "activator status",
        "subscribe_desc": "subscribe to channels to activate checks that require it",
        "unsubscribe_desc": "unsubscribe from channels after activating the check",
        "no_track_users_desc": "whose checks not to activate (specify the user without @)",
        "testnet_desc": "activate checks sent using @CryptoTestnetBot",
        "gemini_api_key_desc": "API key for Gemini AI (aistudio.google.com/apikey)",
        "gemini_model_name_desc": "model for Gemini AI. examples: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash-exp, gemini-2.0-flash-thinking-exp-1219",
        "proxy_desc": "proxy in the format http://<user>:<pass>@<proxy>:<port>, or http://<proxy>:<port>",
    }

    strings_ru = {
        "name": "yg_checks",
        "language": "ru",
        "activator": "{} <b>Активатор {}</b>",
        "log_sending": "{} <b>Отправка логов {}</b>",
        "password_cracking": "{} <b>Подбор паролей с помощью нейросети {}</b>",
        "private_check_activation": "{} <b>Активация чеков отправленных в личке {}</b>",
        "auto_subscription": "{} <b>Авто-подписка {}</b>",
        "auto_unsubscription": "{} <b>Авто-отписка {}</b>",
        "testnet": "{} <b>Активация тестнет чеков {}</b>",
        "logs_username_desc": "@username куда будут отправляться логи",
        "logs_enabled_desc": "отправка логов",
        "delay_desc": "задержка в секундах перед активацией чека",
        "track_private_desc": "активация чеков отправленных в личке",
        "ai_passwords_desc": "подбор паролей с помощью Gemini AI",
        "watcher_on_desc": "состояние активатора",
        "subscribe_desc": "подписываться ли на каналы чтобы активировать чеки которые этого требуют",
        "unsubscribe_desc": "отписываться ли от каналов после активации чека",
        "no_track_users_desc": "чьи чеки не активировать (юзер указывать обязательно без @)",
        "testnet_desc": "активировать ли чеки отправленные с помощью @CryptoTestnetBot",
        "gemini_api_key_desc": "API ключ для Gemini AI (aistudio.google.com/apikey)",
        "gemini_model_name_desc": "модель для Gemini AI. примеры: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash-exp, gemini-2.0-flash-thinking-exp-1219",
        "proxy_desc": "прокси в формате http://<user>:<pass>@<proxy>:<port>, или http://<proxy>:<port>",
    }

    strings_ua = {
        "name": "yg_checks",
        "language": "ua",
        "activator": "{} <b>Активатор {}</b>",
        "log_sending": "{} <b>Відправка логів {}</b>",
        "password_cracking": "{} <b>Підбір паролей за допомогою нейромережі {}</b>",
        "private_check_activation": "{} <b>Активація чеків, надісланих в особисті повідомлення {}</b>",
        "auto_subscription": "{} <b>Авто-підписка {}</b>",
        "auto_unsubscription": "{} <b>Авто-відписка {}</b>",
        "testnet": "{} <b>Активація тестет чеків {}</b>",
        "logs_username_desc": "@username, куди будуть надсилатися логи",
        "logs_enabled_desc": "надсилання логів",
        "delay_desc": "затримка в секундах перед активацією чека",
        "track_private_desc": "активація чеків, надісланих в особисті повідомлення",
        "ai_passwords_desc": "підбір паролів за допомогою Gemini AI",
        "watcher_on_desc": "стан активатора",
        "subscribe_desc": "підписуватися на канали, щоб активувати чеки, які цього потребують",
        "unsubscribe_desc": "відписуватися від каналів після активації чека",
        "no_track_users_desc": "чиї чеки не активувати (користувача вказувати обов'язково без @)",
        "testnet_desc": "активувати чеки, надіслані за допомогою @CryptoTestnetBot",
        "gemini_api_key_desc": "API ключ для Gemini AI (aistudio.google.com/apikey)",
        "gemini_model_name_desc": "модель для Gemini AI. приклади: gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash-exp, gemini-2.0-flash-thinking-exp-1219",
        "proxy_desc": "проксі у форматі http://<user>:<pass>@<proxy>:<port>, або http://<proxy>:<port>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "logs_username",
                "",
                doc=lambda: self.strings("logs_username_desc"),
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "logs_enabled",
                True,
                doc=lambda: self.strings("logs_enabled_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "delay",
                0,
                doc=lambda: self.strings("delay_desc"),
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "track_private",
                True,
                doc=lambda: self.strings("track_private_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "ai_passwords",
                False,
                doc=lambda: self.strings("ai_passwords_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "watcher_on",
                True,
                doc=lambda: self.strings("watcher_on_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "subscribe",
                True,
                doc=lambda: self.strings("subscribe_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "unsubscribe",
                True,
                doc=lambda: self.strings("unsubscribe_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "no_track_users",
                ["username"],
                doc=lambda: self.strings("no_track_users_desc"),
                validator=loader.validators.Series(
                    loader.validators.Union(loader.validators.String(), loader.validators.Integer())
                ),
            ),
            loader.ConfigValue(
                "testnet",
                False,
                doc=lambda: self.strings("testnet_desc"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "gemini_api_key",
                "",
                doc=lambda: self.strings("gemini_api_key_desc"),
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "gemini_model_name",
                "gemini-2.0-flash-exp",
                doc=lambda: self.strings("gemini_model_name_desc"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "proxy",
                "",
                doc=lambda: self.strings("proxy_desc"),
                validator=loader.validators.String(),
            )
        )
        self.sent_codes = defaultdict(bool)

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.me = await self.client.get_me()
        self.me_id = self.me.id
        self.cd_id = 1559501630
        self.testnet_id = 1622808649
        self.extractor = URLExtract()
        self.scraper = cloudscraper.create_scraper()
        handlers = [
            (self.cb, [events.NewMessage, events.MessageEdited]),
            (self.channels, [events.NewMessage, events.MessageEdited]),
            (self.passwords, [events.NewMessage, events.MessageEdited]),
        ]

        for handler_func, event_list in handlers:
            for event in event_list:
                self.client.add_event_handler(handler_func, event)


        if self.config["gemini_api_key"]:
            self.passworder = Passworder(self.config["gemini_api_key"], self.config["gemini_model_name"])
        else:
            self.passworder = None

        proxy = self.config["proxy"]
        if proxy:
            os.environ["http_proxy"] = proxy
            os.environ["HTTP_PROXY"] = proxy
            os.environ["https_proxy"] = proxy
            os.environ["HTTPS_PROXY"] = proxy

    async def stars(self, url, bot_username):
        web_view = await self.client(RequestWebViewRequest(
            peer=bot_username,
            bot=bot_username,
            platform='android',
            from_bot_menu=False,
            url=url
        ))

        auth_url = web_view.url
        params = unquote(auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        access_token = await self.get_token('https://api.send.tg/internal/v1/authentication/webapp', params)

        if access_token:
            code = url.split('/')[-1]
            await self.claim_stars(code, access_token)

    async def get_token(self, url, params):
        json_data = {
            "initData": params
        }
        UserAgent = self.generate_random_user_agent()
        headers = {
            'Accept': 'application/json',
            'User-Agent': UserAgent
        }

        response = self.scraper.post(url, json=json_data, headers=headers)
        
        if response.status_code == 200:
            headers = response.headers
            set_cookie = headers.get('Set-Cookie')
            if set_cookie:
                access_token = set_cookie.split('access_token=')[1].split(';')[0]
                return access_token
            else:
                return None
        else:
            return None

    async def claim_stars(self, code, access_token):
        url = f'https://api.send.tg/internal/v1/stars/claim/{code}'
        UserAgent = self.generate_random_user_agent()
        headers = {
            'Accept': 'application/json',
            'Cookie': f'access_token={access_token}',
            'User-Agent': UserAgent
        }

        response = self.scraper.post(url, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            stars = response_data.get("stars")
            gifted_by = response_data.get("gifted_by")
            await self.log(f"<b>+{stars}</b> <emoji document_id=5897920748101571572>🌟</emoji> (от {gifted_by})")
        else:
            pass

    async def get_codes(self, text, entities, markup):
        urls_in_message = set()
        finded_codes = set()
        finded_stars_codes = set()
        finded_testnet_codes = set()

        url_pattern = r'https?://t\.me/(?:send|CryptoBot)\?start=([A-Za-z0-9_-]+)'
        stars_pattern = r'https?://t\.me/CryptoBot/app\?startapp=stars-([A-Za-z0-9_-]+)'
        testnet_pattern = r'https?://t\.me/CryptoTestnetBot\?start=([A-Za-z0-9_-]+)'

        if entities:
            for entity in entities:
                if isinstance(entity, MessageEntityUrl):
                    urls_in_text = self.extractor.find_urls(text)
                    for found_url in urls_in_text:
                        urls_in_message.add(found_url.strip())

                elif isinstance(entity, MessageEntityTextUrl):
                    url = entity.url.strip()
                    urls_in_message.add(url)

                elif isinstance(entity, MessageMediaWebPage):
                    url = entity.url.strip()
                    urls_in_message.add(url)

        if markup:
            for button_row in markup.rows:
                for button in button_row.buttons:
                    if hasattr(button, "url") and button.url:
                        urls_in_message.add(button.url.strip())

        for found_url in urls_in_message:
            if not found_url.startswith(('http://', 'https://')):
                found_url = 'https://' + found_url.strip() #не обращайте внимания на костыли пажеее

            clean_url = re.sub(r'[^\w:/?&=.-]', '', found_url)
            
            code_match = re.match(url_pattern, clean_url)
            if code_match:
                code = code_match.group(1)
                finded_codes.add(code)
            
            stars_match = re.match(stars_pattern, clean_url)
            if stars_match:
                stars_code = stars_match.group(1)
                finded_stars_codes.add(stars_code)

            testnet_match = re.match(testnet_pattern, clean_url)
            if testnet_match:
                testnet_code = testnet_match.group(1)
                finded_testnet_codes.add(testnet_code)

        return list(finded_codes), list(finded_stars_codes), list(finded_testnet_codes)

    async def password(self, description):
        if not self.config["gemini_api_key"]:
            await self.log(f"<emoji document_id=5274099962655816924>❗️</emoji> <b>API ключ не указан. Получить его можно тут: aistudio.google.com/apikey (бесплатно), затем укажи его в конфиге (<code>{self.get_prefix()}cfg yg_checks</code>)</b>")
            return

        if self.passworder:
            result = await self.passworder.generate(description)
        else:
            return

        if "error" in result:
            await self.log(f"<emoji document_id=5274099962655816924>❗️</emoji> <b>Ошибка генерации пароля:</b> <code>{utils.escape_html(result['error'])}</code>")
            return

        if result.get("password"):
            return result["password"]
        elif result.get("password") == "":
            return
        else:
            await self.log(f"<emoji document_id=5274099962655816924>❗️</emoji> <b>Ошибка генерации пароля:</b> <code>{utils.escape_html(str(result))}</code>")
            return

    async def cb(self, message):
        if self.config["watcher_on"]:
            if message and message.sender_id not in [self.me_id, self.cd_id, self.testnet_id]:
                try:
                    if not self.config["track_private"] and message.is_private:
                        return

                    sender_username = getattr(message.sender, 'username', None) if message.sender else None
                    if sender_username in self.config["no_track_users"]:
                        return

                    codes, stars_codes, testnet_codes = await self.get_codes(message.text, message.entities, message.reply_markup)

                    if codes:
                        for code in codes:
                            if not self.sent_codes[code]:
                                if code.startswith('CQ'):
                                    await message.mark_read()
                                    await asyncio.sleep(int(self.config["delay"]))
                                    await self.client.send_message(self.cd_id, f"/start {code}")
                                    self.sent_codes[code] = True
                                    await self.send_log_message(message, code)

                    if stars_codes:
                        for stars_code in stars_codes:
                            if not self.sent_codes[stars_code]:
                                await message.mark_read()
                                await self.stars(f"https://app.send.tg/stars/{stars_code}", "send")
                                self.sent_codes[stars_code] = True

                    if testnet_codes:
                        if self.config["testnet"]:
                            for testnet_code in testnet_codes:
                                if not self.sent_codes[testnet_code]:
                                    if testnet_code.startswith('CQ'):
                                        await message.mark_read()
                                        await asyncio.sleep(int(self.config["delay"]))
                                        await self.client.send_message(self.testnet_id, f"/start {testnet_code}")
                                        self.sent_codes[testnet_code] = True
                                        await self.send_log_message(message, testnet_code)
                except AttributeError:
                    pass

    async def channels(self, event):
        if not self.config["subscribe"]:
            return

        if not self.config["watcher_on"]:
            return

        if event.sender_id == self.cd_id and any(event.text.startswith(prefix) for prefix in ['Чтобы активировать этот чек, подпишитесь на канал','To activate this check, join the channel(s)']):
            subscribed = []
            try:
                rows = event.reply_markup.rows if event.reply_markup else []
                for row in rows:
                    for button in row.buttons:
                        if button.url:
                            invite_code = button.url.split('+', 1)[1]
                            await self.client(ImportChatInviteRequest(invite_code))
                            subscribed.append(invite_code)
            except Exception:
                pass

            await asyncio.sleep(1)
            await event.click(data=b'check-subscribe')
            await asyncio.sleep(1)

            if self.config["unsubscribe"]:
                for invite_code in subscribed:
                    channel_info = await self.client(CheckChatInviteRequest(hash=invite_code))
                    channel = channel_info.chat
                    await self.client(LeaveChannelRequest(channel))

    async def passwords(self, message): 
        if not self.config["watcher_on"]:
            return
    
        if not self.config["ai_passwords"]:
            return

        if message.sender_id == self.cd_id and any(phrase in message.text for phrase in ["Введите пароль от чека для получения", "Enter the password for this check to receive"]):
            description = " ".join("\n".join(message.raw_text.split("\n")[2:]).split(" ")[1:])
            r = await self.password(description)
            if r:
                await self.client.send_message(self.cd_id, r)

    async def log(self, message):
        if self.config["logs_username"]:
            await self.client.send_message(self.config["logs_username"], message, link_preview=False)

    async def send_log_message(self, message, code):
        if self.config["logs_enabled"]:
            chat_id = str(message.chat_id).replace('-100', '')
            if message.is_private:
                sender_username = getattr(message.sender, 'username', None) if message.sender else None
                await self.log(f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5879770735999717115>👤</emoji> <b>Чек был обнаружен в личных сообщениях:</b> <i>@{sender_username}</i>")
            else:
                message_link = f"t.me/c/{chat_id}/{message.id}"
                await self.log(f"<emoji document_id=5431449001532594346>⚡️</emoji> <b>Обнаружен новый чек:</b>\n\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка чека:</b> <i>t.me/send?start={code}<i>\n<emoji document_id=5870527201874546272>🔗</emoji> <b>Ссылка на сообщение с чеком:</b> <i>{message_link}</i>")

    @loader.command(ru_doc="вкл/выкл активатор", ua_doc="увімк/вимк активатор")
    async def checkscmd(self, m: Message):
        """on/off auto-check activation"""
        self.config["watcher_on"] = not self.config["watcher_on"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включен", "ua": "увімкнено"}[lang] if self.config["watcher_on"] else {"en": "disabled", "ru": "выключен", "ua": "вимкнено"}[lang]
        list = [
            "<emoji document_id=5931703809800672260>🦋</emoji>",
            "<emoji document_id=5931685899787049183>🦋</emoji>",
            "<emoji document_id=5931254745200072637>🦋</emoji>",
            "<emoji document_id=5931420135800706406>🦋</emoji>",
            "<emoji document_id=5931579221389350286>🦋</emoji>",
            "<emoji document_id=5931796606864070138>🦋</emoji>",
            "<emoji document_id=5931709595121620710>🦋</emoji>",
            "<emoji document_id=5931689305696113988>🦋</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["activator"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл активатор testnet", ua_doc="увімк/вимк активатор testnet")
    async def testnetcmd(self, m: Message):
        """on/off auto-check activation for testnet"""
        self.config["testnet"] = not self.config["testnet"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включена", "ua": "увімкнена"}[lang] if self.config["testnet"] else {"en": "disabled", "ru": "выключена", "ua": "вимкнена"}[lang]
        list = [
            "<emoji document_id=5931703809800672260>🦋</emoji>",
            "<emoji document_id=5931685899787049183>🦋</emoji>",
            "<emoji document_id=5931254745200072637>🦋</emoji>",
            "<emoji document_id=5931420135800706406>🦋</emoji>",
            "<emoji document_id=5931579221389350286>🦋</emoji>",
            "<emoji document_id=5931796606864070138>🦋</emoji>",
            "<emoji document_id=5931709595121620710>🦋</emoji>",
            "<emoji document_id=5931689305696113988>🦋</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["testnet"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл отправку логов", ua_doc="увімк/вимк відправку логів")
    async def yglogscmd(self, m: Message):
        """on/off log sending"""
        self.config["logs_enabled"] = not self.config["logs_enabled"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включена", "ua": "увімкнена"}[lang] if self.config["logs_enabled"] else {"en": "disabled", "ru": "выключена", "ua": "вимкнена"}[lang]
        list = [
            "<emoji document_id=5931246400078616786>🍑</emoji>",
            "<emoji document_id=5931283302437623922>🍑</emoji>",
            "<emoji document_id=5933573709712331850>🍑</emoji>",
            "<emoji document_id=5931412164341404834>🍑</emoji>",
            "<emoji document_id=5931408105597310922>🍑</emoji>",
            "<emoji document_id=5931347907335689957>🍑</emoji>",
            "<emoji document_id=5933527787922005080>🍑</emoji>",
            "<emoji document_id=5931255728747583490>🍑</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["log_sending"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл подбор паролей с помощью нейросети", ua_doc="увімк/вимк підбір паролей за допомогою нейромережі")
    async def passwordscmd(self, m: Message):
        """on/off password cracking with neural network"""
        self.config["ai_passwords"] = not self.config["ai_passwords"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включен", "ua": "увімкнено"}[lang] if self.config["ai_passwords"] else {"en": "disabled", "ru": "выключен", "ua": "вимкнено"}[lang]
        list = [
            "<emoji document_id=5931715028255249602>🔐</emoji>",
            "<emoji document_id=5931759476871797208>🔐</emoji>",
            "<emoji document_id=5931604879523976952>🔐</emoji>",
            "<emoji document_id=5931569115331306831>🔐</emoji>",
            "<emoji document_id=5931530997496551899>🔐</emoji>",
            "<emoji document_id=5931464008891635480>🔐</emoji>",
            "<emoji document_id=5931781312485529416>🔐</emoji>",
            "<emoji document_id=5931434210408536378>🔐</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["password_cracking"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл активацию чеков отправленных в личке", ua_doc="увімк/вимк активацію чеків, надісланих в особисті повідомлення")
    async def yglscmd(self, m: Message):
        """on/off activation of checks sent in private messages"""
        self.config["track_private"] = not self.config["track_private"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включена", "ua": "увімкнена"}[lang] if self.config["track_private"] else {"en": "disabled", "ru": "выключена", "ua": "вимкнена"}[lang]
        list = [
            "<emoji document_id=5931534008268625877>🔁</emoji>",
            "<emoji document_id=5933704920963225481>🔁</emoji>",
            "<emoji document_id=5931351192985671828>🔁</emoji>",
            "<emoji document_id=5931570287857374798>🔁</emoji>",
            "<emoji document_id=5931284676827158390>🔁</emoji>",
            "<emoji document_id=5931776850014508762>🔁</emoji>",
            "<emoji document_id=5931430675650451345>🔁</emoji>",
            "<emoji document_id=5931768827015602073>🔁</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["private_check_activation"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл авто-подписку", ua_doc="увімк/вимк авто-підписку")
    async def subscribecmd(self, m: Message):
        """on/off auto-subscription"""
        self.config["subscribe"] = not self.config["subscribe"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включена", "ua": "увімкнена"}[lang] if self.config["subscribe"] else {"en": "disabled", "ru": "выключена", "ua": "вимкнена"}[lang]
        list = [
            "<emoji document_id=5931461638069687926>💡</emoji>",
            "<emoji document_id=5931599476455118181>💡</emoji>",
            "<emoji document_id=5931620642053953532>💡</emoji>",
            "<emoji document_id=5931776927323920236>💡</emoji>",
            "<emoji document_id=5931773113392962977>💡</emoji>",
            "<emoji document_id=5931673221043590661>💡</emoji>",
            "<emoji document_id=5931462436933604912>💡</emoji>",
            "<emoji document_id=5931295409950431661>💡</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["auto_subscription"].format(emoji, on_off))

    @loader.command(ru_doc="вкл/выкл авто-отписку", ua_doc="увімк/вимк авто-відписку")
    async def unsubscribecmd(self, m: Message):
        """on/off auto-unsubscription"""
        self.config["unsubscribe"] = not self.config["unsubscribe"]
        lang = self.strings.get("language", "en")
        on_off = {"en": "enabled", "ru": "включена", "ua": "увімкнена"}[lang] if self.config["unsubscribe"] else {"en": "disabled", "ru": "выключена", "ua": "вимкнена"}[lang]
        list = [
            "<emoji document_id=5931279570111043408>✅</emoji>",
            "<emoji document_id=5931602010485823634>✅</emoji>",
            "<emoji document_id=5931642602221737965>✅</emoji>",
            "<emoji document_id=5933944919440758085>✅</emoji>",
            "<emoji document_id=5933523918156469650>✅</emoji>",
            "<emoji document_id=5931644148409964015>✅</emoji>",
            "<emoji document_id=5931387421034812889>✅</emoji>",
            "<emoji document_id=5931344333922900261>✅</emoji>"
        ]
        emoji = random.choice(list)
        await utils.answer(m, self.strings["auto_unsubscription"].format(emoji, on_off))

    def generate_random_user_agent(self, device_type='android', browser_type='chrome'):
        existing_versions = {
            110: [
                '110.0.5481.154',
                '110.0.5481.153',
                '110.0.5481.65',
                '110.0.5481.64',
                '110.0.5481.63',
                '110.0.5481.61'
            ],
            111: [
                "111.0.5563.116",
                '111.0.5563.115',
                '111.0.5563.58',
                '111.0.5563.49'
            ],
            112: [
                '112.0.5615.136',
                '112.0.5615.136',
                '112.0.5615.101',
                '112.0.5615.100',
                '112.0.5615.48'
            ],
            113: [
                '113.0.5672.77',
                '113.0.5672.76'
            ],
            114: [
                '114.0.5735.60',
                '114.0.5735.53'
            ],
            115: [
                '115.0.5790.136'
            ],
            116: [
                '116.0.5845.172',
                '116.0.5845.164',
                '116.0.5845.163',
                '116.0.5845.114',
                '116.0.5845.92'
            ],
            117: [
                '117.0.5938.154',
                '117.0.5938.141',
                '117.0.5938.140',
                '117.0.5938.61',
                '117.0.5938.61',
                '117.0.5938.60'
            ],
            118: [
                '118.0.5993.112',
                '118.0.5993.111',
                '118.0.5993.80',
                '118.0.5993.65',
                '118.0.5993.48'
            ],
            119: [
                '119.0.6045.194',
                '119.0.6045.193',
                '119.0.6045.164',
                '119.0.6045.163',
                '119.0.6045.134',
                '119.0.6045.134',
                '119.0.6045.66',
                '119.0.6045.53'
            ],
            120: [
                '120.0.6099.230',
                '120.0.6099.210',
                '120.0.6099.194',
                '120.0.6099.193',
                '120.0.6099.145',
                '120.0.6099.144',
                '120.0.6099.144',
                '120.0.6099.116',
                '120.0.6099.116',
                '120.0.6099.115',
                '120.0.6099.44',
                '120.0.6099.43'
            ],
            121: [
                '121.0.6167.178',
                '121.0.6167.165',
                '121.0.6167.164',
                '121.0.6167.164',
                '121.0.6167.144',
                '121.0.6167.143',
                '121.0.6167.101'
            ],
            122: [
                '122.0.6261.119',
                '122.0.6261.106',
                '122.0.6261.105',
                '122.0.6261.91',
                '122.0.6261.90',
                '122.0.6261.64',
                '122.0.6261.43'
            ],
            123: [
                '123.0.6312.121',
                '123.0.6312.120',
                '123.0.6312.119',
                '123.0.6312.118',
                '123.0.6312.99',
                '123.0.6312.80',
                '123.0.6312.41',
                '123.0.6312.40'
            ],
            124: [
                '124.0.6367.179',
                '124.0.6367.172',
                '124.0.6367.171',
                '124.0.6367.114',
                '124.0.6367.113',
                '124.0.6367.83',
                '124.0.6367.82',
                '124.0.6367.54'
            ],
            125: [
                '125.0.6422.165',
                '125.0.6422.164',
                '125.0.6422.147',
                '125.0.6422.146',
                '125.0.6422.113',
                '125.0.6422.72',
                '125.0.6422.72',
                '125.0.6422.53',
                '125.0.6422.52'
            ],
            126: [
                '126.0.6478.122',
                '126.0.6478.72',
                '126.0.6478.71',
                '126.0.6478.50'
            ]
        }

        devices = [
            ('Samsung', 'SM-G980F', 'AVERAGE', 10),
            ('Samsung', 'SM-G973F', 'AVERAGE', 9),
            ('Samsung', 'SM-G973U', 'AVERAGE', 9),
            ('Samsung', 'SM-N986B', 'AVERAGE', 11),
            ('Samsung', 'SM-N981B', 'AVERAGE', 11),
            ('Samsung', 'SM-F916B', 'AVERAGE', 11),
            ('Samsung', 'SM-G998B', 'HIGH', 12),
            ('Samsung', 'SM-G991B', 'HIGH', 12),
            ('Samsung', 'SM-G996B', 'HIGH', 12),
            ('Samsung', 'SM-G990E', 'HIGH', 12),
            ('Samsung', 'SM-G990B', 'HIGH', 12),
            ('Samsung', 'SM-G990B2', 'HIGH', 12),
            ('Samsung', 'SM-G990U', 'HIGH', 12),
            ('Google', 'Pixel 5', 'AVERAGE', 11),
            ('Google', 'Pixel 5a', 'AVERAGE', 11),
            ('Google', 'Pixel 6', 'AVERAGE', 12),
            ('Google', 'Pixel 6 Pro', 'AVERAGE', 12),
            ('Google', 'Pixel 6 XL', 'AVERAGE', 12),
            ('Google', 'Pixel 6a', 'AVERAGE', 12),
            ('Google', 'Pixel 7', 'HIGH', 13),
            ('Google', 'Pixel 7a', 'AVERAGE', 13),
            ('Google', 'Pixel 7 Pro', 'HIGH', 13),
            ('Google', 'Pixel 8', 'HIGH', 14),
            ('Google', 'Pixel 8a', 'HIGH', 14),
            ('Google', 'Pixel 8 Pro', 'HIGH', 14),
            ('Google', 'Pixel 9', 'HIGH', 14),
            ('Google', 'Pixel 9 Pro', 'HIGH', 14),
            ('Google', 'Pixel 9 Pro XL', 'HIGH', 14),
            ('Xiaomi', 'Mi 10', 'AVERAGE', 10),
            ('Xiaomi', 'Mi 11', 'AVERAGE', 11),
            ('Xiaomi', 'Mi 12', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 10', 'HIGH', 11),
            ('Xiaomi', 'Redmi Note 10 Pro', 'HIGH', 11),
            ('Xiaomi', 'Redmi Note 11', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 11 Pro', 'HIGH', 12),
            ('Xiaomi', 'Redmi Note 12', 'HIGH', 13),
            ('Xiaomi', 'Redmi Note 12 Pro', 'HIGH', 13),
            ('Xiaomi', 'POCO M3 Pro', 'HIGH', 11),
            ('Xiaomi', 'POCO X5', 'HIGH', 12),
            ('Xiaomi', 'POCO X5 Pro', 'HIGH', 12),
            ('Xiaomi', 'POCO X6 Pro', 'HIGH', 13),
            ('Xiaomi', 'POCO F4', 'HIGH', 12),
            ('Xiaomi', 'POCO F4 GT', 'HIGH', 12),
            ('Xiaomi', 'POCO F3', 'HIGH', 11),
            ('OnePlus', 'NE2215', 'AVERAGE', 12),
            ('OnePlus', 'NE2210', 'AVERAGE', 12),
            ('OnePlus', 'IN2010', 'AVERAGE', 10),
            ('OnePlus', 'IN2023', 'AVERAGE', 11),
            ('OnePlus', 'LE2117', 'AVERAGE', 11),
            ('OnePlus', 'LE2123', 'AVERAGE', 11),
            ('OnePlus', 'CPH2423', 'AVERAGE', 12),
            ('Huawei', 'VOG-AL00', 'AVERAGE', 9),
            ('Huawei', 'ANA-AL00', 'AVERAGE', 10),
            ('Huawei', 'TAS-AL00', 'AVERAGE', 10),
            ('Huawei', 'OCE-AN10', 'AVERAGE', 11),
            ('Sony', 'J9150', 'AVERAGE', 9),
            ('Sony', 'J9210', 'AVERAGE', 10)
        ]

        firefox_versions = list(range(100, 127))

        if browser_type == 'chrome':
            major_version = random.choice(list(existing_versions.keys()))
            browser_version = random.choice(existing_versions[major_version])
        elif browser_type == 'firefox':
            browser_version = random.choice(firefox_versions)

        user_agent = ""

        if device_type == 'android':
            android_versions = {
                '10': 29,
                '11': 30,
                '12': 31,
                '13': 33,
                '14': 34
            }

            manufacturer, model, performance_class, min_android_version = random.choice(devices)
            android_version = str(random.choice([v for v in android_versions.keys() if int(v) >= min_android_version]))
            sdk_version = android_versions[android_version]

            if browser_type == 'chrome':
                major_version = random.choice(list(existing_versions.keys()))
                browser_version = random.choice(existing_versions[major_version])
                user_agent = (f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 "
                              f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 "
                              f"Telegram-Android/11.4.2 ({manufacturer} {model}; Android {android_version}; "
                              f"SDK {sdk_version}; {performance_class})")
            elif browser_type == 'firefox':
                browser_version = random.choice(firefox_versions)
                user_agent = (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                              f"Gecko/{browser_version}.0 Firefox/{browser_version}.0 "
                              f"Telegram-Android/11.4.2 ({manufacturer} {model}; Android {android_version}; "
                              f"SDK {sdk_version}; {performance_class})")

        elif device_type == 'ios':
            ios_versions = ['13.0', '14.0', '15.0', '16.0', '17.0', '18.0']
            ios_version = random.choice(ios_versions)
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                              f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                              f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version}.0 Mobile/15E148 Safari/605.1.15")

        elif device_type == 'windows':
            windows_versions = ['10.0', '11.0']
            windows_version = random.choice(windows_versions)
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              f"Chrome/{browser_version} Safari/537.36")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                              f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

        elif device_type == 'ubuntu':
            if browser_type == 'chrome':
                user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                              f"Chrome/{browser_version} Safari/537.36")
            elif browser_type == 'firefox':
                user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) Gecko/{browser_version}.0 "
                              f"Firefox/{browser_version}.0")

        return user_agent
