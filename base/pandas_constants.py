class FilesConstants:
    """
    Stores file name constants
    """

    CSV_SUFFIX = '.csv'
    MERGED = f'merged{CSV_SUFFIX}'
    BAD_LOCATIONS = f'bad_locations{CSV_SUFFIX}'
    FOUND_LOCATIONS = f'found_locations{CSV_SUFFIX}'
    OCCURRENCES = f'occurrences{CSV_SUFFIX}'
    OCCURRENCES_TYPES = f'occurrences_types{CSV_SUFFIX}'


class DataFrameConstants:
    """
    Stores DataFrame constants
    """
    IS_CONFIRMED = 'is_confirmed'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'
    PROCESSO_OCORRENCIA = 'processo_ocorrencia'
    PROCESSO_NUMERO = 'processo_numero'
    SOLICITACAO_BAIRRO = 'solicitacao_bairro'
    SOLICITACAO_LOCALIDADE = 'solicitacao_localidade'
    SOLICITACAO_ENDERECO = 'solicitacao_endereco'
    SOLICITACAO_DESCRICAO = 'solicitacao_descricao'

class LocationConstants:
    """
    Stores location constants
    """
    ADDRESS = 'address'
    CITY = 'city'
    SUBURB = 'suburb'

class ProcessingConstants:
    """
    Stores processing constants
    """

    CONFIRMED = 2
    MAYBE_CONFIRMED = 1
    NOT_CONFIRMED = 0
    UNKNOWN_COORDINATES = 0.0
    RECIFE = 'Recife'


class ValuesConstants:
    """
    Stores values constants
    """

    DESLIZAMENTOS_DE_BARREIRAS = 'Deslizamentos de Barreiras'
    NAO_HA_OCORRENCIAS = 'Não há Ocorrência para essa Solicitação'
    TESTES = 'testes'


class PathConstants(FilesConstants):
    """
    Stores path constants
    """

    MERGED_PATH = f'../location/{FilesConstants.MERGED}'
    BAD_LOCATIONS_PATH = f'../location/{FilesConstants.BAD_LOCATIONS}'
    FOUND_LOCATIONS_PATH = f'../location/{FilesConstants.FOUND_LOCATIONS}'
