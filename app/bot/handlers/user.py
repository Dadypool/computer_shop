from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import os, sys

from state_machine import userstate

#sys.path.append(os.path.join(os.getcwd(), '..'))
from keyboards import user

router = Router()  

@router.message(userstate.register)
async def register(message: types.Message, state: FSMContext):
    await state.set_state(userstate.menu)
    await message.answer("Вы успешно зарегистрированы", reply_markup=user.usermenu())