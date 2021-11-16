import dbutils

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def cmd_menu(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await select_option(message)
    else:
        await message.answer("Сначала зарегистрируйтесь /register")
        await state.finish()


async def select_option(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(
        text="Изменить профиль", callback_data="menu_change")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Изменить аватар", callback_data="menu_avatar")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Верифицировать аккаунт", callback_data="menu_verify")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Показать мой профиль", callback_data="menu_show_profile")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Удалить аккаунт", callback_data="menu_delete")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Задать веб-пароль", callback_data="menu_web_password")
    keyboard.add(key)
    key = types.InlineKeyboardButton(
        text="Обновить никнейм", callback_data="menu_nick_refresh")
    keyboard.add(key)
    await message.bot.send_message(message.from_user.id, text="Выберите опцию:", reply_markup=keyboard)


def register_handlers_profile(dp: Dispatcher):
    dp.register_message_handler(cmd_menu, commands="profile")
