from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import userstate
from app.bot.keyboards import user as user_kb, seller as seller_kb
from app.database.crud import user, product, order

router = Router()  


######################## Обработка редактирования списка товаров ################################
@router.callback_query(F.data == "catalog_edit")
async def delete_or_create(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберите тип действия", reply_markup=seller_kb.delete_or_create())



@router.callback_query(F.data == "delete_product")
async def delete_product(callback: types.CallbackQuery, state: FSMContext):
    pass

@router.callback_query(F.data == "create_product")
async def create_product(callback: types.CallbackQuery, state: FSMContext):
    pass

#################################################################################################