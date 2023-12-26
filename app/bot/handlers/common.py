from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


from state_machine import userstate


router = Router()  

'''@router.message()
async def echo_handler(message: types.Message):
    await message.delete()
'''

@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    await message.answer("Приветсвуем Вас в нашем магазине!")
    if None == None:
        await message.answer("Мы не знакомы! Запускаем процесс регистрации:\nВведите ваше имя:")
        await state.set_state(userstate.register)