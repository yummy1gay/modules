__version__ = (1, 1)

# This file is a part of Hikka Userbot
# Code is NOT licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# requires: lottie rlottie-python

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import os
import io
import json
import gzip
import zipfile

from telethon import types
from telethon.tl.types import Message
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.functions.messages import GetCustomEmojiDocumentsRequest

from lottie.importers.svg import import_svg
from lottie.exporters.core import export_tgs
from lottie.parsers.baseporter import Baseporter
from rlottie_python import LottieAnimation

from .. import loader, utils

@loader.tds
class yg_tgs(loader.Module):
    """Модуль для работы с .tgs (Telegram Animated Sticker)"""

    strings = {
        "name": "yg_tgs",
        "converting": "<emoji document_id=5386367538735104399>⌛</emoji> <b>Converting...</b>",
        "no_reply": "<emoji document_id=5276240711795107620>⚠️</emoji> <i>Reply to an file, animated sticker or custom emoji!</i>",
        "not_svg": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Attached file is not an SVG!</i>",
        "not_json": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Attached file is not a JSON!</i>",
        "not_tgs_or_emoji": "<emoji document_id=5276240711795107620>⚠️</emoji> <i>Reply to an animated sticker or custom emoji!</i>",
        "conversion_error": "<emoji document_id=5278578973595427038>🚫</emoji> <b>Error during conversion:</b> <code>{}</code>",
        "emoji_not_found": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Custom emoji not found!</i>"
    }

    strings_ru = {
        "name": "yg_tgs",
        "converting": "<emoji document_id=5386367538735104399>⌛</emoji> <b>Конвертирую...</b>",
        "no_reply": "<emoji document_id=5276240711795107620>⚠️</emoji> <i>Ответь на файл, анимированный стикер или кастомный эмодзи!</i>",
        "not_svg": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Прикрепленный файл не является SVG!</i>",
        "not_json": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Прикрепленный файл не является JSON!</i>",
        "not_tgs_or_emoji": "<emoji document_id=5276240711795107620>⚠️</emoji> <i>Ответь на анимированный стикер или кастомный эмодзи!</i>",
        "conversion_error": "<emoji document_id=5278578973595427038>🚫</emoji> <b>Ошибка при конвертации:</b> <code>{}</code>",
        "emoji_not_found": "<emoji document_id=5278578973595427038>🚫</emoji> <i>Кастомный эмодзи не найден!</i>"
    }

    @loader.command(ru_doc="<reply to .svg> - конвертировать svg в tgs")
    async def svg2tgscmd(self, msg: Message):
        """<reply to .svg> - convert svg to tgs"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])

        reply = await msg.get_reply_message()
        
        if not reply.file or not reply.file.name.endswith(".svg"):
            await utils.answer(msg, self.strings["not_svg"])
            return
        
        try:
            tgs_buffer = io.BytesIO()
            await reply.download_media(tgs_buffer)
            tgs_buffer.seek(0)
            
            svg_buffer = self.svg2tgs(tgs_buffer.getvalue())
            
            await utils.answer(
                msg,
                svg_buffer,
                attributes=[types.DocumentAttributeFilename("sticker.tgs")],
                reply_to=reply
            )
        except Exception as e:
            await utils.answer(msg, self.strings["conversion_error"].format(str(e)))

    @loader.command(ru_doc="<reply to tgs or custom emoji> - конвертировать tgs в lottie json")
    async def tgs2jsoncmd(self, msg: Message):
        """<reply to tgs or custom emoji> - convert tgs to lottie json"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])
        
        reply = await msg.get_reply_message()
        
        if reply.file and reply.file.name.endswith(".tgs"):
            tgs_buffer = io.BytesIO()
            await reply.download_media(tgs_buffer)
            tgs_buffer.seek(0)
            
            json_buffer = self.tgs2json(tgs_buffer.getvalue())

            await utils.answer(
                msg,
                json_buffer,
                attributes=[types.DocumentAttributeFilename("sticker.json")],
                reply_to=reply
            )
        
        elif reply.entities and isinstance(reply.entities[0], MessageEntityCustomEmoji):
            emoji_id = reply.entities[0].document_id
            data = await msg.client(GetCustomEmojiDocumentsRequest(document_id=[emoji_id]))
            
            if data:
                tgs_buffer = io.BytesIO()
                await msg.client.download_media(data[0], tgs_buffer)
                tgs_buffer.seek(0)

                json_buffer = self.tgs2json(tgs_buffer.getvalue())
                
                await utils.answer(
                    msg,
                    json_buffer,
                    attributes=[types.DocumentAttributeFilename("sticker.json")],
                    reply_to=reply
                )
        else:
            await utils.answer(msg, self.strings["not_tgs_or_emoji"])

    @loader.command(ru_doc="<reply to tgs or custom emoji> - разбить tgs на кадры (ZIP с PNG)")
    async def tgs2pngscmd(self, msg: Message):
        """<reply to tgs or custom emoji> - split tgs into frames (ZIP with PNGs)"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])
        
        reply = await msg.get_reply_message()
        
        if reply.file and reply.file.name.endswith(".tgs"):
            tgs_buffer = io.BytesIO()
            await reply.download_media(tgs_buffer)
            tgs_buffer.seek(0)
            
            pngs_buffer = self.tgs2pngs(tgs_buffer.getvalue())
            pngs_buffer.name = "frames.zip"

            await utils.answer(
                msg,
                pngs_buffer,
                reply_to=reply
            )
        
        elif reply.entities and isinstance(reply.entities[0], MessageEntityCustomEmoji):
            emoji_id = reply.entities[0].document_id
            data = await msg.client(GetCustomEmojiDocumentsRequest(document_id=[emoji_id]))
            
            if data:
                tgs_buffer = io.BytesIO()
                await msg.client.download_media(data[0], tgs_buffer)
                tgs_buffer.seek(0)

                pngs_buffer = self.tgs2pngs(tgs_buffer.getvalue())
                pngs_buffer.name = "frames.zip"
                
                await utils.answer(
                    msg,
                    pngs_buffer,
                    reply_to=reply
                )
        else:
            await utils.answer(msg, self.strings["not_tgs_or_emoji"])

    @loader.command(ru_doc="<reply to .json> - конвертировать lottie json в tgs")
    async def json2tgscmd(self, msg: Message):
        """<reply to .json> - convert lottie json to tgs"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])
        
        reply = await msg.get_reply_message()
        
        if not reply.file or not reply.file.name.endswith(".json"):
            await utils.answer(msg, self.strings["not_json"])
            return
        
        try:
            tgs_buffer = io.BytesIO()
            await reply.download_media(tgs_buffer)
            tgs_buffer.seek(0)
            
            svg_buffer = self.json2tgs(tgs_buffer.getvalue())
            
            await utils.answer(
                msg,
                svg_buffer,
                attributes=[types.DocumentAttributeFilename("sticker.tgs")],
                reply_to=reply
            )
        except Exception as e:
            await utils.answer(msg, self.strings["conversion_error"].format(str(e)))

    @loader.command(ru_doc="<reply to tgs or custom emoji> - конвертировать tgs в gif")
    async def tgs2gifcmd(self, msg: Message):
        """<reply to tgs or custom emoji> - convert tgs to gif"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])
        
        reply = await msg.get_reply_message()
        
        if reply.file and reply.file.name.endswith(".tgs"):
            tgs_buffer = io.BytesIO()
            await reply.download_media(tgs_buffer)
            tgs_buffer.seek(0)
            
            gif_buffer = self.tgs2gif(tgs_buffer.getvalue())
            gif_buffer.name = "sticker.gif"

            await utils.answer(
                msg,
                gif_buffer,
                force_document=False,
                reply_to=reply
            )
        
        elif reply.entities and isinstance(reply.entities[0], MessageEntityCustomEmoji):
            emoji_id = reply.entities[0].document_id
            data = await msg.client(GetCustomEmojiDocumentsRequest(document_id=[emoji_id]))
            
            if data:
                tgs_buffer = io.BytesIO()
                await msg.client.download_media(data[0], tgs_buffer)
                tgs_buffer.seek(0)

                gif_buffer = self.tgs2gif(tgs_buffer.getvalue())
                gif_buffer.name = "sticker.gif"

                await utils.answer(
                    msg,
                    gif_buffer,
                    force_document=False,
                    reply_to=reply.id
                )
        else:
            await utils.answer(msg, self.strings["not_tgs_or_emoji"])

    @loader.command(ru_doc="<reply to custom emoji> - конвертировать кастом эмодзи в tgs")
    async def emoji2tgscmd(self, msg: Message):
        """<reply to custom emoji> - convert custom emoji to tgs"""
        if not msg.reply_to_msg_id:
            await utils.answer(msg, self.strings["no_reply"])
            return
        
        await utils.answer(msg, self.strings["converting"])
        
        reply = await msg.get_reply_message()
        
        if reply.entities and isinstance(reply.entities[0], MessageEntityCustomEmoji):
            emoji_id = reply.entities[0].document_id
            data = await msg.client(GetCustomEmojiDocumentsRequest(document_id=[emoji_id]))
            
            if data:
                tgs_buffer = io.BytesIO()
                await msg.client.download_media(data[0], tgs_buffer)
                tgs_buffer.seek(0)
                
                await utils.answer(
                    msg,
                    tgs_buffer.getvalue(),
                    attributes=[types.DocumentAttributeFilename("sticker.tgs")],
                    reply_to=reply
                )
            else:
                await utils.answer(msg, self.strings["emoji_not_found"])
        else:
            await utils.answer(msg, self.strings["not_tgs_or_emoji"])

    def tgs2json(self, inbytes):
        data = gzip.decompress(inbytes).decode('utf-8')
        return data.encode('utf-8')
    
    def json2tgs(self, inbytes):
        data = json.loads(inbytes.decode("utf-8"))
        compressed = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        buffer = io.BytesIO()

        with gzip.GzipFile(fileobj=buffer, mode="wb", compresslevel=9) as out:
            out.write(compressed.encode("utf-8"))

        return buffer.getvalue()

    def svg2tgs(self, inbytes):
        infile = io.BytesIO(inbytes)
        importer = Baseporter(extensions=["svg", "svgz"],
                              callback=import_svg,
                              name="SVG")

        exporter = Baseporter(extensions=["tgs"],
                              callback=export_tgs,
                              name="Telegram Animated Sticker")

        an = importer.process(infile)
        an.frame_rate = 60
        an.scale(512, 512)

        buffer = io.BytesIO()
        exporter.process(an, buffer)
        buffer.seek(0)
        return buffer
    
    def tgs2gif(self, inbytes):
        temp = "/tmp/output.gif"

        try:
            tgs_stream = io.BytesIO(inbytes)
            anim = LottieAnimation.from_tgs(tgs_stream)

            anim.save_animation(temp, format="gif")

            gif_buffer = io.BytesIO()
            with open(temp, "rb") as gif_file:
                gif_buffer.write(gif_file.read())

            gif_buffer.seek(0)
            return gif_buffer

        finally:
            if os.path.exists(temp):
                os.remove(temp)

    def tgs2pngs(self, inbytes):
        temp = "/tmp/frames.zip"

        try:
            tgs_stream = io.BytesIO(inbytes)
            anim = LottieAnimation.from_tgs(tgs_stream)

            total_frames = anim.lottie_animation_get_totalframe()

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for i in range(total_frames):
                    frame = anim.render_pillow_frame(i)
                    
                    frame_buffer = io.BytesIO()
                    frame.save(frame_buffer, format="PNG")
                    frame_buffer.seek(0)

                    zipf.writestr(f"frame_{i}.png", frame_buffer.getvalue())

            zip_buffer.seek(0)
            return zip_buffer

        finally:
            if os.path.exists(temp):
                os.remove(temp)