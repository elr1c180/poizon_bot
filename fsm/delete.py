from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class DeletePromo(StatesGroup):
    num = State()