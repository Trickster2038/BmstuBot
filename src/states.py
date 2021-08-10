from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterStates(StatesGroup):
    # default = State()
    name = State()
    surname = State()
    confirm = State()
    faculty = State()
    department = State()