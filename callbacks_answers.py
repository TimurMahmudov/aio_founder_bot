from aiogram import F, types

from .main import dp
from .db_options import get_quiz_index, update_quiz_index, update_count_right_answers
from .quiz_questions import quiz_data
from .quiz import get_question


@dp.callback_query(F.data in ["right_answer", "wrong_answer"])
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]["correct_option"]
    options_answer = {
        "right_answer": "Верно!",
        "wrong_answer": "Неправильно. Правильный ответ: {}".format(
            quiz_data[current_question_index]["options"][correct_option]
        )
    }
    await callback.message.answer(options_answer.get(F.data))
    if F.data == "right_answer":
        await update_count_right_answers(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")

