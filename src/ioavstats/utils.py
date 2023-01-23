# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Application Utilities."""
import datetime

import streamlit as st
from psycopg2.extensions import connection


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

    about_msg = f"IO-AVSTATS Application: **{app_name}**"
    about_msg = about_msg + "<br/>"
    about_msg = about_msg + f"\nLatest NTSB database: **{file_name} - {processed}**"
    about_msg = about_msg + "<br/>"
    about_msg = (
        about_msg
        + f"\n**:copyright: 2022-{datetime.date.today().year} - "
        + "IO AERONAUTICAL AUTONOMY LABS, LLC**"
    )
    about_msg = (
        about_msg
        # pylint: disable=line-too-long
        + """\n<a href="https://www.io-aero.com/disclaimer" target="_blank">Disclaimer</a>
          """
    )

    st.markdown(about_msg, unsafe_allow_html=True)


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
         ORDER BY COALESCE(last_processed, first_processed) DESC;
        """
        )

        return cur.fetchone()  # type: ignore
