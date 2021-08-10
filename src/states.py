from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterStates(StatesGroup):
    name = State()
    surname = State()
    confirm = State()
    faculty = State()
    department = State()
    # department2 = State()
    course = State()