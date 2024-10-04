import aiosqlite

from .config import DB_NAME


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO {} (user_id, question_index) VALUES (?, ?)".format(DB_NAME),
            (user_id, index)
        )
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT question_index FROM {} WHERE user_id = (?)".format(DB_NAME),
            (user_id)
        ) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            return 0


async def update_count_right_answers(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "INSERT OR REPLACE INTO {} (user_id, right_answers) VALUES (?, right_answers + 1)".format(DB_NAME),
            (user_id)
        )
        await db.commit()

