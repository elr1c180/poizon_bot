from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def recalc() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
            text="Рассчитать стоимость заново🔄", 
            callback_data="calc")
        )
    kb.add(InlineKeyboardButton(
            text="Оформить заказ🛍", 
            callback_data="order")
        )
    kb.add(InlineKeyboardButton(
            text="◀️Вернуться в главное меню", 
            callback_data="main_menu")
        )
    kb.adjust(1)
    return kb.as_markup()