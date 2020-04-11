import os
import requests
from random import seed, random


def _get_random(min_num, max_num):
    return random() * (max_num - min_num) + min_num


def generate_time_series_data(n):
    data = []
    seed()
    for i in range(n):
        if i == 0:
            y = _get_random(0, 1)
        else:
            y = max(data[i-1]['y'] + _get_random(-1, 1), 0)
        data.append({
            'x': i,
            'y': y
        })

    return data


def generate_multi_time_series_data(n, m):
    data = []
    seed()
    for i in range(m):
        group = 'group {}'.format(i)
        for j in range(n):
            if j == 0:
                y = _get_random(0, 1)
            else:
                y = max(data[len(data) - 1]['y'] + _get_random(-1, 1), 0)
            data.append({
                'x': j,
                'y': y,
                'group': group
            })
    return data


def generate_scatter_plot_data(n):
    data = []
    seed()
    a = _get_random(-1, 1)
    b = _get_random(0, 1)

    for i in range(n):
        x = _get_random(-1, 1)
        y = x * a + _get_random(0, b)
        data.append({'x': x, 'y': y})

    return data


def generate_multi_scatter_plot_data(n, m):
    data = []
    seed()
    for i in range(m):
        group = 'group {}'.format(i)
        a = _get_random(-1, 1)
        b = _get_random(0, 1)
        for j in range(n):
            x = _get_random(-1, 1)
            y = x * a + _get_random(0, b)
            data.append({
                'x': x,
                'y': y,
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


def generate_dosing_data(p_age=None, p_weight=None, p_bmi=None):
    pds_host = os.getenv("PDS_HOST", "localhost")
    pds_port = os.getenv("PDS_PORT", "8080")
    pds_version = os.getenv("PDS_VERSION", "v1")
    json_post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    if p_weight:
        vd = 0.3 * float(p_weight)
    else:
        vd = _get_random(22, 25)

    if p_weight and p_age:
        crcl = ((140 - float(p_age)) * float(p_weight))/(72 * 1.56)
    else:
        crcl = _get_random(29.3516, 63.4812)
    seed()
    post_input = {
        "dose": _get_random(120, 240),
        "tau": int(_get_random(8, 16)),
        "crcl":  crcl,
        "t_infusion": 0.5,
        "vd": vd,
        "num_cycles": int(_get_random(4, 8))
    }
    url_str = "http://{}:{}/{}/plugin/tx-generator-dosing/concentration_data".format(pds_host, pds_port, pds_version)
    resp = requests.post(url_str, headers=json_post_headers, json=post_input)
    if resp.status_code == 200:
        return resp.json()
    else:
        return []
