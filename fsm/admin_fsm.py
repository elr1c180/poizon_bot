from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AdminForm(StatesGroup):
    text = State()
    username = State()