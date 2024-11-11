from difflib import SequenceMatcher

import geopy.distance
import pandas as pd
import requests
import unicodedata
from geopy.geocoders import Nominatim

df = pd.read_csv("merged.csv")
actual_df = pd.read_csv("../rain_elevation/location.csv")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def getDistance(lat1, lon1, lat2, lon2):  # get the distance between two points
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)

    return geopy.distance.geodesic(coord1, coord2).km


def get_local(address):
    try:
        url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1'
        location = requests.get(url=url)
        location = location.json()
        app = Nominatim(user_agent="test")
        location = app.geocode(address).raw

        return (location['lat'], location['lon'])

    except:
        return None


def get_area(address):
    try:
        app = Nominatim(user_agent="test")
        location = app.geocode(address).raw
        lat1 = location['boundingbox'][0]
        lat2 = location['boundingbox'][1]
        lon1 = location['boundingbox'][2]
        lon2 = location['boundingbox'][3]

        side1 = getDistance(lat1, lon1, lat1, lon2)
        side2 = getDistance(lat1, lon2, lat2, lon2)

        area = side1 * side2

        return area
    except:
        return None


def check_city(lat, lon):
    lat = str(lat)
    lon = str(lon)
    app2 = Nominatim(user_agent="test")
    location = app2.reverse(lat + "," + lon)
    address = location.raw['address']
    city = address.get('city', '')

    if (city == 'Recife'):
        return True
    else:
        return False


def check_suburb(lat, lon, input_suburb, input_suburb2):
    lat = str(lat)
    lon = str(lon)
    app2 = Nominatim(user_agent="test")
    location = app2.reverse(lat + "," + lon)
    address = location.raw['address']
    city = address.get('city', '')
    suburb = address.get('suburb', '')

    # filters the string suburb
    suburb = ''.join((c for c in unicodedata.normalize(
        'NFD', suburb) if unicodedata.category(c) != 'Mn'))
    suburb = suburb.lower()
    suburb = suburb.replace(" ", "")

    # filters the string input_suburb
    input_suburb = str(input_suburb)
    input_suburb = ''.join((c for c in unicodedata.normalize(
        'NFD', input_suburb) if unicodedata.category(c) != 'Mn'))
    input_suburb = input_suburb.lower()
    input_suburb = input_suburb.replace(" ", "")
    similarity = similar(suburb, input_suburb)

    input_suburb2 = str(input_suburb2)
    input_suburb2 = ''.join((c for c in unicodedata.normalize(
        'NFD', input_suburb2) if unicodedata.category(c) != 'Mn'))
    input_suburb2 = input_suburb2.lower()
    input_suburb2 = input_suburb2.replace(" ", "")

    similarity2 = similar(suburb, input_suburb2)

    if (similarity > 0.6 and city == 'Recife'):
        return True
    else:
        if (similarity2 > 0.6 and city == 'Recife'):
            return True
        else:
            print(input_suburb, input_suburb2, suburb, similarity, similarity2)
            return False


df['latitude'] = ''
df['longitude'] = ''
df['cond'] = ''

df['processo_numero'] = df['processo_numero'].astype(str)
actual_df['processo_numero'] = actual_df['processo_numero'].astype(str)
df['cond'] = df['processo_numero'].isin(actual_df['processo_numero'])

df = df[df.cond != True]

df = df[df.confirmado != 2]

print(df.info())

total = len(df)
print(total)
df = df[:100]

achou = 0

