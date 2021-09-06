import dbutils
from states import WebStates

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

async def cmd_web_password(call: types.CallbackQuery, state: FSMContext):
    if dbutils.is_filled(call.from_user.id):
        await WebStates.password.set()
        await call.bot.send_message(call.from_user.id, "Введите новый пароль:")
    else:
        await call.bot.send_message(call.from_user.id, "Сначала зарегистрируйтесь /register")
        await state.finish()

async def process_web_password(message: types.Message, state: FSMContext):
    # await state.finsh()
    if len(message.text) < 8:
        await message.bot.send_message(message.from_user.id, "Пароль короче 8 символов")
    else:
       await state.finish() 
       dbutils.set_password(message.from_user.id, message.text)
       await message.bot.send_message(message.from_user.id, "Пароль сохранен")

def register_handlers_web(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_web_password, lambda call: call.data == "menu_web_password") 
    dp.register_message_handler(process_web_password, state=WebStates.password) 
    