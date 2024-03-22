from _typeshed import Incomplete
from psycopg import connection as connection
from psycopg import cursor as cursor

from ioavstats import glob_local as glob_local
from ioavstats import utils as utils

COLUMN_ACCEPTABLE_CITIES: str
COLUMN_AIRANAL: str
COLUMN_AIRPORT_ID: str
COLUMN_CICTT_CODE_LOWER: str
COLUMN_CICTT_CODE_SPACE: str
COLUMN_CICTT_CODE_UNDERSCORE: str
COLUMN_CITY: str
COLUMN_COMP_CODE: str
COLUMN_COUNTRY_LOWER: str
COLUMN_COUNTRY_UPPER: str
COLUMN_DEC_LATITUDE: str
COLUMN_DEC_LONGITUDE: str
COLUMN_DEFINITION: str
COLUMN_DIM_UOM: str
COLUMN_DODHIFLIP: str
COLUMN_ELEVATION: str
COLUMN_EVENTSOE_NO: str
COLUMN_FAR91: str
COLUMN_FAR93: str
COLUMN_GLOBAL_ID: str
COLUMN_IAPEXISTS: str
COLUMN_IDENT: str
COLUMN_IDENTIFIER: str
COLUMN_LAT: str
COLUMN_LATITUDE_LOWER: str
COLUMN_LATITUDE_UPPER: str
COLUMN_LENGTH: str
COLUMN_LNG: str
COLUMN_LOCID: str
COLUMN_LONGITUDE_LOWER: str
COLUMN_LONGITUDE_UPPER: str
COLUMN_MEANING: str
COLUMN_MIL_CODE: str
COLUMN_NAME: str
COLUMN_OPERSTATUS: str
COLUMN_PRIMARY_CITY: str
COLUMN_PRIVATEUSE: str
COLUMN_SERVCITY: str
COLUMN_SOE_NO: str
COLUMN_STATE_CAMEL: str
COLUMN_STATE_ID: str
COLUMN_STATE_LOWER: str
COLUMN_STATE_UPPER: str
COLUMN_TYPE: str
COLUMN_TYPE_CODE: str
COLUMN_X: str
COLUMN_Y: str
COLUMN_ZIP: str
COLUMN_ZIPS: str
FILE_AVIATION_OCCURRENCE_CATEGORIES: Incomplete
FILE_FAA_AIRPORTS: Incomplete
FILE_FAA_NPIAS_DATA: Incomplete
FILE_FAA_RUNWAYS: Incomplete
FILE_SEQUENCE_OF_EVENTS: Incomplete
FILE_SIMPLEMAPS_US_CITIES: Incomplete
FILE_SIMPLEMAPS_US_ZIPS: Incomplete
FILE_ZIP_CODES_ORG: Incomplete
IO_LAST_SEEN: Incomplete
logger: Incomplete

def download_us_cities_file() -> None: ...
def download_zip_code_db_file() -> None: ...
def load_airport_data() -> None: ...
def load_aviation_occurrence_categories() -> None: ...
def load_country_state_data() -> None: ...
def load_sequence_of_events() -> None: ...
def load_simplemaps_data() -> None: ...
def load_zip_codes_org_data() -> None: ...
