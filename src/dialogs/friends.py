from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import dbutils
from dialogs import whoami

async def cmd_friends(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await select_mode(message)
    else:
        await message.answer("Сначала зарегистрируйтесь /register")
        await state.finish()

async def select_mode(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="Искать", callback_data= "friends_search")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Исходящие заявки", callback_data= "friends_outcoming")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Входящие заявки", callback_data= "friends_incoming")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Друзья", callback_data= "friends_list")
    keyboard.add(key)
    await message.bot.send_message(message.from_user.id, text="Выберете категорию:", reply_markup=keyboard) 

async def callback_search(call: types.CallbackQuery):
    friend_id = dbutils.pop_potential_friend(call.from_user.id)
    if friend_id == None:
        await call.bot.send_message(call.from_user.id, "Не найдено потенциальных друзей")   
    else:
        await whoami.show_profile(friend_id, call.from_user.id, call.bot, True, False)
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text="Искать дальше", callback_data= "friends_search")
        keyboard.add(key)
        key = types.InlineKeyboardButton(text="Добавить в друзья", callback_data= "friends_outcoming_" + str(friend_id))
        keyboard.add(key)
        await call.bot.send_message(call.from_user.id, text="Выберете действие:", reply_markup=keyboard)
        # await call.bot.send_message(call.from_user.id, "Потенциальный друг: " + str(friend_id))   

async def callback_add_friend(call: types.CallbackQuery):
    id_to = int(call.data.split("_")[2])
    fl = dbutils.request_friendship(call.from_user.id, id_to)
    if fl:
        await call.bot.send_message(call.from_user.id, "Заявка отправлена")
    else:
        await call.bot.send_message(call.from_user.id, "Заявка уже существует")

def register_handlers_friends(dp: Dispatcher):
    dp.register_message_handler(cmd_friends, commands="friends")
    dp.register_callback_query_handler(callback_search, lambda call: call.data == "friends_search")
    dp.register_callback_query_handler(callback_add_friend, lambda call: call.data.startswith("friends_outcoming_"))