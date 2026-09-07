from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [{"id": 1, "title":"Do some chores", "done":True}, {"id": 2, "title":"Walk the dog", "done":True}, {"id": 3, "title":"Study", "done":False}]


@app.post("/tasks", status_code=201)
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
            

    
    

