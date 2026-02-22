import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types

load_dotenv()  # ← ВАЖНО

router = Router()

TOKEN = os.getenv("BOT_TOKEN")
print(TOKEN)


@router.message()
async def start(message: types.Message):
    await message.answer(message.text)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")