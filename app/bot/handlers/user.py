from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext


from state_machine import userstate


router = Router()  

@router.message(userstate.register)
async def register(message: types.Message, state: FSMContext):
    await state.set_state(userstate.menu)
    await message.answer("Вы успешно зарегистрированы")