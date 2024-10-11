from aiogram import Router, types
from aiogram.filters.command import Command

from statistics_users import get_results

statistic_router = Router()


@statistic_router.message(Command("statistic"))
async def statistic_message(message: types.Message):
    results = await get_results(message.from_user.id)
    answer = '\n'.join([f"Количество игроков: {results['count_players']}",
              f"Решивших все задания правильно: {results['all_quests']}",
              f"Решенных вами задач: {results['cout_quest']}",
              f"Процент правильно решенных задач: {results['percent_right_answers']}", 
              f"Количество правильно решенных задач: {results['right_answers']}"])
    await message.answer(answer)