try:

    for counter, bairro in enumerate(df['solicitacao_bairro']):

        print("!!!", counter, "!!!")
        print("---", achou * 100 / (counter + 1), "%---")
        bairro = str(bairro)
        bairro = bairro.replace("CGO. ", "CÓRREGO ")
        bairro = bairro.replace("JD. ", "CÓRREGO ")
        bairro = bairro.replace("AV ", "AVENIDA ")
        bairro_recife = bairro + ' Recife '

        rua = str(df.iat[counter, df.columns.get_loc('solicitacao_endereco')])
        rua = rua.upper()
        rua = rua.replace("CGO. ", "CÓRREGO ")
        rua = rua.replace("JD. ", "CÓRREGO ")
        rua = rua.replace("TRV ", "TRAVESSA ")
        rua = rua.replace("EST ", "ESTRADA")
        rua = rua.replace("AV ", "Avenida ")
        rua = rua.replace(",", " ")
        rua = rua.replace(".", " ")
        rua = rua.replace("º", " ")
        rua = rua.replace("°", " ")
        rua = rua.replace(" N ", " ")

        rua_recife = rua + ' Recife '

        localidade = str(
            df.iat[counter, df.columns.get_loc('solicitacao_localidade')])
        localidade = localidade.replace("CGO. ", "CÓRREGO ")
        localidade = localidade.replace("JD. ", "CÓRREGO ")
        localidade = localidade.replace("AV ", "Avenida ")

        localidade_recife = localidade + ' Recife '

        first_try = rua_recife + bairro

        if (get_local(first_try) != None):
            lat_and_lon = get_local(first_try)
            lat = lat_and_lon[0]
            lon = lat_and_lon[1]
            print("Achou lat e lon1")

            if (check_suburb(lat, lon, bairro, localidade) == True):
                df.iat[counter, df.columns.get_loc('latitude')] = lat
                df.iat[counter, df.columns.get_loc('longitude')] = lon
                print("Achou cidade com bairro", first_try)
                achou += 1

            else:
                if (get_local(localidade_recife) != None):
                    lat_and_lon2 = get_local(localidade_recife)
                else:
                    lat_and_lon2 = get_local(bairro)

                try:
                    lat2 = lat_and_lon2[0]
                    lon2 = lat_and_lon2[1]
                except:
                    continue
                dist = getDistance(lat, lon, lat2, lon2)
                if (dist < 1.5):
                    print("Achou cidade com distancia", dist)
                    df.iat[counter, df.columns.get_loc('latitude')] = lat
                    df.iat[counter, df.columns.get_loc('longitude')] = lon
                    achou += 1
                else:
                    print("Lugar errado", bairro)

        else:

            second_try = rua_recife + localidade

            if (get_local(second_try) != None):
                lat_and_lon = get_local(second_try)
                lat = lat_and_lon[0]
                lon = lat_and_lon[1]
                print("Achou lat e lon2")

                if (check_suburb(lat, lon, bairro, localidade) == True):
                    df.iat[counter, df.columns.get_loc('latitude')] = lat
                    df.iat[counter, df.columns.get_loc('longitude')] = lon
                    print("Achou cidade")
                    achou += 1
                else:
                    if (get_local(localidade_recife) != None):
                        lat_and_lon2 = get_local(localidade_recife)
                    else:
                        lat_and_lon2 = get_local(bairro)

                    try:
                        lat2 = lat_and_lon2[0]
                        lon2 = lat_and_lon2[1]
                    except:
                        continue
                    dist = getDistance(lat, lon, lat2, lon2)
                    if (dist < 1.5):
                        print("Achou cidade com distancia", dist)
                        df.iat[counter, df.columns.get_loc('latitude')] = lat
                        df.iat[counter, df.columns.get_loc('longitude')] = lon
                        achou += 1
                    else:
                        print("Lugar errado", bairro)
            else:

                third_try = rua_recife

                if (get_local(third_try) != None):
                    lat_and_lon = get_local(third_try)
                    lat = lat_and_lon[0]
                    lon = lat_and_lon[1]
                    print("Achou lat e lon3")

                    if (check_suburb(lat, lon, bairro, localidade) == True):
                        df.iat[counter, df.columns.get_loc('latitude')] = lat
                        df.iat[counter, df.columns.get_loc('longitude')] = lon
                        print("Achou cidade")
                        achou += 1
                    else:
                        if (get_local(localidade_recife) != None):
                            lat_and_lon2 = get_local(localidade_recife)
                        else:
                            lat_and_lon2 = get_local(bairro)

                        try:
                            lat2 = lat_and_lon2[0]
                            lon2 = lat_and_lon2[1]
                        except:
                            continue
                        dist = getDistance(lat, lon, lat2, lon2)

                        if (dist < 1.5):
                            print("Achou cidade com distancia", dist)
                            df.iat[counter, df.columns.get_loc(
                                'latitude')] = lat
                            df.iat[counter, df.columns.get_loc(
                                'longitude')] = lon
                            achou += 1
                        else:
                            print("Lugar errado", bairro)

                else:

                    fourth_try = localidade_recife
                    if (get_area(fourth_try) != None):
                        area = get_area(fourth_try)

                        if (area < 7 and area != None):
                            lat_and_lon = get_local(fourth_try)
                            lat = lat_and_lon[0]
                            lon = lat_and_lon[1]

                            df.iat[counter, df.columns.get_loc(
                                'latitude')] = lat
                            df.iat[counter, df.columns.get_loc(
                                'longitude')] = lon
                            achou += 1

                            print("Achou lat e lon na localidade 4")
                        else:
                            print(bairro, localidade, rua)
                            print("Localidade > 7km2", area)

                    else:
                        print(bairro, localidade, rua)
                        print("Não achou no geral")

    df = df[df.latitude != '']
    df['em_recife'] = ''

    for counter, lat_lon in enumerate(df["solicitacao_bairro"]):
        lat = df.iat[counter, df.columns.get_loc('latitude')]
        lon = df.iat[counter, df.columns.get_loc('longitude')]
        if (lat != ''):
            lat = float(lat)
            lon = float(lon)

            if (check_city(lat, lon) == False):
                df.iat[counter, df.columns.get_loc('em_recife')] = 0
            else:
                print("Esta em Recife")
                df.iat[counter, df.columns.get_loc('em_recife')] = 1

    df = df[df.em_recife != 0]
    df = pd.concat([df, actual_df])

    print(f"----", {achou / total * 100}, "%-----")
    df.to_csv(r'C:\Users\parae\Documents\barreiras_prev\processing\rain_elevation\location.csv',
              index=False, header=True)

except:

    df = df[df.latitude != '']
    df['em_recife'] = ''

    for counter, lat_lon in enumerate(df["solicitacao_bairro"]):
        lat = df.iat[counter, df.columns.get_loc('latitude')]
        lon = df.iat[counter, df.columns.get_loc('longitude')]
        if (lat != ''):
            lat = float(lat)
            lon = float(lon)

            if (check_city(lat, lon) == False):
                df.iat[counter, df.columns.get_loc('em_recife')] = 0
            else:
                print("Esta em Recife")
                df.iat[counter, df.columns.get_loc('em_recife')] = 1

    df = df[df.em_recife != 0]
    df = pd.concat([df, actual_df])
    print(f"----", {achou / total * 100}, "%-----")
    df.to_csv(r'C:\Users\parae\Documents\barreiras_prev\processing\rain_elevation\location.csv',
              index=False, header=True)
