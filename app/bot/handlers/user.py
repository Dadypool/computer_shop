import sys, os

from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import userstate
from app.bot.keyboards import user as user_kb, seller
from app.database.crud import user

#sys.path.append(os.path.join(os.getcwd(), '..'))


router = Router()  

@router.message(userstate.register)
async def register(message: types.Message, state: FSMContext):
    if user.create_user({"id": message.from_user.id, "name": message.text, "rights": "user"}):
        await state.set_state(userstate.menu)
        await message.answer("Вы успешно зарегистрированы", reply_markup=user_kb.usermenu())
    else:
        await message.answer("Ошибка регистрации")


@router.callback_query(F.data == "catalog")
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберете категрию", reply_markup=user_kb.catalog())


@router.callback_query(F.data == "order")
async def order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка заказов", reply_markup=user_kb.usermenu())


@router.callback_query(F.data == "basket")
async def basket(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка корзины", reply_markup=user_kb.usermenu())