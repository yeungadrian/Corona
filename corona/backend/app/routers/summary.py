from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json
import requests
from datetime import datetime

router = APIRouter()

class countryStatsItem(BaseModel):
    country: str
    start_date: str
    end_date: str

    class Config:
        schema_extra = {
            "example": {
                "country": "united-kingdom",
                "start_date": "2020-03-31",
                "end_date": '2020-06-20'
            }
        }


@router.get("/globalStats", tags = ['Summary'])
def globalStats():
    covid_request = 'https://api.covid19api.com/summary'

    response = requests.get(covid_request).json()

    return response['Global']

@router.get("/summaryByCountry", tags = ['Summary'])
def globalStats():
    covid_request = 'https://api.covid19api.com/summary'

    response = requests.get(covid_request).json()

    return response['Countries']

@router.post("/countryStats", tags = ['Summary'])
def countryStats(item: countryStatsItem):

    json_request = item.dict()
    start_date = json_request['start_date']
    end_date = json_request['end_date']
    country = json_request['country']

    covid_request = f'https://api.covid19api.com/total/country/{country}/status/confirmed?from={start_date}T00:00:00Z&to={end_date}T00:00:00Z'

    response = requests.get(covid_request).json()

    country_stats = pd.DataFrame(response)
    country_stats['dailycases'] = country_stats['Cases'] - country_stats['Cases'].shift(1)
    country_stats['rollingaverage'] = country_stats['dailycases'].rolling(window = 7,min_periods = 1).mean()


    statsJSON = country_stats.to_json()

    return json.loads(statsJSON)