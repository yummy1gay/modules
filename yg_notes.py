# meta developer: @yummy_gay

from telethon import events
from .. import loader, utils

class NotesMod(loader.Module):
    """Модуль заметок (для каждого чата отдельный список)"""
    strings = {"name": "yg_notes"}

    async def notecmd(self, message):
        """<текст> добавить новую заметку"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("<b>Пожалуйста, укажи текст заметки <emoji document_id=5348140027698227662>🙀</emoji></b>")
        try:
            notes = await self.get_notes(message)
            note_id = len(notes) + 1
            notes.append({"id": note_id, "text": args})
            await self.save_notes(message, notes)
            await message.edit(f"<b>Заметка</b> <code>#{note_id}</code> <b>добавлена</b> <emoji document_id=5348140027698227662>🙀</emoji>")
        except Exception as e:
            await message.edit(f"<b>Произошла ошибка:</b> <code>{str(e)}</code>")

    async def notescmd(self, message):
        """показать список заметок"""
        notes = await self.get_notes(message)
        if notes:
            text = "<b><emoji document_id=5348140027698227662>🙀</emoji> Твои заметки:</b>\n\n"
            for note in notes:
                text += f"<b>Заметка</b> <code>#{note['id']}</code>: {note['text']}\n\n"
            await message.edit(text)
        else:
            await message.edit("<b>У тебя нет заметок <emoji document_id=5348140027698227662>🙀</emoji></b>")

    async def delnotecmd(self, message):
        """<# заметки> удалить заметку"""
        args = utils.get_args(message)
        if not args:
            return await message.edit("<b>Пожалуйста, укажи номер заметки для удаления <emoji document_id=5348140027698227662>🙀</emoji></b>")
        try:
            note_id = int(args[0].lstrip("#"))
            notes = await self.get_notes(message)
            if note_id <= 0 or note_id > len(notes):
                return await message.edit("<b>Неправильный номер заметки <emoji document_id=5348140027698227662>🙀</emoji></b>")
            del notes[note_id - 1]
            await self.reorder_notes(message, notes)
            await self.save_notes(message, notes)
            await message.edit(f"<b>Заметка</b> <code>#{note_id}</code> <b>удалена</b> <emoji document_id=5348140027698227662>🙀</emoji>")
        except Exception as e:
            await message.edit(f"<b>Произошла ошибка:</b> <code>{str(e)}</code>")

    async def clearnotescmd(self, message):
        """очистить все заметки"""
        try:
            await self.save_notes(message, [])
            await message.edit("<b>Все заметки удалены</b> <emoji document_id=5348140027698227662>🙀</emoji>")
        except Exception as e:
            await message.edit(f"<b>Произошла ошибка:<b> <code>{str(e)}</code>")

    async def get_notes(self, message):
        if not hasattr(message.client, "notes"):
            message.client.notes = {}
        chat_id = utils.get_chat_id(message)
        if chat_id not in message.client.notes:
            message.client.notes[chat_id] = []
        return message.client.notes[chat_id]

    async def save_notes(self, message, notes):
        chat_id = utils.get_chat_id(message)
        message.client.notes[chat_id] = notes

    async def reorder_notes(self, message, notes):
        for i, note in enumerate(notes):
            note['id'] = i + 1