from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import dbutils

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
    await message.bot.send_message(message.from_user.id, text="Выберети категорию:", reply_markup=keyboard)	

async def callback_search(call: types.CallbackQuery, state: FSMContext):
	friend_id = dbutils.pop_potential_friend(call.from_user.id)
	if friend_id == None:
		await call.bot.send_message(call.from_user.id, "Не найдено потенциальных друзей")	
	else:
		# await call.bot.send_message(call.from_user.id, "Потенциальный друг: " + str(friend_id))	

def register_handlers_friends(dp: Dispatcher):
    dp.register_message_handler(cmd_friends, commands="friends")
    dp.register_callback_query_handler(callback_search, lambda call: call.data == "friends_search")