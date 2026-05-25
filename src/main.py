from fastapi import FastAPI, Request, Response
from typing import Callable
from datetime import datetime
import time

from src.api.router import router

app = FastAPI(
    title="NotesManagerService",
    version="0.0.2"
)

@app.middleware("http")
async def log_function(request: Request, call_next: Callable):
    before_r_time: float = time.time()

    response: Response = await call_next(request)

    after_r_time: float = time.time()
    print(f"[{datetime.now()}] Request to {request.url.path} took {after_r_time - before_r_time} s.")

    return response

app.include_router(router, tags=["StartUpRouting"])