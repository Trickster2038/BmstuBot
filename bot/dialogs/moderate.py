from aiogram import Dispatcher, types

import dbutils
from dialogs import whoami


async def cmd_moderate(message: types.Message):
    if dbutils.is_moderator(message.from_user.id):
        await moderate(message)
    else:
        await message.answer("Чтобы стать модератором, обратитесь к администратору системы")


async def moderate(message):
    check_id = dbutils.pop_moderator_pool(message.from_user.id)
    if check_id != None:
        await whoami.show_profile(check_id, message.from_user.id, message.bot, False, False)
        await whoami.show_verify(check_id, message.from_user.id, message.bot)

        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(
            text="Подтвердить", callback_data="submit_" + str(check_id))
        keyboard.add(key)
        key = types.InlineKeyboardButton(
            text="Отклонить", callback_data="discard_" + str(check_id))
        keyboard.add(key)

        await message.bot.send_message(message.from_user.id, text="Подтвердить запись?", reply_markup=keyboard)
    else:
        await message.bot.send_message(message.from_user.id, text="Пулл аккаунтов закончился")


async def callback_moderate(call: types.CallbackQuery):
    if dbutils.is_moderator(call.from_user.id):
        trust = (call.data.split("_")[0] == "submit")
        id = int(call.data.split("_")[1])
        if trust:
            dbutils.grant_trusted(id)
        else:
            dbutils.drop_trusted(id)
        await call.bot.send_message(call.from_user.id, text="Решение сохранено")
        await moderate(call)
    else:
        await call.bot.send_message(call.from_user.id, text="Вы больше не модератор")


def register_handlers_moderate(dp: Dispatcher):
    dp.register_message_handler(cmd_moderate, commands="moderate")
    dp.register_callback_query_handler(callback_moderate, lambda call: call.data.startswith(
        "submit_") or call.data.startswith("discard_"))
