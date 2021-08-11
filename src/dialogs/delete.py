from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from states import DeleteStates
import dbutils

async def cmd_delete(message: types.Message):
    await DeleteStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Вы уверены, что хотите удалить учетную запись?", reply_markup=keyboard)

async def yes_delete(message: types.Message, state: FSMContext):
    await state.finish()
    dbutils.delete(message.from_user.id)
    await message.reply("Аккаунт удален", reply_markup=types.ReplyKeyboardRemove())

async def no_delete(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Удаление отменено", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_delete(dp: Dispatcher):
    dp.register_message_handler(cmd_delete, commands="delete")
    dp.register_message_handler(yes_delete, Text(equals="Да"), state=DeleteStates.confirm)
    dp.register_message_handler(no_delete, Text(equals="Нет"), state=DeleteStates.confirm)