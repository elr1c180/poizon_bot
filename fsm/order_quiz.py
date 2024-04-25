
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Order(StatesGroup):
    item_type = State()
    link = State()
    photo = State()
    size = State()
    color = State()
    price = State()
    promo = State()
    phone = State()
    name = State()
    username = State()