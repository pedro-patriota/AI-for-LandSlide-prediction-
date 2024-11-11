from pandas import read_csv, merge, DataFrame

from base.pandas_constants import (
    DataFrameConstants,
    FilesConstants,
    PathConstants,
    ProcessingConstants,
    ValuesConstants,
)


class MergeTables:
    """
    Merges occurrence table with occurrences type table
    """

    @staticmethod
    def filter_confirmed_occurrences(df_calls_and_types: DataFrame) -> DataFrame:
        df_calls_and_types = df_calls_and_types[
            df_calls_and_types[DataFrameConstants.SOLICITACAO_DESCRICAO] != ValuesConstants.TESTES
            ]

        is_confirmed = []
        for process in df_calls_and_types[DataFrameConstants.PROCESSO_OCORRENCIA]:
            if process == ValuesConstants.DESLIZAMENTOS_DE_BARREIRAS:
                is_confirmed.append(ProcessingConstants.CONFIRMED)
            elif process == ValuesConstants.NAO_HA_OCORRENCIAS:
                is_confirmed.append(ProcessingConstants.MAYBE_CONFIRMED)
            else:
                is_confirmed.append(ProcessingConstants.NOT_CONFIRMED)

        df_calls_and_types[DataFrameConstants.IS_CONFIRMED] = is_confirmed

        return df_calls_and_types.sort_values(DataFrameConstants.IS_CONFIRMED, ascending=False)

    @staticmethod
    def merge_tables(df_occurrences: DataFrame, df_types: DataFrame):
        df_calls_and_types = merge(df_occurrences, df_types)
        df_calls_and_types_after_filters = MergeTables.filter_confirmed_occurrences(df_calls_and_types)

        df_calls_and_types_after_filters.to_csv(PathConstants.LOCATION_MERGED, index=False, header=True)


if __name__ == '__main__':
    df_occurrences = read_csv(FilesConstants.OCCURRENCES)
    df_types = read_csv(FilesConstants.OCCURRENCES_TYPES, delimiter=';')

    MergeTables.merge_tables(df_occurrences, df_types)
