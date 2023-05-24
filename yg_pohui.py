# meta developer: @yummy_gay

from .. import loader, utils
import random


pohuipon = [
    "Мне <b>похуй</b><emoji document_id=5823537588186647980>✅</emoji>", 
    "<b>Похуй<emoji document_id=5823537588186647980>✅</emoji></b>", 
    "Ой, прикинь, мне <b>похуй</b>", 
    "Хмм.. кажется.. мне <b>похуй</b>.. :(", 
    "Абсолютно <b>похуй</b><emoji document_id=5823537588186647980>✅</emoji>", 
    "Какой смысл этого сообщения вообще, если мне <b>похуй</b> на все твои высеры", 
    "Что? Извини, я думал мне <b>похуй</b>", 
    "Не ной и не жалуйся - мне <b>похуй</b> на твои проблемы",
    "Есть один ньюанс, мне <b>похуй</b>..",
    "Моё второе имя - <b>похуист</b>, как дамаешь что это значит?"
]


@loader.tds
class PohuiMod(loader.Module):
    strings = {
        "name": "Похуй-похуй-мне"
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self.users = self.db.get("pohui", "users", [])
        self.phrases = self.db.get("pohui", "phrases", [])
    
    def add_phrase(self, phrase: str):
        self.phrases.append(phrase)
        self.db.set("pohui", "phrases", self.phrases)
    
    def add_user(self, user_id: int):
        self.users.append(user_id)
        self.db.set("pohui", "users", self.users)
    
    def remove_user(self, user_id: int):
        self.users.remove(user_id)
        self.db.set("pohui", "users", self.users)
    
    async def deltpohuicmd(self, message):
        """очистить список челов на которых тебе похуй"""
        
        self.users = []
        self.db.set("pohui", "users", self.users)
        
        await utils.answer(
            message=message,
            response="<b>Список челов на которых тебе похуй очищен</b>"
        )
    
    async def pohuicmd(self, message):
        """<reply> добавить в список челов на которых тебе похуй"""
        
        reply = await message.get_reply_message()
        
        if reply is not None:
            if reply.from_id is not None:
                await utils.answer(
                    message=message,
                    response="Теперь мне на тебя похуй"
                )

                self.add_user(reply.from_id)
            
            else:
                await utils.answer(
                    message=message,
                    response="<b>🚫 Модуль не работает на анонимных администраторах или каналах</b>"
                )

        else:
            await utils.answer(
                message=message,
                response="<b>🚫 Нужен реплай</b>"
            )
    
    async def nepohuicmd(self, message):
        """<reply> убрать человека из списка челов на которых тебе похуй"""
        
        reply = await message.get_reply_message()
        
        if reply is not None:
            await utils.answer(
                message=message,
                response="Ладно, больше мне на тебя не похуй"
            )
            
            try:
                self.remove_user(reply.from_id)
            except:
                await utils.answer(
                    message=message,
                    response="<b>Человека нету в списке челов на которых тебе похуй</b>"
                )

        else:
            await utils.answer(
                message=message,
                response="<b>🚫 Нужен реплай</b>"
            )
    
    async def watcher(self, message):
        if getattr(message, "from_id", None) in self.users:
            await message.reply(random.choice(pohuipon + self.phrases))