from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from fsm import  admin_fsm

from keyboards.cancel import cancel_kb
from keyboards.main import main_menu

from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == 'cancel') 
async def cancel_hand(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Действие отменено",
        parse_mode='html',
        reply_markup=main_menu()
    )

    await state.clear()
