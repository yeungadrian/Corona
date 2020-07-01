from fastapi import FastAPI
from .routers import summary, country

app = FastAPI()

app.include_router(
    summary.router,
    prefix="/summary"
)

app.include_router(
    country.router,
    prefix="/country"
)