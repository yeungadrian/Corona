import streamlit as st
import requests
import pandas as pd
import altair as alt

def show_forecast():

    st.write('Without Intervention')

    constantR0JSON = {}

    population_size = st.sidebar.number_input(label = 'Population Size', value = 3.3e8)
    infected_0 = st.sidebar.number_input(label = '% Infected', value = 1e-7, step = 1e-7, format = '%f')

    constantR0JSON['populationSize'] = population_size
    constantR0JSON['infected_0'] = infected_0

    def getPredictedConstantR0(constantR0JSON):
        url = 'http://api:7000/model/predictConstantR0'
        Response = requests.post(url=url, json=constantR0JSON)
        return (Response.json())

    predictedRO = getPredictedConstantR0(constantR0JSON)
    infectedDF = pd.DataFrame(predictedRO['infectedOutput'])
    cumulativeDF = pd.DataFrame(predictedRO['cumulativeOutput'])

    infected_constantR0 = alt.Chart(infectedDF).mark_line().encode(
        x='index',
        y='infected',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    cumulative_constantR0 = alt.Chart(cumulativeDF).mark_line().encode(
        x='index',
        y='cumulative',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    st.write(infected_constantR0)

    st.write(cumulative_constantR0)

    st.write('Comparing different levels of intervention')

    def getPredictedVariableR0():
        url = 'http://api:7000/model/mitigatedPath'
        Response = requests.get(url=url)
        return (Response.json())

    predicted_variableR0 = getPredictedVariableR0()

    mitigation_levels = pd.DataFrame(predicted_variableR0['mitigatedOutput'])
    mitigation_infected = pd.DataFrame(predicted_variableR0['infectedOutput'])
    mitigation_cumulative = pd.DataFrame(predicted_variableR0['cumulativeOutput'])

    mitigation_strategies = alt.Chart(mitigation_levels).mark_line().encode(
        x='index',
        y='R0',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    infected_mitigated = alt.Chart(mitigation_infected).mark_line().encode(
        x='index',
        y='infected',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    cumulative_mitigated = alt.Chart(mitigation_cumulative).mark_line().encode(
        x='index',
        y='cumulative',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    st.write(mitigation_strategies)

    st.write(infected_mitigated)

    st.write(cumulative_mitigated)

    st.write('Ending Lockdown')