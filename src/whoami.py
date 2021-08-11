from aiogram import Dispatcher, types

import dbutils
import settings

async def cmd_whoami(message: types.Message):
    if dbutils.is_filled(message.from_user.id):
        await show_profile(message.from_user.id, message.from_user.id, message.bot)
    else:
        await message.answer("Ваш аккаунт не заполнен, зарегистрируйтесь /register")

async def show_profile(id_check, id_send, bot):
    data = dbutils.get_info(id_check)
    faculties = settings.Other.faculties
    trust_mods = ["не подтверждены", "на модерации", "подтверждены"]
    s = data[0][0] + " " + data[1][0] + "\n\n"
    s += "кафедра: " + faculties[int(data[2])][0] + "-" + str(int(data[3])) + "\n"
    s += "курс: " + str(int(data[4])) + "\n"
    s += "данные аккаунта: " + trust_mods[int(data[5])] + "\n\n"
    s += data[6][0]

    if dbutils.avatar_exists(id_check):
        photo = open("avatars/" + str(id_check) + ".jpg", 'rb')
    else:
        photo = open("default_avatar.jpg", 'rb')
    await bot.send_photo(chat_id=id_send, photo=photo, caption=s)

def register_handlers_whoami(dp: Dispatcher):
    dp.register_message_handler(cmd_whoami, commands="whoami")