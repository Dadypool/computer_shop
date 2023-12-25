import asyncio
from aiogram import Bot, Dispatcher
from botconfig import settings

dp = Dispatcher()

@dp.message()
async def echo(message):
    await message.answer(message.text)

async def main() -> None:
    bot = Bot(settings.Token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())