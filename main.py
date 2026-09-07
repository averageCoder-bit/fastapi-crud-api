from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [{"id": 1, "title":"Do some chores", "done":True}, {"id": 2, "title":"Walk the dog", "done":True}, {"id": 3, "title":"Study", "done":False}]

@app.get("/tasks", summary="Read tasks")
def read_tasks() -> dict:
    return {"tasks": tasks}

@app.get("/tasks/{id}", summary="Read a specific task")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.post("/tasks", status_code=201, summary="Create a task")
def create_tasks(title: str):
    if title == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    next_id = max(task["id"] for task in tasks) + 1
    task = {
        "id":next_id,
        "title":title,
        "done":False
    }
    tasks.append(task)
    return {"Created":task}


@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, title: str | None = None, done: bool | None = None):
    for task in tasks:
        if task["id"] == id:
            task["title"] = title
            task["done"] = done
            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=404, detail="Task not found")
    

