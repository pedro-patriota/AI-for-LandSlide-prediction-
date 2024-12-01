from pandas import read_csv, DataFrame

from base.pandas_constants import (
    DataFrameConstants,
    PathConstants,
)

USELESS_COLUMNS = [
    DataFrameConstants.IS_CONFIRMED,
    DataFrameConstants.LOCATION_STRATEGY,
    DataFrameConstants.PROCESSO_OCORRENCIA,
    DataFrameConstants.SOLICITACAO_BAIRRO,
    DataFrameConstants.SOLICITACAO_DATA,
    DataFrameConstants.SOLICITACAO_DATA_HORA,
    DataFrameConstants.SOLICITACAO_DESCRICAO,
    DataFrameConstants.SOLICITACAO_ENDERECO,
    DataFrameConstants.SOLICITACAO_HORA,
    DataFrameConstants.SOLICITACAO_LOCALIDADE
]


class MergeTables:
    """
    Setup final dataframe for algorithm analysis
    """

    @staticmethod
    def filter_data_for_algorithm(df_final: DataFrame, path_found: str = PathConstants.LANDSLIDE_FINAL_DF_PATH) -> None:
        """Filters data to algorithm analysis"""
        df_final.dropna(inplace=True)
        df_final = df_final.drop(USELESS_COLUMNS, axis=1)
        df_final.to_csv(path_found, index=False, header=True)
        print("Finished filtering data for algorithm analysis")


if __name__ == '__main__':
    df_final = read_csv(PathConstants.NO_LANDSLIDE_FOUND_RAIN_ELEVATION_PATH)
    MergeTables.filter_data_for_algorithm(df_final, PathConstants.NO_LANDSLIDE_FINAL_DF_PATH)
