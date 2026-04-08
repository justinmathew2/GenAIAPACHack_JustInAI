from fastapi import FastAPI, UploadFile, File, Form
from agents.primary_agent import handle_request
from db.database import get_tasks
from db.database import clear_tasks

app = FastAPI()

@app.get("/")
def home():
    return {"message": "JustInAI running"}

@app.post("/analyze")
async def analyze(query: str = Form(...), file: UploadFile = File(None)):
    return await handle_request(query, file)

@app.get("/tasks")
def tasks():
    return get_tasks()

@app.get("/clear_tasks")
def clear():
    clear_tasks()
    return {"message": "Tasks cleared"}    