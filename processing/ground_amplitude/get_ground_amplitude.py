import time
from typing import Union, Tuple

from geopandas import read_file, GeoDataFrame
from pandas import DataFrame, read_csv, concat
from shapely.geometry import Point

from base.pandas_constants import (
    PathConstants,
    DataFrameConstants, ValuesConstants, GroundAmplitudeConstants
)
from base.pandas_helper import PandasHelper


class GetGroundAmplitude:
    """
    Gets the ground amplitude based on the location.
    """

    @staticmethod
    def check_point_in_geojson(
            gdf: GeoDataFrame,
            latitude: float,
            longitude: float
    ) -> Union[Tuple[str, str, str], Tuple[None, None, None]]:
        """Check if a point (latitude, longitude) is inside any multipolygon in the GeoDataFrame."""
        point = Point(longitude, latitude)

        for index, row in gdf.iterrows():
            geometry = row[GroundAmplitudeConstants.GEOMETRY]
            if geometry.contains(point):
                ground_amplitude = row[GroundAmplitudeConstants.AMPLITUDE]
                slope_degree = row[GroundAmplitudeConstants.DECL_GRAU].replace('�', 'º')
                slope_percentage = row[GroundAmplitudeConstants.DECL_PER]
                print(f'Found ground amplitude of point {point}')

                return ground_amplitude, slope_degree, slope_percentage

        print(f'Did not find ground amplitude of point {point}')
        return None, None, None

    @staticmethod
    def get_ground_amplitude(
            df_ground_type: DataFrame,
            df_bad_ground_amplitude: DataFrame,
            df_found_ground_amplitude: DataFrame,
            path_found: str = PathConstants.LANDSLIDE_FOUND_GROUND_AMPLITUDE_PATH,
            path_bad: str = PathConstants.LANDSLIDE_BAD_GROUND_AMPLITUDE_PATH,
            batch_size: int = 10
    ) -> None:
        """Update the DataFrame with ground amplitude information."""
        df_outer_bad = PandasHelper.get_outer_merge(df_ground_type, df_bad_ground_amplitude)
        df_outer_found = PandasHelper.get_outer_merge(df_outer_bad, df_found_ground_amplitude)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.GROUND_AMPLITUDE] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.SLOPE_DEGREE] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.SLOPE_PERCENTAGE] = ValuesConstants.UNKNOWN_VALUE

        # Load the GeoDataFrame for the ground amplitude data
        gdf = read_file(PathConstants.PADRAO_DE_RELEVO_PATH, encoding='utf-8')

        for index, occurrence in df_outer_found.iterrows():
            latitude = occurrence[DataFrameConstants.LATITUDE]
            longitude = occurrence[DataFrameConstants.LONGITUDE]

            ground_amplitude, slope_degree, slope_percentage = GetGroundAmplitude.check_point_in_geojson(
                gdf,
                latitude,
                longitude
            )

            df_outer_found.loc[index, DataFrameConstants.GROUND_AMPLITUDE] = ground_amplitude
            df_outer_found.loc[index, DataFrameConstants.SLOPE_DEGREE] = slope_degree
            df_outer_found.loc[index, DataFrameConstants.SLOPE_PERCENTAGE] = slope_percentage

        df_bad_rows = df_outer_found[
            df_outer_found[DataFrameConstants.GROUND_AMPLITUDE].isna() |
            df_outer_found[DataFrameConstants.SLOPE_DEGREE].isna() |
            df_outer_found[DataFrameConstants.SLOPE_PERCENTAGE].isna()
            ]
        df_good_rows = df_outer_found[
            df_outer_found[DataFrameConstants.GROUND_AMPLITUDE].notna() &
            df_outer_found[DataFrameConstants.SLOPE_DEGREE].notna() &
            df_outer_found[DataFrameConstants.SLOPE_PERCENTAGE].notna()
            ]

        df_bad_ground_amplitude = concat([df_bad_ground_amplitude, df_bad_rows], ignore_index=True)
        df_found_ground_amplitude = concat([df_found_ground_amplitude, df_good_rows], ignore_index=True)

        df_bad_ground_amplitude.to_csv(path_bad, index=False, header=True)
        df_found_ground_amplitude.to_csv(path_found, index=False, header=True)


if __name__ == '__main__':
    while True:
        df_ground_type = read_csv(PathConstants.NO_LANDSLIDE_FOUND_GROUND_TYPE_PATH)
        path_found = PathConstants.NO_LANDSLIDE_FOUND_GROUND_AMPLITUDE_PATH
        path_bad = PathConstants.NO_LANDSLIDE_BAD_GROUND_AMPLITUDE_PATH

        df_found_ground_amplitude = PandasHelper.safe_read_csv(path_found, df_ground_type.columns.to_list())

        df_bad_ground_amplitude = PandasHelper.safe_read_csv(path_bad, df_ground_type.columns.to_list())

        if len(df_ground_type) == len(df_found_ground_amplitude) + len(df_bad_ground_amplitude):
            print("There is no row to process")
            break

        try:
            GetGroundAmplitude.get_ground_amplitude(
                df_ground_type=df_ground_type,
                df_bad_ground_amplitude=df_bad_ground_amplitude,
                df_found_ground_amplitude=df_found_ground_amplitude,
                path_found=path_found,
                path_bad=path_bad,
                batch_size=300
            )
            print("Finished reading batch")
        except Exception as error:
            print(error, error.__str__())
            print("Applying 10 minutes delay and trying once more...")
            time.sleep(60 * 10)
