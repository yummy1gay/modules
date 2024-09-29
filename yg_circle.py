__version__ = (1, 4, 8, 8)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3
# scope: ffmpeg

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
from yumlib import yummy

from .. import loader

class yg_circle(loader.Module):
    """Модуль для конвертации видео в кружочек"""

    strings = {"name": "yg_circle"}

    async def client_ready(self, client, db):
        await yummy(client)

    async def krcmd(self, message):
        """<reply to video> конвертировать видео в кружочек"""
        reply = await message.get_reply_message()
        if not reply or not reply.video:
            await message.edit("<b><emoji document_id=5210952531676504517>❌</emoji> Ответьте на видео командой <code>.kr</code> для конвертации в кружочек 🎥</b>")
            return
        try:
            await message.edit("<b><emoji document_id=4988080790286894217>🫥</emoji> Обработка...</b>")
            video = await reply.download_media()
            square_video = await self.crop_to_square(video)
            if square_video:
                await message.edit("<b><emoji document_id=4988080790286894217>🫥</emoji> Отправка...</b>")
                await message.client.send_file(message.to_id, square_video, video_note=True)
        except Exception as e:
            await message.edit(f"<b><emoji document_id=5210952531676504517>❌</emoji> Произошла ошибка при конвертации видео в кружочек: {str(e)}</b>")
        finally:
            if os.path.exists(video):
                os.remove(video)
            if square_video and os.path.exists(square_video):
                os.remove(square_video)
        await message.delete()

    async def crop_to_square(self, video):
        """Обрезать видео до квадратного формата (1:1) с помощью ffmpeg"""
        square_video = f"{video}_square.mp4"
        command = (
            f"ffmpeg -i {video} -vf \"crop='min(in_w,in_h)':'min(in_w,in_h)':'(in_w-out_w)/2':'(in_h-out_h)/2'\" -c:a copy {square_video}"
        )
        os.system(command)
        return square_video if os.path.exists(square_video) else None