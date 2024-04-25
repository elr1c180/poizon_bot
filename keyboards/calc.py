from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def calc_order() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
            text="Куртки🥼/Кроссовки👟", 
            callback_data="summer")
        )
    kb.add(InlineKeyboardButton(
        text="Зимняя обувь🥾/Верхняя одежда👗", 
        callback_data="winter"))
    kb.add(InlineKeyboardButton(
        text="Футболки👕/Рубашки👔/Шорты🩳", 
        callback_data="shirt"))
    kb.add(InlineKeyboardButton(
        text="Штаны👖/Толстовки🦺/Летняя обувь👟", 
        callback_data="jeans"))
    kb.add(InlineKeyboardButton(
        text="Парфюм👑/Аксессуары💍", 
        callback_data='parf'))
    kb.add(InlineKeyboardButton(
        text="Рюкзаки🎒/Сумки👜", 
        callback_data='bag'))
    kb.add(InlineKeyboardButton(
        text='Носки🧦/Кепки🧢/Нижнее белье🩲',
        callback_data='socks'
    ))
    kb.add(InlineKeyboardButton(
        text='Нет нужной категории',
        callback_data='not_found'
    ))
    kb.add(InlineKeyboardButton(
            text="◀️Вернуться в главное меню", 
            callback_data="main_menu")
        )
    kb.adjust(1)
    return kb.as_markup()