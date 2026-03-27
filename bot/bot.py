import os, logging, asyncio, aiohttp, sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

TOKEN = os.getenv("TOKEN")
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
async def cats_handler(message: types.Message, command: CommandObject):
    try:
        args = command.args
        cnt = int(args)
    except:
        await message.answer("Сколько фактов?")
        return
    try:
        facts = await get_cat_facts(cnt)
        if not facts:
            await message.answer("Фактов нет 😿")
            return
        text = "🐱 " + "\n🐱 ".join(facts)
        await message.answer(text)
    except Exception:
        await message.answer("Что-то пошло не так с API 😿")

@dp.inline_query(F.query.func(lambda q: q.isdigit()))
async def inline_number(inline_query: InlineQuery):
    try:
        num = int(inline_query.query)
    except ValueError:
        await inline_query.answer([])
        return
    try:
        facts = await get_cat_facts(num)
        if not facts:
            await inline_query.answer([])
            return
        text = "🐱 " + "\n🐱 ".join(facts)
        results = [
            InlineQueryResultArticle(
                id=f"fact{num}",
                title=f"{num} фактов",
                input_message_content=InputTextMessageContent(
                    message_text=text
                )
            )
        ]
        await inline_query.answer(results)  # Только список результатов!
    except Exception as e:
        print(f"Ошибка: {e}")  # Логируй для дебага
        await inline_query.answer([])

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
