from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from models import TaskCreate, TaskUpdate
import db

app = FastAPI()

# В FastAPI используются `@app.get()` и `@app.post()`, не `@app.route()`
@app.get("/")
async def serve_html():
    return FileResponse('templates/index.html')

@app.on_event("startup")
async def startup():
    await db.init_db()

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    task_id = await db.create_task(task.title, task.priority)
    return {"id": task_id, "title": task.title, "priority": task.priority, "done": False}

@app.get("/tasks", response_model=list)
async def get_tasks(status: bool = None):
    tasks = await db.fetch_all_tasks(status)
    return tasks

@app.get("/tasks/{task_id}", response_model=dict)
async def get_task(task_id: int):
    task = await db.fetch_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, task: TaskUpdate):
    existing_task = await db.fetch_task_by_id(task_id)
    
    # Проверяем формат existing_task
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Если existing_task - кортеж, преобразуй его в словарь
    if isinstance(existing_task, tuple):
        existing_task = {
            'id': existing_task[0],
            'title': existing_task[1],
            'priority': existing_task[2],
            'done': existing_task[3]
        }
    
    await db.update_task(
        task_id,
        task.title or existing_task['title'],
        task.priority or existing_task['priority'],
        task.done if task.done is not None else existing_task['done']
    )
    
    updated_task = await db.fetch_task_by_id(task_id)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found after update")
    
    return updated_task

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    task = await db.fetch_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete_task(task_id)
    return {"result": True}
