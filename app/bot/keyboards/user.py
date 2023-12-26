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
            callback_data="order"
        )
    ],

    ])
    return usermenu

def category() -> InlineKeyboardMarkup:
    category = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Процессоры",
            callback_data="cpu" # Отработано
        )
    ],
    [
        InlineKeyboardButton(
            text="Видеокарты", 
            callback_data="gpu"
        )
    ],
    [
        InlineKeyboardButton(
            text="Оперативная память",
            callback_data="ram"
        )
    ],
    [
        InlineKeyboardButton(
            text="Жесткие диски",
            callback_data="hdd"
        )
    ],
    [
        InlineKeyboardButton(
            text="Блоки питания",
            callback_data="ps"
        )
    ],
    [
        InlineKeyboardButton(
            text="Корпуса",
            callback_data="ps"
        )
    ],

    ])
    return category
