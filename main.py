import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import nest_asyncio

from .create_db_responses import create_table

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

await create_table()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)

dp = Dispatcher()


@dp.message(Command(["start"]))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(F.text=="Начать игру")
@dp.message(Command(["quiz"]))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнём игру quiz!")
    await new_quiz(message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

