from pandas import read_csv, DataFrame

from base.pandas_constants import (
    DataFrameConstants,
    PathConstants,
)

USELESS_COLUMNS = [
    DataFrameConstants.IS_CONFIRMED,
    DataFrameConstants.LATITUDE,
    DataFrameConstants.LOCATION_STRATEGY,
    DataFrameConstants.LONGITUDE,
    DataFrameConstants.PROCESSO_NUMERO,
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
    def filter_data_for_algorithm(df_final: DataFrame) -> None:
        """Filters data to algorithm analysis"""
        df_final.dropna(inplace=True)
        df_final = df_final.drop(USELESS_COLUMNS, axis=1)
        df_final.to_csv(PathConstants.FINAL_DF_PATH, index=False, header=True)
        print("Finished filtering data for algorithm analysis")


if __name__ == '__main__':
    df_final = read_csv(PathConstants.FOUND_DANGER_LEVEL_PATH)
    MergeTables.filter_data_for_algorithm(df_final)
