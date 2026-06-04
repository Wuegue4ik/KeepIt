from fastapi import FastAPI, Request, Response, BackgroundTasks
from datetime import datetime
import time

from src.api.router import router as Router
from src.api.db_router import router as DB_Router

def write_log(message: str):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

app = FastAPI(
    title="NotesManagerService",
    version="0.0.3"
)

@app.middleware("http")
async def log_function(request: Request, call_next):
    background_tasks: BackgroundTasks = BackgroundTasks()
    before_r_time: float = time.time()

    response: Response = await call_next(request)

    after_r_time: float = time.time()
    message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request to \"{request.url.path}\" took {after_r_time - before_r_time} s. | {request.method}"
    background_tasks.add_task(write_log, message)

    response.background = background_tasks
    return response

app.include_router(Router, tags=["MVP Routing"])
app.include_router(DB_Router, tags=["Routers with DB"])