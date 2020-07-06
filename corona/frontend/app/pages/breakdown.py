import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

def show_breakdown():

    @st.cache
    def getCountries():
        Request = 'http://api:7000/country/countries'
        Response = requests.get(Request).json()
        return Response

    Countries = pd.DataFrame(getCountries())

    CountriesFormatted = Countries['Country']

    selectedCountry = st.sidebar.selectbox('Country',CountriesFormatted)

    default_date = datetime.strptime('2020-02-28', "%Y-%m-%d")

    start_date = st.sidebar.date_input('Start Date',value = default_date)

    end_date = st.sidebar.date_input('End Date')

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    countryStatsJSON = {}
    countryStatsJSON['country'] = Countries[Countries['Country'] == selectedCountry]['Slug'].reset_index(drop = True)[0]
    countryStatsJSON['start_date'] = start_date
    countryStatsJSON['end_date'] = end_date


    def getCountryStats(countryStatsJSON):
        url = 'http://api:7000/summary/countryStats'
        Response = requests.post(url=url, json=countryStatsJSON)
        return pd.DataFrame(Response.json())

    countryStats = getCountryStats(countryStatsJSON)
    countryStats['Date'] = pd.to_datetime(countryStats['Date'])

    summary = alt.Chart(countryStats).mark_line(color = 'black').encode(
        x='Date',
        y='Cases'
    ).properties(width=700)

    dailycases = alt.Chart(countryStats).mark_bar().encode(
        x='Date',
        y='dailycases'
    ).properties(width=700)

    rollingaverage = alt.Chart(countryStats).mark_line(color = 'black').encode(
        x='Date',
        y='rollingaverage'
    ).properties(width=700)


    st.write('Total Confirmed Cases')
    st.write(summary)

    st.write('Daily Cases')
    st.write(dailycases+rollingaverage)

    


