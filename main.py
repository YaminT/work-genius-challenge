from typing import Union

from fastapi import APIRouter, FastAPI
from api import auth_router, teams_router, membership_router

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(teams_router, prefix="/team")
app.include_router(membership_router, prefix="/membership")


@app.get("/")
def main_page():
    return {"Message": "Hello from work genius"}
