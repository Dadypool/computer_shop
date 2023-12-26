from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import userstate
from app.bot.keyboards import user as user_kb
from app.database.crud import user, product, order

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
    product_name = callback.data.split(":")[1]

    #print(product_name)
    product_id = str(product.read_free_product_by_name(product_name)["id"])
    print(callback.from_user.id, product_id)
    if product_id:
        if product.update_add_product_to_cart(callback.from_user.id, product_id):
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer("Товар успешно добавлен в корзину!", reply_markup=user_kb.usermenu())
        else:
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer("Ошибка добавления в корзину!", reply_markup=user_kb.usermenu())
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Такого продукта нет в наличии!", reply_markup=user_kb.usermenu())
#######################################################################


######################## Просмотр заказов ########################
@router.callback_query(F.data == "order")
async def view_order(callback: types.CallbackQuery, state: FSMContext):
    orders = order.read_orders_by_user_id(callback.from_user.id)
    if orders:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Выберите заказ для просмотра", reply_markup=user_kb.orders(orders))
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("У вас нет заказов", reply_markup=user_kb.usermenu())

@router.callback_query(F.data.startswith("o:"))
async def order_list(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.data.split(":")[1]
    order_list = order.read_products_by_order_id(int(order_id)) # TODO: обработка запроса
    result_str = ""
    total_price = 0

    for index, product in enumerate(order_list, start=1):
        result_str += f"{index}. {product['name']}, price: {product['price']}€\n"
        total_price += product['price']

    result_str += f"Total: {total_price}€."
    await callback.message.answer(result_str, reply_markup=user_kb.usermenu())
##################################################################


######################## Работа с корзиной ########################
@router.callback_query(F.data == "basket")
async def basket(callback: types.CallbackQuery, state: FSMContext):
    products = order.read_products_in_cart_by_user_id(callback.from_user.id)
    if products:
        await callback.message.edit_reply_markup(reply_markup=None)
        total_price = sum(i["price"] for i in products)
        await callback.message.answer(f"Если хотите удалить какой-то товаи из корзины - выберете его.\nОбщая сумма тованов в корзине составляет {total_price}€", reply_markup=user_kb.cart(products))
    else:
        await callback.message.answer("Корзина пуста", reply_markup=user_kb.usermenu())

@router.callback_query(F.data.startswith("c:"))
async def basket_remove(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":")[1]
    if product.update_remove_product_from_cart(callback.from_user.id, product_id):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Товар успешно удален из корзины!", reply_markup=user_kb.usermenu())
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer("Ошибка удаления из корзины!", reply_markup=user_kb.usermenu())


@router.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    if order.create_order(callback.from_user.id):
        await callback.message.answer("Заказ успешно офомлен!", reply_markup=user_kb.usermenu())
    else:
        await callback.message.answer("Ошибка оформления заказа!", reply_markup=user_kb.usermenu())

##################################################################
