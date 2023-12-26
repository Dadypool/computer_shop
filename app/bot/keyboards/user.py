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
            callback_data="category:cpu" # Отработано
        )
    ],
    [
        InlineKeyboardButton(
            text="Видеокарты", 
            callback_data="category:gpu"
        )
    ],
    [
        InlineKeyboardButton(
            text="Оперативная память",
            callback_data="category:ram"
        )
    ],
    [
        InlineKeyboardButton(
            text="Жесткие диски",
            callback_data="category:hdd"
        )
    ],
    [
        InlineKeyboardButton(
            text="Блоки питания",
            callback_data="category:ps"
        )
    ],
    [
        InlineKeyboardButton(
            text="Корпуса",
            callback_data="category:ps"
        )
    ],

    ])
    return category

def products(products) -> InlineKeyboardMarkup:
    inline_keyboard = [
                            [
                                InlineKeyboardButton(text=f"{index + 1}. {product['name']}, {product['price']}₽", callback_data='p:' + str(product['name']))
                            ]

                            for index, product in enumerate(products)
                        ]

    inline_keyboard.append([InlineKeyboardButton(text = "> В меню", callback_data="menu")])
    return  InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)    

def orders(orders) -> InlineKeyboardMarkup:
    inline_keyboard = [

            [
                InlineKeyboardButton(text=f"{index + 1}. {order['id']}, {order['created_at']}, {order['status']}", callback_data='o:' + str(order['id'])) 
                for index, order in enumerate(orders)
            ]

    ]
    inline_keyboard.append([InlineKeyboardButton(text = "> В меню", callback_data="menu")])
    return  InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)

def cart(products) -> InlineKeyboardMarkup:
    inline_keyboard = [
            [
                InlineKeyboardButton(text=f"{index + 1}. {product['name']}, {product['category']}, {product['manufacturer']}", callback_data='c:' + str(product['id'])) 
                for index, product in enumerate(products)
            ]
    ]
    inline_keyboard.append([InlineKeyboardButton(text = "Оформить!", callback_data="buy")])
    #inline_keyboard.append([InlineKeyboardButton(text = "> В меню", callback_data="menu")])
    return  InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)
