import dbutils
from states import AvatarStates

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def cmd_avatar(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await confirm_avatar(message)
    else:
        await message.answer("Чтобы задать аватар, зарегистрируйтесь /register")
        await state.finish()

async def confirm_avatar(message: types.Message):
    await AvatarStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Если у вас доверенная учетная запись, понадобится повторная модерация, продолжить?", reply_markup=keyboard)

async def yes_avatar(message: types.Message, state: FSMContext):
    await message.answer("Пришлите фото", reply_markup=types.ReplyKeyboardRemove())
    await AvatarStates.send.set()

async def no_avatar(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Отправка фото отменена", reply_markup=types.ReplyKeyboardRemove())

async def process_avatar(message: types.Message, state: FSMContext):
	dbutils.drop_trusted(message.from_user.id)
	path = "avatars/" + str(message.from_user.id) + ".jpg"
	await message.photo[-1].download(path)
	await message.answer("Фото сохранено")
	await state.finish()

def register_handlers_avatar(dp: Dispatcher):
    dp.register_message_handler(cmd_avatar, commands="avatar")
    dp.register_message_handler(yes_avatar, Text(equals="Да"), state=AvatarStates.confirm)
    dp.register_message_handler(no_avatar, Text(equals="Нет"), state=AvatarStates.confirm)
    dp.register_message_handler(process_avatar, content_types=['photo'], state=AvatarStates.send)