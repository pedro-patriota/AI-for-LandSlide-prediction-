class FilesConstants:
    """
    Stores file name constants
    """

    CSV_SUFFIX = '.csv'
    BAD_GROUND_TYPE = f'bad_ground_type{CSV_SUFFIX}'
    BAD_LOCATIONS = f'bad_locations{CSV_SUFFIX}'
    BAD_RAIN_ELEVATION = f'bad_rain_elevation{CSV_SUFFIX}'
    FOUND_GROUND_TYPE = f'found_ground_type{CSV_SUFFIX}'
    FOUND_LOCATIONS = f'found_locations{CSV_SUFFIX}'
    FOUND_RAIN_ELEVATION = f'found_rain_elevation{CSV_SUFFIX}'
    MERGED = f'merged{CSV_SUFFIX}'
    OCCURRENCES = f'occurrences{CSV_SUFFIX}'
    GROUND_MAP = f'mapa_exploratorio_solos_pernambuco_wgs84{CSV_SUFFIX}'
    OCCURRENCES_TYPES = f'occurrences_types{CSV_SUFFIX}'


class DataFrameConstants:
    """
    Stores DataFrame constants
    """
    ELEVATION = 'elevation'
    GROUND_TYPE = 'ground_type'
    IS_CONFIRMED = 'is_confirmed'
    LATITUDE = 'latitude'
    LOCATION_STRATEGY = 'location_strategy'
    LONGITUDE = 'longitude'
    PROCESSO_NUMERO = 'processo_numero'
    PROCESSO_OCORRENCIA = 'processo_ocorrencia'
    RAIN_DAY = 'rain_day'
    RAIN_HOUR = 'rain_hour'
    SOLICITACAO_BAIRRO = 'solicitacao_bairro'
    SOLICITACAO_DATA = 'solicitacao_data'
    SOLICITACAO_DATA_HORA = 'solicitacao_data_hora'
    SOLICITACAO_DESCRICAO = 'solicitacao_descricao'
    SOLICITACAO_ENDERECO = 'solicitacao_endereco'
    SOLICITACAO_HORA = 'solicitacao_hora'
    SOLICITACAO_LOCALIDADE = 'solicitacao_localidade'

class GroundTypeConstants:
    """
    Stores ground type constants
    """
    LEGENDA = 'Legenda'
    THE_GEOM = 'the_geom'

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
    ELEVATION = 'elevation'
    ELEVATION_API = 'https://api.open-elevation.com/api/v1/lookup?locations='
    INMEP_STATION = 'A301'
    PRCP = 'prcp'
    RAIN = 'rain'
    RAIN_INMEP_API = 'https://apitempo.inmet.gov.br/estacao'
    TIMEZONE = 'America/Recife'
    WMO = 'wmo'

class ProcessingConstants:
    """
    Stores processing constants
    """
    CONFIRMED = 2
    MAYBE_CONFIRMED = 1
    NOT_CONFIRMED = 0
    RECIFE = 'Recife'
    RESULTS = 'results'


class ValuesConstants:
    """
    Stores values constants
    """
    DESLIZAMENTOS_DE_BARREIRAS = 'Deslizamentos de Barreiras'
    IMOVEIS_COM_DANOS = 'Imoveis com Danos/Risco'
    NAO_HA_OCORRENCIAS = 'Não há Ocorrência para essa Solicitação'
    TESTES = 'testes'
    UNKNOWN_COORDINATES = 0.0
    UNKNOWN_VALUE = ''


class PathConstants(FilesConstants):
    """
    Stores path constants
    """

    BAD_GROUND_TYPE_PATH = f'../ground_type/{FilesConstants.BAD_GROUND_TYPE}'
    BAD_LOCATIONS_PATH = f'../location/{FilesConstants.BAD_LOCATIONS}'
    BAD_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.BAD_RAIN_ELEVATION}'
    FOUND_GROUND_TYPE_PATH = f'../ground_type/{FilesConstants.FOUND_GROUND_TYPE}'
    FOUND_LOCATIONS_PATH = f'../location/{FilesConstants.FOUND_LOCATIONS}'
    FOUND_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.FOUND_RAIN_ELEVATION}'
    MERGED_PATH = f'../merge/{FilesConstants.MERGED}'
