from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# main user menu

def usermenu() -> InlineKeyboardMarkup:
    usermenu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Каталог",
            callback_data="catalog" # Отработано
        )
    ],
    [
        InlineKeyboardButton(
            text="Корзина", 
            callback_data="basket"
        )
    ],
    [
        InlineKeyboardButton(
            text="Мои заказы",
            callback_data="Order"
        )
    ]

    ])
    return usermenu
