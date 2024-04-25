from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from fsm import  admin_fsm

from keyboards.cancel import cancel_kb
from main import *
from aiogram.fsm.context import FSMContext

from keyboards.main import main_menu
router = Router()

@router.callback_query(F.data == 'reply_to_admin') 
async def reply_to_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(admin_fsm.AdminForm.text)
    await callback.message.answer(
        f"Напишите ваше обращение, после чего наш менеджер <b>в ближайшее время</b> с вами свяжется.\n\nЕсли у вас скрыто имя пользователя, то напишите в обращении ваши контактные данные.",
        parse_mode='html',
        reply_markup=cancel_kb()
    )

@router.message(admin_fsm.AdminForm.text)
async def forward_text(message: Message, state: FSMContext):
    await state.update_data(text = message.text)
    await state.update_data(username=message.from_user.username)

    user_message = await state.get_data()

    username = user_message['username']
    user_message = user_message['text']
    

    await message.answer('<b>Спасибо за обращение!</b>\n\nВаше сообщение доставлено, с вами скоро свяжутся', parse_mode='html', reply_markup=main_menu())
    await message.bot.send_message('-4137583061', f'{user_message}\n\n<b>Сообщение от пользователя:</b>@{username}', parse_mode='html')
    await state.clear()