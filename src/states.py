from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterStates(StatesGroup):
    name = State()
    surname = State()
    faculty = State()
    department = State()
    course = State()
    bio = State()

class DeleteStates(StatesGroup):
	confirm = State()

class AvatarStates(StatesGroup):
	confirm = State()
	send = State()

class VerifyStates(StatesGroup):
	confirm = State()
	send = State()