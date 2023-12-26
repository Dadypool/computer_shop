from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram import F

class userstate(StatesGroup):
    menu = State()      # main menu state
    register = State()  # register state
    
    


#class userstate(StatesGroup):