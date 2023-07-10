#meta developer: @yummy_gay

import os
from .. import loader
from PIL import Image
from moviepy.editor import VideoFileClip

class circleMod(loader.Module):
    """Модуль для конвертации видео в кружочек"""

    strings = {"name": "yg_circle"}

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
        """Обрезать видео до квадратного формата (1:1)"""
        square_video = None
        video_clip = VideoFileClip(video)
        width, height = video_clip.size
        if width != height:
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            cropped_clip = video_clip.crop(x1=left, y1=top, x2=right, y2=bottom)
            square_video = f"{video}_square.mp4"
            cropped_clip.write_videofile(square_video, codec="libx264", audio_codec="aac")
        return square_video if square_video else video
    
    async def del_failed_kr_messages(self, message):
        """Удалить все сообщения, содержащие текст '🚫 Call .kr failed!'"""
        async for msg in message.client.iter_messages(message.to_id):
            if msg.raw_text and '🚫 Call .kr failed!' in msg.raw_text:
                await msg.delete()