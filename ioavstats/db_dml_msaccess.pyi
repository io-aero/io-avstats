from _typeshed import Incomplete
from psycopg import connection as connection
from psycopg import cursor as cursor

from ioavstats import glob_local as glob_local
from ioavstats import utils as utils
from ioavstats import utils_msaccess as utils_msaccess

COLUMN_CITY: str
COLUMN_COUNT: str
COLUMN_COUNTRY: str
COLUMN_DEC_LATITUDE: str
COLUMN_DEC_LONGITUDE: str
COLUMN_STATE: str
IO_LAST_SEEN: Incomplete
logger: Incomplete

def load_ntsb_msaccess_data(msaccess: str) -> None: ...
def download_ntsb_msaccess_file(msaccess: str) -> None: ...
