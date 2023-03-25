# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Application Utilities."""
import argparse
import datetime

import psycopg2
import streamlit as st
from dynaconf import Dynaconf  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_keycloak import login


# -----------------------------------------------------------------------------
# Load the command line arguments into the memory.
# -----------------------------------------------------------------------------
def get_args() -> tuple[str, str]:
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
        help="the host mode: '" + "cloud' (Cloud host) or '" + "local' (Local host)",
        metavar="host",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--mode",
        help="the execution mode: '"
        + "ltd' (The limited demo version) or '"
        + "std' (The full version)",
        metavar="mode",
        required=False,
        type=str,
    )

    # -------------------------------------------------------------------------
    # Load and check the command line arguments.
    # -------------------------------------------------------------------------
    parsed_args = parser.parse_args()

    mode = "Ltd"
    if parsed_args.mode is not None:
        if parsed_args.mode == "Std":
            mode = parsed_args.mode

    host = "Local"
    if parsed_args.host is not None:
        if parsed_args.host == "Cloud":
            host = parsed_args.host

    return host, mode


# ------------------------------------------------------------------
# Create a simple user PostgreSQL database engine.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def get_engine(_settings: Dynaconf) -> Engine:
    """Create a simple user PostgreSQL database engine."""
    print(
        f"[engine  ] User connect request host={_settings.postgres_host} "
        + f"port={_settings.postgres_connection_port} "
        + f"dbname={_settings.postgres_dbname} "
        + f"user={_settings.postgres_user_guest}"
    )

    return create_engine(
        f"postgresql://{_settings.postgres_user_guest}:"
        + f"{_settings.postgres_password_guest}@"
        + f"{_settings.postgres_host}:"
        + f"{_settings.postgres_connection_port}/"
        + f"{_settings.postgres_dbname}",
    )


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def get_postgres_connection(_settings: Dynaconf) -> connection:
    """Create a PostgreSQL connection."""
    print(
        f"[psycopg2] User connect request host={_settings.postgres_host} "
        + f"port={_settings.postgres_connection_port} "
        + f"dbname={_settings.postgres_dbname} "
        + f"user={_settings.postgres_user_guest}"
    )

    return psycopg2.connect(**st.secrets["db_postgres"])


# -----------------------------------------------------------------------------
# Authentication and authorization check.
# -----------------------------------------------------------------------------
def has_access(
    host_cloud: bool, app_id: str
) -> tuple[str, dict[str, dict[str, list[str]]]]:
    """Authentication and authorization check."""

    # pylint: disable=line-too-long
    print(
        str(datetime.datetime.now())
        + f"                         - Authentication through Keycloak starts     - Cloud: {host_cloud} - Application: {app_id}",
        flush=True,
    )

    # pylint: disable=R0801
    keycloak = login(
        url="http://auth.io-aero.com:8080"
        if host_cloud
        else "http://auth.localhost:8080",
        realm="IO-Aero",
        client_id=app_id,
    )

    if not keycloak.authenticated:
        st.stop()

    if (resource_access := keycloak.user_info.get("resource_access")) is None:
        keycloak.authenticated = False
        # pylint: disable=line-too-long
        st.error(
            "##### Error: Your user info doesn't contain the resource_access property! Perhaps the client scope mapping isn't configured properly."
        )
        st.stop()

    user_info = f"User:  {keycloak.user_info.get('family_name')+', '+keycloak.user_info.get('given_name')} [{keycloak.user_info.get('email')}]"
    print(
        str(datetime.datetime.now())
        + f"                         -                                            - {user_info}",
        flush=True,
    )

    if (client_access := resource_access.get(app_id)) is None:
        keycloak.authenticated = False
        st.error("##### Error: You have no permission to access this application.")
        del st.session_state["KEYCLOAK"]
        print(
            str(datetime.datetime.now())
            + "                         -                                            - Authentication Error: You have no permission to access this application.",
            flush=True,
        )
        st.stop()

    if app_id + "-access" not in client_access.get("roles", []):
        keycloak.authenticated = False
        st.error(
            "##### Error: You are missing the required role to access this application."
        )
        print(
            str(datetime.datetime.now())
            + "                         -                                            - Authentication Error: You are missing the required role to access this application.",
            flush=True,
        )
        st.stop()

    # pylint: disable=line-too-long
    print(
        str(datetime.datetime.now())
        + f"                         - Authentication through Keycloak successful - app_id={app_id}",
        flush=True,
    )

    return user_info, keycloak.user_info.get("resource_access")


# ------------------------------------------------------------------
# Present the 'about' information.
# ------------------------------------------------------------------
# flake8: noqa: E501
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

**:copyright: 2022-{datetime.date.today().year} - IO AERONAUTICAL AUTONOMY LABS, LLC**

[Disclaimer](https://www.io-aero.com/disclaimer)
    """
    )


# ------------------------------------------------------------------
# Determine the last processed update file.
# ------------------------------------------------------------------
# flake8: noqa: E501
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
        SELECT file_name, TO_CHAR(COALESCE(last_processed, first_processed), 'DD.MM.YYYY')
          FROM io_processed_files
         WHERE file_name LIKE 'up%'
            OR file_name IN ('Pre2008', 'avall')
         ORDER BY COALESCE(last_processed, first_processed) DESC;
        """
        )

        return cur.fetchone()  # type: ignore
