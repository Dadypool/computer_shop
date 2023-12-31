from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram import F


class userstate(StatesGroup):
    menu = State()  # main menu state
    register = State()  # register state


class sellerstate(StatesGroup):
    menu = State()  # main menu state
    enter_id = State()  # enter id state
    add_product = State()  # add product state


# class userstate(StatesGroup):
