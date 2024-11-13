from difflib import SequenceMatcher
from typing import Union, Tuple

import geopy.distance
import requests
import unicodedata
from geopy.geocoders import Nominatim
from geopy.location import Location

from base.pandas_constants import LocationConstants, ProcessingConstants


class GetLatitudeLongitudeHelper:
    def __init__(self, lat_lon_file):
        self.lat_lon_file = lat_lon_file

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def getDistance(lat1, lon1, lat2, lon2):  # get the distance between two points
        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)

        return geopy.distance.geodesic(coord1, coord2).km

    @staticmethod
    def normalize_address(address: str) -> str:
        address = address.replace("CGO. ", "CÓRREGO ")
        address = address.replace("JD. ", "CÓRREGO ")
        address = address.replace("TRV ", "TRAVESSA ")
        address = address.replace("EST ", "ESTRADA")
        address = address.replace("AV ", "AVENIDA ")
        address = address.replace(",", " ")
        address = address.replace(".", " ")
        address = address.replace("º", " ")
        address = address.replace(" N ", " ")

        return address.title()

    @staticmethod
    def get_latitude_longitude(address: str) -> Union[Tuple[float, float], Tuple[None, None]]:
        try:
            app = Nominatim(user_agent="test")
            location = app.geocode(address).raw

            return float(location['lat']), float(location['lon'])

        except Exception:
            return None, None

    @staticmethod
    def get_area(address):
        try:
            app = Nominatim(user_agent="test")
            location = app.geocode(address).raw
            lat1 = location['boundingbox'][0]
            lat2 = location['boundingbox'][1]
            lon1 = location['boundingbox'][2]
            lon2 = location['boundingbox'][3]

            side1 = GetLatitudeLongitudeHelper.getDistance(lat1, lon1, lat1, lon2)
            side2 = GetLatitudeLongitudeHelper.getDistance(lat1, lon2, lat2, lon2)

            area = side1 * side2

            return area
        except:
            return None

    @staticmethod
    def get_location(latitude: float, longitude: float) -> Location:
        nominatim = Nominatim(user_agent="test")
        location = nominatim.reverse(str(latitude) + "," + str(longitude))
        return location

    @staticmethod
    def check_city(location: Location) -> bool:
        address = location.raw[LocationConstants.ADDRESS]
        city = address.get(LocationConstants.CITY, '')

        if city == ProcessingConstants.RECIFE:
            return True
        else:
            return False

    @staticmethod
    def assert_distance_to_neighborhood_and_locality(
            latitude: float,
            longitude: float,
            neighborhood: str,
            locality: str
    ) -> Union[Tuple[float, float], None]:

        lat_and_lon_from_close_location = GetLatitudeLongitudeHelper.get_latitude_longitude(locality)
        if not lat_and_lon_from_close_location:
            lat_and_lon_from_close_location = GetLatitudeLongitudeHelper.get_latitude_longitude(neighborhood)
        if not lat_and_lon_from_close_location:
            return None

        latitude_from_close_location = lat_and_lon_from_close_location[0]
        longitude_from_close_location = lat_and_lon_from_close_location[1]

        if GetLatitudeLongitudeHelper.getDistance(
                latitude,
                longitude,
                latitude_from_close_location,
                longitude_from_close_location
        ) < 1:
            return latitude, longitude

    @staticmethod
    def check_suburb(location: Location, input_suburb):
        address = location.raw[LocationConstants.ADDRESS]
        suburb = address.get(LocationConstants.SUBURB, '')

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
        similarity = GetLatitudeLongitudeHelper.similar(suburb, input_suburb)

        has_same_suburb = False

        if similarity > 0.7:
            has_same_suburb = True

        return has_same_suburb
