from datetime import datetime
from math import nan
from typing import Optional, Tuple, Union

import requests
from meteostat import Hourly, Point, Daily
from pandas import DataFrame, json_normalize

from base.pandas_constants import RainElevationConstants, ProcessingConstants, DataFrameConstants


class GetRaiElevationHelper:
    """
    Helper class for get rain and altitude
    """

    @staticmethod
    def get_elevation(lat: float, long: float) -> Optional[float]:
        """Get the elevation for a given latitude and longitude using Open Elevation API."""
        query = f'{RainElevationConstants.ELEVATION_API}{lat},{long}'
        elevation = None
        try:
            response = requests.get(query).json()
            elevation = json_normalize(
                response,
                ProcessingConstants.RESULTS
            )[RainElevationConstants.ELEVATION].values[0]
        except Exception:
            pass
        return elevation

    @staticmethod
    def get_rain_inmep(date: str, hour: int) -> Optional[float]:
        """Fetch rain data from INMEP API for a specific date and hour."""
        rain = None
        try:
            query = f'{RainElevationConstants.RAIN_INMEP_API}/{date}/{date}/{RainElevationConstants.INMEP_STATION}'
            r = requests.get(query).json()
            rain = json_normalize(r)['CHUVA'].values[hour]
            rain = float(rain)
        except:
            pass
        return rain

    @staticmethod
    def get_rain_meteostat(
            station: Union[Point, int],
            start_date: datetime,
            end_date: datetime,
            hour: int
    ) -> Tuple[Optional[float], Optional[float]]:
        rain_hour, rain_day = nan, nan
        try:
            data = Hourly(station, start_date, end_date, timezone=RainElevationConstants.TIMEZONE).fetch()
            rain_hour = data.iat[hour, data.columns.get_loc(RainElevationConstants.PRCP)]
            rain_day = round(float(sum(data[RainElevationConstants.PRCP])), 2)
        except Exception as error:
            print(error.__str__())
            pass
        return rain_hour, rain_day

    @staticmethod
    def extract_metadata_from_date_time(date_time_str: str) -> tuple[int, int, int, int, int]:
        date_time = datetime.strptime(date_time_str, '%Y/%m/%d %H:%M:%S')
        return date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute

    @staticmethod
    def preprocess_data(df: DataFrame) -> DataFrame:
        """Preprocess the data to format date and time correctly."""
        df[DataFrameConstants.SOLICITACAO_DATA] = df[DataFrameConstants.SOLICITACAO_DATA].str.replace('-', '/')

        df[DataFrameConstants.SOLICITACAO_DATA_HORA] = df[DataFrameConstants.SOLICITACAO_DATA] + ' ' + df[
            DataFrameConstants.SOLICITACAO_HORA].astype(str) + ':00'

        return df
