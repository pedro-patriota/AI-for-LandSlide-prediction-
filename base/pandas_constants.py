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
    CLUSTER = 'cluster'
    DISTANCE_TO_CENTROID = 'distance_to_centroid'
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
    ADDRESS_COMPONENTS = 'address_components'
    LONG_NAME = 'long_name'
    LOCATION = 'location'
    LAT = 'lat'
    LNG = 'lng'

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
    API_KEY = 'API_KEY'
    GOOGLE_MAPS_API = 'google maps api'
    MAYBE_CONFIRMED = 1
    NOT_CONFIRMED = 0
    NO_LANDSLIDE = -1
    RECIFE = 'Recife'
    RESULTS = 'results'
    GEOMETRY = 'geometry'

class DangerLevelConstants(ProcessingConstants):
    """
    Stores danger level constants
    """
    CLASSE = 'CLASSE'
    CORRECT_MEDIA = 'Media'
    WRONG_MEDIA = 'M�dia'


class GroundAmplitudeConstants(ProcessingConstants):
    """
    Stores ground amplitude constants
    """
    AMPLITUDE = 'AMPLITUDE_'
    DECL_GRAU = 'DECL_GRAU'
    DECL_PER = 'DECL_PER'

class ValuesConstants:
    """
    Stores values constants
    """
    INCENDIOS = 'Incendios'
    IMOVEIS_ALAGADOS = 'Imoveis Alagados'
    ARVORES_EM_RISCO = 'Arvores em Risco'
    ALAGAMENTOS = 'Alagamentos'
    INVASAO_TERRENO = 'Invasao de Terreno de Auxilio Moradia'
    TRANSBORDAMENTO_CANAL = 'Transbordamentos de Canais'
    ELEVACAO_RIO = 'Elevacao do Nivel do Rio'
    PRODUTOS_QUIMICOS = 'Produtos Quimicos Perigosos'
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
    LANDSLIDE_DIR = 'landslide'
    NO_LANDSLIDE_DIR = 'no_landslide'
    LANDSLIDE_PREFIX = 'landslide_'
    NO_LANDSLIDE_PREFIX = 'no_landslide_'

    LANDSLIDE_MERGED_PATH = f'../merge/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.MERGED}'
    NO_LANDSLIDE_MERGED_PATH = f'../merge/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.MERGED}'

    LANDSLIDE_BAD_GROUND_TYPE_PATH = f'../ground_type/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.BAD_GROUND_TYPE}'
    NO_LANDSLIDE_BAD_GROUND_TYPE_PATH = f'../ground_type/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.BAD_GROUND_TYPE}'
    LANDSLIDE_FOUND_GROUND_TYPE_PATH = f'../ground_type/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.FOUND_GROUND_TYPE}'
    NO_LANDSLIDE_FOUND_GROUND_TYPE_PATH = f'../ground_type/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.FOUND_GROUND_TYPE}'

    LANDSLIDE_BAD_LOCATIONS_PATH = f'../location/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.BAD_LOCATIONS}'
    NO_LANDSLIDE_BAD_LOCATIONS_PATH = f'../location/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.BAD_LOCATIONS}'
    LANDSLIDE_FOUND_LOCATIONS_PATH =  f'../location/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.FOUND_LOCATIONS}'
    NO_LANDSLIDE_FOUND_LOCATIONS_PATH = f'../location/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.FOUND_LOCATIONS}'

    LANDSLIDE_FOUND_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.FOUND_GROUND_AMPLITUDE}'
    LANDSLIDE_BAD_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.BAD_GROUND_AMPLITUDE}'
    NO_LANDSLIDE_FOUND_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.FOUND_GROUND_AMPLITUDE}'
    NO_LANDSLIDE_BAD_GROUND_AMPLITUDE_PATH = f'../ground_amplitude/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.BAD_GROUND_AMPLITUDE}'

    LANDSLIDE_BAD_DANGER_LEVEL_PATH = f'../danger_level/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.BAD_DANGER_LEVEL}'
    LANDSLIDE_FOUND_DANGER_LEVEL_PATH = f'../danger_level/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.FOUND_DANGER_LEVEL}'
    NO_LANDSLIDE_BAD_DANGER_LEVEL_PATH = f'../danger_level/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.BAD_DANGER_LEVEL}'
    NO_LANDSLIDE_FOUND_DANGER_LEVEL_PATH = f'../danger_level/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.FOUND_DANGER_LEVEL}'

    LANDSLIDE_BAD_RAIN_ELEVATION_PATH = f'../rain_elevation/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.BAD_RAIN_ELEVATION}'
    LANDSLIDE_FOUND_RAIN_ELEVATION_PATH = f'../rain_elevation/{LANDSLIDE_DIR}/{LANDSLIDE_PREFIX}{FilesConstants.FOUND_RAIN_ELEVATION}'
    NO_LANDSLIDE_BAD_RAIN_ELEVATION_PATH = f'../rain_elevation/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.BAD_RAIN_ELEVATION}'
    NO_LANDSLIDE_FOUND_RAIN_ELEVATION_PATH = f'../rain_elevation/{NO_LANDSLIDE_DIR}/{NO_LANDSLIDE_PREFIX}{FilesConstants.FOUND_RAIN_ELEVATION}'

    LANDSLIDE_FINAL_DF_PATH = f'../../algorithm/{LANDSLIDE_PREFIX}{FilesConstants.FINAL_DF}'
    NO_LANDSLIDE_FINAL_DF_PATH  =  f'../../algorithm/{NO_LANDSLIDE_PREFIX}{FilesConstants.FINAL_DF}'
    MOVIMENTO_MASSA_PATH = f'../danger_level/deslizamento_de_massas/{FilesConstants.MOVIMENTO_MASSA}'
    PADRAO_DE_RELEVO_PATH = f'../ground_amplitude/ground_amplitude_data/{FilesConstants.PADRAO_DE_RELEVO}'


class AlgorithmConstants:
    """
    Stores algorithm constants
    """
    FINAL_DF_PATH = f'../{FilesConstants.FINAL_DF}'
