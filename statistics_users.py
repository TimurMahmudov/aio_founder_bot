import aiosqlite

from .config import DB_NAME


async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "SELECT question_index, right_answers
             FROM 

