from fastapi import FastAPI
from .routers import summary

app = FastAPI()

app.include_router(
    summary.router,
    prefix="/summary"
)