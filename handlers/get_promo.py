from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
import sqlite3

from fsm import delete, promo_quiz

from aiogram.fsm.context import FSMContext

router = Router()  # [1]

@router.message(Command("show_promo"))
async def show_promo(message: Message):
    promos = ''
    with sqlite3.connect('promo.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM promo')
        for promo in cur.fetchall():
            promos += f'{promo[0]}. {promo[1]} - {promo[2]}%\n'
    
    await message.answer(f'<b>Список активных промокодов:</b>\n\n{promos}', parse_mode='html')

@router.message(Command("delete_promo"))
async def delete_promo(message:Message,  state: FSMContext):
    await state.set_state(delete.DeletePromo.num)
    promos = ''
    with sqlite3.connect('promo.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM promo')
            for promo in cur.fetchall():
                print(promo)
                promos += f'{promo[0]}. {promo[1]} - {promo[2]}%\n'
        except Exception as e:
            await message.answer('Пожалуйста, введите ID промокода')
    
    await message.answer(f'<b>Список активных промокодов, введите номер промокода, который нужно удалить:</b>\n\n{promos}', parse_mode='html')

@router.message(delete.DeletePromo.num)
async def delete_final(message: Message, state: FSMContext):
    await state.update_data(num=message.text)

    with sqlite3.connect('promo.db') as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE from promo where id = {message.text}")
    
    await message.answer('Успешное удаление')
    await state.clear()

@router.message(Command("set_promo"))  # [2]
async def promo(message: Message, state: FSMContext):
    await state.set_state(promo_quiz.Promo.name)
    await message.answer(
        f"<b>Приветствую, {message.from_user.first_name}</b>!\n\nВведи название нового промкода",
        parse_mode='html'
    )

@router.message(promo_quiz.Promo.name)
async def get_price(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(promo_quiz.Promo.disc)
    await message.answer(
        "Отлично, теперь укажите размер скидки(%)"
    )

@router.message(promo_quiz.Promo.disc)
async def final(message: Message, state: FSMContext):
    await state.update_data(disc=message.text)
    data = await state.get_data()
    name = data["name"]
    disc = data["disc"]

    with sqlite3.connect('promo.db') as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO promo (name, perc) VALUES (?, ?)", (name, disc))

    
    await message.answer('<b>Отлично!</b>\nВы добавили новый промокод', parse_mode='html')

    await state.clear()