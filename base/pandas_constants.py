class FilesConstants:
    """
    Stores file name constants
    """

    CSV_SUFFIX = '.csv'
    MERGED = f'merged{CSV_SUFFIX}'
    BAD_LOCATIONS = f'bad_locations{CSV_SUFFIX}'
    BAD_RAIN_ELEVATION = f'bad_rain_elevation{CSV_SUFFIX}'
    FOUND_RAIN_ELEVATION = f'found_rain_elevation{CSV_SUFFIX}'
    FOUND_LOCATIONS = f'found_locations{CSV_SUFFIX}'
    OCCURRENCES = f'occurrences{CSV_SUFFIX}'
    OCCURRENCES_TYPES = f'occurrences_types{CSV_SUFFIX}'


class DataFrameConstants:
    """
    Stores DataFrame constants
    """
    IS_CONFIRMED = 'is_confirmed'
    LATITUDE = 'latitude'
    RAIN_DAY = 'rain_day'
    RAIN_HOUR = 'rain_hour'
    ELEVATION = 'elevation'
    LOCATION_STRATEGY = 'location_strategy'
    LONGITUDE = 'longitude'
    PROCESSO_NUMERO = 'processo_numero'
    SOLICITACAO_DATA = 'solicitacao_data'
    SOLICITACAO_HORA = 'solicitacao_hora'
    SOLICITACAO_DATA_HORA = 'solicitacao_data_hora'
    PROCESSO_OCORRENCIA = 'processo_ocorrencia'
    SOLICITACAO_BAIRRO = 'solicitacao_bairro'
    SOLICITACAO_DESCRICAO = 'solicitacao_descricao'
    SOLICITACAO_ENDERECO = 'solicitacao_endereco'
    SOLICITACAO_LOCALIDADE = 'solicitacao_localidade'

class LocationConstants:
    """
    Stores location constants
    """
    ADDRESS = 'address'
    CITY = 'city'
    SUBURB = 'suburb'

class RainElevationConstants:
    """
    Stores rain and elevation constants
    """
    ELEVATION_API = 'https://api.open-elevation.com/api/v1/lookup?locations='
    RAIN_INMEP_API = 'https://apitempo.inmet.gov.br/estacao'
    INMEP_STATION = 'A301'
    ELEVATION = 'elevation'
    PRCP = 'prcp'
    WMO = 'wmo'
    TIMEZONE = 'America/Recife'
    RAIN = 'rain'

class ProcessingConstants:
    """
    Stores processing constants
    """
    RESULTS = 'results'
    CONFIRMED = 2
    MAYBE_CONFIRMED = 1
    NOT_CONFIRMED = 0
    RECIFE = 'Recife'


class ValuesConstants:
    """
    Stores values constants
    """
    UNKNOWN_COORDINATES = 0.0
    UNKNOWN_VALUE = ''
    DESLIZAMENTOS_DE_BARREIRAS = 'Deslizamentos de Barreiras'
    IMOVEIS_COM_DANOS = 'Imoveis com Danos/Risco'
    NAO_HA_OCORRENCIAS = 'Não há Ocorrência para essa Solicitação'
    TESTES = 'testes'


class PathConstants(FilesConstants):
    """
    Stores path constants
    """

    MERGED_PATH = f'../merge/{FilesConstants.MERGED}'
    BAD_LOCATIONS_PATH = f'../location/{FilesConstants.BAD_LOCATIONS}'
    BAD_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.BAD_RAIN_ELEVATION}'
    FOUND_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.FOUND_RAIN_ELEVATION}'
    FOUND_LOCATIONS_PATH = f'../location/{FilesConstants.FOUND_LOCATIONS}'
