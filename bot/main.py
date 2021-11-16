import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import commands
import settings
import dbutils


async def main():
    bot = Bot(token=settings.Other.token)

    # TODO: connect Redis storage?
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)
    dbutils.connect()

    commands.register_handlers_common(dp)
    commands.register_handlers_branches(dp)
    commands.register_handlers_default(dp)

    await commands.set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
