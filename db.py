import aiosqlite

DATABASE_URL = "./tasks.db"

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            )
        ''')
        await db.commit()

async def fetch_all_tasks(status=None):
    async with aiosqlite.connect(DATABASE_URL) as db:
        if status is None:
            query = "SELECT * FROM tasks"
            cursor = await db.execute(query)
        else:
            query = "SELECT * FROM tasks WHERE done = ?"
            cursor = await db.execute(query, (status,))
        rows = await cursor.fetchall()
        return rows

async def fetch_task_by_id(task_id):
    async with aiosqlite.connect(DATABASE_URL) as db:
        query = "SELECT * FROM tasks WHERE id = ?"
        cursor = await db.execute(query, (task_id,))
        row = await cursor.fetchone()
        return row

async def create_task(title, priority):
    async with aiosqlite.connect(DATABASE_URL) as db:
        query = "INSERT INTO tasks (title, priority) VALUES (?, ?)"
        cursor = await db.execute(query, (title, priority))
        await db.commit()
        return cursor.lastrowid

async def update_task(task_id, title=None, priority=None, done=None):
    async with aiosqlite.connect(DATABASE_URL) as db:
        query = "UPDATE tasks SET title = ?, priority = ?, done = ? WHERE id = ?"
        await db.execute(query, (title, priority, done, task_id))
        await db.commit()

async def delete_task(task_id):
    async with aiosqlite.connect(DATABASE_URL) as db:
        query = "DELETE FROM tasks WHERE id = ?"
        await db.execute(query, (task_id,))
        await db.commit()
