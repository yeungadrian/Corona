from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import requests

router = APIRouter()


@router.get("/countries", tags = ['Country'])
def countries():
    covid_request = 'https://api.covid19api.com/countries'

    response = requests.get(covid_request).json()

    return response

