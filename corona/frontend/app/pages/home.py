import streamlit as st
import requests
import pandas as pd

def show_home():
    @st.cache
    def getGlobalStats():
        Request = 'http://api:7000/summary/globalStats'
        Response = requests.get(Request).json()
        return Response

    GlobalStats = getGlobalStats()
    
    NewRecovered = GlobalStats['NewRecovered']
    TotalRecovered = GlobalStats['TotalRecovered']

    st.write(f'New recoveries today: {NewRecovered}')
    st.write(f'Total Recovered: {TotalRecovered}')

    @st.cache
    def getCountryStats():
        Request = 'http://api:7000/summary/summaryByCountry'
        Response = requests.get(Request).json()
        return Response

    country_summary = pd.DataFrame(getCountryStats()).sort_values(by = ['NewConfirmed'], ascending = False).reset_index(drop = True)

    st.write('New cases today by Country')

    st.write(country_summary)
    zerocases = len(country_summary[country_summary['NewConfirmed'] == 0])
    number_countries = len(country_summary)
    percent_zerocases = round(zerocases * 100 / number_countries)
    st.write(f'There are {zerocases} countries with no new confirmed cases today, which is {percent_zerocases}%')

    