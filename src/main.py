import logging
import dbutils
# import register
from aiogram import Bot, Dispatcher, executor, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

class RegisterStates(StatesGroup):
    name = State()
    surname = State()


# TODO: connect Redis storage
bot = Bot(token="1940130843:AAHhJtTJBlJMLUignP8Z70znzl9BQ0MBeuE")

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

dbutils.connect()


# TODO: delete
@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

@dp.message_handler(commands="register")
async def cmd_register(message: types.Message):
    await message.answer("Введите имя (кириллицей):")
    await RegisterStates.name.set()

@dp.message_handler(lambda message: not dbutils.validShortString(message.text), state=RegisterStates.name)
async def process_age_invalid(message: types.Message):
    return await message.reply("Недопустимые символы или длина имени")

@dp.message_handler(lambda message: dbutils.validShortString(message.text), state=RegisterStates.name)
async def process_age_invalid(message: types.Message):
    dbutils.write_name(message.from_user.id, message.text)
    return await message.reply("Имя допустимо")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)