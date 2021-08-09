import logging
import dbutils
# import register
from aiogram import Bot, Dispatcher, executor, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text

# CMD:
# help
# cancel
# register
# delete

# TODO: real data, position=id, num=number of depts
FACULTIES = [["ИУ", 11],["ФН", 14],["СГН", 11],["МТ", 11],["РЛ", 11]]

class RegisterStates(StatesGroup):
    # default = State()
    name = State()
    surname = State()
    confirm = State()
    faculty = State()
    department = State()

bot = Bot(token="1940130843:AAHhJtTJBlJMLUignP8Z70znzl9BQ0MBeuE")

# TODO: connect Redis storage
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

dbutils.connect()

@dp.message_handler(commands="cancel", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Регистрация отменена")

@dp.message_handler(commands="help", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("< Здесь будет help >")

# ===========================

@dp.message_handler(commands="delete")
async def cmd_delete(message: types.Message):
    await RegisterStates.confirm.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer("Вы уверены, что хотите удалить учетную запись?", reply_markup=keyboard)

@dp.message_handler(Text(equals="Да"), state=RegisterStates.confirm)
async def yes_delete(message: types.Message, state: FSMContext):
    await state.finish()
    dbutils.delete(message.from_user.id)
    await message.reply("Аккаунт удален", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Нет"), state=RegisterStates.confirm)
async def no_delete(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Удаление отменено", reply_markup=types.ReplyKeyboardRemove())

# ===========================

@dp.message_handler(commands="register")
async def cmd_register(message: types.Message, state: FSMContext):
    if dbutils.id_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы, удалите профиль, если что-то пошло не так")
        await state.finish()
    else:
        await message.answer("Введите имя (кириллицей):")
        await RegisterStates.name.set()

@dp.message_handler(lambda message: not dbutils.validShortString(message.text), state=RegisterStates.name)
async def process_name_invalid(message: types.Message):
    return await message.reply("Недопустимые символы или длина имени, попробуйте снова")

@dp.message_handler(lambda message: dbutils.validShortString(message.text), state=RegisterStates.name)
async def process_name_valid(message: types.Message):
    dbutils.write_name(message.from_user.id, message.text, message.from_user.username)
    await message.answer("Введите фамилию (кириллицей):")
    await RegisterStates.surname.set()

@dp.message_handler(lambda message: not dbutils.validShortString(message.text), state=RegisterStates.surname)
async def process_name_invalid(message: types.Message):
    return await message.reply("Недопустимые символы или длина фамилии, попробуйте снова")

@dp.message_handler(lambda message: dbutils.validShortString(message.text), state=RegisterStates.surname)
async def process_name_valid(message: types.Message):
    dbutils.write_surname(message.from_user.id, message.text)
    await RegisterStates.faculty.set()
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(FACULTIES)):
    	key = types.InlineKeyboardButton(text=FACULTIES[i][0], callback_data=str(i))
    	keyboard.add(key)
    await message.answer("Выберете кафедру", reply_markup=keyboard)
    

@dp.callback_query_handler(state=RegisterStates.faculty)
async def callback_faculty(call: types.CallbackQuery):
	code = int(call.data)
	dbutils.write_faculty(call.from_user.id, code)
	await call.message.answer("Информация о факультете сохранена")
	await RegisterStates.department.set()

# ===========================

@dp.message_handler()
async def cmd_default(message: types.Message):
    await message.answer("Неизвестная команда, попробуйте /help")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)