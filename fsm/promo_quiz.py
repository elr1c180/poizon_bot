
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Promo(StatesGroup):
    name = State()
    disc = State()