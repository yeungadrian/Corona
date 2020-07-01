import streamlit as st
import requests

def show_home():
    @st.cache
    def getGlobalStats():
        Request = 'http://api:7000/summary/globalStats'
        Response = requests.get(Request).json()
        return Response

    GlobalStats = getGlobalStats()

    NewDeaths = GlobalStats['NewDeaths']
    TotalDeaths = GlobalStats['TotalDeaths']
    
    NewRecovered = GlobalStats['NewRecovered']
    TotalRecovered = GlobalStats['TotalRecovered']

    st.write(f'New deaths today: {NewDeaths}')
    st.write(f'Total deaths: {TotalDeaths}')
    st.write(f'New recoveries today: {NewRecovered}')
    st.write(f'Total Recovered: {TotalRecovered}')



    