import io
import json
from urllib.request import urlopen
import pandas as pd
import numpy as np
from comodels.utils import states


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


datafile = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
state_data = {}
for n in states.values():
    data = []
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
    state_data[n] = data
with open('/usr/src/app/data/multi_time_series_nytimes_data.json', 'w') as fp:
    json.dump(state_data, fp)
