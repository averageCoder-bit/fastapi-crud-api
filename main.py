from fastapi import FastAPI, HTTPException
from database import init_db, get_tasks, get_task, create_task, update_task, delete_task_db

app = FastAPI()
init_db()

@app.get("/tasks", summary="Read tasks")
def read_tasks() -> dict:
    rows = get_tasks()

    tasks = [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

    return {"tasks": tasks}

@app.get("/tasks/{task_id}", summary="Read a task")
def read_task(task_id: int) -> dict:
    row = get_task(task_id)

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.post("/tasks", status_code=201, summary="Create a task")
def create_tasks(title: str):
    if title == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    task_id = create_task(title)

    return {
        "id": task_id,
        "title": title,
        "done": False
    }


@app.put("/tasks/{task_id}", summary="Update a task")
def update_tasks(task_id: int, title: str | None = None, done: bool | None = None):
    if title is None and done is None:
        raise HTTPException(status_code=400, detail="No fields to update")

    existing = get_task(task_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if title is None:
        title = existing["title"]

    if done is None:
        done = bool(existing["done"])

    task = update_task(task_id, title, done)

    return {
        "id": task["id"],
        "title": task["title"],
        "done": bool(task["done"])
    }

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    deleted = delete_task_db(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return
    

