#dev: @yummy_gay

from telethon import TelegramClient, events, Button

api_id = '9609511'
api_hash = '066c47a00d147eb82ccd6af1f7bc7826'
bot_token = '6572233598:AAE14WYwDdqmueyhUlNUGftViYo46gA2Ats'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline("Альбомы", b"albums"), Button.inline("Синглы", b"singles")]
    ]
    await event.respond(f"👋 <i>Привет! В этом боте собраны песни Инстасамки из альбомов:\n\n</i>"
                        f"💿 <b>Sped Up Album</b>\n"
                        f"💿 <b>Popstar</b>\n"
                        f"💿 <b>Queen Of Rap</b>\n"
                        f"💿 <b>Moneydealer</b>\n\n"
                        f"💾 <i>А так же ее синглы 2020-2023, выбери что хочешь слушать нажав одну из кнопок ниже 👇🏻</i>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/albums'))
async def albums(event):
    buttons = [
        [Button.inline("Sped Up Album", b"sped_up_album"), Button.inline("Popstar", b"popstar_album")],
        [Button.inline("Queen Of Rap", b"queen_of_rap_album"), Button.inline("Moneydealer", b"moneydealer_album")],
        [Button.inline("‹ Назад", b"back_to_menu")]
    ]
    await event.respond("<b>💿 Выбери альбом который хочешь полушать 👇🏻</b>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"albums"))
async def albums(event):
    buttons = [
        [Button.inline("Sped Up Album", b"sped_up_album"), Button.inline("Popstar", b"popstar_album")],
        [Button.inline("Queen Of Rap", b"queen_of_rap_album"), Button.inline("Moneydealer", b"moneydealer_album")],
        [Button.inline("‹ Назад", b"back_to_menu")]
    ]
    await event.edit("<b>💿 Выбери альбом который хочешь полушать 👇🏻</b>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/singles'))
async def singles(event):
    buttons = [
        [Button.inline("Who I Am", b"who_i_am"), Button.inline("Mommy", b"mommy_single")],
        [Button.inline("Бизнес Класс", b"biznes_klass"), Button.inline("В Моей Голове", b"v_moey_golove")],
        [Button.inline("Bestie", b"bestie"), Button.inline("Отключаю Телефон (slow)", b"otklychay_telefon_slow")],
        [Button.inline("Тяги", b"tyagi"), Button.inline("Жара", b"djara")],
        [Button.inline("Отключаю Телефон", b"otklychay_telefon"), Button.inline("За Деньги Да", b"3a_dengi_da")],
        [Button.inline("Волосы Назад", b"volosi_nazad"), Button.inline("Popstar", b"popstar_single")],
        [Button.inline("RaRaRa", b"rarar_single"), Button.inline("Снова?", b"snova_single")],
        [Button.inline("Shake", b"shake_single"), Button.inline("Витон 2", b"viton_dva")],
        [Button.inline("Lipsi Ha", b"lipsi_ha_single"), Button.inline("Terminal", b"terminal")],
        [Button.inline("Juicy", b"juicy_single"), Button.inline("Money Day", b"moneyday_single")],
        [Button.inline("Факт", b"fakt_single"), Button.inline("Витон", b"viton")],
        [Button.inline("‹ Назад", b"back_to_menu")]
    ]
    await event.respond("💾 <b>Синглы</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"singles"))
async def singles(event):
    buttons = [
        [Button.inline("Who I Am", b"who_i_am"), Button.inline("Mommy", b"mommy_single")],
        [Button.inline("Бизнес Класс", b"biznes_klass"), Button.inline("В Моей Голове", b"v_moey_golove")],
        [Button.inline("Bestie", b"bestie"), Button.inline("Отключаю Телефон (slow)", b"otklychay_telefon_slow")],
        [Button.inline("Тяги", b"tyagi"), Button.inline("Жара", b"djara")],
        [Button.inline("Отключаю Телефон", b"otklychay_telefon"), Button.inline("За Деньги Да", b"3a_dengi_da")],
        [Button.inline("Волосы Назад", b"volosi_nazad"), Button.inline("Popstar", b"popstar_single")],
        [Button.inline("RaRaRa", b"rarar_single"), Button.inline("Снова?", b"snova_single")],
        [Button.inline("Shake", b"shake_single"), Button.inline("Витон 2", b"viton_dva")],
        [Button.inline("Lipsi Ha", b"lipsi_ha_single"), Button.inline("Terminal", b"terminal")],
        [Button.inline("Juicy", b"juicy_single"), Button.inline("Money Day", b"moneyday_single")],
        [Button.inline("Факт", b"fakt_single"), Button.inline("Витон", b"viton")],
        [Button.inline("‹ Назад", b"back_to_menu")]
    ]
    await event.edit("💾 <b>Синглы</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/spedupalbum'))
async def sped_up_album(event):
    buttons = [
        [Button.inline("Как Mommy", b"kak_mommy_sped"), Button.inline("За Деньги Да", b"za_dengi_da_sped")],
        [Button.inline("Moneyken Love", b"moneyken_love_sped"), Button.inline("Хлопай", b"hlopai_sped")],
        [Button.inline("Бич Плис", b"bi4_plis_sped"), Button.inline("DaDaDa", b"dadada_sped")],
        [Button.inline("Lipsi Ha", b"lipsi_ha_sped"), Button.inline("Popstar", b"popstar_sped")],
        [Button.inline("Facetime", b"facetime_sped"), Button.inline("Факт", b"fakt_sped")],
        [Button.inline("Go Go", b"go_go_sped"), Button.inline("Жопа Джуси", b"jopa_juicy_sped")],
        [Button.inline("И ЧТОЭ", b"i_chtoe_sped"), Button.inline("Mommy", b"mommy_sped")],
        [Button.inline("Money Day", b"money_day_sped"), Button.inline("Moneydealer", b"moneydealer_sped")],
        [Button.inline("RaRaRa", b"rarara_sped"), Button.inline("Shake", b"shake_sped")],
        [Button.inline("Снова?", b"snova_sped"), Button.inline("Этот Огонь", b"etot_ogon_sped")],
        [Button.inline("Что Ты Хочешь", b"chto_ti_xo4esh_sped"), Button.inline("Сто Раз", b"sto_raz_sped")],
        [Button.inline("Волчок", b"vol4ek_sped"), Button.inline("Три Слова", b"tri_slova_sped")],
        [Button.inline("Эй Проснись", b"ei_prosnis_sped"), Button.inline("Worldstar", b"worldstar_sped")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.respond("<b>💿 Альбом: Sped Up Album</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"sped_up_album"))
async def sped_up_album(event):
    buttons = [
        [Button.inline("Как Mommy", b"kak_mommy_sped"), Button.inline("За Деньги Да", b"za_dengi_da_sped")],
        [Button.inline("Moneyken Love", b"moneyken_love_sped"), Button.inline("Хлопай", b"hlopai_sped")],
        [Button.inline("Бич Плис", b"bi4_plis_sped"), Button.inline("DaDaDa", b"dadada_sped")],
        [Button.inline("Lipsi Ha", b"lipsi_ha_sped"), Button.inline("Popstar", b"popstar_sped")],
        [Button.inline("Facetime", b"facetime_sped"), Button.inline("Факт", b"fakt_sped")],
        [Button.inline("Go Go", b"go_go_sped"), Button.inline("Жопа Джуси", b"jopa_juicy_sped")],
        [Button.inline("И ЧТОЭ", b"i_chtoe_sped"), Button.inline("Mommy", b"mommy_sped")],
        [Button.inline("Money Day", b"money_day_sped"), Button.inline("Moneydealer", b"moneydealer_sped")],
        [Button.inline("RaRaRa", b"rarara_sped"), Button.inline("Shake", b"shake_sped")],
        [Button.inline("Снова?", b"snova_sped"), Button.inline("Этот Огонь", b"etot_ogon_sped")],
        [Button.inline("Что Ты Хочешь", b"chto_ti_xo4esh_sped"), Button.inline("Сто Раз", b"sto_raz_sped")],
        [Button.inline("Волчок", b"vol4ek_sped"), Button.inline("Три Слова", b"tri_slova_sped")],
        [Button.inline("Эй Проснись", b"ei_prosnis_sped"), Button.inline("Worldstar", b"worldstar_sped")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.edit("<b>💿 Альбом: Sped Up Album</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/popstar'))
async def popstar(event):
    buttons = [
        [Button.inline("Этот Огонь", b"etot_ogon_popstar"), Button.inline("Что Ты Хочешь", b"chto_ti_xochesh_popstar")],
        [Button.inline("Волчок", b"volchek_popstar"), Button.inline("За Деньги Да", b"za_dengi_da_popstar")],
        [Button.inline("Сто Раз", b"sto_raz_popstar"), Button.inline("Три Слова", b"tri_slova_popstar")],
        [Button.inline("Popstar", b"popstar_popstar"), Button.inline("Эй Проснись", b"ei_prosnis_popstar")],
        [Button.inline("Как Mommy", b"kak_mommy_popstar"), Button.inline("Волосы Назад", b"volosy_nazad_popstar")],
        [Button.inline("World Star", b"world_star_popstar")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.respond("<b>💿 Альбом: Popstar</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"popstar_album"))
async def popstar(event):
    buttons = [
        [Button.inline("Этот Огонь", b"etot_ogon_popstar"), Button.inline("Что Ты Хочешь", b"chto_ti_xochesh_popstar")],
        [Button.inline("Волчок", b"volchek_popstar"), Button.inline("За Деньги Да", b"za_dengi_da_popstar")],
        [Button.inline("Сто Раз", b"sto_raz_popstar"), Button.inline("Три Слова", b"tri_slova_popstar")],
        [Button.inline("Popstar", b"popstar_popstar"), Button.inline("Эй Проснись", b"ei_prosnis_popstar")],
        [Button.inline("Как Mommy", b"kak_mommy_popstar"), Button.inline("Волосы Назад", b"volosy_nazad_popstar")],
        [Button.inline("World Star", b"world_star_popstar")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.edit("<b>💿 Альбом: Popstar</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/queenofrap'))
async def queen_of_rap(event):
    buttons = [
        [Button.inline("RaRaRa", b"rarara_queenofrap"), Button.inline("Balance", b"balance_queenofrap")],
        [Button.inline("Walking", b"walking_queenofrap"), Button.inline("Goyard", b"goyard_queenofrap")],
        [Button.inline("Toxic", b"toxic_queenofrap"), Button.inline("Juicy Drill", b"juicy_drill_queenofrap")],
        [Button.inline("Hate Me", b"hate_me_queenofrap"), Button.inline("Jimmy Choo", b"jimmy_choo_queenofrap")],
        [Button.inline("Pussy P", b"pussy_p_queenofrap"), Button.inline("Oh Mama", b"oh_mama_queenofrap")],
        [Button.inline("Lipsi Hi", b"lipsi_hi_queenofrap"), Button.inline("Six Bitches", b"six_bitches_queenofrap")],
        [Button.inline("Go Go", b"go_go_queenofrap"), Button.inline("Moneyken Love", b"moneyken_love_queenofrap")],
        [Button.inline("Instasamka Is", b"instasamka_is_queenofrap")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.respond("<b>💿 Альбом: Queen Of Rap</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"queen_of_rap_album"))
async def queen_of_rap(event):
    buttons = [
        [Button.inline("RaRaRa", b"rarara_queenofrap"), Button.inline("Balance", b"balance_queenofrap")],
        [Button.inline("Walking", b"walking_queenofrap"), Button.inline("Goyard", b"goyard_queenofrap")],
        [Button.inline("Toxic", b"toxic_queenofrap"), Button.inline("Juicy Drill", b"juicy_drill_queenofrap")],
        [Button.inline("Hate Me", b"hate_me_queenofrap"), Button.inline("Jimmy Choo", b"jimmy_choo_queenofrap")],
        [Button.inline("Pussy P", b"pussy_p_queenofrap"), Button.inline("Oh Mama", b"oh_mama_queenofrap")],
        [Button.inline("Lipsi Hi", b"lipsi_hi_queenofrap"), Button.inline("Six Bitches", b"six_bitches_queenofrap")],
        [Button.inline("Go Go", b"go_go_queenofrap"), Button.inline("Moneyken Love", b"moneyken_love_queenofrap")],
        [Button.inline("Instasamka Is", b"instasamka_is_queenofrap")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.edit("<b>💿 Альбом: Queen Of Rap</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.NewMessage(pattern='/moneydealer'))
async def moneydealer(event):
    buttons = [
        [Button.inline("Facetime", b"facetime_moneydealer"), Button.inline("Lipsi Ha", b"lipsi_ha_moneydealer")],
        [Button.inline("Juicy", b"juicy_moneydealer"), Button.inline("Moneydealer", b"moneydealer_moneydealer")],
        [Button.inline("DaDaDa", b"dadada_moneydealer"), Button.inline("Хлопай", b"hlopai_moneydealer")],
        [Button.inline("И ЧТОЭ", b"i_chtoe_moneydealer")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.respond("<b>💿 Альбом: Moneydealer</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"moneydealer_album"))
async def moneydealer(event):
    buttons = [
        [Button.inline("Facetime", b"facetime_moneydealer"), Button.inline("Lipsi Ha", b"lipsi_ha_moneydealer")],
        [Button.inline("Juicy", b"juicy_moneydealer"), Button.inline("Moneydealer", b"moneydealer_moneydealer")],
        [Button.inline("DaDaDa", b"dadada_moneydealer"), Button.inline("Хлопай", b"hlopai_moneydealer")],
        [Button.inline("И ЧТОЭ", b"i_chtoe_moneydealer")],
        [Button.inline("‹ Назад", b"back_to_albums")]
    ]
    await event.edit("<b>💿 Альбом: Moneydealer</b>\n<i>🔊 Выбери песню которую хочешь послушать 👇🏻</i>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"back_to_albums"))
async def back_to_albums(event):
    buttons = [
        [Button.inline("Sped Up Album", b"sped_up_album"), Button.inline("Popstar", b"popstar_album")],
        [Button.inline("Queen Of Rap", b"queen_of_rap_album"), Button.inline("Moneydealer", b"moneydealer_album")],
        [Button.inline("‹ Назад", b"back_to_menu")]
    ]
    await event.edit("<b>💿 Выбери альбом который хочешь полушать 👇🏻</b>\n\n<b>(dev:</b> <code>@yummy_gay</code><b>)</code>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"back_to_menu"))
async def back_to_menu(event):
    buttons = [
        [Button.inline("Альбомы", b"albums"), Button.inline("Синглы", b"singles")]
    ]
    await event.edit(f"👋 <i>Привет! В этом боте собраны песни Инстасамки из альбомов:\n\n</i>"
                    f"💿 <b>Sped Up Album</b>\n"
                    f"💿 <b>Popstar</b>\n"
                    f"💿 <b>Queen Of Rap</b>\n"
                    f"💿 <b>Moneydealer</b>\n\n"
                    f"💾 <i>А так же ее синглы 2020-2023, выбери что хочешь слушать нажав одну из кнопок ниже 👇🏻</i>", buttons=buttons, parse_mode='html')

@client.on(events.CallbackQuery(data=b"kak_mommy_sped"))
async def kak_mommy_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/2",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"moneyken_love_sped"))
async def moneyken_love_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/3",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"bi4_plis_sped"))
async def bi4_plis_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/4",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"lipsi_ha_sped"))
async def lipsi_ha_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/5",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"facetime_sped"))
async def facetime_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/6",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"go_go_sped"))
async def go_go_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/7",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"i_chtoe_sped"))
async def i_chtoe_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/8",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"money_day_sped"))
async def money_day_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/9",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"rarara_sped"))
async def rarara_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/10",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"snova_sped"))
async def snova_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/11",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"chto_ti_xo4esh_sped"))
async def chto_ti_xo4esh_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/12",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"vol4ek_sped"))
async def vol4ek_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/13",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"ei_prosnis_sped"))
async def ei_prosnis_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/14",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"za_dengi_da_sped"))
async def za_dengi_da_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/15",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"hlopai_sped"))
async def hlopai_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/16",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"dadada_sped"))
async def dadada_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/17",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"popstar_sped"))
async def popstar_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/18",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"fakt_sped"))
async def fakt_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/19",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"jopa_juicy_sped"))
async def jopa_juicy_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/20",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"mommy_sped"))
async def mommy_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/21",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"moneydealer_sped"))
async def moneydealer_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/22",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"shake_sped"))
async def shake_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/23",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"etot_ogon_sped"))
async def etot_ogon_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/24",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"sto_raz_sped"))
async def sto_raz_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/25",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"tri_slova_sped"))
async def tri_slova_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/26",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"worldstar_sped"))
async def worldstar_sped(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/27",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"etot_ogon_popstar"))
async def etot_ogon_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/28",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"chto_ti_xochesh_popstar"))
async def chto_ti_xo4esh_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/29",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"volchek_popstar"))
async def volchek_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/30",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"za_dengi_da_popstar"))
async def za_dengi_da_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/31",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"sto_raz_popstar"))
async def sto_raz_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/32",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"tri_slova_popstar"))
async def tri_slova_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/33",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"popstar_popstar"))
async def popstar_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/34",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"ei_prosnis_popstar"))
async def ei_prosnis_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/35",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"kak_mommy_popstar"))
async def kak_mommy_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/36",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"volosy_nazad_popstar"))
async def volosy_nazad_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/37",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"world_star_popstar"))
async def world_star_popstar(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/38",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"rarara_queenofrap"))
async def rarara_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/39",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"balance_queenofrap"))
async def balance_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/40",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"walking_queenofrap"))
async def walking_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/41",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"goyard_queenofrap"))
async def goyard_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/42",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"toxic_queenofrap"))
async def toxic_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/43",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"juicy_drill_queenofrap"))
async def juicy_drill_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/44",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"hate_me_queenofrap"))
async def hate_me_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/45",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"jimmy_choo_queenofrap"))
async def jimmy_choo_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/46",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"pussy_p_queenofrap"))
async def pussy_p_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/47",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"oh_mama_queenofrap"))
async def oh_mama_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/48",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"lipsi_hi_queenofrap"))
async def lipsi_hi_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/49",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"six_bitches_queenofrap"))
async def six_bitches_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/50",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"go_go_queenofrap"))
async def go_go_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/51",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"moneyken_love_queenofrap"))
async def moneyken_love_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/52",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"instasamka_is_queenofrap"))
async def instasamka_is_queenofrap(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/53",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"facetime_moneydealer"))
async def facetime_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/54",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"lipsi_ha_moneydealer"))
async def lipsi_ha_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/55",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"juicy_moneydealer"))
async def juicy_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/56",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"moneydealer_moneydealer"))
async def moneydealer_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/57",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"dadada_moneydealer"))
async def dadada_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/58",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"hlopai_moneydealer"))
async def hlopai_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/59",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"i_chtoe_moneydealer"))
async def i_chtoe_moneydealer(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/60",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"who_i_am"))
async def who_i_am(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/61",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

@client.on(events.CallbackQuery(data=b"biznes_klass"))
async def biznes_klass(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/62",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"v_moey_golove"))
async def v_moey_golove(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/63",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"bestie"))
async def bestie(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/64",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"otklychay_telefon_slow"))
async def otklychay_telefon_slow(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/65",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"tyagi"))
async def tyagi(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/66",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"djara"))
async def djara(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/67",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"otklychay_telefon"))
async def otklychay_telefon(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/68",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"3a_dengi_da"))
async def za_dengi_da(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/69",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"volosi_nazad"))
async def volosi_nazad(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/70",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"popstar_single"))
async def popstar_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/71",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"rarar_single"))
async def rarar_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/72",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"snova_single"))
async def snova_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/73",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"shake_single"))
async def shake_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/74",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"viton_dva"))
async def viton_dva(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/75",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"lipsi_ha_single"))
async def lipsi_ha_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/76",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"terminal"))
async def terminal(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/77",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"juicy_single"))
async def juicy_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/78",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"moneyday_single"))
async def moneyday_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/79",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"mommy_single"))
async def mommy_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/80",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"fakt_single"))
async def fakt_single(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/81",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )
@client.on(events.CallbackQuery(data=b"viton"))
async def viton(event):
    await client.send_file(
        event.chat_id,
        "https://t.me/yg_instasamka/82",
        caption="<i><b>@yg_instasamkabot</b></i>",
        parse_mode='html'
    )

client.run_until_disconnected()