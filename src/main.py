import time
from src.config import settings
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Callable, Awaitable

from src.api.router import router as Router

def write_log(message: str):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

app = FastAPI(
    title="NotesManagerService",
    version="0.0.4"
)

if settings.CORS_ORIGINS:
    cors_origins = [str(url).rstrip("/") for url in settings.CORS_ORIGINS]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

@app.middleware("http")
async def log_function(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    background_tasks: BackgroundTasks = BackgroundTasks()
    before_r_time: float = time.time()

    response: Response = await call_next(request)

    after_r_time: float = time.time()
    message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request to \"{request.url.path}\" took {after_r_time - before_r_time} s. | {request.method}"
    background_tasks.add_task(write_log, message)

    response.background = background_tasks
    return response

app.include_router(Router, tags=["Routers"])