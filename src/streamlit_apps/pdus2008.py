# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Profiling Data for the US since 2008."""
import os

import pandas as pd
import psycopg2
import streamlit as st
from dynaconf import Dynaconf  # type: ignore
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

# ------------------------------------------------------------------
# Global constants.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# Query data for the US since 2008.
# ------------------------------------------------------------------
QUERIES = {
    "aircraft": """
        SELECT *
          FROM aircraft
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key;
    """,
    "dt_aircraft": """
        SELECT *
          FROM dt_aircraft
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 col_name,
                 code;
    """,
    "dt_events": """
        SELECT *
          FROM dt_events
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 col_name,
                 code;
    """,
    "dt_flight_crew": """
        SELECT *
          FROM dt_flight_crew
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 crew_no,
                 col_name,
                 code;
    """,
    "engines": """
        SELECT *
          FROM engines
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 eng_no;
    """,
    "events": """
        SELECT *
          FROM events
         WHERE ev_state IN (SELECT state
                              FROM io_states
                             WHERE country = 'USA')
           AND ev_year >= 2008
         ORDER BY ev_id;
    """,
    "events_sequence": """
        SELECT *
          FROM events_sequence
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 occurrence_no;
    """,
    "findings": """
        SELECT *
          FROM findings
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 finding_no;
    """,
    "flight_crew": """
        SELECT *
          FROM flight_crew
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 crew_no;
    """,
    "flight_time": """
        SELECT *
          FROM flight_time
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 crew_no,
                 flight_type,
                 flight_craft;
    """,
    "injury": """
        SELECT *
          FROM injury
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 inj_person_category,
                 injury_level;
    """,
    "io_app_faaus2008": """
        SELECT *
          FROM io_app_faaus2008
        ORDER BY ev_id;
    """,
    "io_countries": """
        SELECT *
          FROM io_countries
        ORDER BY country;
    """,
    "io_fatalities_us_2008": """
        SELECT *
          FROM io_fatalities_us_2008
        ORDER BY ev_id;
    """,
    "io_lat_lng": """
        SELECT *
          FROM io_lat_lng
        ORDER BY id;
    """,
    "io_lat_lng_issues": """
        SELECT *
          FROM io_lat_lng_issues
        ORDER BY ev_id;
    """,
    "io_processed_files": """
        SELECT *
          FROM io_processed_files
        ORDER BY first_processed DESC;
    """,
    "io_states": """
        SELECT *
          FROM io_states
        ORDER BY country,
                 state;
    """,
    "io_us_2008": """
        SELECT *
          FROM io_us_2008
        ORDER BY ev_id;
    """,
    "narratives": """
        SELECT *
          FROM narratives
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key;
    """,
    "ntsb_admin": """
        SELECT *
          FROM ntsb_admin
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id;
    """,
    "occurrences": """
        SELECT *
          FROM occurrences
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 occurrence_no;
    """,
    "seq_of_events": """
        SELECT *
          FROM seq_of_events
         WHERE ev_id IN (SELECT ev_id
                           FROM events
                          WHERE ev_state IN (SELECT state
                                               FROM io_states
                                              WHERE country = 'USA')
                            AND ev_year >= 2008)
        ORDER BY ev_id,
                 aircraft_key,
                 occurrence_no,
                 seq_event_no,
                 group_code;
    """,
}

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)


# ------------------------------------------------------------------
# Create a simple user PostgreSQL database engine.
# ------------------------------------------------------------------
# pylint: disable=R0801
def _get_engine() -> Engine:
    """Create a simple user PostgreSQL database engine.

    Returns:
        Engine: Database engine.
    """
    return create_engine(
        f"postgresql://{SETTINGS.postgres_user}:"
        + f"{SETTINGS.postgres_password}@"
        + f"{SETTINGS.postgres_host}:"
        + f"{SETTINGS.postgres_connection_port}/"
        + f"{SETTINGS.postgres_dbname}",
    )


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=R0801
def _get_postgres_connection() -> connection:
    """Create a PostgreSQL connection,

    Returns:
        connection: Database connection.
    """
    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Setup the page.
# ------------------------------------------------------------------
st.set_page_config(layout="wide")
st.header("Profiling Data for the US since 2008")

# ------------------------------------------------------------------
# Setup the controls.
# ------------------------------------------------------------------
choice_data_profile = st.sidebar.checkbox(
    help="Pandas profiling of the dataset.",
    label="**`Show data profile`**",
    value=False,
)

if choice_data_profile:
    choice_data_profile_type = st.sidebar.radio(
        help="explorative: thorough but also slow - minimal: minimal but faster.",
        index=1,
        label="Data profile type",
        options=(
            [
                "explorative",
                "minimal",
            ]
        ),
    )
    choice_data_profile_file = st.sidebar.checkbox(
        help="Export the Pandas profile into a file.",
        label="Export profile to file",
        value=False,
    )

choice_details = st.sidebar.checkbox(
    help="Tabular representation of the selected detailed data.",
    label="**`Show details`**",
    value=True,
)

table_selection = st.sidebar.radio(
    help="Available database tables and views for profiling.",
    index=5,
    label="Database table",
    options=(QUERIES.keys()),
)

# ------------------------------------------------------------------
# Read and filter data.
# ------------------------------------------------------------------
pg_conn = _get_postgres_connection()

df_db_data = pd.read_sql(QUERIES[table_selection], con=_get_engine())  # type: ignore

# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
if choice_data_profile:
    st.subheader(f"Profiling of the database table `{table_selection}`")
    # noinspection PyUnboundLocalVariable
    if choice_data_profile_type == "explorative":
        df_db_data_profile = ProfileReport(
            df_db_data,
            explorative=True,
        )
    else:
        df_db_data_profile = ProfileReport(
            df_db_data,
            minimal=True,
        )
    st_profile_report(df_db_data_profile)
    # noinspection PyUnboundLocalVariable
    if choice_data_profile_file:
        if not os.path.isdir(SETTINGS.pandas_profile_dir):
            os.mkdir(SETTINGS.pandas_profile_dir)
        df_db_data_profile.to_file(
            os.path.join(
                SETTINGS.pandas_profile_dir,
                table_selection + "_" + choice_data_profile_type,  # type: ignore
            )
        )


# ------------------------------------------------------------------
# Present details.
# ------------------------------------------------------------------
if choice_details:
    st.subheader(f"The database table `{table_selection}` in detail")
    st.dataframe(df_db_data)
