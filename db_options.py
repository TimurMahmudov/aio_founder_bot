import aiosqlite

from config import DB_NAME

TABLE_NAME="quiz_state"


async def update_user_data(user_id, question_index, right_answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT OR REPLACE INTO {} (user_id, question_index, right_answers) VALUES (?, ?, ?)
            '''.format(TABLE_NAME), (user_id, question_index, right_answers)
        )
        await db.commit()


async def get_value(user_id, param):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT {} FROM {} WHERE user_id = (?)".format(param, TABLE_NAME),
            (user_id,)
        ) as cursor:
            results = await cursor.fetchone()
            if not results:
                return 0
            return results[0]

