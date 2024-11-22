class FilesConstants:
    """
    Stores file name constants
    """

    CSV_SUFFIX = '.csv'
    GEOJSON_SUFFIX = '.geojson'
    BAD_DANGER_LEVEL = f'bad_danger_level{CSV_SUFFIX}'
    BAD_GROUND_AMPLITUDE = f'bad_ground_amplitude{CSV_SUFFIX}'
    BAD_GROUND_TYPE = f'bad_ground_type{CSV_SUFFIX}'
    BAD_LOCATIONS = f'bad_locations{CSV_SUFFIX}'
    BAD_RAIN_ELEVATION = f'bad_rain_elevation{CSV_SUFFIX}'
    FOUND_DANGER_LEVEL = f'found_danger_level{CSV_SUFFIX}'
    FOUND_GROUND_AMPLITUDE = f'found_ground_amplitude{CSV_SUFFIX}'
    FOUND_GROUND_TYPE = f'found_ground_type{CSV_SUFFIX}'
    FOUND_LOCATIONS = f'found_locations{CSV_SUFFIX}'
    FINAL_DF = f'final_df{CSV_SUFFIX}'
    FOUND_RAIN_ELEVATION = f'found_rain_elevation{CSV_SUFFIX}'
    GROUND_MAP = f'mapa_exploratorio_solos_pernambuco_wgs84{CSV_SUFFIX}'
    MERGED = f'merged{CSV_SUFFIX}'
    MOVIMENTO_MASSA = f'Movimento_de_Massa_A{GEOJSON_SUFFIX}'
    PADRAO_DE_RELEVO = f'Padroes_de_Relevo_A{GEOJSON_SUFFIX}'
    OCCURRENCES = f'occurrences{CSV_SUFFIX}'
    OCCURRENCES_TYPES = f'occurrences_types{CSV_SUFFIX}'


class DataFrameConstants:
    """
    Stores DataFrame constants
    """
    DANGER_LEVEL = 'danger_level'
    SLOPE_DEGREE = 'slope_degree'
    SLOPE_PERCENTAGE = 'slope_percentage'
    ELEVATION = 'elevation'
    GROUND_AMPLITUDE = 'ground_amplitude'
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


class DangerLevelConstants:
    """
    Stores danger level constants
    """
    CLASSE = 'CLASSE'
    CORRECT_MEDIA = 'Media'
    GEOMETRY = 'geometry'
    WRONG_MEDIA = 'M�dia'


class GroundAmplitudeConstants:
    """
    Stores ground amplitude constants
    """
    AMPLITUDE = 'AMPLITUDE_'
    DECL_GRAU = 'DECL_GRAU'
    DECL_PER = 'DECL_PER'
    GEOMETRY = 'geometry'


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

    BAD_DANGER_LEVEL_PATH = f'../danger_level/{FilesConstants.BAD_DANGER_LEVEL}'
    BAD_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{FilesConstants.BAD_GROUND_AMPLITUDE}'
    BAD_GROUND_TYPE_PATH = f'../ground_type/{FilesConstants.BAD_GROUND_TYPE}'
    BAD_LOCATIONS_PATH = f'../location/{FilesConstants.BAD_LOCATIONS}'
    BAD_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.BAD_RAIN_ELEVATION}'
    FINAL_DF_PATH = f'../../algorithm/{FilesConstants.FINAL_DF}'
    FOUND_DANGER_LEVEL_PATH = f'../danger_level/{FilesConstants.FOUND_DANGER_LEVEL}'
    FOUND_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{FilesConstants.FOUND_GROUND_AMPLITUDE}'
    FOUND_GROUND_TYPE_PATH = f'../ground_type/{FilesConstants.FOUND_GROUND_TYPE}'
    FOUND_LOCATIONS_PATH = f'../location/{FilesConstants.FOUND_LOCATIONS}'
    FOUND_RAIN_ELEVATION_PATH = f'../rain_elevation/{FilesConstants.FOUND_RAIN_ELEVATION}'
    MERGED_PATH = f'../merge/{FilesConstants.MERGED}'
    MOVIMENTO_MASSA_PATH = f'../danger_level/deslizamento_de_massas/{FilesConstants.MOVIMENTO_MASSA}'
    PADRAO_DE_RELEVO_PATH = f'../ground_amplitude/ground_amplitude_data/{FilesConstants.PADRAO_DE_RELEVO}'
