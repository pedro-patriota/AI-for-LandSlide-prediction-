from pandas import read_csv, merge, DataFrame

from base.pandas_constants import (
    DataFrameConstants,
    FilesConstants,
    PathConstants,
    ProcessingConstants,
    ValuesConstants,
)

DELIMITER_SEMICOLON = ';'

class MergeTables:
    """
    Merges occurrence table with occurrences type table
    """

    @staticmethod
    def mark_confirmation_status(process: str) -> int:
        if process == ValuesConstants.DESLIZAMENTOS_DE_BARREIRAS:
            return ProcessingConstants.CONFIRMED
        elif process == ValuesConstants.NAO_HA_OCORRENCIAS:
            return ProcessingConstants.MAYBE_CONFIRMED
        else:
            return ProcessingConstants.NOT_CONFIRMED

    @staticmethod
    def filter_confirmed_occurrences(df: DataFrame) -> DataFrame:
        df = df[df[DataFrameConstants.SOLICITACAO_DESCRICAO] != ValuesConstants.TESTES]
        df[DataFrameConstants.IS_CONFIRMED] = df[DataFrameConstants.PROCESSO_OCORRENCIA].apply(
            MergeTables.mark_confirmation_status
        )
        return df.sort_values(DataFrameConstants.IS_CONFIRMED, ascending=False)

    @staticmethod
    def merge_tables(df_occurrences: DataFrame, df_types: DataFrame) -> None:
        df_merged = merge(df_occurrences, df_types)
        df_filtered = MergeTables.filter_confirmed_occurrences(df_merged)
        df_filtered.to_csv(PathConstants.MERGED_PATH, index=False, header=True)


if __name__ == '__main__':
    df_occurrences = read_csv(FilesConstants.OCCURRENCES)
    df_types = read_csv(FilesConstants.OCCURRENCES_TYPES, delimiter=DELIMITER_SEMICOLON)
    MergeTables.merge_tables(df_occurrences, df_types)
