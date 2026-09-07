from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [{"id": 1, "title":"Do some chores", "done":True}, {"id": 2, "title":"Walk the dog", "done":True}, {"id": 3, "title":"Study", "done":False}]

@app.get("/tasks")
def read_tasks() -> dict:
    return {"tasks": tasks}

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )
    
    

