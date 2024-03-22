from _typeshed import Incomplete
from psycopg import connection as connection
from psycopg import cursor as cursor

from ioavstats import glob_local as glob_local

COLUMN_CATEGORY_NO: str
COLUMN_COUNT: str
COLUMN_DESCRIPTION: str
COLUMN_EVENTSOE_NO: str
COLUMN_FINDING_DESCRIPTION: str
COLUMN_MAIN_PHASE: str
COLUMN_MODIFIER_DESCRIPTION: str
COLUMN_MODIFIER_NO: str
COLUMN_OCCURRENCE_DESCRIPTION: str
COLUMN_PHASE_CODE: str
COLUMN_PHASE_NO: str
COLUMN_SECTION_NO: str
COLUMN_SUBCATEGORY_CODE: str
COLUMN_SUBCATEGORY_NO: str
COLUMN_SUBSECTION_NO: str
COLUMN_TABLE_NAME: str
DLL_TABLE_STMNTS: dict[str, str]
DLL_VIEW_STMNTS_CREATE: dict[str, str]
DLL_VIEW_STMNTS_CREATE_MAT: dict[str, str]
DLL_VIEW_STMNTS_DROP: list[str]
DLL_VIEW_STMNTS_REFRESH: list[str]
FILE_MAIN_PHASES_OF_FLIGHT: Incomplete
logger: Incomplete

def create_db_schema() -> None: ...
def refresh_db_schema() -> None: ...
def update_db_schema() -> None: ...
