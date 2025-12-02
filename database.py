# database.py
import aiosqlite

DB = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INTEGER PRIMARY KEY,
                posicion TEXT,
                objetivo TEXT
            )
        """)
        await db.commit()

async def set_posicion(user_id, posicion):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO usuarios (user_id, posicion)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET posicion=excluded.posicion
        """, (user_id, posicion))
        await db.commit()

async def set_objetivo(user_id, objetivo):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO usuarios (user_id, objetivo)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET objetivo=excluded.objetivo
        """, (user_id, objetivo))
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT posicion, objetivo FROM usuarios WHERE user_id=?", (user_id,))
        row = await cursor.fetchone()
        return row  # (posicion, objetivo) or None
