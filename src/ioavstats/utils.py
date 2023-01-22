# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Application Utilities."""
import datetime

import streamlit as st
from sqlalchemy.engine import Connection


# ------------------------------------------------------------------
# Present the 'about' information.
# ------------------------------------------------------------------
def present_about(pg_conn: Connection, app_name: str) -> None:
    """Present the 'about' information.

    Args:
        pg_conn (Connection): Database connection.
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
        + """\n<a href="https://www.io-aero.com" target="_blank">Disclaimer</a>
          """
    )

    st.markdown(about_msg, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Determine the last processed update file.
# ------------------------------------------------------------------
def _sql_query_last_file_name(pg_conn: Connection) -> tuple[str, str]:
    """Determine the last processed update file.

    Args:
        pg_conn (Connection): Database connection.

    Returns:
        tuple[str, str]: File name and processing date.
    """
    with pg_conn.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT file_name, TO_CHAR(first_processed, 'DD.MM.YYYY')
          FROM io_processed_files
         ORDER BY first_processed DESC ;
        """
        )

        return cur.fetchone()  # type: ignore
