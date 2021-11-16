from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from dialogs.delete import *
from dialogs.register import *
from dialogs.avatar import *
from dialogs.whoami import *
from dialogs.moderate import *
from dialogs.change import *
from dialogs.friends import *
from dialogs.profile import *
from dialogs.web import *

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/cancel", description="Вернуться к командам"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/profile", description="Настроить профиль"),
        BotCommand(command="/friends", description="Друзья")
        # hidden: /moderate
    ]
    await bot.set_my_commands(commands)

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Возврат к режиму команд")

async def cmd_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("< Здесь будет help >")

async def cmd_default(message: types.Message):
    await message.answer("Неизвестная команда, попробуйте /help")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")

def register_handlers_default(dp: Dispatcher):
	dp.register_message_handler(cmd_default)

def register_handlers_branches(dp: Dispatcher):
    register_handlers_delete(dp)
    register_handlers_register(dp)
    register_handlers_avatar(dp)
    register_handlers_verify(dp)
    register_handlers_whoami(dp)
    register_handlers_moderate(dp)
    register_handlers_change(dp)
    register_handlers_web(dp)
    register_handlers_friends(dp)
    register_handlers_profile(dp)