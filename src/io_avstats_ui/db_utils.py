# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Managing the database schema of the PostgreSQL database."""

import psycopg

from io_avstats_ui import io_config
from io_avstats_ui import io_glob
from io_avstats_ui import io_utils


# ------------------------------------------------------------------
# Create a PostgreSQL cursor.
# ------------------------------------------------------------------
# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-arguments
def _get_postgres_cursor_admin(
    autocommit: bool, dbname: str, host: str, password: str, port: int, user: str
) -> tuple:
    """Create a PostgreSQL cursor.

    Args:
        autocommit (bool): _description_
        dbname (str): Database name.
        host (str): Host name.
        password (str): Password.
        port (int): Port number.
        user (str): User name.

    Returns:
        tuple: Connection, Cursor.
    """
    io_glob.logger.debug(io_glob.LOGGER_START)

    try:
        conn_pg = psycopg.connect(
            conninfo=f"dbname={dbname} "
            + f"user={user} "
            + f"password={password} "
            + f"host={host} "
            + f"port={port}",
            autocommit=autocommit,
        )

        io_glob.logger.debug(io_glob.LOGGER_END)

        return conn_pg, conn_pg.cursor()

    except psycopg.OperationalError as exc:
        io_utils.terminate_fatal(str(exc))


# ------------------------------------------------------------------
# Create a PostgreSQL cursor.
# ------------------------------------------------------------------
def get_postgres_cursor() -> tuple:
    """Create a PostgreSQL cursor."""
    return _get_postgres_cursor_admin(
        autocommit=True,
        dbname=io_config.settings.postgres_dbname,
        host=io_config.settings.postgres_host,
        password=io_config.settings.postgres_password,
        port=io_config.settings.postgres_connection_port,
        user=io_config.settings.postgres_user,
    )


# ------------------------------------------------------------------
# Create a PostgreSQL cursor - Administrator.
# ------------------------------------------------------------------
def get_postgres_cursor_admin() -> tuple:
    """Create a PostgreSQL cursor - Administrator."""
    return _get_postgres_cursor_admin(
        autocommit=True,
        dbname=io_config.settings.postgres_dbname_admin,
        host=io_config.settings.postgres_host,
        password=io_config.settings.postgres_password_admin,
        port=io_config.settings.postgres_connection_port,
        user=io_config.settings.postgres_user_admin,
    )
