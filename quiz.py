import logging


from db_options import update_user_data, get_value
from quiz_questions import quiz_data
from generate_keyboards import generate_options_keyboard

START = 0


async def get_question_index(user_id):
    question_index = await get_value(user_id, "question_index")
    return question_index


async def get_right_answers(user_id):
    right_answers = await get_value(user_id, "right_answers")
    return right_answers


async def get_question(message, user_id):
    current_question_index = await get_question_index(user_id)
    question = quiz_data[current_question_index]
    correct_index, opts = question["correct_option"], question["options"]
    keyboards = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{question['question']}", reply_markup=keyboards)
    logging.info("Клавиатура с callback-ами создана")


async def new_quiz(message):
    user_id = message.from_user.id
    await update_user_data(user_id, START, START)
    logging.info("Новый квиз создан")
    await get_question(message, user_id)

