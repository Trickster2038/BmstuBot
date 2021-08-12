import dbutils
from states import ChangeStates

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

async def cmd_change(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await select_change(message)
    else:
        await message.answer("Сначала зарегистрируйтесь /register")
        await state.finish()

async def select_change(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="О себе", callback_data= "bio")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Курс", callback_data= "course")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Режим наставника", callback_data= "curator")
    keyboard.add(key)
    await ChangeStates.select.set()
    await message.bot.send_message(message.from_user.id, text="Изменить поле:", reply_markup=keyboard)

async def process_callback_bio(call: types.CallbackQuery):
    await ChangeStates.bio.set()
    await call.bot.send_message(call.from_user.id, text="Расскажите о себе (контакты, любимые предметы и т.д.)")

async def process_bio(message: types.Message, state: FSMContext):
    dbutils.write_bio(message.from_user.id, message.text)
    await message.answer("Информация 'о себе' сохранена")
    await state.finish()

async def process_callback_course(call: types.CallbackQuery):
    await ChangeStates.course.set()
    keyboard = types.InlineKeyboardMarkup()
    for i in range(6):
        key = types.InlineKeyboardButton(text=str(i+1), callback_data=str(i+1))
        keyboard.add(key)
    await call.bot.send_message(call.from_user.id, "Выберете курс", reply_markup=keyboard)

async def callback_course(call: types.CallbackQuery, state: FSMContext):
    code = int(call.data)
    dbutils.write_course(call.from_user.id, code)
    await call.message.answer("Информация о курсе сохранена")
    await state.finish()

async def process_callback_curator(call: types.CallbackQuery):
    await ChangeStates.curator.set()
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="Включить", callback_data= "curator_on")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Выключить", callback_data= "curator_off")
    keyboard.add(key)
    await call.bot.send_message(call.from_user.id, text="Режим куратора:", reply_markup=keyboard)

async def callback_curator(call: types.CallbackQuery, state: FSMContext):
    fl = (call.data == "curator_on")
    dbutils.write_curator(call.from_user.id, fl)
    await call.bot.send_message(call.from_user.id, text="Информация о режиме сохранена")
    await state.finish()

def register_handlers_change(dp: Dispatcher):
    dp.register_message_handler(cmd_change, commands="change")
    dp.register_callback_query_handler(process_callback_bio, lambda call: call.data == "bio", state=ChangeStates.select)
    dp.register_callback_query_handler(process_callback_course, lambda call: call.data == "course", state=ChangeStates.select)
    dp.register_callback_query_handler(process_callback_curator, lambda call: call.data == "curator", state=ChangeStates.select)
    dp.register_message_handler(process_bio, state=ChangeStates.bio)
    dp.register_callback_query_handler(callback_course, state=ChangeStates.course)
    dp.register_callback_query_handler(callback_curator, state=ChangeStates.curator)