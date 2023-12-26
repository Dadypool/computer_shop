from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from state_machine import userstate

from keyboards import user

router = Router()  

@router.message(userstate.register)
async def register(message: types.Message, state: FSMContext):
    await state.set_state(userstate.menu)
    await message.answer("Вы успешно зарегистрированы", reply_markup=user.usermenu())


@router.callback_query(F.data == "catalog")
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка каталога", reply_markup=user.usermenu())


@router.callback_query(F.data == "order")
async def order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка заказов", reply_markup=user.usermenu())


@router.callback_query(F.data == "basket")
async def basket(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка корзины", reply_markup=user.usermenu())