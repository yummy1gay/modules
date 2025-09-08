__version__ = (1, 1, 1, 1)

# This file is a part of Hikka Userbot!
# This product includes software developed by t.me/Fl1yd and t.me/spypm.
# Based on the "SQuotes" module.

# 🌐 https://github.com/hikariatama/Hikka

# You CAN edit this file without direct permission from the author.
# You can redistribute this file with any modifications.

# thx to t.me/LyoSU for github.com/LyoSU/quote-api

# meta developer: @yg_modules
# scope: hikka_only
# scope: hikka_min 1.6.3

# █▄█ █░█ █▀▄▀█ █▀▄▀█ █▄█   █▀▄▀█ █▀█ █▀▄ █▀
# ░█░ █▄█ █░▀░█ █░▀░█ ░█░   █░▀░█ █▄█ █▄▀ ▄█

import base64, io, requests, telethon
from time import gmtime
from typing import List, Optional, Tuple, Union
from PIL import Image, ImageDraw
from telethon.tl import types
from telethon.tl.patched import Message

from .. import loader, utils

class Dick:
    @staticmethod
    def ents(es: types.TypeMessageEntity) -> List[dict]:
        out: List[dict] = []
        if not es: return out
        for e in es:
            try:
                d = e.to_dict(); t = d.pop("_","").replace("MessageEntity","").lower()
                if not t: continue
                mt = {"bold": "bold","italic": "italic","underline": "underline","strikethrough": "strikethrough",
                      "code": "code","pre": "pre","texturl": "text_link","url": "url","email": "email",
                      "phone": "phone_number","mention": "mention",
                      "mentionname": "text_mention","hashtag": "hashtag","cashtag": "cashtag",
                      "botcommand": "bot_command","spoiler": "spoiler","customemoji": "custom_emoji"}.get(t,t)
                it = {"type": mt,"offset": d.get("offset",0),"length": d.get("length",0)}
                if t=="texturl": it["url"]=d.get("url","")
                elif t=="mentionname": it["user"]={"id": d.get("user_id",0)}
                elif t=="customemoji": it["custom_emoji_id"]=str(d.get("document_id",""))
                elif t=="pre": it["language"]=d.get("language","")
                out.append(it)
            except Exception: continue
        return out

    @staticmethod
    def dur(s: Union[int,float]) -> str:
        t=gmtime(s); return (f"{t.tm_hour:02d}:" if t.tm_hour>0 else "")+f"{t.tm_min:02d}:{t.tm_sec:02d}"

    @staticmethod
    def desc(m: Message, rep: bool=False) -> str:
        return (
            "📷 Фото" if m.photo and rep else
            (m.file.emoji+" Стикер") if m.sticker and rep else
            "📹 Видеосообщение" if m.video_note and rep else
            "📹 Видео" if m.video and rep else
            "🖼 GIF" if m.gif else
            "📊 Опрос" if m.poll else
            "📍 Местоположение" if m.geo else
            "👤 Контакт" if m.contact else
            (f"🎵 Голосовое сообщение: {Dick.dur(m.voice.attributes[0].duration)}" if m.voice else
             (f"🎧 Музыка: {Dick.dur(m.audio.attributes[0].duration)} | {m.audio.attributes[0].performer} - {m.audio.attributes[0].title}" if m.audio else
              (f"💾 Файл: {m.file.name}" if isinstance(m.media, types.MessageMediaDocument) and not Dick.pick(m) else
               (f"{m.media.emoticon} Кость: {m.media.value}" if isinstance(m.media, types.MessageMediaDice) else
                (f"Сервисное сообщение: {m.action.to_dict().get('_')}" if isinstance(m, types.MessageService) else "")))))) #)))

    @staticmethod
    def split(name: Optional[str]) -> Tuple[str,str]:
        if not name: return "",""
        p=name.split(); return (p[0], " ".join(p[1:]) if len(p)>1 else "")

    @staticmethod
    def pick(m: Message):
        if m and m.media:
            return m.photo or m.sticker or m.video or m.video_note or m.gif or m.web_preview
        return None

    @staticmethod
    def wf(b: Optional[bytes]) -> List[int]:
        if not b: return []
        n=(len(b)*8)//5
        if not n: return []
        out: List[int]=[]
        last=n-1
        for i in range(last):
            j=i*5; bi,sh=j//8,j%8
            v=int.from_bytes(b[bi:bi+2],"little") if bi+1<len(b) else b[bi]
            out.append((v>>sh)&0b11111)
        j=last*5; bi,sh=j//8,j%8
        v=int.from_bytes(b[bi:bi+2],"little") if bi+1<len(b) else b[bi]
        out.append((v>>sh)&0b11111)
        return out

    @staticmethod
    async def img(b: bytes, circle: bool=False) -> Optional[str]:
        try:
            im=Image.open(io.BytesIO(b))
            if im.mode!="RGBA": im=im.convert("RGBA")
            if circle:
                size=min(im.size)
                mask=Image.new("L",(size,size),0); ImageDraw.Draw(mask).ellipse((0,0,size,size),fill=255)
                sq=Image.new("RGBA",(size,size),(0,0,0,0))
                off=((size-im.width)//2,(size-im.height)//2);  sq.paste(im,off)
                im=Image.composite(sq,Image.new("RGBA",(size,size),(0,0,0,0)),mask)
            o=io.BytesIO(); im.save(o,format="PNG")
            return f"data:image/png;base64,{base64.b64encode(o.getvalue()).decode()}"
        except Exception:
            return None

    @staticmethod
    async def stc(b: bytes) -> Optional[str]:
        try:
            im=Image.open(io.BytesIO(b))
            if im.mode not in ("RGBA","LA"): im=im.convert("RGBA")
            elif im.mode=="LA": im=im.convert("RGBA")
            o=io.BytesIO(); im.save(o,format="PNG")
            return f"data:image/png;base64,{base64.b64encode(o.getvalue()).decode()}"
        except Exception:
            return None

    @staticmethod
    async def proc(cli, obj, m: Message) -> Optional[dict]:
        try:
            if m.voice:
                for a in m.voice.attributes or []:
                    if getattr(a,"voice",False) and hasattr(a,"waveform"):
                        return {"voice":{"waveform":Dick.wf(a.waveform)}}
            b: bytes = await cli.download_media(obj, bytes, thumb=-1)
            if not b: return None
            if m.sticker:
                u=await Dick.stc(b); return {"url": u} if u else None
            u=await Dick.img(b, circle=bool(m.video_note))
            return {"url": u} if u else None
        except Exception:
            return None

    @staticmethod
    async def ava(cli, uid: int) -> Optional[str]:
        try:
            b=await cli.download_profile_photo(uid, bytes)
            if b: return f"data:image/jpeg;base64,{base64.b64encode(b).decode()}"
        except Exception: pass
        return None

    @staticmethod
    async def post(url: str, data: dict):
        try:
            return await utils.run_sync(requests.post, url, json=data, timeout=30)
        except Exception:
            return None

@loader.tds
class Quotes(loader.Module):
    """Модуль для создания цитат из сообщений"""

    strings = {"name": "yg_quotes",
               "no_reply": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Нет реплая на сообщение",
               "processing": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Обработка…",
               "api_processing": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Ожидание ответа API…",
               "api_error": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Ошибка API: {}",
               "loading_media": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Отправка…",
               "no_args_or_reply": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Нет аргументов или реплая",
               "args_error": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Ошибка разбора аргументов. Запрос: <code>{}</code>",
               "too_many_messages": "<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Слишком много сообщений. Максимум: <code>{}</code>"}

    def __init__(self):
        self.config=loader.ModuleConfig(
        loader.ConfigValue("type","quote",
                            lambda:"Тип цитаты",
                            validator=loader.validators.Choice(["quote", "stories"])),
        loader.ConfigValue("bg_color","#162330",
                            lambda:"Цвет фона цитаты (например, #1a1a1a или red)"),
        loader.ConfigValue("width",512,
                            lambda:"Ширина цитаты (px)",
                            validator=loader.validators.Integer(minimum=200,maximum=2000)),
        loader.ConfigValue("height",768,
                            lambda:"Высота цитаты (px)",
                            validator=loader.validators.Integer(minimum=200,maximum=2000)),
        loader.ConfigValue("scale",2,
                            lambda:"Масштаб рендера",
                            validator=loader.validators.Choice([1, 2, 3])),
        loader.ConfigValue("emoji_brand","apple",
                            lambda:"Стиль эмодзи (apple, google, twitter и т.д.)"),
        loader.ConfigValue("max_messages",15,
                            lambda:"Максимальное число сообщений в цитате",
                            validator=loader.validators.Integer(minimum=1,maximum=50)),
        loader.ConfigValue("endpoint","https://kok.gay/gayotes/generate",
                            lambda:"URL API-эндпоинта (можешь поднять локально - github.com/yummy1gay/quote-api)",
                            validator=loader.validators.Link()))

    async def client_ready(self, client, db):
        self.client=client; self.db=db

    async def qcmd(self, m: Message):
        """
        Обычные цитаты:
        • .q — процитировать одно сообщение из реплая
        • .q 2 — процитировать 2 сообщения
        • .q 3 #2d2d2d — 3 сообщения на тёмном фоне
        • .q pink — фон по имени цвета
        • .q !file — отправить как файл (PNG)
        """
        try:
            args=utils.get_args(m); rep=await m.get_reply_message()
            if not rep: return await utils.answer(m,self.strings["no_reply"])
            st=await utils.answer(m,self.strings["processing"])
            doc="!file" in args
            n=next((int(a) for a in args if a.isdigit() and int(a)>0),1)
            bg=next((a for a in args if a!="!file" and not a.isdigit()), self.config["bg_color"])
            if n>self.config["max_messages"]:
                return await utils.answer(st,self.strings["too_many_messages"].format(self.config["max_messages"]))

            js=await self.parse(m,n)
            if not js: return await utils.answer(st,self.strings["api_error"].format("Не удалось собрать сообщения"))

            pay={"backgroundColor":bg,"width":self.config["width"],"height":self.config["height"],
                 "scale":self.config["scale"],"emojiBrand":self.config["emoji_brand"],"messages":js,
                 "format": "webp" if not doc else "png", "type": self.config["type"]}

            await utils.answer(st,self.strings["api_processing"])
            r=await Dick.post(f"{self.config['endpoint']}.webp",pay)
            if not r or r.status_code!=200:
                try: err=r.json().get("error",f"HTTP {r.status_code}") if r else "Нетворк еррорь"
                except Exception: err=f"HTTP {r.status_code}" if r else "Нетворк еррорь"
                return await utils.answer(st,self.strings["api_error"].format(err))

            buf=io.BytesIO(r.content); buf.name="YgQuote"+(".png" if doc else ".webp")
            await utils.answer(st,buf,force_document=doc)
        except Exception as e:
            return await utils.answer(m,f"<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Ошибка: {e}")

    async def fqcmd(self, m: Message):
        """
        Фейковые цитаты:
        • .fq <@ или ID> <текст> — цитата от пользователя
        • .fq <reply> <текст> — цитата от автора реплая
        • .fq <@/ID> <текст> -r <@/ID> <текст> — с ответом
        • .fq user1 текст; user2 текст — несколько сообщений
        """
        try:
            raw=utils.get_args_raw(m); rep=await m.get_reply_message()
            if not (raw or rep): return await utils.answer(m,self.strings["no_args_or_reply"])
            st= await utils.answer(m,self.strings["processing"])
            try: js=await self.fake(raw,rep)
            except (IndexError,ValueError): return await utils.answer(st,self.strings["args_error"].format(m.text))
            if len(js)>self.config["max_messages"]:
                return await utils.answer(st,self.strings["too_many_messages"].format(self.config["max_messages"]))

            dickk={"backgroundColor":self.config["bg_color"],"width":self.config["width"],"height":self.config["height"],
                 "scale":self.config["scale"],"emojiBrand":self.config["emoji_brand"],"messages":js,
                "format": "webp","type":self.config["type"]}

            await utils.answer(st,self.strings["api_processing"])
            r=await Dick.post(f"{self.config['endpoint']}.webp",dickk)
            if not r or r.status_code!=200:
                try: err=r.json().get("error",f"HTTP {r.status_code}") if r else "Нетворк еррорь"
                except Exception: err=f"HTTP {r.status_code}" if r else "Нетворк еррорь"
                return await utils.answer(st,self.strings["api_error"].format(err))

            buf=io.BytesIO(r.content); buf.name="YgQuote.webp"
            await utils.answer(st,buf)
        except Exception as e:
            return await utils.answer(m,f"<emoji document_id=6321272741005624970>🏳️‍🌈</emoji> Ошибка: {e}")

    async def parse(self, trg: Message, n: int) -> Optional[List[dict]]:
        try:
            rep= await trg.get_reply_message()
            lst: List[Message]=[mm async for mm in self.client.iter_messages(trg.chat_id,limit=n,reverse=True,add_offset=1,offset_id=rep.id if rep else None)]
        except Exception:
            return None

        out: List[dict]=[]
        for mm in lst:
            try:
                u=await self.who(mm)
                if not u: continue
                name=telethon.utils.get_display_name(u); f,l=Dick.split(name)
                ava=await Dick.ava(self.client,getattr(u,"id",0)) if getattr(u,"id",None) else None

                rb=None
                try:
                    r=await mm.get_reply_message()
                    if r:
                        rname=telethon.utils.get_display_name(r.sender)
                        rtxt=Dick.desc(r,True)
                        if r.raw_text: rtxt=(rtxt+". "+r.raw_text) if rtxt else r.raw_text
                        rb={"name":rname,"text":rtxt or "","entities":Dick.ents(r.entities),
                            "chatId": r.sender.id if r.sender else mm.chat_id,"from":{"name":rname}}
                except Exception: rb=None

                med=None; obj=Dick.pick(mm)
                if obj: med=await Dick.proc(self.client,obj,mm)

                txt=mm.raw_text or ""; ad=Dick.desc(mm)
                if ad: txt=f"{txt}\n\n{ad}" if txt else ad

                item={"from":{"id":getattr(u,"id", 0),"first_name":getattr(u,"first_name","") or f,"last_name":getattr(u,"last_name","") or l,
                               "username":getattr(u,"username",None),"name":name,"photo":{"url":ava} if ava else {}},
                      "text":txt,"entities":Dick.ents(mm.entities),"avatar":True}

                try:
                    if mm.voice:
                        a = next((a for a in mm.voice.attributes or [] 
                                if getattr(a, "voice", False) and hasattr(a, "waveform")), None)
                        if a: item["voice"] = {"waveform": Dick.wf(a.waveform)}
                except Exception: pass

                if med: item["voice" if "voice" in med else "media"] = med.get("voice", med)

                es=getattr(u,"emoji_status",None)
                if getattr(es,"document_id",None): item["from"]["emoji_status"]=str(es.document_id)
                if rb: item["replyMessage"]=rb
                out.append(item)
            except Exception: continue
        return out

    async def who(self, m: Message):
        try:
            if m.fwd_from:
                if m.fwd_from.from_id:
                    pid=m.fwd_from.from_id
                    uid=pid.channel_id if isinstance(pid, types.PeerChannel) else pid.user_id
                    try: return await self.client.get_entity(uid)
                    except Exception: return m.sender
                if m.fwd_from.from_name:
                    return types.User(
                        id=hash(m.fwd_from.from_name)%2147483647, first_name=m.fwd_from.from_name,
                        username=None, phone=None, bot=False, verified=False, restricted=False,
                        scam=False, fake=False, premium=False)
            return m.sender
        except Exception:
            return m.sender

    async def fake(self, args: str, rep: Optional[Message]) -> List[dict]:
        async def tok(ch: str):
            p=ch.split()
            if not p: return None,""
            who=p[0]; tx=ch.split(maxsplit=1)[1] if len(p)>1 else ""
            try:
                u=await self.client.get_entity(int(who) if who.isdigit() else who)
                return u,tx
            except Exception:
                return None,tx

        if rep and not args:
            u=rep.sender; name=telethon.utils.get_display_name(u); f,l=Dick.split(name)
            ava=await Dick.ava(self.client,u.id) if getattr(u,"id",None) else None
            msg={"from":{"id":u.id,"first_name":getattr(u,"first_name","") or f,"last_name":getattr(u,"last_name","") or l,
                         "username":getattr(u,"username",None),"name":name,"photo":{"url":ava} if ava else {}},
                 "text":"","entities":[], "avatar":True}
            es=getattr(u,"emoji_status",None)
            if getattr(es,"document_id", None): msg["from"]["emoji_status"]=str(es.document_id)
            return [msg]

        if rep and args:
            u=rep.sender
            return await self.fake(f"{getattr(u,'id','')} {args}", None)

        out: List[dict]=[]
        for part in args.split("; "):
            try:
                rb=None
                if " -r " in part:
                    a,b=part.split(" -r ",1); u1,t1=await tok(a); u2,t2=await tok(b)
                else:
                    u1,t1=await tok(part); u2,t2=None,None
                if not u1: continue

                name=telethon.utils.get_display_name(u1); f,l=Dick.split(name)
                ava=await Dick.ava(self.client,u1.id)

                if u2:
                    name2=telethon.utils.get_display_name(u2); ava2=await Dick.ava(self.client,u2.id)
                    rb={"name":name2,"text":t2,"entities":[],"chatId":u2.id,"from":{"name":name2,"photo":{"url":ava2} if ava2 else {}}}

                msg={"from":{"id":u1.id,"first_name":getattr(u1,"first_name","") or f,"last_name":getattr(u1,"last_name","") or l,
                             "username":getattr(u1,"username",None),"name":name,"photo":{"url":ava} if ava else {}},
                     "text":t1,"entities":[], "avatar":True}

                es=getattr(u1,"emoji_status",None)
                if getattr(es,"document_id",None): msg["from"]["emoji_status"]=str(es.document_id)
                if rb: msg["replyMessage"]=rb
                out.append(msg)
            except Exception: continue
        return out