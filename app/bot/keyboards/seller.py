from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def sellermenu() -> InlineKeyboardMarkup:
    sellermenu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Редактировать каталог",
            callback_data="catalog_edit"
        )
    ],
    [
        InlineKeyboardButton(
            text="Просмотр заказов", 
            callback_data="order_view"
        )
    ],

    ])
    return sellermenu

def delete_or_create() -> InlineKeyboardMarkup:
    delete_or_create = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Удалить товар",
            callback_data="delete_product"
        )
    ],
    [
        InlineKeyboardButton(
            text="Создать товар",
            callback_data="create_product"
        )
    ],

    ])
    return delete_or_create


def yes_or_no(id) -> InlineKeyboardMarkup:
    yes_or_no = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Да",
            callback_data="delid:" + str(id)
        )
    ],
    [
        InlineKeyboardButton(
            text="Нет",
            callback_data="menu"
        )
    ],

    ])
    return yes_or_no

def order_action() -> InlineKeyboardMarkup:
    order_action = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="На подтверждение",
            callback_data="approve"
        )
    ],
    [
        InlineKeyboardButton(
            text="На выдачу",
            callback_data="ready"
        )
    ],
    [
        InlineKeyboardButton(
            text="Hardset",
            callback_data="hardset"
        )
    ],
    ])
    return order_action

def orders(orders, key) -> InlineKeyboardMarkup:
    inline_keyboard = [

            [
                InlineKeyboardButton(text=f"Заказ №{order['id']} от {order['created_at'].strftime('%d.%m.%Y %H:%M')}", callback_data=str(key) + str(order['id'])) 
                for order in orders
            ]

    ]
    inline_keyboard.append([InlineKeyboardButton(text = "> В меню", callback_data="menu")])
    return  InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)



