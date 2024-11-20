from typing import List

from pandas import DataFrame, read_csv, concat

from base.pandas_constants import (
    DataFrameConstants
)


class PandasHelper:

    @staticmethod
    def safe_read_csv(path: str, columns: List[str]) -> DataFrame:
        """Safely read a CSV file into a DataFrame, creating a new DataFrame if the file is not found."""
        df = DataFrame(columns=columns)
        try:
            df = read_csv(path)
        except Exception:
            print(f'File not found: {path}, creating new file...')
        return df

    @staticmethod
    def get_outer_merge(df1: DataFrame, df2: DataFrame) -> DataFrame:
        """Perform an outer merge on two DataFrames and return the unique rows."""
        df_concatenated = concat([df1, df2])
        df_unique = df_concatenated.drop_duplicates(subset=[DataFrameConstants.PROCESSO_NUMERO], keep=False)
        return df_unique[df_unique.index.isin(df1.index)]
