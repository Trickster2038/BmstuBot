from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/cancel", description="Вернуться к командам"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/delete", description="Удалить профиль"),
        BotCommand(command="/avatar", description="Добавить/обновить аватар"),
        BotCommand(command="/verify", description="Верифицировать аккаунт"),
        BotCommand(command="/whoami", description="Показать мой профиль"),
        BotCommand(command="/change", description="Изменить данные профиля")
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