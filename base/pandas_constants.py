class FilesConstants:
    """
    Stores file name constants
    """

    CSV_SUFFIX = '.csv'
    MERGED = f'merged{CSV_SUFFIX}'
    OCCURRENCES = f'occurrences{CSV_SUFFIX}'
    OCCURRENCES_TYPES = f'occurrences_types{CSV_SUFFIX}'


class DataFrameConstants:
    """
    Stores DataFrame constants
    """

    SOLICITACAO_DESCRICAO = 'solicitacao_descricao'
    PROCESSO_OCORRENCIA = 'processo_ocorrencia'
    IS_CONFIRMED = 'is_confirmed'


class ProcessingConstants:
    """
    Stores processing constants
    """

    CONFIRMED = 2
    MAYBE_CONFIRMED = 1
    NOT_CONFIRMED = 0


class ValuesConstants:
    """
    Stores values constants
    """

    TESTES = 'testes'
    DESLIZAMENTOS_DE_BARREIRAS = 'Deslizamentos de Barreiras'
    NAO_HA_OCORRENCIAS = 'Não há Ocorrência para essa Solicitação'


class PathConstants(FilesConstants):
    """
    Stores path constants
    """

    LOCATION_MERGED = f'../location/{FilesConstants.MERGED}'
