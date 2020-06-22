import streamlit as st
import requests
from pages.home import * 
from pages.about import * 
from pages.breakdown import * 
from pages.forecast import * 

st.sidebar.title('Covid-19 Dashboard')

appOptions = ["Home","Breakdown","Forecast","About"]

currentPage = st.sidebar.radio("Go to", appOptions)

if currentPage == "Home":
    st.title('Dashboard')
    show_home()

if currentPage == "Breakdown":
    st.title('Breakdown')
    show_breakdown()

if currentPage == "Forecast":
    st.title('Forecast')
    show_forecast()


if currentPage == "About":
    st.title('About')
    show_about()

