import streamlit as st
import requests

def show_home():
    st.write("Covid-19 Dashboard")

    st.write(r'''
    Roadmap - Should probably not live here, but

    Home
    - Simple statistics like biggest changes
    - Current stats

    Breakdown
    - Some cool stuff where you can pick your country and see stats
    - World map
    - For UK / US can be see more detail by region?

    Forecast
    - The SIR Model
    - Predictions of the SIR model
    - Seeing what different estimates of the parameters effect on the prediction
    - Estimating the parameters based on data at a point in time

    About
    - Whatever


    ''')

    def getGlobalStats():
        Request = 'http://api:7000/summary/globalStats'
        Response = requests.get(Request).json()
        return Response

    st.write(getGlobalStats())

    