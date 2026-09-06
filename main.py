from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Hello, world"}

