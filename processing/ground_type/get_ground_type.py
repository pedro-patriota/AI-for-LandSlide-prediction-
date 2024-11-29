import time

from pandas import DataFrame, read_csv, concat
from shapely import wkt, Point, MultiPolygon

from base.pandas_constants import (
    PathConstants,
    FilesConstants,
    GroundTypeConstants, DataFrameConstants, ValuesConstants
)
from base.pandas_helper import PandasHelper


class GetGroundType:
    """
    Gets the ground type based on the location
    """

    @staticmethod
    def get_label(ground_map_df: DataFrame, point: Point) -> str:
        """Get the ground type label for a given point."""
        label = None
        for multipolygon, type in zip(
                ground_map_df[GroundTypeConstants.THE_GEOM],
                ground_map_df[GroundTypeConstants.LEGENDA]
        ):
            poly = MultiPolygon(multipolygon)
            is_inside = point.within(poly)
            if is_inside:
                label = type
                break
        if label is None:
            print(f'Did not found ground type of point {point}')
        else:
            print(f'Found ground type of point {point} {label}')
        return label

    @staticmethod
    def get_ground_type(
            df_location: DataFrame,
            df_bad_ground_type: DataFrame,
            df_found_ground_type: DataFrame,
            batch_size: int = 10
    ) -> None:
        """Process ground types for a batch of points."""
        df_outer_bad = PandasHelper.get_outer_merge(df_location, df_bad_ground_type)
        df_outer_found = PandasHelper.get_outer_merge(df_outer_bad, df_found_ground_type)

        print(f'There are {len(df_outer_found)} occurrences not processed')
        print(f'Reading batch of size {batch_size}')

        df_outer_found = df_outer_found.iloc[:batch_size]
        df_outer_found[DataFrameConstants.GROUND_TYPE] = ValuesConstants.UNKNOWN_VALUE

        ground_map_df = read_csv(FilesConstants.GROUND_MAP)
        ground_map_df[GroundTypeConstants.THE_GEOM] = ground_map_df[GroundTypeConstants.THE_GEOM].apply(wkt.loads)

        for index, occurrence in df_outer_found.iterrows():
            latitude = occurrence[DataFrameConstants.LATITUDE]
            longitude = occurrence[DataFrameConstants.LONGITUDE]
            point = Point(longitude, latitude)

            df_outer_found.loc[index, DataFrameConstants.GROUND_TYPE] = GetGroundType.get_label(ground_map_df, point)

        df_bad_rows = df_outer_found[df_outer_found[DataFrameConstants.GROUND_TYPE].isna()]
        df_good_rows = df_outer_found[df_outer_found[DataFrameConstants.GROUND_TYPE].notna()]

        df_bad_ground_type = concat([df_bad_ground_type, df_bad_rows], ignore_index=True)
        df_found_ground_type = concat([df_found_ground_type, df_good_rows], ignore_index=True)

        df_bad_ground_type.to_csv(PathConstants.BAD_GROUND_TYPE, index=False, header=True)
        df_found_ground_type.to_csv(PathConstants.FOUND_GROUND_TYPE, index=False, header=True)


if __name__ == '__main__':
    while True:
        df_location = read_csv(PathConstants.LANDSLIDE_FOUND_LOCATIONS_PATH)

        df_found_ground_type = PandasHelper.safe_read_csv(
            PathConstants.LANDSLIDE_FOUND_GROUND_TYPE_PATH,
            df_location.columns.to_list()
        )
        df_bad_ground_type = PandasHelper.safe_read_csv(
            PathConstants.LANDSLIDE_BAD_GROUND_TYPE_PATH,
            df_location.columns.to_list()
        )

        if len(df_location) == len(df_found_ground_type) + len(df_bad_ground_type):
            print("There is no row to process")
            break

        try:
            GetGroundType.get_ground_type(
                df_location=df_location,
                df_bad_ground_type=df_bad_ground_type,
                df_found_ground_type=df_found_ground_type,
                batch_size=200
            )
            print("Finished reading batch")
        except Exception as error:
            print(error, error.__str__())
            print("Applying 10 minutes delay and trying once more...")
            time.sleep(60 * 10)
