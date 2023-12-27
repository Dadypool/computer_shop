from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from app.bot.state_machine import userstate

from app.bot.keyboards import user as user_kb, seller as seller_kb
from app.bot.state_machine import userstate
from app.bot.state_machine import sellerstate
from app.database.crud import user



router = Router()  



@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    #await message.answer("Приветсвуем Вас в нашем магазине!")
    usr = user.read_user(message.from_user.id)
    if usr == None: # if there is no user with this id in database - register
        await message.answer("Мы не знакомы! Запускаем процесс регистрации:\nВведите ваше имя:")
        await state.set_state(userstate.register)
    else:
        name = usr["name"]
        if usr["rights"] == "user": # if user connection detected
             # TODO: replace with name
            await message.answer(f"Приветсвуем, {name}!", reply_markup=user_kb.usermenu())
            await state.set_state(userstate.menu)
        elif usr["rights"] == "seller": # if seller connection detected
            await message.answer(f"Здравствуйте, {name}!", reply_markup=seller_kb.sellermenu())
            await state.set_state(sellerstate.menu)

# TODO: implement menu handler
@router.message(Command("menu"))
async def command_menu(message: types.Message, state: FSMContext):
    await menu(state, message)

@router.callback_query(F.data == "menu")
async def callback_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await menu(state, callback.message)
    

async def menu(state: FSMContext, message: types.Message):
    current_state = await state.get_state()
    print("Current state:", userstate)
    if current_state in [sellerstate.menu, sellerstate.enter_id, sellerstate.add_product]:
        await state.set_state(sellerstate.menu)
        await message.answer("Главное меню", reply_markup=seller_kb.sellermenu())
        
    else:
         await state.set_state(userstate.menu)   
         await message.answer("Главное меню", reply_markup=user_kb.usermenu())
