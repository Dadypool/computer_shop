from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from state_machine import userstate

from keyboards import user, seller

from state_machine import userstate
from state_machine import sellerstate

router = Router()  

@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    await message.answer("Приветсвуем Вас в нашем магазине!")
    ##############################################################
    ##
    ## TODO: getting data about user with id = message.from_user.id
    ##
    ##############################################################
    if None == 1: # if there is no user with this id in database - register
        await message.answer("Мы не знакомы! Запускаем процесс регистрации:\nВведите ваше имя:")
        await state.set_state(userstate.register)
    elif None == 1: # if user connection detected
        name = "name" # TODO: replace with name
        await message.answer(f"Приветсвуем, {name}!", reply_markup=user.usermenu())
        await state.set_state(userstate.menu)
    elif None == None: # if seller connection detected
        name = "name" # TODO: replace with name
        await message.answer(f"Приветсвуем, {name}!", reply_markup=seller.sellermenu())
        await state.set_state(sellerstate.menu)

# TODO: implement menu handler
'''@router.message(Command("menu"))
async def command_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print("Current state:", userstate)
    if current_state in userstate:
        await state.set_state(userstate.menu)
    else:
        await state.set_state(sellerstate.menu)'''

@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.delete()