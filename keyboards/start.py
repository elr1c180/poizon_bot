from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
            text="Оформить заказ🛍", 
            callback_data="order")
        )
    kb.add(InlineKeyboardButton(
        text="Калькулятор стоимости🧾", 
        callback_data="calc"))
    kb.add(InlineKeyboardButton(
        text="Актуальный курс📊", 
        callback_data="current_rates"))
    kb.add(InlineKeyboardButton(
        text="Как пользоваться POIZON📲", 
        url="https://teletype.in/@maxim_ruchko/TSGrvgkVB1w"))
    kb.add(InlineKeyboardButton(
        text="Отзывы о нашей работе🌟", 
        url='https://t.me/kungfu_delivery/4'))
    kb.add(InlineKeyboardButton(
        text="Задать вопрос❓", 
        callback_data='reply_to_admin'))
    kb.adjust(1)
    return kb.as_markup()