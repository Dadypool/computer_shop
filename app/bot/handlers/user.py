import sys, os

from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import userstate
from app.bot.keyboards import user as user_kb, seller
from app.database.crud import user, product, order

#sys.path.append(os.path.join(os.getcwd(), '..'))


router = Router()  

@router.message(userstate.register)
async def register(message: types.Message, state: FSMContext):
    if user.create_user({"id": message.from_user.id, "name": message.text, "rights": "user"}):
        await state.set_state(userstate.menu)
        await message.answer("Вы успешно зарегистрированы", reply_markup=user_kb.usermenu())
    else:
        await message.answer("Ошибка регистрации")



######################## Добавление в корзину ########################
        
@router.callback_query(F.data == "catalog") # вывод корневого каталога
async def category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберете категрию", reply_markup=user_kb.category())

@router.callback_query(F.data.startswith("category:")) # вывод подкаталога (выбранного типа товара)
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[1]
    products = product.read_product_by_category(category)
    if products:
        await callback.message.edit_reply_markup(reply_markup=user_kb.products(products))
    else:
        await callback.message.edit_reply_markup(reply_markup=user_kb.usermenu)
        await callback.message.answer("Ошибка чтения каталога.", reply_markup=user_kb.usermenu())

@router.callback_query(F.data.startswith("p:")) # добавление в корзину
async def add(callback: types.CallbackQuery, state: FSMContext):
    product = callback.data.split(":")[1]
    ### TODO: add product to basket
    ###
    ### 
    ###
    ###

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Товар успешно добавлен в корзину!", reply_markup=user_kb.usermenu())

#######################################################################


######################## Просмотр заказов ########################
@router.callback_query(F.data == "order")
async def order(callback: types.CallbackQuery, state: FSMContext):
    orders = order.read_orders_by_user_id(callable.message.from_user.id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Выберите заказ для просмотра", reply_markup=user_kb.usermenu())

##################################################################


######################## Работа с корзиной ########################
@router.callback_query(F.data == "basket")
async def basket(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Заглушка корзины", reply_markup=user_kb.usermenu())

##################################################################
