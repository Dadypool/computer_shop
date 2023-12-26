from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def sellermenu() -> InlineKeyboardMarkup:
    usermenu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Редактировать каталог",
            callback_data="catalog_edit"
        )
    ],
    [
        InlineKeyboardButton(
            text="Просотр заказов", 
            callback_data="order_view"
        )
    ],

    ])
    return sellermenu