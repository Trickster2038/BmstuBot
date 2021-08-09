from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterStates(StatesGroup):
    register_name = State()
    register_surname = State()

# class RegisterFunc:
# 	def register():
		