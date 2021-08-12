import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dialogs.commands import *
from dialogs.delete import *
from dialogs.register import *
from dialogs.avatar import *
from dialogs.whoami import *
from dialogs.moderate import *
from dialogs.change import *
import settings

async def main():
    bot = Bot(token=settings.Other.token)

    # TODO: connect Redis storage?
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)
    dbutils.connect()

    register_handlers_common(dp)
    register_handlers_delete(dp)
    register_handlers_register(dp)
    register_handlers_avatar(dp)
    register_handlers_verify(dp)
    register_handlers_whoami(dp)
    register_handlers_moderate(dp)
    register_handlers_change(dp)
    register_handlers_default(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())