#meta developer: @D4n13l3k00, @yummy1gay

import os
from asyncio import sleep

from telethon import functions, types
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest

from .. import loader, utils  # type: ignore

@loader.tds
class CuMod(loader.Module):
    """Полное копирование юзера (ава, имя|фамилия, био, эмодзи статус)"""

    strings = {"name": "CopyUser"}

    @loader.owner
    async def cucmd(self, message):
        """.cu <s> <a> <reply/@username>
        <s> - Скрытый режим
        <a> - Удалить ваши аватарки
        Аргументы после юзера не указывайте, не скушает
        Примеры:
        .cu s @user/reply
        .cu a @user/reply
        .cu s a @user/reply"""
        reply = await message.get_reply_message()
        user = None
        s = False
        a = False
        if utils.get_args_raw(message):
            args = utils.get_args_raw(message).split(" ")
            for i in args:
                if i.lower() == "s":
                    s = True
                elif i.lower() in ["а", "a"]:
                    a = True
                else:
                    try:
                        user = await message.client.get_entity(i)
                        break
                    except Exception:
                        continue
        if user is None and reply is not None:
            user = reply.sender
        if user is None and reply is None:
            if not s:
                await message.edit("Кого?")
            return
        if s:
            await message.delete()
        if not s:
            for i in range(11):
                await message.edit(
                    "Получаем доступ к аккаунту пользователя"
                    f" [{i*10}%]\n[{(i*'#').ljust(10, '–')}]"
                )
                await sleep(0.3)
        if a:
            avs = await message.client.get_profile_photos("me")
            if len(avs) > 0:
                await message.client(
                    functions.photos.DeletePhotosRequest(
                        await message.client.get_profile_photos("me")
                    )
                )
        full = await message.client(GetFullUserRequest(user.id))
        if not s:
            await message.edit("Получаем аватарку... [35%]\n[###–––––––]")
        if full.full_user.profile_photo:
            user_directory = "./downloads"
            if not os.path.exists(user_directory):
                os.makedirs(user_directory)
            photo_file = await message.client.download_profile_photo(user.id, file=bytes)
            photo_path = os.path.join(user_directory, f'{user.id}_profile.jpg')
            with open(photo_path, 'wb') as file:
                file.write(photo_file)
            if not s:
                await message.edit("Ставим аватарку... [50%]\n[#####–––––]")
            file = await message.client.upload_file(photo_path)
            await message.client(functions.photos.UploadProfilePhotoRequest(file=file))
            os.remove(photo_path)
        if not s:
            await message.edit("Получаем данные...  [99%]\n[#########–]")
        user_info = full.users[0]
        await message.client(
            UpdateProfileRequest(
                first_name=user_info.first_name if user_info.first_name is not None else "",
                last_name=user_info.last_name if user_info.last_name is not None else "",
                about=full.full_user.about[:70] if full.full_user.about is not None else "",
            )
        )
        if user_info.emoji_status:
            await message.client(
                UpdateEmojiStatusRequest(
                    emoji_status=types.EmojiStatus(
                        document_id=user_info.emoji_status.document_id
                    )
                )
            )
        if not s:
            await message.edit("Аккаунт клонирован! [100%]\n[##########]")
            await sleep(5)
            await message.edit("Аккаунт клонирован!")
