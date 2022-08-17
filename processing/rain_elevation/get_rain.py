import code
from math import nan
from pprint import pprint
from tkinter.tix import Tree
from numpy import NaN
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
from meteostat import Hourly, Point, Stations, Daily
import time as tm



def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    # json object, various ways you can extract value
    r = requests.get(query).json()
    # one approach is to use pandas json functionality:
    elevation = pd.json_normalize(r, 'results')['elevation'].values[0]
    return elevation

def get_rain_inmep(date, hour):
    try:
        query = (f'https://apitempo.inmet.gov.br/estacao/{date}/{date}/A301')
        r = requests.get(query).json()
        rain = pd.json_normalize(r)['CHUVA'].values[hour]

        rain = float(rain)
        return rain
    except:
        return None

while(True):
    pd.set_option("display.max.columns", None)
    df = pd.read_csv("processing/rain_elevation/location.csv")
    actual_df = pd.read_csv("processing/ground_type/rain_elevation.csv")
    counters = 0
    for time in df['solicitacao_data']:
        time = time.replace(":", "")
        time = time.replace("00", "")

        temp_str = df.iat[counters, df.columns.get_loc('solicitacao_hora')] + ":00"
        df.iat[counters, df.columns.get_loc(
            'solicitacao_data')] = time + " " + temp_str
        counters += 1


    df['rain_hour'] = ''
    df['rain_day'] = ''
    df['altitude'] = ''

    df['cond'] = ''


    df['processo_numero'] = df['processo_numero'].astype(str)
    actual_df['processo_numero'] = actual_df['processo_numero'].astype(str)
    df['cond']= df['processo_numero'].isin(actual_df['processo_numero'])


    df = df[df.cond != True]

    total = len(df)
    print(total)


    df = df[:1]

    counters = 0
    try:
        for time in df["solicitacao_data"]:
            lat = float(df.iat[counters, df.columns.get_loc('latitude')])
            lon = float(df.iat[counters, df.columns.get_loc('longitude')])

            # df.iat[counters, df.columns.get_loc('altitude')] =  get_elevation(lat, lon)

            time = time.replace("-", "/")
            date_time = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')

            location = Point(lat, lon)

            year = date_time.year
            month = date_time.month
            day = date_time.day
            hour = date_time.hour
            minutes = date_time.minute
            start = datetime(year, month, day)

            end = start + timedelta(days=1)

            stations = Stations()
            stations = stations.nearby(lat, lon)
            station = stations.fetch(1)


            id = station.iat[0, station.columns.get_loc('wmo')]

            start_str = str(start)
            start_str = start_str.replace('00:00:00', '')
            min_hour = float(int(minutes)/60)
            hour_total = round(hour + min_hour)
            rain = get_rain_inmep(start_str, hour_total)
            last_rain = get_rain_inmep(start_str, 23)

            data = 'blank'
            print(start, rain, last_rain)
            if (rain == None or last_rain == None ):
                print('inmep falhou')
                data = Hourly(location, start, end) # pega a chuva das ultimas 1 hora
                data = data.fetch()
                rain = data.iat[hour_total, data.columns.get_loc('prcp')]
                rain_day = round(float(sum(data['prcp'])), 2)

                if (rain == None):
                    print('inmep falhou 2')
                    data = Hourly(id, start, end)
                    data = data.fetch()
                    rain = data.iat[hour_total, data.columns.get_loc('prcp')]
                    rain_day = round(float(sum(data['prcp'])), 2)
                
                    if (rain == None):
                        rain = -1
            else:
                try:
                    rain_day = 0
                    for i in range(24):
                        rain_day += get_rain_inmep(start_str, i)
                    rain_day = round(rain_day)
                except:
                    rain_day = -1            

            
            #tm.sleep(0.5)
            if (rain != nan and rain_day != nan):
                df.iat[counters, df.columns.get_loc('rain_hour')] = rain
                df.iat[counters, df.columns.get_loc('rain_day')] = rain_day
                df.iat[counters, df.columns.get_loc('altitude')] = get_elevation(lat, lon)

            print(counters, rain, rain_day)
            counters += 1

        df = df[df.rain_hour != '']
        df = pd.concat([df, actual_df])
        df.to_csv(r'C:\Users\parae\Documents\barreiras\barreiras\processing\ground_type\rain_elevation.csv',
                    index=False, header=True)


        print(df.info())
    except:
        df = df[df.rain_hour != '']
        df = pd.concat([df, actual_df])
        df.to_csv(r'C:\Users\parae\Documents\barreiras\barreiras\processing\ground_type\rain_elevation.csv',
                    index=False, header=True)


        print(df.info())