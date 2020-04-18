from random import seed, random


def _get_random(min_num, max_num):
    return random() * (max_num - min_num) + min_num


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
