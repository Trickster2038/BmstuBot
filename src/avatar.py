import dbutils
from states import AvatarStates

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types

async def cmd_avatar(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await message.answer("Пришлите фото")
        await AvatarStates.send.set()
    else:
        await message.answer("Чтобы задать аватар, зарегистрируйтесь /register")
        await state.finish()

async def process_avatar(message: types.Message, state: FSMContext):
	dbutils.drop_trusted(message.from_user.id)
	path = "avatars/" + str(message.from_user.id) + ".jpg"
	await message.photo[-1].download(path)
	await message.answer("Фото сохранено")
	await state.finish()

def register_handlers_avatar(dp: Dispatcher):
    dp.register_message_handler(cmd_avatar, commands="avatar")
    dp.register_message_handler(process_avatar, content_types=['photo'], state=AvatarStates.send)