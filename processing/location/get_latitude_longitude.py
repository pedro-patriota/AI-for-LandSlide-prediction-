import time
from typing import Tuple, Optional

from pandas import DataFrame, Series, read_csv, concat

from base.pandas_constants import (
    DataFrameConstants,
    ProcessingConstants,
    PathConstants,
    FilesConstants, ValuesConstants, LocationConstants
)
from base.pandas_helper import PandasHelper
from get_latitude_longitude_helper import GetLatitudeLongitudeHelper
import os
import googlemaps

class GetLatitudeLongitude:
    """
    Gets latitude and longitude information based on an address.
    """

    @staticmethod
    def find_and_assert_latitude_longitude(
            address: str,
            neighborhood_recife: str,
            locality_recife: str
    ) -> Tuple[Optional[float], Optional[float]]:
        """Find and assert latitude and longitude based on address."""
        latitude, longitude = GetLatitudeLongitudeHelper.get_latitude_longitude(address)
        if latitude and longitude:
            location = GetLatitudeLongitudeHelper.get_location(latitude, longitude)
            in_recife = GetLatitudeLongitudeHelper.is_in_city(location)
            belongs_to_neighborhood = GetLatitudeLongitudeHelper.check_suburb(location, neighborhood_recife)
            belongs_to_locality = GetLatitudeLongitudeHelper.check_suburb(location, locality_recife)

            if in_recife and (belongs_to_neighborhood or belongs_to_locality):
                return latitude, longitude
        return None, None

    @staticmethod
    def get_latitude_longitude_using_nominatim(
            street_recife,
            street_neighborhood,
            street_locality,
            neighborhood,
            locality
    ):
        """Get latitude and longitude from a single occurrence using nominatim api."""
        latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
            street_neighborhood,
            neighborhood,
            locality
        )
        strategy = 'street_neighborhood'

        if latitude_longitude == (None, None):
            latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
                street_locality,
                neighborhood,
                locality
            )
            strategy = 'street_locality'

            if latitude_longitude == (None, None):
                latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
                    street_recife,
                    neighborhood,
                    locality
                )
                strategy = 'street_recife'

        return latitude_longitude[0], latitude_longitude[1], strategy

    @staticmethod
    def get_latitude_longitude_from_occurrence(occurrence: Series) -> Tuple[
        Optional[float], Optional[float], Optional[str]]:
        """Get latitude and longitude from a single occurrence using google maps api."""
        neighborhood = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_BAIRRO])
        street = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_ENDERECO])
        locality = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_LOCALIDADE])

        address = street + ', ' + neighborhood + ', ' + locality + ', ' + ProcessingConstants.RECIFE

        key = str(os.environ[ProcessingConstants.API_KEY])
        strategy = ProcessingConstants.GOOGLE_MAPS_API
        gmaps = googlemaps.Client(key=key)
        geocode_result = gmaps.geocode(address)
        if not geocode_result or len(geocode_result) == 0:
            print(f"Did not found latitude and longitude for occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}")
            return None, None, None

        address_components = geocode_result[0][LocationConstants.ADDRESS_COMPONENTS]
        is_in_recife = False
        for component in address_components:
            if component[LocationConstants.LONG_NAME] == ProcessingConstants.RECIFE:
                is_in_recife = True
                break
        if not is_in_recife:
            print(f"Did not found latitude and longitude for occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}")
            return None, None, None

        latitude = (geocode_result[0][ProcessingConstants.GEOMETRY][LocationConstants.LOCATION][LocationConstants.LAT])
        longitude = (geocode_result[0][ProcessingConstants.GEOMETRY][LocationConstants.LOCATION][LocationConstants.LNG])
        print(f"Found latitude and longitude for occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}")

        return latitude, longitude, strategy

    @staticmethod
    def get_latitude_longitude(
            df_merged: DataFrame,
            df_found_locations: DataFrame,
            df_bad_locations: DataFrame,
            path_found: str = PathConstants.LANDSLIDE_FOUND_LOCATIONS_PATH,
            path_bad: str = PathConstants.LANDSLIDE_BAD_LOCATIONS_PATH,
            batch_size: int = 100
    ):
        """Process occurrences to get latitude and longitude in batches."""
        df_outer_bad = PandasHelper.get_outer_merge(df_merged, df_bad_locations)
        df_outer_found = PandasHelper.get_outer_merge(df_outer_bad, df_found_locations)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.LATITUDE] = ValuesConstants.UNKNOWN_COORDINATES
        df_outer_found[DataFrameConstants.LONGITUDE] = ValuesConstants.UNKNOWN_COORDINATES
        df_outer_found[DataFrameConstants.LOCATION_STRATEGY] = None

        for index, occurrence in df_outer_found.iterrows():
            latitude, longitude, strategy = GetLatitudeLongitude.get_latitude_longitude_from_occurrence(occurrence)

            df_outer_found.loc[index, DataFrameConstants.LATITUDE] = latitude
            df_outer_found.loc[index, DataFrameConstants.LONGITUDE] = longitude
            df_outer_found.loc[index, DataFrameConstants.LOCATION_STRATEGY] = strategy

        df_bad_rows = df_outer_found[
            df_outer_found[DataFrameConstants.LATITUDE].isna() |
            df_outer_found[DataFrameConstants.LONGITUDE].isna()
            ]
        df_good_rows = df_outer_found[
            df_outer_found[DataFrameConstants.LATITUDE].notna() &
            df_outer_found[DataFrameConstants.LONGITUDE].notna()
            ]

        df_bad_locations = concat([df_bad_locations, df_bad_rows], ignore_index=True)
        df_found_locations = concat([df_found_locations, df_good_rows], ignore_index=True)

        df_bad_locations.to_csv(path_bad, index=False, header=True)
        df_found_locations.to_csv(path_found, index=False, header=True)


if __name__ == '__main__':
    while True:
        df_merged = read_csv(PathConstants.LANDSLIDE_MERGED_PATH)
        path_found = PathConstants.LANDSLIDE_FOUND_LOCATIONS_PATH
        path_bad = PathConstants.LANDSLIDE_BAD_LOCATIONS_PATH

        df_found_locations = PandasHelper.safe_read_csv(path_found, df_merged.columns.to_list())
        df_bad_locations = PandasHelper.safe_read_csv(path_bad, df_merged.columns.to_list())

        if len(df_merged) == len(df_found_locations) + len(df_bad_locations):
            print("There is no row to process")
            break

        try:
            GetLatitudeLongitude.get_latitude_longitude(
                df_merged,
                df_found_locations,
                df_bad_locations,
                path_found=path_found,
                path_bad=path_bad,
                batch_size=50
            )
            print("Finished reading batch")
        except Exception as error:
            print(error.__str__())
            print("Applying 10 minutes delay and trying once more...")
            time.sleep(60 * 10)
