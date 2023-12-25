from aiogram import types
from aiogram import Dispatcher

from aiogram import Router, F
router = Router()  

@router.message()
async def echo_handler(message: types.Message):
    await message.delete()