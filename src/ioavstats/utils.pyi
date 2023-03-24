# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Module stub file."""
from psycopg2.extensions import connection

def get_args() -> tuple[str, str]: ...
def has_access(host_cloud: bool, app_id: str) -> str: ...
def present_about(pg_conn: connection, app_id: str) -> None: ...
