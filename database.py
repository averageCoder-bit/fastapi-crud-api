import sqlite3

DATABASE = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            done BOOLEAN
        )
    """)

    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]

    if count == 0:
        tasks = [
            {"title": "Learn FastAPI", "done": 0},
            {"title": "Learn SQLite", "done": 0},
            {"title": "Build CRUD API", "done": 0}
        ]

        c.executemany(
            "INSERT INTO tasks (title, done) VALUES (:title, :done)",
            tasks
        )

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_task(task_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def create_task(title: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, done) VALUES (:title, :done)",{"title":title, "done":0})
    task_id = c.lastrowid
    conn.commit()
    conn.close
    return task_id

def update_task(task_id: int, title: str, done: bool):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, done, task_id)
    )

    if c.rowcount == 0:
        conn.close()
        return None

    conn.commit()

    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()

    conn.close()

    return task

def delete_task_db(task_id: int):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    if c.rowcount == 0:
        conn.close()
        return False

    conn.commit()
    conn.close()

    return True


if __name__ == "__main__":
    init_db()