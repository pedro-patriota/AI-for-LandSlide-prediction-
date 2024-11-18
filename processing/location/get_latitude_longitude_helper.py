from difflib import SequenceMatcher
from typing import Union, Tuple, Optional

import geopy.distance
import unicodedata
from geopy.geocoders import Nominatim
from geopy.location import Location

from base.pandas_constants import LocationConstants, ProcessingConstants


class GetLatitudeLongitudeHelper:
    """
    Helper class for get latitude and longitude
    """

    def __init__(self, lat_lon_file: str):
        self.lat_lon_file = lat_lon_file

    @staticmethod
    def similar(a: str, b: str) -> float:
        """Calculate similarity between two strings."""
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the geodesic distance between two points."""
        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)
        return geopy.distance.geodesic(coord1, coord2).km

    @staticmethod
    def normalize_address(address: str) -> str:
        """Normalize the address to a standard format."""
        replacements = {
            "CGO. ": "CÓRREGO ",
            "JD. ": "CÓRREGO ",
            "TRV ": "TRAVESSA ",
            "EST ": "ESTRADA",
            "AV ": "AVENIDA ",
            ",": " ",
            ".": " ",
            "º": " ",
            " N ": " "
        }
        for old, new in replacements.items():
            address = address.replace(old, new)
        return address.title()

    @staticmethod
    def get_latitude_longitude(address: str) -> Union[Tuple[float, float], Tuple[None, None]]:
        """Get the latitude and longitude for a given address."""
        app = Nominatim(user_agent="test")
        location = app.geocode(address)
        if location:
            location_data = location.raw
            return float(location_data['lat']), float(location_data['lon'])
        return None, None

    @staticmethod
    def get_area(address: str) -> Optional[float]:
        """Get the area of a bounding box for a given address."""
        try:
            app = Nominatim(user_agent="test")
            location = app.geocode(address).raw
            lat1, lat2 = float(location['boundingbox'][0]), float(location['boundingbox'][1])
            lon1, lon2 = float(location['boundingbox'][2]), float(location['boundingbox'][3])

            side1 = GetLatitudeLongitudeHelper.calculate_distance(lat1, lon1, lat1, lon2)
            side2 = GetLatitudeLongitudeHelper.calculate_distance(lat1, lon2, lat2, lon2)

            return side1 * side2
        except:
            return None

    @staticmethod
    def get_location(latitude: float, longitude: float) -> Location:
        """Get the location object for given latitude and longitude."""
        nominatim = Nominatim(user_agent="test")
        return nominatim.reverse(f"{latitude},{longitude}")

    @staticmethod
    def is_in_city(location: Location, city_name: str = ProcessingConstants.RECIFE) -> bool:
        """Check if the location corresponds to a specific city."""
        address = location.raw.get(LocationConstants.ADDRESS, {})
        city = address.get(LocationConstants.CITY, '')
        return city == city_name

    @staticmethod
    def assert_distance_to_neighborhood_and_locality(
            latitude: float,
            longitude: float,
            neighborhood: str,
            locality: str
    ) -> Optional[Tuple[float, float]]:
        """Assert if the distance to given neighborhood or locality is less than 1 km."""
        lat_lon = GetLatitudeLongitudeHelper.get_latitude_longitude(locality)
        if not lat_lon:
            lat_lon = GetLatitudeLongitudeHelper.get_latitude_longitude(neighborhood)
        if not lat_lon:
            return None

        lat_from_loc, lon_from_loc = lat_lon

        distance = GetLatitudeLongitudeHelper.calculate_distance(
            latitude, longitude, lat_from_loc, lon_from_loc
        )

        if distance < 1:
            return latitude, longitude
        return None

    @staticmethod
    def check_suburb(location: Location, input_suburb: str) -> bool:
        """Check if the given suburb matches the location suburb."""
        address = location.raw.get(LocationConstants.ADDRESS, {})
        suburb = address.get(LocationConstants.SUBURB, '')

        suburb_normalized = GetLatitudeLongitudeHelper._normalize_string(suburb)
        input_suburb_normalized = GetLatitudeLongitudeHelper._normalize_string(input_suburb)

        similarity = GetLatitudeLongitudeHelper.similar(suburb_normalized, input_suburb_normalized)
        return similarity > 0.7

    @staticmethod
    def _normalize_string(value: str) -> str:
        """Normalize a string to a comparable format."""
        value = unicodedata.normalize('NFD', value)
        value = ''.join(c for c in value if unicodedata.category(c) != 'Mn')
        return value.lower().replace(" ", "")
