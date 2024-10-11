import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from create_db_responses import create_table
from quiz import new_quiz
from config import API_TOKEN
from callbacks_answers import router
from statistics_users import get_results

# nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнём игру quiz!")
    await new_quiz(message)


@dp.message(F.text == "statistic")
async def statistic_message(message: types.Message):
    results = await get_results(message.from_user.id)
    answer = '\n'.join(
        [f"Количество игроков: {results['count_players']}",
         f"Решивших все задания правильно: {results['all_quests']}",
         f"Решенных вами задач: {results['count_quest']}",
         f"Процент правильно решенных задач: {results['percent_right_answers']}",
         f"Количество правильно решенных задач: {results['right_answers']}"]
    )
    await message.answer(answer)


async def main():
    
    await create_table()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

