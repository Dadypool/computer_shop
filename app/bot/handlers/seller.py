from aiogram import types
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.state_machine import userstate
from app.bot.keyboards import user as user_kb, seller as seller_kb
from app.database.crud import user, product, order

router = Router()  
