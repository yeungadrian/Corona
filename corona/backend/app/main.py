from fastapi import FastAPI
from .routers import summary, country, model

app = FastAPI()

app.include_router(
    summary.router,
    prefix="/summary"
)

app.include_router(
    country.router,
    prefix="/country"
)

app.include_router(
    model.router,
    prefix="/model"
)