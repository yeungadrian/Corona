from fastapi import FastAPI
from .routers import daily

app = FastAPI()

app.include_router(
    daily.router,
    prefix="/daily"
)