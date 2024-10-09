import logging

from aiogram import F, types, Router

from db_options import update_user_data
from quiz_questions import quiz_data
from quiz import get_question, get_right_answers, get_question_index

router = Router()


async def forming_answer(user_id, current_question_index, data):
    
    question = quiz_data[current_question_index]
    correct_option = question["correct_option"]
    right_answers = await get_right_answers(user_id)

    options_answer = {
        "right_answer": ["Верно!", right_answers + 1],
        "wrong_answer": [
            "Неправильно. Правильный ответ: {}".format(
                question["options"][correct_option]
            ),
            right_answers]
    }
    answer_data = options_answer.get(data)
    return answer_data


@router.callback_query(F.data.endswith("_answer"))
async def callback_answers(callback: types.CallbackQuery):
    logging.info(f"Пойман callback.data {callback.data}")
    user_id = callback.from_user.id
    
    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    current_question_index = await get_question_index(user_id)
    answer_data = await forming_answer(user_id, current_question_index, callback.data)
    
    await callback.message.answer(answer_data[0])

    current_question_index += 1
    await update_user_data(user_id, current_question_index, answer_data[1])

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершён!")

