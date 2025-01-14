# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Application Utilities."""
import argparse
from datetime import UTC, datetime

import psycopg
import streamlit as st
from dynaconf import Dynaconf  # type: ignore
from psycopg import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

# -----------------------------------------------------------------------------

def _sql_query_last_file_name(pg_conn: connection) -> tuple[str, str]:
    """Determine the last processed update file.

    This function executes a database query to determine the last update file
    processed. It returns the file name and the date it was processed.

    Args:
        pg_conn (connection): Database connection.

    Returns:
        tuple[str, str]: File name and processing date.

    """
    # Determine the last processed file and date
    with pg_conn.cursor() as cur:  # type: ignore
        cur.execute(
            """
            -- Determine the last processed file and date
            SELECT data_source,
                   MAX(TO_CHAR(COALESCE(last_processed, first_processed), 'DD.MM.YYYY'))
              FROM io_processed_data
             WHERE table_name = 'events'
             GROUP BY data_source,
                      COALESCE(last_processed, first_processed)
             ORDER BY COALESCE(last_processed, first_processed) DESC
             LIMIT 1;
        """,
        )

        # Fetch and return the result
        return cur.fetchone()  # type: ignore


# -----------------------------------------------------------------------------

def get_args() -> str:
    """Load the command line arguments into the memory.

    This function parses the command line arguments and determines the host
    mode and the execution mode.

    The host mode can be either 'Cloud' or 'Local'. The execution mode can be
    either 'ltd' (limited demo version) or 'std' (full version).

    Returns:
        str: The host mode: 'Cloud' or 'Local'.

    """
    parser = argparse.ArgumentParser(
        description="Streamlit Applications",
        prog="streamlit",
        prefix_chars="--",
        usage="%(prog)s options",
    )

    # -------------------------------------------------------------------------
    # Definition of the command line arguments.
    # ------------------------------------------------------------------------
    parser.add_argument(
        "--host",
        help="the host mode: 'cloud_old' (Cloud host) or 'local' (Local host)",
        metavar="host",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--mode",
        help="the execution mode: '"
        "ltd' (The limited demo version) or '"
        "std' (The full version)",
        metavar="mode",
        required=False,
        type=str,
    )

    # -------------------------------------------------------------------------
    # Load and check the command line arguments.
    # -------------------------------------------------------------------------
    parsed_args = parser.parse_args()

    host = "Local"
    if parsed_args.host is not None and parsed_args.host == "Cloud":
        host = parsed_args.host

    return host


# -----------------------------------------------------------------------------

def get_engine(settings: Dynaconf) -> Engine:
    """Create a simple user PostgreSQL database engine.

    This function creates a database engine which is used to connect to the
    PostgreSQL database.

    Args:
        settings (Dynaconf): The settings object.

    Returns:
        Engine: The database engine.

    The engine is created using the following parameters:

    - `postgres_user_guest`: The PostgreSQL user for the database.
    - `postgres_password_guest`: The password for the PostgreSQL user.
    - `postgres_host`: The host name of the PostgreSQL server.
    - `postgres_connection_port`: The port number of the PostgreSQL server.
    - `postgres_dbname`: The name of the PostgreSQL database.

    """
    return create_engine(
        f"postgresql://{settings.postgres_user_guest}:"
        f"{settings.postgres_password_guest}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_connection_port}/"
        f"{settings.postgres_dbname}",
    )


# -----------------------------------------------------------------------------

def get_postgres_connection() -> connection:
    """Create a PostgreSQL connection.

    The function creates a connection to the PostgreSQL database.

    Returns:
        connection: The PostgreSQL connection object.

    """
    # Create a PostgreSQL connection using the secrets stored in the Streamlit
    # secrets dictionary.
    return psycopg.connect(**st.secrets["db_postgres"])


# -----------------------------------------------------------------------------

def prepare_latitude(latitude_string: str) -> str:
    """Prepare a latitude structure.

    Args:
        latitude_string (str): Latitude string.

    Returns:
        str: Latitude structure.

    This function takes a latitude string and prepares it for display. The string
    is expected to be in the format "DDDMMSS" where DDD is the degrees, MM is the
    minutes and SS is the seconds. The string will be divided into its components
    and returned as a string with spaces between the components.

    """
    len_latitude_string = len(latitude_string)

    if len_latitude_string == 7:
        # 7 character latitude string format: DDDMMSS
        return (
            latitude_string[:2]
            + " "
            + latitude_string[2:4]
            + " "
            + latitude_string[4:6]
            + " "
            + latitude_string[6:]
        )

    if len_latitude_string == 6:
        # 6 character latitude string format: DMMSSS
        return (
            latitude_string[:1]
            + " "
            + latitude_string[1:3]
            + " "
            + latitude_string[3:5]
            + " "
            + latitude_string[5:]
        )

    if len_latitude_string == 5:
        # 5 character latitude string format: DDMMSS
        return (
            latitude_string[:2] + " " + latitude_string[2:4] + " " + latitude_string[4:]
        )

    if len_latitude_string == 4:
        # 4 character latitude string format: DMMSS
        return (
            latitude_string[:1] + " " + latitude_string[1:3] + " " + latitude_string[3:]
        )

    if len_latitude_string == 3:
        # 3 character latitude string format: DDMM
        return latitude_string[:2] + " " + latitude_string[2:]

    if len_latitude_string == 2:
        # 2 character latitude string format: DD
        return latitude_string[:1] + " " + latitude_string[1:]

    return latitude_string


# -----------------------------------------------------------------------------

def prepare_longitude(longitude_string: str) -> str:
    """Prepare a longitude structure.

    Args:
        longitude_string (str): longitude string.

    Returns:
        str: longitude structure.

    This function takes a longitude string and prepares it for display. The string
    is expected to be in the format "DDDMMSS" where DDD is the degrees, MM is the
    minutes and SS is the seconds. The function will split the string into its
    components and return a string in the format "DD MM SS.SSS".

    If the string is not in the expected format, the function will return the
    original string.

    """
    if len(longitude_string) == 8:
        return (
            longitude_string[:3]
            + " "
            + longitude_string[3:5]
            + " "
            + longitude_string[5:7]
            + " "
            + longitude_string[7:]
        )

    return prepare_latitude(longitude_string)


# -----------------------------------------------------------------------------

def present_about(pg_conn: connection, app_id: str) -> None:
    """Present the 'about' information.

    Args:
        pg_conn (connection): Database connection.
        app_id (str): Application name.

    This function presents the 'about' information, including the latest NTSB
    database file and the copyright information.

    """
    # Get the latest NTSB database file name and the date it was processed
    file_name, processed = _sql_query_last_file_name(pg_conn)

    # Present the 'about' information
    st.warning(
        f"""
IO-AVSTATS Application: **{app_id}**

Latest NTSB database: **{file_name} - {processed}**

**:copyright: 2022-{datetime.now(UTC).year} - IO AERONAUTICAL AUTONOMY LABS, LLC**

[Disclaimer](https://www.io-aero.com/disclaimer)
    """,
    )
