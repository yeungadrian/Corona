from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import requests

router = APIRouter()


@router.get("/globalStats")
def globalStats():
    covid_request = 'https://api.covid19api.com/summary'

    response = requests.get(covid_request).json()

    return response['Global']
