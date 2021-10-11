from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import dbutils
import settings
from dialogs import whoami

async def cmd_friends(message: types.Message, state: FSMContext):
    if dbutils.is_filled(message.from_user.id):
        await select_mode(message)
    else:
        await message.answer("Сначала зарегистрируйтесь /register")
        await state.finish()

async def select_mode(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Чтобы показать более {} людей в списке, повторите нажатие на категорию"\
        .format(settings.Friends.limit))
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="Искать наставника", callback_data= "friends_search_unsafe")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Искать подтвержденного наставника", callback_data= "friends_search_safe")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Исходящие заявки", callback_data= "friends_outcoming")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Входящие заявки", callback_data= "friends_incoming")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Наставники", callback_data= "list_curators")
    keyboard.add(key)
    key = types.InlineKeyboardButton(text="Подопечные", callback_data= "list_mypeople")
    keyboard.add(key)
    await message.bot.send_message(message.from_user.id, text="Выберете категорию:", reply_markup=keyboard) 

async def callback_search(call: types.CallbackQuery):
    safety = call.data.split("_")[2]
    if safety == "unsafe":
        friend_id = dbutils.pop_potential_friend_unsafe(call.from_user.id)
    else:
        friend_id = dbutils.pop_potential_friend_safe(call.from_user.id)

    if friend_id == None:
        await call.bot.send_message(call.from_user.id, "Не найдено потенциальных наставников")   
    else:
        await whoami.show_profile(friend_id, call.from_user.id, call.bot)
        keyboard = types.InlineKeyboardMarkup()
        key = types.InlineKeyboardButton(text="Искать дальше", callback_data= "friends_search_" + safety)
        keyboard.add(key)
        key = types.InlineKeyboardButton(text="Добавить в друзья", callback_data= "friends_add_" + str(friend_id))
        keyboard.add(key)
        await call.bot.send_message(call.from_user.id, text="Выберете действие:", reply_markup=keyboard)
        # await call.bot.send_message(call.from_user.id, "Потенциальный друг: " + str(friend_id))   

async def callback_add_friend(call: types.CallbackQuery):
    id_to = int(call.data.split("_")[2])
    fl = dbutils.request_friendship(call.from_user.id, id_to)
    if fl:
        await call.bot.send_message(call.from_user.id, "Заявка отправлена")
    else:
        await call.bot.send_message(call.from_user.id, "Заявка уже существует")

async def callback_incoming(call: types.CallbackQuery):
    n = settings.Friends.limit
    incoming_list = dbutils.get_incoming(call.from_user.id, n)
    if incoming_list == []:
        await call.bot.send_message(call.from_user.id, "Список пуст")
    else:
        for x in incoming_list:
            await whoami.show_profile(x, call.from_user.id, call.bot)
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text="Отклонить", callback_data= "friends_discard_" + str(x))
            keyboard.add(key)
            key = types.InlineKeyboardButton(text="Принять", callback_data= "friends_apply_" + str(x))
            keyboard.add(key)
            await call.bot.send_message(call.from_user.id, text="Выберете действие:", reply_markup=keyboard)

async def callback_discard(call: types.CallbackQuery):
    id_discard = int(call.data.split("_")[2])
    dbutils.discard_friend(call.from_user.id, id_discard)
    await call.bot.send_message(call.from_user.id, "Заявка отклонена / друг удален")

async def callback_apply(call: types.CallbackQuery):
    id_apply = int(call.data.split("_")[2])
    fl = dbutils.apply_friend(id_apply, call.from_user.id)
    if fl:
        await call.bot.send_message(call.from_user.id, "Заявка принята")
    else:
        await call.bot.send_message(call.from_user.id, "Заявка уже принята или удалена")

async def callback_outcoming(call: types.CallbackQuery):
    n = settings.Friends.limit
    outcoming_list = dbutils.get_outcoming(call.from_user.id, n)
    if outcoming_list == []:
        await call.bot.send_message(call.from_user.id, "Список пуст")
    else:
        for x in outcoming_list:
            await whoami.show_profile(x, call.from_user.id, call.bot)
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text="Отменить", callback_data= "friends_discard_" + str(x))
            keyboard.add(key)
            await call.bot.send_message(call.from_user.id, text="Выберете действие:", reply_markup=keyboard)

async def callback_lists(call: types.CallbackQuery):
    n = settings.Friends.limit
    mode = call.data.split("_")[1]
    if mode == "curators":
        data = dbutils.get_curators(call.from_user.id, n)
    else:
        data = dbutils.get_mypeople(call.from_user.id, n)

    if data == []:
        await call.bot.send_message(call.from_user.id, "Список пуст")
    else:
        for x in data:
            await whoami.show_profile(x, call.from_user.id, call.bot, with_nick=True)
            keyboard = types.InlineKeyboardMarkup()
            key = types.InlineKeyboardButton(text="Удалить", callback_data= "friends_discard_" + str(x))
            keyboard.add(key)
            await call.bot.send_message(call.from_user.id, text="Выберете действие:", reply_markup=keyboard)    

def register_handlers_friends(dp: Dispatcher):
    dp.register_message_handler(cmd_friends, commands="friends")
    dp.register_callback_query_handler(callback_search, lambda call: call.data.startswith("friends_search_"))
    dp.register_callback_query_handler(callback_add_friend, lambda call: call.data.startswith("friends_add_"))
    dp.register_callback_query_handler(callback_incoming, lambda call: call.data == "friends_incoming")
    dp.register_callback_query_handler(callback_discard, lambda call: call.data.startswith("friends_discard_"))
    dp.register_callback_query_handler(callback_apply, lambda call: call.data.startswith("friends_apply_"))
    dp.register_callback_query_handler(callback_outcoming, lambda call: call.data == "friends_outcoming")
    dp.register_callback_query_handler(callback_lists, lambda call:  call.data.startswith("list_"))