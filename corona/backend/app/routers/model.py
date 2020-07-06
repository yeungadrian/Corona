from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np
from numpy import exp
from scipy.integrate import odeint

router = APIRouter()

class countryStatsItem(BaseModel):
    populationSize: float
    gamma: float
    sigma: float

    class Config:
        schema_extra = {
            "example": {
                "populationSize": "united-kingdom",
                "start_date": "2020-03-31",
                "end_date": '2020-06-20'
            }
        }

def F(x, t, R0=1.6):
    """
    Time derivative of the state vector.

        * x is the state vector (array_like)
        * t is time (scalar)
        * R0 is the effective transmission rate, defaulting to a constant

    """
    s, e, i = x

    # New exposure of susceptibles
    β = R0(t) * γ if callable(R0) else R0 * γ
    ne = β * s * i

    # Time derivatives
    ds = - ne
    de = ne - σ * e
    di = σ * e - γ * i

    return ds, de, di

def solve_path(R0, t_vec, x_init=x_0):
    """
    Solve for i(t) and c(t) via numerical integration,
    given the time path for R0.

    """
    G = lambda x, t: F(x, t, R0)
    s_path, e_path, i_path = odeint(G, x_init, t_vec).transpose()

    c_path = 1 - s_path - e_path       # cumulative cases
    return i_path, c_path

@router.get("/predictPaths", tags = ['Model'])
def predict_path():
    # initial conditions of s, e, i
    i_0 = 1e-7
    e_0 = 4 * i_0
    s_0 = 1 - i_0 - e_0

    x_0 = s_0, e_0, i_0

    t_length = 550
    grid_size = 1000
    t_vec = np.linspace(0, t_length, grid_size)

    R0_vals = np.linspace(1.6, 3.0, 6)
    labels = [f'$R0 = {r:.2f}$' for r in R0_vals]
    i_paths, c_paths = [], []

    for r in R0_vals:
        i_path, c_path = solve_path(r, t_vec)
        i_paths.append(i_path)
        c_paths.append(c_path)


    return i_paths