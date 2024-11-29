import re

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

    DESLIZAMENTO_DE_BARREIRAS_KEYWORDS = [
        r'\bdeslizamento\b',
        r'\bbarreira\b',
        r'\bdeslizamento de barreira\b',
        r'\bdesabamento\b',
        r'\berosão\b',
        r'\bqueda de barreira\b',
        r'\bdesmoronamento\b',
        r'\bdeslizamento de terra\b',
        r'\brompimento\b',
        r'\bcolapso\b',
    ]

    FIELDS_NOT_RELATED_TO_LANDSLIDES = {
        ValuesConstants.ALAGAMENTOS,
        ValuesConstants.ARVORES_EM_RISCO,
        ValuesConstants.IMOVEIS_ALAGADOS,
        ValuesConstants.PRODUTOS_QUIMICOS,
        ValuesConstants.INCENDIOS,
        ValuesConstants.INVASAO_TERRENO,
        ValuesConstants.TRANSBORDAMENTO_CANAL,
        ValuesConstants.ELEVACAO_RIO
    }

    @staticmethod
    def is_related_to_deslizamento(description: str) -> bool:
        """
        Check if the description is related to deslizamentos de barreiras.
        """
        description_lower = description.lower()

        for pattern in MergeTables.DESLIZAMENTO_DE_BARREIRAS_KEYWORDS:
            if re.search(pattern, description_lower):
                return True
        return False

    @staticmethod
    def mark_confirmation_status(process: str, description: str) -> int:
        if process == ValuesConstants.DESLIZAMENTOS_DE_BARREIRAS:
            return ProcessingConstants.CONFIRMED
        elif process == ValuesConstants.IMOVEIS_COM_DANOS and MergeTables.is_related_to_deslizamento(description):
            return ProcessingConstants.MAYBE_CONFIRMED
        elif (process in MergeTables.FIELDS_NOT_RELATED_TO_LANDSLIDES
              and not MergeTables.is_related_to_deslizamento(description)):
            return ProcessingConstants.NO_LANDSLIDE
        else:
            return ProcessingConstants.NOT_CONFIRMED

    @staticmethod
    def filter_confirmed_occurrences(df: DataFrame) -> DataFrame:
        df = df[df[DataFrameConstants.SOLICITACAO_DESCRICAO] != ValuesConstants.TESTES]
        df[DataFrameConstants.IS_CONFIRMED] = df.apply(
            lambda row: MergeTables.mark_confirmation_status(
                row[DataFrameConstants.PROCESSO_OCORRENCIA], row[DataFrameConstants.SOLICITACAO_DESCRICAO]
            ), axis=1
        )
        return df.sort_values(DataFrameConstants.IS_CONFIRMED, ascending=False)

    @staticmethod
    def merge_tables(df_occurrences: DataFrame, df_types: DataFrame) -> None:
        df_merged = merge(df_occurrences, df_types)
        df_unique = df_merged.drop_duplicates(subset=[DataFrameConstants.PROCESSO_NUMERO])
        df_filtered = MergeTables.filter_confirmed_occurrences(df_unique)
        df_final = df_filtered[
            (df_filtered[DataFrameConstants.IS_CONFIRMED] == ProcessingConstants.CONFIRMED) |
            (df_filtered[DataFrameConstants.IS_CONFIRMED] == ProcessingConstants.MAYBE_CONFIRMED)
            ]
        df_no_landslide = df_filtered[df_filtered[DataFrameConstants.IS_CONFIRMED] == ProcessingConstants.NO_LANDSLIDE]
        df_final.to_csv(PathConstants.LANDSLIDE_MERGED_PATH, index=False, header=True)
        df_no_landslide.to_csv(PathConstants.NO_LANDSLIDE_MERGED_PATH, index=False, header=True)


if __name__ == '__main__':
    df_occurrences = read_csv(FilesConstants.OCCURRENCES)
    df_types = read_csv(FilesConstants.OCCURRENCES_TYPES, delimiter=DELIMITER_SEMICOLON)
    MergeTables.merge_tables(df_occurrences, df_types)
