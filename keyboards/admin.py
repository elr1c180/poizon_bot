from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def text_admin() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
            text="Обратиться к администраторам", 
            callback_data="reply_to_admin")
        )
    kb.adjust(1)
    return kb.as_markup()