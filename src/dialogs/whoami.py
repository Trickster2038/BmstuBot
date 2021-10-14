from aiogram import Dispatcher, types

import dbutils
import settings

async def cmd_whoami(call: types.CallbackQuery):
    if dbutils.is_filled(call.from_user.id):
        await show_profile(call.from_user.id, call.from_user.id, call.bot, False, True, True, True)
    else:
        await call.bot.send_message(call.from_user.id, "Ваш аккаунт не заполнен, зарегистрируйтесь /register")
        # await message.answer("Ваш аккаунт не заполнен, зарегистрируйтесь /register")

async def show_profile(id_check, id_send, bot, with_nick=False, with_id=False, with_moderator=False, with_curator=False):
    data = dbutils.get_info(id_check)
    # faculties = settings.Other.faculties
    trust_mods = ["не подтверждены", "на модерации", "подтверждены"]
    # if with_nick or with_id or with_moderator:
    s = data[0] + " " + data[1] + "\n\n"
    if with_nick:
        s += "username: " + "@" + data[7] + "\n"
    if with_id:
        s += "id: " + str(id_check) + "\n" 
    if with_moderator:
        if data[8]:
            s += "модератор: да\n" 
        else:
            s += "модератор: нет\n"
    if with_curator:
        if data[9]:
            s += "куратор: да\n" 
        else:
            s += "куратор: нет\n" 
    s += "\n" # only for long?
    # else:
    #     s = data[0] + " " + data[1] + "\n\n"
    s += "кафедра: " + data[2] + "-" + str(int(data[3])) + "\n"
    s += "курс: " + str(int(data[4])) + "\n"
    s += "данные аккаунта: " + trust_mods[int(data[5])] + "\n\n"
    s += "О себе: " + data[6]

    if dbutils.avatar_exists(id_check):
        photo = open("../web/proj/media/avatars/" + str(id_check) + ".jpg", 'rb')
    else:
        photo = open("default_avatar.jpg", 'rb')
    await bot.send_photo(chat_id=id_send, photo=photo, caption=s)

async def show_verify(id_check, id_send, bot):
    s = "verification photo"
    if dbutils.verify_exists(id_check):
        photo = open("../web/proj/media/verify/" + str(id_check) + ".jpg", 'rb')
    else:
        photo = open("default_avatar.jpg", 'rb')
    await bot.send_photo(chat_id=id_send, photo=photo, caption=s)

def register_handlers_whoami(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_whoami, lambda call: call.data == "menu_show_profile") 
    # dp.register_message_handler(cmd_whoami, commands="whoami")
