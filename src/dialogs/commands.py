from aiogram.types import BotCommand
from aiogram import Bot

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/cancel", description="Сброс состояния"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/delete", description="удалить профиль")
    ]
    await bot.set_my_commands(commands)