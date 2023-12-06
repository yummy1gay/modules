#meta developer: @yummy1gay

import os
import uuid
from .. import loader, utils

@loader.tds
class VoiceModule(loader.Module):
    """Converts music and video"""

    strings = {"name": "yg_vm"}

    async def m2vcmd(self, message):
        """Convert music to voice message"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>Reply to audio file</b>")
            return

        media = reply.file
        mime_type = media.mime_type.split('/')[0] if '/' in media.mime_type else 'audio'

        if mime_type == 'audio':
            await utils.answer(message, "<emoji document_id=4988080790286894217>🫥</emoji> <b>Converting audio...</b>")
            voice_message = await self.convert_audio(reply)
        else:
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>Unsupported file type</b>")
            return

        await message.delete()
        await message.client.send_file(message.to_id, voice_message, voice_note=True, reply_to=reply)

    async def convert_audio(self, message):
        tmp_filename = "tmp_audio.ogg"
        await message.download_media(file=tmp_filename)
        os.system(f"ffmpeg -y -i {tmp_filename} -c:a libopus {tmp_filename}.ogg")
        os.remove(tmp_filename)
        return f"{tmp_filename}.ogg"

    async def v2acmd(self, message):
        """Convert video to audio"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>Reply to video file</b>")
            return

        media = reply.file
        mime_type = media.mime_type.split('/')[0] if '/' in media.mime_type else 'video'

        if mime_type == 'video':
            await utils.answer(message, "<emoji document_id=4988080790286894217>🫥</emoji> <b>Converting video to audio...</b>")
            audio_message = await self.convert_video_to_mp3(reply)
        else:
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>Unsupported file type</b>")
            return

        await message.delete()
        await message.client.send_file(message.to_id, audio_message, reply_to=reply)

    async def convert_video_to_mp3(self, message):
        tmp_filename = f"{uuid.uuid4().hex}.mp4"
        await message.download_media(file=tmp_filename)

        audio_filename = f"{uuid.uuid4().hex}.mp3"
        os.system(f"ffmpeg -y -i {tmp_filename} -vn -acodec libmp3lame -ab 192k -ar 44100 -ac 2 {audio_filename}")

        os.remove(tmp_filename)

        return audio_filename