import asyncio

from aiogram import Bot, Dispatcher
from botconfig import settings

from handlers import user, common

bot = Bot(settings.Token)
dp = Dispatcher()


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.include_routers(common.router)
    dp.include_routers(user.router)
    asyncio.run(main())