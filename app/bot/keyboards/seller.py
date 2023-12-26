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