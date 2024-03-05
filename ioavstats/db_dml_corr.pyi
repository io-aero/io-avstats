from collections import OrderedDict

from _typeshed import Incomplete
from psycopg import connection as connection
from psycopg import cursor as cursor

from ioavstats import glob_local as glob_local
from ioavstats.utils import prepare_latitude as prepare_latitude
from ioavstats.utils import prepare_longitude as prepare_longitude

COLUMN_NAME: str
COUNT_ERROR: int
COUNT_SELECT: int
COUNT_UPDATE: int
EV_ID: str
ROW: list[OrderedDict]
ROW_COLUMN_TABLE_NAME_IDX: int
ROW_COLUMN_COLUMN_NAME_IDX: int
ROW_COLUMN_VALUE_IDX: int
ROW_COLUMN_EV_ID_IDX: int
ROW_COLUMN_AIRCRAFT_KEY_IDX: int
ROW_COLUMN_CREW_NO_IDX: int
ROW_COLUMN_OCCURRENCE_NO_IDX: int
ROW_COLUMN_NOTE_1_IDX: int
ROW_COLUMN_NOTE_2_IDX: int
ROW_COLUMN_NOTE_3_IDX: int
TABLE_NAME: str
TERMINAL_AREA_DISTANCE_NMI: float
VALUE: str
logger: Incomplete

def cleansing_postgres_data() -> None: ...
def correct_dec_lat_lng() -> None: ...
def find_nearest_airports() -> None: ...
def load_correction_data(filename: str) -> None: ...
def verify_ntsb_data() -> None: ...
