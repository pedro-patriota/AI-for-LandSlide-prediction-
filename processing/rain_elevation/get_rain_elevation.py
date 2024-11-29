import time
from datetime import datetime, timedelta
from math import isnan
from typing import Optional, Tuple

from meteostat import Point, Stations
from pandas import DataFrame, read_csv, concat, Series

from base.pandas_constants import (
    RainElevationConstants,
    DataFrameConstants,
    ValuesConstants,
    PathConstants
)
from base.pandas_helper import PandasHelper
from processing.rain_elevation.get_rain_elevation_helper import GetRainElevationHelper


class GetRainElevation:
    """
    Gets the rain and elevation based on the location
    """

    @staticmethod
    def get_rain(occurrence: Series, latitude: float, longitude: float) -> Tuple[Optional[float], Optional[float]]:
        """Fetch the rain data for a given occurrence, latitude, and longitude."""
        date = occurrence[DataFrameConstants.SOLICITACAO_DATA]
        date_time_str = occurrence[DataFrameConstants.SOLICITACAO_DATA_HORA]
        year, month, day, hour, minute = GetRainElevationHelper.extract_metadata_from_date_time(date_time_str)

        minutes_in_hour = float(minute) / 60
        hour_plus_minutes = round(hour + minutes_in_hour)

        rain_hour = GetRainElevationHelper.get_rain_inmep(date, hour_plus_minutes)
        rain_day = sum(
            GetRainElevationHelper.get_rain_inmep(date, i) for i in range(24)
        ) if rain_hour is not None else None

        if rain_hour is None or rain_day is None:
            start_date = datetime(year, month, day)
            end_date = start_date + timedelta(days=1)

            location = Point(latitude, longitude)

            rain_hour, rain_day = GetRainElevationHelper.get_rain_meteostat(location, start_date, end_date, hour)
            if isnan(rain_hour) or isnan(rain_day):
                stations = Stations().nearby(latitude, longitude).fetch(3)
                for i in range(min(3, len(stations))):
                    station_id = stations.iat[i, stations.columns.get_loc(RainElevationConstants.WMO)]
                    rain_hour, rain_day = GetRainElevationHelper.get_rain_meteostat(
                        station_id,
                        start_date,
                        end_date,
                        hour
                    )
                    if not isnan(rain_hour) and not isnan(rain_day):
                        break
        if isnan(rain_hour) or isnan(rain_day):
            print(f'Did not find rain and elevation of occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]}')
        else:
            print(
                f'Found rain and elevation of occurrence {occurrence[DataFrameConstants.PROCESSO_NUMERO]} {rain_hour:.2f} {rain_day:.2f}')
        return rain_hour, rain_day

    @staticmethod
    def get_rain_elevation(
            df_danger_level: DataFrame,
            df_bad_rain_elevation: DataFrame,
            df_found_rain_elevation: DataFrame,
            path_found: str = PathConstants.LANDSLIDE_FOUND_RAIN_ELEVATION_PATH,
            path_bad: str = PathConstants.LANDSLIDE_BAD_RAIN_ELEVATION_PATH,
            batch_size: int = 5
    ) -> None:
        """Update the DataFrame with rain and elevation information."""
        df_outer_bad = PandasHelper.get_outer_merge(df_danger_level, df_bad_rain_elevation)
        df_outer_found = PandasHelper.get_outer_merge(df_outer_bad, df_found_rain_elevation)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.RAIN_DAY] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.RAIN_HOUR] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.ELEVATION] = ValuesConstants.UNKNOWN_VALUE

        df_outer_found = GetRainElevationHelper.preprocess_data(df_outer_found)
        for index, occurrence in df_outer_found.iterrows():
            latitude = occurrence[DataFrameConstants.LATITUDE]
            longitude = occurrence[DataFrameConstants.LONGITUDE]

            rain_hour, rain_day = GetRainElevation.get_rain(occurrence, latitude, longitude)
            elevation = GetRainElevationHelper.get_elevation(latitude, longitude)

            df_outer_found.loc[index, DataFrameConstants.RAIN_DAY] = rain_day
            df_outer_found.loc[index, DataFrameConstants.RAIN_HOUR] = rain_hour
            df_outer_found.loc[index, DataFrameConstants.ELEVATION] = elevation

        df_bad_rows = df_outer_found[
            df_outer_found[DataFrameConstants.RAIN_DAY].isna() |
            df_outer_found[DataFrameConstants.RAIN_HOUR].isna() |
            df_outer_found[DataFrameConstants.ELEVATION].isna()
            ]
        df_good_rows = df_outer_found[
            df_outer_found[DataFrameConstants.RAIN_DAY].notna() &
            df_outer_found[DataFrameConstants.RAIN_HOUR].notna() &
            df_outer_found[DataFrameConstants.ELEVATION].notna()
            ]

        df_bad_rain_elevation = concat([df_bad_rain_elevation, df_bad_rows], ignore_index=True)
        df_found_rain_elevation = concat([df_found_rain_elevation, df_good_rows], ignore_index=True)

        df_bad_rain_elevation.to_csv(path_bad, index=False, header=True)
        df_found_rain_elevation.to_csv(path_found, index=False, header=True)


if __name__ == '__main__':
    while True:
        df_danger_level = read_csv(PathConstants.NO_LANDSLIDE_FOUND_DANGER_LEVEL_PATH)

        path_found = PathConstants.NO_LANDSLIDE_FOUND_RAIN_ELEVATION_PATH
        path_bad = PathConstants.NO_LANDSLIDE_BAD_RAIN_ELEVATION_PATH

        df_found_rain_elevation = PandasHelper.safe_read_csv(
            path_found,
            df_danger_level.columns.to_list()
        )
        df_bad_rain_elevation = PandasHelper.safe_read_csv(
            path_bad,
            df_danger_level.columns.to_list()
        )

        if len(df_danger_level) == len(df_found_rain_elevation) + len(df_bad_rain_elevation):
            print("There is no row to process")
            break

        try:
            GetRainElevation.get_rain_elevation(
                df_danger_level=df_danger_level,
                df_bad_rain_elevation=df_bad_rain_elevation,
                df_found_rain_elevation=df_found_rain_elevation,
                path_found=path_found,
                path_bad=path_bad,
                batch_size=20
            )
            print("Finished reading batch")
        except Exception as error:
            print(error, error.__str__())
            print("Applying 10 minutes delay and trying once more...")
            time.sleep(60 * 10)
