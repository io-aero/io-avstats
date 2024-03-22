from collections import OrderedDict

from _typeshed import Incomplete
from psycopg import connection as connection
from psycopg import cursor as cursor

from ioavstats import glob_local as glob_local
from ioavstats.utils import prepare_latitude as prepare_latitude
from ioavstats.utils import prepare_longitude as prepare_longitude

COLUMN_AIRCRAFT_KEY: str
COLUMN_COLUMN_NAME: str
COLUMN_CREW_NO: str
COLUMN_DEC_LATITUDE: str
COLUMN_DEC_LONGITUDE: str
COLUMN_EV_ID: str
COLUMN_LATITUDE: str
COLUMN_LONGITUDE: str
COLUMN_NAME: str
COLUMN_NOTE_1: str
COLUMN_NOTE_2: str
COLUMN_NOTE_3: str
COLUMN_OCCURRENCE_NO: str
COLUMN_TABLE_NAME: str
COLUMN_VALUE: str
COLUMN_COUNTRY: str
COLUMN_COUNTRY_DEC_LATITUDE: str
COLUMN_COUNTRY_DEC_LONGITUDE: str
COLUMN_STATE: str
COLUMN_SITE_ZIPCODE: str
COLUMN_ZIPCODE_DEC_LATITUDE: str
COLUMN_ZIPCODE_DEC_LONGITUDE: str
COLUMN_CITY: str
COLUMN_CITY_DEC_LATITUDE: str
COLUMN_CITY_DEC_LONGITUDE: str
COLUMN_STATE_DEC_LATITUDE: str
COLUMN_STATE_DEC_LONGITUDE: str
COUNT_ERROR: int
COUNT_SELECT: int
COUNT_UPDATE: int
EV_ID: str
ROW: list[OrderedDict]
TABLE_NAME: str
TERMINAL_AREA_DISTANCE_NMI: float
VALUE: str
logger: Incomplete

def cleansing_postgres_data() -> None: ...
def correct_dec_lat_lng() -> None: ...
def find_nearest_airports() -> None: ...
def load_correction_data(filename: str) -> None: ...
def verify_ntsb_data() -> None: ...
