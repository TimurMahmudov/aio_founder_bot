import aiosqlite

from config import DB_NAME
from db_options import TABLE_NAME


async def get_users_data():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(f"SELECT question_index, right_answers FROM {TABLE_NAME}") as cursor:
            data = await cursor.fetchall()
            return data

async def get_request_user_data(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(f"SELECT question_index, right_answers FROM {TABLE_NAME} WHERE user_id = (?)", (user_id,)) as cursor:
            user_data = await cursor.fetchone()
            return user_data


async def request_user_info(user_id):
    user_data = await get_request_user_data(user_id)
    user_result = {"count_quest": user_data[0],
                   "percent_right_answers": user_data[1]/user_data[0] * 100,
                   "right_answers": user_data[1]}
    return user_result


async def calc_results(users_data):
    out_result = {"count_players": len(users_data),
                  "all_quests": 0,
                  "others": 0}
    for index, answers in users_data:
        if index == answers:
            out_result["all_quests"] += 1
        else:
            out_result["others"] += 1
    return out_result
            


async def get_results(user_id):
    users_data = await get_users_data()
    out_result = await calc_results(users_data)
    request_user_results = await request_user_info(user_id)
    out_result.update(request_user_results)
    return out_result

