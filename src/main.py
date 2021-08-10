import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from dialogs.commands import *
from states import RegisterStates
from dialogs.delete import *
from dialogs.register import *
import settings

bot = Bot(token=settings.Other.token)

# TODO: connect Redis storage?
dp = Dispatcher(bot, storage=MemoryStorage())

async def main():
    bot = Bot(token=settings.Other.token)

    # TODO: connect Redis storage?
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)
    dbutils.connect()

    register_handlers_delete(dp)
    register_handlers_register(dp)
    register_handlers_common(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())