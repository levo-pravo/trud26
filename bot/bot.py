import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://api.railway.internal:8080/facts")

bot = Bot(TOKEN)
dp = Dispatcher()


async def get_cat_facts(n: int = 3):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}?n={n}") as resp:
            data = await resp.json()
            return data.get("facts", [])


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Напиши /cats, чтобы получить факты о котах.")


@dp.message(Command("cats"))
async def cats_handler(message: types.Message):
    try:
        facts = await get_cat_facts(3)
        if not facts:
            await message.answer("Фактов нет 😿")
            return
        text = "🐱 " + "\n🐱 ".join(facts)
        await message.answer(text)
    except Exception:
        await message.answer("Что-то пошло не так с API 😿")


async def main():
    #dp.include_routers()  # на будущее, сейчас пусто
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
