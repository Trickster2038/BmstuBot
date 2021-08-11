import dbutils
from states import AvatarStates
from states import VerifyStates

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
    await message.answer("Если у вас доверенная учетная запись, понадобится повторная верификация, продолжить?", reply_markup=keyboard)

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

async def cmd_verify(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        if dbutils.avatar_exists(message.from_user.id):
            await confirm_verify(message)
        else:
            await message.answer("Чтобы верифицировать аккаунт, добавьте аватар /avatar")
            await state.finish()
    else:
        await message.answer("Чтобы задать аватар, зарегистрируйтесь /register")
        await state.finish()

async def confirm_verify(message: types.Message):
    await VerifyStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Если у вас доверенная учетная запись, понадобится повторная модерация, продолжить?", reply_markup=keyboard)

async def yes_verify(message: types.Message, state: FSMContext):
    await message.answer("Пришлите фото", reply_markup=types.ReplyKeyboardRemove())
    await VerifyStates.send.set()

async def no_verify(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Отправка фото отменена", reply_markup=types.ReplyKeyboardRemove())

async def process_verify(message: types.Message, state: FSMContext):
	dbutils.turn_moderate(message.from_user.id)
	path = "verify/" + str(message.from_user.id) + ".jpg"
	await message.photo[-1].download(path)
	await message.answer("Фото сохранено")
	await state.finish()

def register_handlers_avatar(dp: Dispatcher):
    dp.register_message_handler(cmd_avatar, commands="avatar")
    dp.register_message_handler(yes_avatar, Text(equals="Да"), state=AvatarStates.confirm)
    dp.register_message_handler(no_avatar, Text(equals="Нет"), state=AvatarStates.confirm)
    dp.register_message_handler(process_avatar, content_types=['photo'], state=AvatarStates.send)

def register_handlers_verify(dp: Dispatcher):
    dp.register_message_handler(cmd_verify, commands="verify")
    dp.register_message_handler(yes_verify, Text(equals="Да"), state=VerifyStates.confirm)
    dp.register_message_handler(no_verify, Text(equals="Нет"), state=VerifyStates.confirm)
    dp.register_message_handler(process_verify, content_types=['photo'], state=VerifyStates.send)