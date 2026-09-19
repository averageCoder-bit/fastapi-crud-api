from fastapi import FastAPI, HTTPException
from database import init_db, get_tasks, get_task, create_task

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


# @app.put("/tasks/{id}", summary="Update a task")
# def update_task(id: int, title: str | None = None, done: bool | None = None):
#     for task in tasks:
#         if task["id"] == id:
#             task["title"] = title
#             task["done"] = done
#             return task

#     raise HTTPException(status_code=404, detail="Task not found")

# @app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
# def delete_task(id: int):
#     for task in tasks:
#         if task["id"] == id:
#             tasks.remove(task)
#             return

#     raise HTTPException(status_code=404, detail="Task not found")
    

