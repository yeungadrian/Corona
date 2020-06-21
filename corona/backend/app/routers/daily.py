from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import requests

router = APIRouter()


@router.get("/")
def daily():

    return 'hello'
