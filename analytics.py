def get_updates():
    bronx_time = []
    bronx_vaccine = []
    manhattan_time = []
    manhattan_vaccine = []
    queens_time = []
    queens_vaccine = []
    brooklyn_time = []
    brooklyn_vaccine = []

    import csv
    import plotly.express as px
    import pandas as pd

    with open('records/manhattan_vaccine_history.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[1] == 'Bronx':
                append_city(bronx_time, bronx_vaccine, row[0], row[3])
            if row[1] == 'Manhattan':
                append_city(manhattan_time, manhattan_vaccine, row[0], row[3])
            if row[1] == 'Queens':
                append_city(queens_time, queens_vaccine, row[0], row[3])
            if row[1] == 'Brooklyn':
                append_city(brooklyn_time, brooklyn_vaccine, row[0], row[3])

    final_dfs = []

    bronx_time_series = pd.Series(bronx_time, None, None, 'time')
    bronx_vaccine_series = pd.Series(bronx_vaccine, None, None, 'vaccine')
    bronx_name_series = pd.Series(["Bronx"] * len(bronx_time), None, None, 'name')
    if len(bronx_name_series) > 0:
        final_dfs.append(pd.concat([bronx_name_series, bronx_time_series, bronx_vaccine_series], axis=1))

    manhattan_time_series = pd.Series(manhattan_time, None, None, 'time')
    manhattan_vaccine_series = pd.Series(manhattan_vaccine, None, None, 'vaccine')
    manhattan_name_series = pd.Series(["Manhattan"] * len(manhattan_time), None, None, 'name')
    if len(manhattan_name_series) > 0:
        final_dfs.append(pd.concat([manhattan_name_series, manhattan_time_series, manhattan_vaccine_series], axis=1))

    queens_time_series = pd.Series(queens_time, None, None, 'time')
    queens_vaccine_series = pd.Series(queens_vaccine, None, None, 'vaccine')
    queens_name_series = pd.Series(["Queens"] * len(queens_time), None, None, 'name')
    if len(queens_name_series) > 0:
        final_dfs.append(pd.concat([queens_name_series, queens_vaccine_series], axis=1))

    brooklyn_time_series = pd.Series(brooklyn_time, None, None, 'time')
    brooklyn_vaccine_series = pd.Series(brooklyn_vaccine, None, None, 'vaccine')
    brooklyn_name_series = pd.Series(["Brooklyn"] * len(brooklyn_time), None, None, 'name')
    if len(brooklyn_name_series) > 0:
        final_dfs.append(pd.concat([brooklyn_name_series, brooklyn_time_series, brooklyn_vaccine_series], axis=1))

    fig = px.line(pd.concat(final_dfs).reset_index(drop=True), x='time', y='vaccine', color='name')
    fig.update_yaxes(rangemode='tozero')
    fig.show()

def append_city(city_time, city_vaccine, time, amount):
    if time not in city_time:
        city_time.append(time)
        city_vaccine.append(int(amount))
    else:
        city_vaccine[len(city_vaccine) - 1] += int(amount)


if __name__ == '__main__':
    get_updates()
