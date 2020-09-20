from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np
from numpy import exp
from scipy.integrate import odeint
import json 
import pandas as pd

router = APIRouter()

class constantR0Item(BaseModel):
    populationSize: float
    infected_0: float

    class Config:
        schema_extra = {
            "example": {
                "populationSize": 3.3e8,
                "infected_0": 1e-7
            }
        }

@router.post("/predictConstantR0", tags = ['Model'])
def predict_path(item:constantR0Item):

    json_request = item.dict()
    population_size = json_request['populationSize']
    infected_0 = json_request['infected_0']

    sigma = 1 / 5.2 # Reflects an incubation period of 5.2 days
    gamma = 1 / 18 # Average illness duration of 18 days

    def SIRSystem(state_vector, time, R0=1.6):
        """
        Time derivative of the state vector.

            * x is the state vector (array_like)
            * t is time (scalar)
            * R0 is the effective transmission rate, defaulting to a constant

        """
        susceptible, exposed, infected = state_vector

        # New exposure of susceptibles
        beta = R0(time) * gamma if callable(R0) else R0 * gamma

        # Time derivatives
        d_susceptible = - beta * susceptible * infected
        d_exposed = -d_susceptible - sigma * exposed
        d_infected = sigma * exposed - gamma * infected

        return d_susceptible, d_exposed, d_infected

    # initial conditions of s, e, i
    exposed_0 = 4 * infected_0
    susceptible_0 = 1 - infected_0 - exposed_0

    state_vector_0 = susceptible_0, exposed_0, infected_0

    def solve_path(R0, time_vec, state_vector_init=state_vector_0):
        """
        Solve for i(t) and c(t) via numerical integration,
        given the time path for R0.

        """
        G = lambda state_vector, time: SIRSystem(state_vector, time, R0)
        susceptible_path, exposed_path, infected_path = odeint(G, state_vector_init, time_vec).transpose()

        cumulative_path = 1 - susceptible_path - exposed_path
        return infected_path, cumulative_path

    time_length = 550
    grid_size = 1000
    time_vec = np.linspace(0, time_length, grid_size)

    R0_values = np.linspace(1.6, 3.0, 6)
    labels = [f'R0 = {r:.2f}' for r in R0_values]
    infected_paths, cumulative_paths = [], []

    for r in R0_values:
        infected_path, cumulative_path = solve_path(r, time_vec)
        infected_paths.append(infected_path)
        cumulative_paths.append(cumulative_path)

    infected_DF = pd.DataFrame(infected_paths).transpose()
    infected_DF.columns = labels

    cumulative_DF = pd.DataFrame(cumulative_paths).transpose()
    cumulative_DF.columns = labels
    
    temporary_list = []
    for x in labels:
        temporary_DF = pd.DataFrame(infected_DF[x])
        temporary_DF = temporary_DF.assign(Infected=x)
        temporary_DF.columns = ['infected','symbol']
        temporary_DF = temporary_DF.reset_index()
        temporary_DF['index'] = time_vec
        temporary_list.append(temporary_DF)
    infectedOutput = (pd.concat(temporary_list)).reset_index(drop = True)

    temporary_list = []
    for x in labels:
        temporary_DF = pd.DataFrame(cumulative_DF[x])
        temporary_DF = temporary_DF.assign(Cumulative=x)
        temporary_DF.columns = ['cumulative','symbol']
        temporary_DF = temporary_DF.reset_index()
        temporary_DF['index'] = time_vec
        temporary_list.append(temporary_DF)
    cumulativeOutput = (pd.concat(temporary_list)).reset_index(drop = True)

    JSON_Output = {}
    JSON_Output['infectedOutput'] = json.loads(infectedOutput.to_json(orient = 'columns'))
    JSON_Output['cumulativeOutput'] = json.loads(cumulativeOutput.to_json(orient = 'columns'))

    return JSON_Output

