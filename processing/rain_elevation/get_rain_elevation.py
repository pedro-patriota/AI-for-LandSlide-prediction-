import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

from meteostat import Point, Stations
from pandas import DataFrame, read_csv, concat, Series

from base.pandas_constants import (
    RainElevationConstants,
    DataFrameConstants,
    ValuesConstants,
    PathConstants,
    FilesConstants
)
from base.pandas_helper import PandasHelper
from processing.rain_elevation.get_rain_elevation_helper import GetRaiElevationHelper


class GetRainElevation:
    """
    Gets the rain and elevation based on the location
    """

    @staticmethod
    def get_rain(occurrence: Series, latitude: float, longitude: float) -> Tuple[Optional[float], Optional[float]]:
        date = occurrence[DataFrameConstants.SOLICITACAO_DATA]
        date_time_str = occurrence[DataFrameConstants.SOLICITACAO_DATA_HORA]
        year, month, day, hour, minute = GetRaiElevationHelper.extract_metadata_from_date_time(date_time_str)

        minutes_in_hour = float(minute) / 60
        hour_plus_minutes = round(hour + minutes_in_hour)

        rain_hour = GetRaiElevationHelper.get_rain_inmep(date, hour_plus_minutes)
        rain_day = sum(
            GetRaiElevationHelper.get_rain_inmep(date, i) for i in range(24)
        ) if rain_hour is not None else None

        if rain_hour is None and rain_day is None:
            start_date = datetime(year, month, day)
            end_date = start_date + timedelta(days=1)

            location = Point(latitude, longitude)

            rain_hour, rain_day = GetRaiElevationHelper.get_rain_meteostat(location, start_date, end_date, hour)
            if rain_hour is None and rain_day is None:
                stations = Stations().nearby(latitude, longitude).fetch(1)
                station_id = stations.iat[0, stations.columns.get_loc(RainElevationConstants.WMO)]
                rain_hour, rain_day = GetRaiElevationHelper.get_rain_meteostat(station_id, start_date, end_date, hour)

        return rain_hour, rain_day

    @staticmethod
    def get_rain_elevation(
            df_locations: DataFrame,
            df_bad_rain_elevation: DataFrame,
            df_found_rain_elevation: DataFrame,
            batch_size: int = 5
    ) -> None:
        """Update the DataFrame with rain and elevation information."""
        df_outer_bad = PandasHelper.get_outer_merge(df_locations, df_bad_rain_elevation)
        df_outer_found = PandasHelper.get_outer_merge(df_outer_bad, df_found_rain_elevation)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.RAIN_DAY] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.RAIN_HOUR] = ValuesConstants.UNKNOWN_VALUE
        df_outer_found[DataFrameConstants.ELEVATION] = ValuesConstants.UNKNOWN_VALUE

        df_outer_found = GetRaiElevationHelper.preprocess_data(df_outer_found)
        for index, occurrence in df_outer_found.iterrows():
            latitude = occurrence[DataFrameConstants.LATITUDE]
            longitude = occurrence[DataFrameConstants.LONGITUDE]

            rain_hour, rain_day = GetRainElevation.get_rain(occurrence, latitude, longitude)
            elevation = GetRaiElevationHelper.get_elevation(latitude, longitude)

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

        df_bad_rain_elevation.to_csv(PathConstants.BAD_RAIN_ELEVATION_PATH, index=False, header=True)
        df_found_rain_elevation.to_csv(PathConstants.FOUND_RAIN_ELEVATION_PATH, index=False, header=True)


if __name__ == '__main__':
    while True:
        df_locations = read_csv(PathConstants.FOUND_LOCATIONS_PATH)

        df_found_rain_elevation = PandasHelper.safe_read_csv(
            FilesConstants.FOUND_RAIN_ELEVATION,
            df_locations.columns.to_list()
        )
        df_bad_rain_elevation = PandasHelper.safe_read_csv(
            FilesConstants.BAD_RAIN_ELEVATION,
            df_locations.columns.to_list()
        )

        if len(df_locations) == len(df_found_rain_elevation) + len(df_bad_rain_elevation):
            print("There is no row to process")
            break

        try:
            GetRainElevation.get_rain_elevation(
                df_locations=df_locations,
                df_bad_rain_elevation=df_bad_rain_elevation,
                df_found_rain_elevation=df_found_rain_elevation,
                batch_size=10
            )
            print("Finished reading batch")
        except Exception as error:
            print(error, error.__str__())
            print("Applying 10 minutes delay and trying once more...")
            time.sleep(60 * 10)
