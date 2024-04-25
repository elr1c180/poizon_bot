from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class CalcForm(StatesGroup):
    item_type = State()
    price = State()
    promo = State()