from pandas import DataFrame, merge, Series, read_csv, concat

from base.pandas_constants import DataFrameConstants, ProcessingConstants, PathConstants, FilesConstants
from get_latitude_longitude_helper import GetLatitudeLongitudeHelper


class GetLatitudeLongitude:
    """
    Gets latitude and longitude information based on an address
    """

    @staticmethod
    def find_and_assert_latitude_longitude(
            address: str,
            neighborhood_recife: str,
            locality_recife: str
    ) -> (float, float):
        latitude, longitude = GetLatitudeLongitudeHelper.get_latitude_longitude(address)
        found = False

        if latitude and longitude:
            location = GetLatitudeLongitudeHelper.get_location(latitude, longitude)

            in_recife = GetLatitudeLongitudeHelper.check_city(location)
            belongs_to_neighborhood = GetLatitudeLongitudeHelper.check_suburb(location, neighborhood_recife)
            belongs_to_locality = GetLatitudeLongitudeHelper.check_suburb(location, locality_recife)

            found = in_recife and (belongs_to_neighborhood or belongs_to_locality)

        return (latitude, longitude) if found else (None, None)

    @staticmethod
    def get_latitude_longitude_from_occurrence(occurrence: Series, found_dict: dict):
        neighborhood = occurrence[DataFrameConstants.SOLICITACAO_BAIRRO]
        street = occurrence[DataFrameConstants.SOLICITACAO_ENDERECO]
        locality = occurrence[DataFrameConstants.SOLICITACAO_LOCALIDADE]

        neighborhood = GetLatitudeLongitudeHelper.normalize_address(neighborhood)
        street = GetLatitudeLongitudeHelper.normalize_address(street)
        locality = GetLatitudeLongitudeHelper.normalize_address(locality)

        street_recife = f'{street} {ProcessingConstants.RECIFE}'
        street_neighborhood = f'{street_recife} {neighborhood}'
        street_locality = f'{street_recife} {locality}'

        latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
            street_neighborhood,
            neighborhood,
            locality
        )

        if latitude_longitude == (None, None):
            latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
                street_locality,
                neighborhood,
                locality
            )

            if latitude_longitude == (None, None):
                latitude_longitude = GetLatitudeLongitude.find_and_assert_latitude_longitude(
                    street_recife,
                    neighborhood,
                    locality
                )
                if latitude_longitude != (None, None):
                    found_dict['street_recife'] += 1
            else:
                found_dict['street_locality'] += 1
        else:
            found_dict['street_neighborhood'] += 1

        if latitude_longitude != (None, None):
            print(f'Found latitude and longitude of occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}')

        return latitude_longitude

    @staticmethod
    def get_latitude_longitude(
            df_merged: DataFrame,
            df_found_locations: DataFrame,
            df_bad_locations: DataFrame,
            batch_size: int = 100
    ):
        # df_merged is already sorted based on the is_confirmed column

        df_outer_bad = merge(df_merged, df_bad_locations, how='outer', on=[DataFrameConstants.PROCESSO_NUMERO])
        df_outer_found = merge(df_outer_bad, df_found_locations, how='outer', on=[DataFrameConstants.PROCESSO_NUMERO])

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[0:batch_size]
        df_outer_found[DataFrameConstants.LATITUDE] = ProcessingConstants.UNKNOWN_COORDINATES
        df_outer_found[DataFrameConstants.LONGITUDE] = ProcessingConstants.UNKNOWN_COORDINATES

        found_dict = {
            'street_neighborhood': 0,
            'street_locality': 0,
            'street_recife': 0
        }

        for index, occurrence in df_outer_found.iterrows():
            latitude, longitude = GetLatitudeLongitude.get_latitude_longitude_from_occurrence(occurrence, found_dict)
            print(found_dict)

            df_outer_found.loc[index, DataFrameConstants.LATITUDE] = latitude
            df_outer_found.loc[index, DataFrameConstants.LONGITUDE] = longitude

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


def safe_read_csv(path: str, columns: list[str]) -> DataFrame:
    df = DataFrame(columns=columns)
    try:
        df = read_csv(path)
    except Exception:
        print(f'File not found: {path}, creating new file...')
    return df


if __name__ == '__main__':
    df_merged = read_csv(FilesConstants.MERGED)
    df_found_locations = safe_read_csv(FilesConstants.FOUND_LOCATIONS, df_merged.columns.to_list())
    df_bad_locations = safe_read_csv(FilesConstants.BAD_LOCATIONS, df_merged.columns.to_list())

    GetLatitudeLongitude.get_latitude_longitude(df_merged, df_found_locations, df_bad_locations, 10)
