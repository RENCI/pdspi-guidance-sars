from random import seed, random
import csv
import io
import math
from typing import Any, Dict, List
from urllib.request import urlopen
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from comodels import PennDeath
from comodels.utils import states


def _get_random(min_num, max_num):
    return random() * (max_num - min_num) + min_num


def _read_data(url: str) -> dict:
    response = urlopen(url)
    byts = response.read()
    data = io.StringIO(byts.decode())
    reader = csv.DictReader(data)
    result = {}
    for row in reader:
        for column, value in row.items():
            result.setdefault(column, []).append(value)
    return result


def _convert_data(data: dict) -> dict:
    out = {}
    for k in list(data.keys())[:-1]:
        if k in ["Province/State", "Country/Region"]:
            out[k] = data[k]
        elif k in ["Lat", "Long"]:
            out[k] = list(map(float, data[k]))
        else:
            try:
                out[k] = list(map(int, data[k]))
            except ValueError:
                out[k] = [0]
    return out


def _read_nytimes_data(url:str) -> (dict, dict):
    response = urlopen(url)
    byts = response.read()
    data = io.StringIO(byts.decode())
    ori_data = pd.read_csv(data).drop('fips', axis=1)
    dates = ori_data.date.unique()
    cases = {}
    deaths = {}
    for name in states.values():
        df_filter = ori_data['state'] == name
        filter_data = ori_data[df_filter]
        cases.setdefault('state', []).append(name)
        deaths.setdefault('state', []).append(name)
        for date in dates:
            if date in filter_data.date.unique():
                cases.setdefault(date, []).append(filter_data[filter_data.date == date].iloc[0]['cases'])
                deaths.setdefault(date, []).append(filter_data[filter_data.date == date].iloc[0]['deaths'])
            else:
                cases.setdefault(date, []).append(0)
                deaths.setdefault(date, []).append(0)
    return (cases, deaths)


def _convert_nytimes_data(data: dict) -> dict:
    out = {}
    for k in list(data.keys()):
        if k == "state":
            out[k] = data[k]
        else:
            try:
                out[k] = list(map(int, data[k]))
            except ValueError:
                out[k] = [0]
    return out


def get_nytimes_state_level(d: dict) -> dict:
    idx = [
        i for i in range(len(d["state"]))
    ]
    return {k: np.array(v)[idx] for k, v in d.items()}


def get_multi_time_series_nytimes_data(state='NC'):
    data = []
    n = states[state]
    datafile = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    (cases_dict, deaths_dict) = _read_nytimes_data(datafile)
    cases_df = pd.DataFrame.from_dict(get_nytimes_state_level(_convert_nytimes_data(cases_dict)))
    deaths_df = pd.DataFrame.from_dict(get_nytimes_state_level(_convert_nytimes_data(deaths_dict)))
    case_df_filter = cases_df['state'] == n
    death_df_filter = deaths_df['state'] == n
    out = {
        'confirmed cases': cases_df[case_df_filter].drop('state', axis=1),
        'deaths': deaths_df[death_df_filter].drop('state', axis=1)
    }
    # Generate all the traces.
    # Each distancing rate is a different plot, which is made visible with the update buttons
    for key, df_values in out.items():
        for date, value in df_values.items():
            data.append({
                'x': date,
                'y': int(value),
                'group': key
            })
    return data


def get_hopkins() -> (dict, dict, dict):
    datafiles = [
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv",
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv",
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv",
    ]
    return (_convert_data(_read_data(dat)) for dat in datafiles)


def get_state_level(d: dict) -> dict:
    idx = [
        i
        for i in range(len(d["Province/State"]))
        if d["Province/State"][i] in states.values()
    ]
    return {k: np.array(v)[idx] for k, v in d.items()}


# get the growth rate from the data
def get_slope(X: pd.DataFrame) -> float:
    lm = LinearRegression()
    lm.fit(
        np.arange(X.shape[0]).reshape(-1, 1),
        X.apply(lambda x: math.log(x) if x != 0 else x),
    )
    return lm.coef_[0]


def doubling_time(gr: float) -> float:
    return 1 / np.log2(1 + gr)