@router.get("/mitigatedPath", tags = ['Model'])
def mitigatedPath():

    population_size = 3.3e8
    infected_0 = 1e-7

    sigma = 1 / 5.2 # Reflects an incubation period of 5.2 days
    gamma = 1 / 18 # Average illness duration of 18 days

    def SIRSystem(state_vector, time, R0=1.6):
        """
        Time derivative of the state vector.

            * x is the state vector (array_like)
            * t is time (scalar)
            * R0 is the effective transmission rate, defaulting to a constant

        """
        susceptible, exposed, infected = state_vector

        # New exposure of susceptibles
        beta = R0(time) * gamma if callable(R0) else R0 * gamma

        # Time derivatives
        d_susceptible = - beta * susceptible * infected
        d_exposed = -d_susceptible - sigma * exposed
        d_infected = sigma * exposed - gamma * infected

        return d_susceptible, d_exposed, d_infected

    # initial conditions of s, e, i
    exposed_0 = 4 * infected_0
    susceptible_0 = 1 - infected_0 - exposed_0

    state_vector_0 = susceptible_0, exposed_0, infected_0

    def solve_path(R0, time_vec, state_vector_init=state_vector_0):
        """
        Solve for i(t) and c(t) via numerical integration,
        given the time path for R0.

        """
        G = lambda state_vector, time: SIRSystem(state_vector, time, R0)
        susceptible_path, exposed_path, infected_path = odeint(G, state_vector_init, time_vec).transpose()

        cumulative_path = 1 - susceptible_path - exposed_path
        return infected_path, cumulative_path

    time_length = 550
    grid_size = 1000
    time_vec = np.linspace(0, time_length, grid_size)

    def R0_mitigating(time, r0=3, eta=1, r_bar=1.6):
        R0 = r0 * exp(- eta * time) + (1 - exp(- eta * time)) * r_bar
        return R0

    eta_values = 1/5, 1/10, 1/20, 1/50, 1/100
    labels = [f'eta = {eta:.2f}' for eta in eta_values]
    
    mitigating_list = []
    for eta in eta_values:
        temporary_path = pd.DataFrame(R0_mitigating(time_vec, eta=eta))
        temporary_path.columns = [len(mitigating_list)]
        mitigating_list.append(temporary_path)

    mitigated_path = pd.concat(mitigating_list, axis = 1)
    mitigated_path.columns = labels

    temporary_list = []
    for x in labels:
        temporary_DF = pd.DataFrame(mitigated_path[x])
        temporary_DF = temporary_DF.assign(restriction=x)
        temporary_DF.columns = ['R0','symbol']
        temporary_DF = temporary_DF.reset_index()
        temporary_DF['index'] = time_vec
        temporary_list.append(temporary_DF)
    mitigated_output = (pd.concat(temporary_list)).reset_index(drop = True)

    infected_paths, cumulative_paths = [], []

    for eta in eta_values:
        R0 = lambda time: R0_mitigating(time, eta=eta)
        infected_path, cumulative_path = solve_path(R0, time_vec)
        infected_paths.append(infected_path)
        cumulative_paths.append(cumulative_path)

    infected_DF = pd.DataFrame(infected_paths).transpose()
    infected_DF.columns = labels

    cumulative_DF = pd.DataFrame(cumulative_paths).transpose()
    cumulative_DF.columns = labels

    temporary_list = []
    for x in labels:
        temporary_DF = pd.DataFrame(infected_DF[x])
        temporary_DF = temporary_DF.assign(Infected=x)
        temporary_DF.columns = ['infected','symbol']
        temporary_DF = temporary_DF.reset_index()
        temporary_DF['index'] = time_vec
        temporary_list.append(temporary_DF)
    infected_output = (pd.concat(temporary_list)).reset_index(drop = True)

    temporary_list = []
    for x in labels:
        temporary_DF = pd.DataFrame(cumulative_DF[x])
        temporary_DF = temporary_DF.assign(Cumulative=x)
        temporary_DF.columns = ['cumulative','symbol']
        temporary_DF = temporary_DF.reset_index()
        temporary_DF['index'] = time_vec
        temporary_list.append(temporary_DF)
    cumulative_output = (pd.concat(temporary_list)).reset_index(drop = True)

    JSON_Output = {}
    JSON_Output['mitigatedOutput'] = json.loads(mitigated_output.to_json(orient = 'columns'))
    JSON_Output['infectedOutput'] = json.loads(infected_output.to_json(orient = 'columns'))
    JSON_Output['cumulativeOutput'] = json.loads(cumulative_output.to_json(orient = 'columns'))

    return JSON_Output