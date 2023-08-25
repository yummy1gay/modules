#meta developer: @yummy_gay
#channel tg: @yg_modules
#st1tl cl0wn

#██╗░░░██╗░██████╗░░░░░███╗░░░███╗░█████╗░██████╗░██╗░░░██╗██╗░░░░░███████╗░██████╗
#╚██╗░██╔╝██╔════╝░░░░░████╗░████║██╔══██╗██╔══██╗██║░░░██║██║░░░░░██╔════╝██╔════╝
#░╚████╔╝░██║░░██╗░░░░░██╔████╔██║██║░░██║██║░░██║██║░░░██║██║░░░░░█████╗░░╚█████╗░
#░░╚██╔╝░░██║░░╚██╗░░░░██║╚██╔╝██║██║░░██║██║░░██║██║░░░██║██║░░░░░██╔══╝░░░╚═══██╗
#░░░██║░░░╚██████╔╝░░░░██║░╚═╝░██║╚█████╔╝██████╔╝╚██████╔╝███████╗███████╗██████╔╝
#░░░╚═╝░░░░╚═════╝░░░░░╚═╝░░░░░╚═╝░╚════╝░╚═════╝░░╚═════╝░╚══════╝╚══════╝╚═════╝░

import asyncio
import time
from telethon.tl.types import Message
from .. import loader, utils

class yg_timer(loader.Module):
    """Модуль для установки и управления таймерами."""

    strings = {"name": "yg_timer"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "update_interval", 11, "Interval for updating the timer display in seconds"
        )
        self.timers = {}
        self.timer_counter = 0

    async def start_timer(self, message, timer_id, duration, initial_time_text):
        start_time = time.time()
        while time.time() - start_time < duration:
            remaining_time = int(duration - (time.time() - start_time))
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_message = (
                f"<emoji document_id=5872756762347573066>⏲</emoji> <b>Таймер</b> <code>#{timer_id}</code>\n"
                f"<emoji document_id=5451732530048802485>⏳</emoji> <b>Заданное время:</b> <code>{initial_time_text}</code>\n"
                f"<emoji document_id=5469741319330996757>💫</emoji> <b>Осталось:</b> <code>{hours:02}:{minutes:02}:{seconds:02}</code>\n\n"
                f"<i>Частота обновления каждые {self.config['update_interval']} секунд (можно изменить в конфиге)</i>"
            )
            await message.edit(timer_message)
            await asyncio.sleep(self.config["update_interval"])
            if timer_id not in self.timers or not self.timers[timer_id]:
                return
        await message.edit(f"<emoji document_id=5427009714745517609>✅</emoji> <b>Таймер</b> <code>#{timer_id}</code> <b>завершен!</b>\n<b>Заданное время истекло!</b>")

    @loader.unrestricted
    async def timercmd(self, message: Message):
        """<время> - устанавливает таймер"""
        args = utils.get_args(message)
        if len(args) < 2:
            await utils.answer(message, "<emoji document_id=5465665476971471368>❌</emoji> <b>Некорректные аргументы. Пример:</b> <code>.timer 1 час</code>")
            return

        time_amount = float(args[0])
        time_unit = args[1].lower()
        if time_unit.endswith("сек") or time_unit.endswith("s"):
            duration = time_amount
            initial_time_text = f"{time_amount} сек"
        elif time_unit.endswith("мин") or time_unit.endswith("m"):
            duration = time_amount * 60
            initial_time_text = f"{time_amount} мин"
        elif time_unit.endswith("час") or time_unit.endswith("h"):
            duration = time_amount * 3600
            initial_time_text = f"{time_amount} час"
        elif time_unit.endswith("день") or time_unit.endswith("d"):
            duration = time_amount * 86400
            initial_time_text = f"{time_amount} день"
        else:
            await utils.answer(message, "<emoji document_id=5465665476971471368>❌</emoji> <b>Некорректная единица времени. Используйте сек, мин, час, день или их английские аналоги</b>")
            return

        self.timer_counter += 1
        timer_id = self.timer_counter
        timer_message = await utils.answer(
            message, f"Таймер #{timer_id}\nЗаданное время: {initial_time_text}\nОсталось: 00:00:00\nЧастота обновления: каждые {self.config['update_interval']} секунд"
        )
        self.timers[timer_id] = True

        await asyncio.create_task(self.start_timer(timer_message, timer_id, duration, initial_time_text))

    @loader.unrestricted
    async def stoptimercmd(self, message: Message):
        """<номер таймера> - останавить указанный таймер"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5465665476971471368>❌</emoji> <b>Укажите номер таймера для остановки</b>")
            return

        try:
            timer_id = int(args[0])
            if timer_id in self.timers and self.timers[timer_id]:
                self.timers[timer_id] = False
                await utils.answer(message, f"<emoji document_id=5427009714745517609>✅</emoji> <b>Таймер</b> <code>#{timer_id}</code> <b>oстановлен</b>")
            else:
                await utils.answer(message, f"<emoji document_id=5465665476971471368>❌</emoji> <b>Таймер с номером</b> <code>#{timer_id}</code> <b>не найден или уже остановлен</b>")
        except ValueError:
            await utils.answer(message, "<emoji document_id=5465665476971471368>❌</emoji> <b>Некорректный номер таймера</b>")

    async def client_ready(self, client, db):
        self.client = client

    async def __unload(self):
        for timer_id in self.timers:
            self.timers[timer_id] = False

    async def client_ready(self, client, db):
        self.client = client
