import dbutils
from states import AvatarStates
from states import VerifyStates

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def cmd_avatar(call: types.CallbackQuery, state: FSMContext):
    if dbutils.is_filled(call.from_user.id):
        await confirm_avatar(call)
    else:
        await call.bot.send_message(call.from_user.id, text="Чтобы задать аватар, зарегистрируйтесь /register")
        # await message.answer("Чтобы задать аватар, зарегистрируйтесь /register")
        await state.finish()

async def confirm_avatar(call: types.CallbackQuery):
    await AvatarStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await call.bot.send_message(call.from_user.id,"Если у вас доверенная учетная запись, понадобится повторная верификация, продолжить?", reply_markup=keyboard)

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

async def cmd_verify(call: types.CallbackQuery, state: FSMContext):
    if dbutils.is_filled(call.from_user.id):
        if dbutils.avatar_exists(call.from_user.id):
            await confirm_verify(call)
        else:
            await call.bot.send_message(call.from_user.id, "Чтобы верифицировать аккаунт, добавьте аватар /avatar") 
            # await message.answer("Чтобы верифицировать аккаунт, добавьте аватар /avatar")
            await state.finish()
    else:
        await call.bot.send_message(call.from_user.id, "Чтобы задать аватар, зарегистрируйтесь /register") 
        # await message.answer("Чтобы задать аватар, зарегистрируйтесь /register")
        await state.finish()

async def confirm_verify(call: types.CallbackQuery):
    await VerifyStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await call.bot.send_message(call.from_user.id, "Если у вас доверенная учетная запись, понадобится повторная модерация, продолжить?", reply_markup=keyboard)
    # await message.answer("Если у вас доверенная учетная запись, понадобится повторная модерация, продолжить?", reply_markup=keyboard)

async def yes_verify(message: types.Message, state: FSMContext):
    await message.answer("Пришлите фото документа, подтверждающего данные аккаунта (пропуск/студ. билет/зач. книжка)", reply_markup=types.ReplyKeyboardRemove())
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
    dp.register_callback_query_handler(cmd_avatar, lambda call: call.data == "menu_avatar") 
    # dp.register_message_handler(cmd_avatar, commands="avatar")
    dp.register_message_handler(yes_avatar, Text(equals="Да"), state=AvatarStates.confirm)
    dp.register_message_handler(no_avatar, Text(equals="Нет"), state=AvatarStates.confirm)
    dp.register_message_handler(process_avatar, content_types=['photo'], state=AvatarStates.send)

def register_handlers_verify(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_verify, lambda call: call.data == "menu_verify") 
    # dp.register_message_handler(cmd_verify, commands="verify")
    dp.register_message_handler(yes_verify, Text(equals="Да"), state=VerifyStates.confirm)
    dp.register_message_handler(no_verify, Text(equals="Нет"), state=VerifyStates.confirm)
    dp.register_message_handler(process_verify, content_types=['photo'], state=VerifyStates.send)