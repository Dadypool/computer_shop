import asyncio

from aiogram import Bot, Dispatcher
from app.config import settings

from app.bot.handlers import user, common

bot = Bot(settings.Token)
dp = Dispatcher()


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.include_routers(user.router)   # the order is important!!!
    dp.include_routers(common.router) # because the order of handlers
    asyncio.run(main())