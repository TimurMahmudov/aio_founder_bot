import aiosqlite

from .config import DB_NAME
async def create_table():
    async with aiosqlite.connect("quiz_bot.db") as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS {} (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER,
                right_answers INTEGER)
            '''.format(DB_NAME)
        )

        await db.commit()

