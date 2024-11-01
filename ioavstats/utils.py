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
# Global variables.
# -----------------------------------------------------------------------------


# ------------------------------------------------------------------
# Determine the last processed update file.
# ------------------------------------------------------------------
def _sql_query_last_file_name(pg_conn: connection) -> tuple[str, str]:
    """Determine the last processed update file.

    Args:
        pg_conn (connection): Database connection.

    Returns:
        tuple[str, str]: File name and processing date.

    """
    with pg_conn.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT table_name, TO_CHAR(COALESCE(last_processed, first_processed), 'DD.MM.YYYY')
          FROM io_processed_table
         WHERE table_name = 'events';
        """,
        )

        return cur.fetchone()  # type: ignore


# -----------------------------------------------------------------------------
# Load the command line arguments into the memory.
# -----------------------------------------------------------------------------
def get_args() -> str:
    """Load the command line arguments into the memory."""
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


# ------------------------------------------------------------------
# Create a simple user PostgreSQL database engine.
# ------------------------------------------------------------------
# pylint: disable=R0801
def get_engine(settings: Dynaconf) -> Engine:
    """Create a simple user PostgreSQL database engine."""
    return create_engine(
        f"postgresql://{settings.postgres_user_guest}:"
        f"{settings.postgres_password_guest}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_connection_port}/"
        f"{settings.postgres_dbname}",
    )


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=R0801
def get_postgres_connection() -> connection:
    """Create a PostgreSQL connection."""
    return psycopg.connect(**st.secrets["db_postgres"])


# -----------------------------------------------------------------------------
# Prepare a latitude structure.
# -----------------------------------------------------------------------------
# pylint: disable=too-many-return-statements
def prepare_latitude(latitude_string: str) -> str:
    """Prepare a latitude structure.

    Args:
        latitude_string (str): Latitude string.

    Returns:
        str: Latitude structure.

    """
    len_latitude_string = len(latitude_string)

    if len_latitude_string == 7:
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
        return (
            latitude_string[:2] + " " + latitude_string[2:4] + " " + latitude_string[4:]
        )

    if len_latitude_string == 4:
        return (
            latitude_string[:1] + " " + latitude_string[1:3] + " " + latitude_string[3:]
        )

    if len_latitude_string == 3:
        return latitude_string[:2] + " " + latitude_string[2:]

    if len_latitude_string == 2:
        return latitude_string[:1] + " " + latitude_string[1:]

    return latitude_string


# -----------------------------------------------------------------------------
# Prepare a longitude structure.
# -----------------------------------------------------------------------------
def prepare_longitude(longitude_string: str) -> str:
    """Prepare a longitude structure.

    Args:
        longitude_string (str): longitude string.

    Returns:
        str: longitude structure.

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


# ------------------------------------------------------------------
# Present the 'about' information.
# ------------------------------------------------------------------
def present_about(pg_conn: connection, app_id: str) -> None:
    """Present the 'about' information.

    Args:
        pg_conn (connection): Database connection.
        app_id (str): Application name.

    """
    file_name, processed = _sql_query_last_file_name(pg_conn)

    st.warning(
        f"""
IO-AVSTATS Application: **{app_id}**

Latest NTSB database: **{file_name} - {processed}**

**:copyright: 2022-{datetime.now(UTC).year} - IO AERONAUTICAL AUTONOMY LABS, LLC**

[Disclaimer](https://www.io-aero.com/disclaimer)
    """,
    )
