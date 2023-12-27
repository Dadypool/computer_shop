from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import sellerstate
from app.bot.keyboards import user as user_kb, seller as seller_kb
from app.database.crud import user, product, order

router = Router()  


######################## Обработка редактирования списка товаров ################################

# Удаление:
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


# Создание:
@router.callback_query(F.data == "create_product")
async def create_product(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите занные в формате:", reply_markup=None)
    await callback.message.answer("<ID>\n<Название>\n<Цена>\n<Категория>\n<Производитель>", reply_markup=None)
    await state.set_state(sellerstate.add_product)


@router.message(sellerstate.add_product)
async def add_product(message: types.Message, state: FSMContext):
    parsed = message.text.split("\n")
    print(parsed)
    if len(parsed) != 5:
        await message.answer("Неправильно введены данные, повторите попытку")
    else:
        id, name, price, category, manufacturer = parsed
        try:
            if product.create_product({"id": int(id), "name": name, "price": int(price), "category": category, "manufacturer": manufacturer}): # (int(id), str(name), int(price), str(category), str(manufacturer))
                await message.answer("Товар успешно добавлен", reply_markup=seller_kb.sellermenu())
                await state.set_state(sellerstate.menu)
            else:
                await message.answer("Ошибка добавления, повторите попытку")
                await message.answer("<ID>\n<Название>\n<Цена>\n<Категория>\n<Производитель>", reply_markup=None)

        except:
            print(id, name, price, category, manufacturer = parsed)
            await message.answer("Неправильно введены данные, повторите попытку")
            await message.answer("<ID>\n<Название>\n<Цена>\n<Категория>\n<Производитель>", reply_markup=None)

#################################################################################################



######################## Обработка редактирования заказов ################################
@router.callback_query(F.data == "order_view")
async def order_view(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберите действие для заказа", reply_markup=seller_kb.order_action())



@router.callback_query(F.data == "approve")
async def approve(callback: types.CallbackQuery, state: FSMContext):
    orders = order.read_created_orders()
    if orders: 
        await callback.message.answer("Выберите заказ для подтверждения", reply_markup=seller_kb.orders(orders,'apv:'))
    else:
        await callback.message.answer("Нет созданных заказов", reply_markup=seller_kb.sellermenu())


@router.callback_query(F.data == "ready")
async def ready(callback: types.CallbackQuery, state: FSMContext):
    orders = order.read_confirmed_orders()
    if orders: 
        await callback.message.answer("Выберите заказ для выдачи", reply_markup=seller_kb.orders(orders, 'giv:'))
    else:
        await callback.message.answer("Нет подтвержденных заказов", reply_markup=seller_kb.sellermenu())



@router.callback_query(F.data.startswith("apv:"))
async def approve_by_id(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data[4:]
    if order.update_order_status(int(id), "confirmed"): # order.update_order_status
        await callback.message.answer("Заказ подтвержден", reply_markup=seller_kb.sellermenu())
    else:
        await callback.message.answer("Ошибка подтверждения, повторите попытку", reply_markup=seller_kb.sellermenu())
    await state.set_state(sellerstate.menu)


@router.callback_query(F.data.startswith("giv:"))
async def hardset(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data[4:]
    if order.update_order_status(int(id), "closed"): # order.update_order_status
        await callback.message.answer("Заказ выдан", reply_markup=seller_kb.sellermenu())
    else:
        await callback.message.answer("Ошибка выдачи, повторите попытку", reply_markup=seller_kb.sellermenu())
    await state.set_state(sellerstate.menu)

##########################################################################################

@router.message(sellerstate.menu)
async def echo_handler(message: types.Message) -> None:
    await message.delete()