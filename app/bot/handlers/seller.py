from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import sellerstate
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
    await callback.message.answer("Введите id товара для удаления", reply_markup=None)
    await state.set_state(sellerstate.enter_id)

@router.message(sellerstate.enter_id)
async def enter_id(message: types.Message, state: FSMContext):
    product_to_delete = product.read_product_by_id(int(message.text))
    if product_to_delete == None:
        await message.answer("Такого товара не существует, повторите попытку")
    else:
        await message.answer(f"Подтвердите уддаление товара:\nID: {product_to_delete['id']}\nНазвание: {product_to_delete['name']}\nЦена: {product_to_delete['price']}", reply_markup=seller_kb.yes_or_no(product_to_delete['id']))
        await state.set_state(sellerstate.menu)

@router.callback_query(F.data.startswith("delid:"))
async def delete_product(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    id = callback.data[6:]
    if product.delete_product(int(id)):
        await callback.message.answer("Товар успешно удален", reply_markup=seller_kb.sellermenu())
        await state.set_state(sellerstate.menu)
    else:
        await callback.message.answer("Ошибка удаления, повторите попытку", reply_markup=seller_kb.sellermenu())
        await state.set_state(sellerstate.menu)

@router.callback_query(F.data == "create_product")
async def create_product(callback: types.CallbackQuery, state: FSMContext):
    pass


#################################################################################################