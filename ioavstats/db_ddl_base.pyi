from _typeshed import Incomplete

from ioavstats import glob_local as glob_local

DLL_TABLE_STMNTS: dict[str, str]
DLL_VIEW_STMNTS_CREATE: dict[str, str]
DLL_VIEW_STMNTS_CREATE_MAT: dict[str, str]
DLL_VIEW_STMNTS_DROP: list[str]
DLL_VIEW_STMNTS_REFRESH: list[str]
logger: Incomplete

def create_db_schema() -> None: ...
def refresh_db_schema() -> None: ...
def update_db_schema() -> None: ...