def _get_model_data(state='NC', type='SIR', sds=0):
    """
    Get model output data
    :param state: name of the state to return data for
    :param type: 'SIR' or 'Hospital Use' or 'Hospital Census'
    :param sds: social distance rate within [0, 1] with 0 meaning no social distancing and 1 meaning maximal
    social distancing
    :return:
    """
    n = states[state]
    census = pd.read_csv("data/census.csv")
    pops = census[["NAME", "POPESTIMATE2019"]]
    nms = pops["NAME"]
    t_recovery = 23
    conf, dead, rec = (
        pd.DataFrame.from_dict(get_state_level(x)).drop(
            ["Lat", "Long", "Country/Region"], axis=1
        )
        for x in get_hopkins()
    )
    # the zeros mess up our slope
    state_conf = conf[conf['Province/State'] == n]
    data = state_conf.drop("Province/State", axis=1)
    data = data.iloc[0]
    data = data.loc[data != 0]
    state_growth = get_slope(data)
    td = doubling_time(state_growth)
    new_names = {i: v for i, v in enumerate(conf["Province/State"])}
    c_tot, d_tot, r_tot = (x.sum(1).rename(new_names) for x in [conf, dead, rec])

    state_curve = {}
    N = pops[pops["NAME"] == n]["POPESTIMATE2019"].values[0]
    I = c_tot[n]
    R = r_tot[n]
    D = d_tot[n]
    model = PennDeath(N, I, R, D, 0, contact_reduction=sds, t_double=td, recover_time=t_recovery)
    curve, occ = model.sir(60)
    sir = {
        k: v
        for k, v in curve.items()
        if k in ["susceptible", "infected", "recovered", "dead"]
    }
    hosp_use = {
        k: v
        for k, v in curve.items()
        if k not in ["susceptible", "infected", "recovered", "dead"]
    }
    state_curve = {"SIR": sir, "Hospital Use": hosp_use, "Hospital Census": occ}
    return state_curve


def get_multi_time_series_data(state='NC', type='SIR', sds=0):
    """

    :param state: name of the state to return data for
    :param type: 'SIR' or 'Hospital Use' or 'Hospital Census'
    :param sds: social distance rate within [0, 1] with 0 meaning no social distancing and 1 meaning maximal
    social distancing
    :return:
    """
    data = []
    out = _get_model_data(state, type, sds)
    # Generate all the traces.
    # Each distancing rate is a different plot, which is made visible with the update buttons
    for key, values in out[type].items():
        for i in range(len(values)):
            data.append({
                'x': i,
                'y': values[i],
                'group': key
            })
    return data


def generate_time_series_exponential_growth_data(n, x0=1.565, b=1.1194):
    """
    generate exponential growth SARS active case simulation data
    :param n: number of points
    :param x0: initial value of infected people
    :param b: growth rate
    :return: time series points to show exponential growth of active cases
    """
    data = []
    for i in range(n):
        if i == 0:
            y = x0
        else:
            y = x0 * b ** i
        data.append({
            'x': i,
            'y': int(y + 0.5)
        })

    return data


def generate_multi_time_series_exponential_growth_data(n, m, groups):
    """
    generate multiple exponential growth SARS active case simulation data
    :param n: number of points
    :param m: number of groups
    :return: time series points to show exponential growth of multiple groups
    """
    data = []
    for i in range(m):
        group = groups[i]
        x0 = 1.565
        b = 1.1194
        for j in range(n):
            if j == 0:
                y = x0 + i * 10
            else:
                y = x0 * b ** j + i * 10
            data.append({
                'x': j,
                'y': int(y + 0.5),
                'group': group
            })
    return data


def generate_scatter_plot_data(n):
    data = []
    seed()
    a = _get_random(0, 1)
    b = _get_random(0, 500)

    for i in range(n):
        x = _get_random(0, 5000)
        y = x * a + _get_random(0, b)
        data.append({'x': int(x), 'y': int(y)})

    return data


def generate_multi_scatter_plot_data(n, m, groups):
    data = []
    seed()
    for i in range(m):
        group = groups[i]
        a = _get_random(0, 1)
        b = _get_random(0, 500)
        for j in range(n):
            x = _get_random(0, 5000)
            y = x * a + _get_random(0, b)
            data.append({
                'x': int(x),
                'y': int(y),
                'group': group
            })
    return data


def generate_histogram_data(n):
    data = []
    seed()
    for i in range(n):
        x = round(_get_random(1, 10))
        data.append({
            'x': x
        })
    return data

