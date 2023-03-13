# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Application Utilities."""
import argparse
import datetime

import streamlit as st
from psycopg2.extensions import connection
from streamlit_keycloak import login


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

    return mode


# -----------------------------------------------------------------------------
# Authentication and authorization check.
# -----------------------------------------------------------------------------
def has_access(app_id:str) -> str:
    """Authentication and authorization check."""

    keycloak = login(
        url="http://auth.localhost:8080",
        realm="IO-Aero",
        client_id=app_id,
    )

    if not keycloak.authenticated:
        if "KEYCLOAK" in st.session_state:
            st.error(
                f"**Error**: The login has failed - client_id='{app_id}'."
            )
        else:
            st.session_state["KEYCLOAK"] = "KEYCLOAK"
        st.stop()

    if (resource_access := keycloak.user_info.get("resource_access")) is None:
        st.error(
            "**Error**: Your user info doesn't contain the resource_access property! Perhaps the client scope mapping isn't configured properly."
        )
        st.stop()
    elif (client_access := resource_access.get(app_id)) is None:
        st.error(
            "**Error**: You have no permission to access this application."
        )
        del st.session_state["KEYCLOAK"]
        st.stop()
    elif app_id + "-access" not in client_access.get("roles", []):
        st.error(
            "**Error**: You are missing the required role to access this application."
        )
        st.stop()


# ------------------------------------------------------------------
# Present the 'about' information.
# ------------------------------------------------------------------
# flake8: noqa: E501
def present_about(pg_conn: connection, app_name: str) -> None:
    """Present the 'about' information.

    Args:
        pg_conn (connection): Database connection.
        app_name (str): Application name.
    """
    file_name, processed = _sql_query_last_file_name(pg_conn)

    st.warning(
        f"""
IO-AVSTATS Application: **{app_name}**

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
