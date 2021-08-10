from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from states import RegisterStates
import dbutils
import settings

async def cmd_register(message: types.Message, state: FSMContext):
    if dbutils.id_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы, удалите профиль, если что-то пошло не так")
        await state.finish()
    else:
        await message.answer("Введите имя (кириллицей):")
        await RegisterStates.name.set()

async def process_name_invalid(message: types.Message):
    return await message.reply("Недопустимые символы или длина имени, попробуйте снова")

async def process_name_valid(message: types.Message):
    dbutils.write_name(message.from_user.id, message.text, message.from_user.username)
    await message.answer("Имя сохранено")
    await message.answer("Введите фамилию (кириллицей):")
    await RegisterStates.surname.set()

async def process_surname_invalid(message: types.Message):
    return await message.reply("Недопустимые символы или длина фамилии, попробуйте снова")

async def process_surname_valid(message: types.Message):
    await message.answer("Фамилия сохранена")
    faculties = settings.Other.faculties
    dbutils.write_surname(message.from_user.id, message.text)
    await RegisterStates.faculty.set()
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(faculties)):
        key = types.InlineKeyboardButton(text=faculties[i][0], callback_data=str(i))
        keyboard.add(key)
    await message.answer("Выберете кафедру", reply_markup=keyboard)

async def callback_faculty(call: types.CallbackQuery):
    code = int(call.data)
    dbutils.write_faculty(call.from_user.id, code)
    await call.message.answer("Информация о факультете сохранена")
    await process_department(call.from_user.id, call.bot)

async def process_department(user_id, bot):
    faculties = settings.Other.faculties
    faculty_id = dbutils.get_faculty_id(user_id)
    n_departments = faculties[faculty_id][1]
    keyboard = types.InlineKeyboardMarkup()
    for i in range(n_departments):
        key = types.InlineKeyboardButton(text=str(i+1), callback_data=str(i+1))
        keyboard.add(key)
    await bot.send_message(user_id, "Выберете номер кафедры", reply_markup=keyboard)
    await RegisterStates.department.set()

async def callback_department(call: types.CallbackQuery):
    code = int(call.data)
    dbutils.write_department(call.from_user.id, code)
    await call.message.answer("Информация о номере кафедры сохранена")
    await process_course(call.from_user.id, call.bot)

async def process_course(user_id, bot):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(6):
        key = types.InlineKeyboardButton(text=str(i+1), callback_data=str(i+1))
        keyboard.add(key)
    await bot.send_message(user_id, "Выберете курс", reply_markup=keyboard)
    await RegisterStates.course.set()

async def callback_course(call: types.CallbackQuery):
    code = int(call.data)
    dbutils.write_course(call.from_user.id, code)
    await call.message.answer("Информация о курсе сохранена")
    await call.message.answer("Расскажите о себе (контакты, любимые предметы и т.д.)")
    await RegisterStates.bio.set()

async def process_bio_invalid(message: types.Message):
    return await message.reply("Недопустимые символы, попробуйте снова")

async def process_bio_valid(message: types.Message):
    dbutils.write_bio(message.from_user.id, message.text)
    await message.answer("Информация 'о себе' сохранена")
    fl = dbutils.finish_registration(message.from_user.id)
    if fl:
        await message.answer("Аккаунт зарегистрирован, не забывайте про /avatar и /verify")
    else:
        await message.answer("Что-то пошло не так. Удалите аккаунт и создайте заново")


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(cmd_register, commands="register")
    dp.register_message_handler(process_name_invalid, lambda message: not dbutils.validShortString(message.text), state=RegisterStates.name)
    dp.register_message_handler(process_name_valid, lambda message: dbutils.validShortString(message.text), state=RegisterStates.name)
    dp.register_message_handler(process_surname_invalid, lambda message: not dbutils.validShortString(message.text), state=RegisterStates.surname)
    dp.register_message_handler(process_surname_valid, lambda message: dbutils.validShortString(message.text), state=RegisterStates.surname)
    dp.register_callback_query_handler(callback_faculty, state=RegisterStates.faculty)
    dp.register_callback_query_handler(callback_department, state=RegisterStates.department)
    dp.register_callback_query_handler(callback_course, state=RegisterStates.course)
    dp.register_message_handler(process_bio_invalid, lambda message: not dbutils.validLongString(message.text), state=RegisterStates.bio)
    dp.register_message_handler(process_bio_valid, lambda message: dbutils.validLongString(message.text), state=RegisterStates.bio)