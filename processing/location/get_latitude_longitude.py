import time
from typing import Tuple, List, Optional
from xmlrpc.client import Error

from pandas import DataFrame, Series, read_csv, concat

from base.pandas_constants import (
    DataFrameConstants,
    ProcessingConstants,
    PathConstants,
    FilesConstants
)
from get_latitude_longitude_helper import GetLatitudeLongitudeHelper


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
    def get_latitude_longitude_from_occurrence(occurrence: Series) -> Tuple[
        Optional[float], Optional[float], Optional[str]]:
        """Get latitude and longitude from a single occurrence."""
        neighborhood = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_BAIRRO])
        street = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_ENDERECO])
        locality = GetLatitudeLongitudeHelper.normalize_address(occurrence[DataFrameConstants.SOLICITACAO_LOCALIDADE])

        street_recife = f'{street} {ProcessingConstants.RECIFE}'
        street_neighborhood = f'{street_recife} {neighborhood}'
        street_locality = f'{street_recife} {locality}'

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

        if latitude_longitude == (None, None):
            strategy = None
        else:
            print(f'Found latitude and longitude of occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}')

        return latitude_longitude[0], latitude_longitude[1], strategy

    @staticmethod
    def get_outer_merge(df1: DataFrame, df2: DataFrame) -> DataFrame:
        """Perform an outer merge on two DataFrames and return the unique rows."""
        df_concatenated = concat([df1, df2])
        df_unique = df_concatenated.drop_duplicates(subset=[DataFrameConstants.PROCESSO_NUMERO], keep=False)
        return df_unique[df_unique.index.isin(df1.index)]

    @staticmethod
    def get_latitude_longitude(
            df_merged: DataFrame,
            df_found_locations: DataFrame,
            df_bad_locations: DataFrame,
            batch_size: int = 100
    ):
        """Process occurrences to get latitude and longitude in batches."""
        df_outer_bad = GetLatitudeLongitude.get_outer_merge(df_merged, df_bad_locations)
        df_outer_found = GetLatitudeLongitude.get_outer_merge(df_outer_bad, df_found_locations)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.LATITUDE] = ProcessingConstants.UNKNOWN_COORDINATES
        df_outer_found[DataFrameConstants.LONGITUDE] = ProcessingConstants.UNKNOWN_COORDINATES
        df_outer_found[DataFrameConstants.LOCATION_STRATEGY] = None

        for index, occurrence in df_outer_found.iterrows():
            latitude, longitude, strategy = GetLatitudeLongitude.get_latitude_longitude_from_occurrence(occurrence)

            df_outer_found.loc[index, DataFrameConstants.LATITUDE] = latitude
            df_outer_found.loc[index, DataFrameConstants.LONGITUDE] = longitude
            df_outer_found.loc[index, DataFrameConstants.LOCATION_STRATEGY] = strategy

        df_bad_rows = df_outer_found[
            df_outer_found[DataFrameConstants.LATITUDE].isna() | df_outer_found[DataFrameConstants.LONGITUDE].isna()
            ]
        df_good_rows = df_outer_found[
            df_outer_found[DataFrameConstants.LATITUDE].notna() & df_outer_found[DataFrameConstants.LONGITUDE].notna()
            ]

        df_bad_locations = concat([df_bad_locations, df_bad_rows], ignore_index=True)
        df_found_locations = concat([df_found_locations, df_good_rows], ignore_index=True)

        df_bad_locations.to_csv(PathConstants.BAD_LOCATIONS_PATH, index=False, header=True)
        df_found_locations.to_csv(PathConstants.FOUND_LOCATIONS, index=False, header=True)


def safe_read_csv(path: str, columns: List[str]) -> DataFrame:
    """Safely read a CSV file into a DataFrame, creating a new DataFrame if the file is not found."""
    df = DataFrame(columns=columns)
    try:
        df = read_csv(path)
    except Exception:
        print(f'File not found: {path}, creating new file...')
    return df


if __name__ == '__main__':
    while True:
        df_merged = read_csv(FilesConstants.MERGED)
        df_found_locations = safe_read_csv(FilesConstants.FOUND_LOCATIONS, df_merged.columns.to_list())
        df_bad_locations = safe_read_csv(FilesConstants.BAD_LOCATIONS, df_merged.columns.to_list())

        if len(df_merged) == len(df_found_locations) + len(df_bad_locations):
            print("There is no row to process")
            break

        try:
            GetLatitudeLongitude.get_latitude_longitude(df_merged, df_found_locations, df_bad_locations, 10)
            print("Finished reading batch")
        except Exception as error:
            print(Error)
            print("Trying once more...")
            time.sleep(10)
