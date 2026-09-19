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

if __name__ == "__main__":
    init_db()