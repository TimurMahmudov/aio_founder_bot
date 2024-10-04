from .db_options import update_quiz_index, get_quiz_index
from .quiz_questions import quiz_data
from .generate_keyboards import generate_options_keyboard


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    question = quiz_data[current_question_index]
    correct_index, opts = question["correct_index"], question["options"]
    keyboards = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{question['question']}", reply_markup=keyboards)


async def new_quiz(message):
    user_id = message.from_user.id
    corrent_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

