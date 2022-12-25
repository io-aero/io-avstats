# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Profiling Data for the US since 1982."""
import datetime
import os

import pandas as pd
import psycopg2
import streamlit as st
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

# ------------------------------------------------------------------
# Global constants.
# ------------------------------------------------------------------
# pylint: disable=R0801
CHOICE_DATA_PROFILE = None
CHOICE_DATA_PROFILE_FILE = None
CHOICE_DATA_PROFILE_TYPE = None
CHOICE_DETAILS = None
CHOICE_FILTER_DATA = None
CHOICE_TABLE_SELECTION = None

DF: DataFrame = DataFrame()

FILTER_YEAR_FROM = None
FILTER_YEAR_TO = None

PG_CONN: Connection | None = None

# ------------------------------------------------------------------
# Query data for the US since 1982.
# ------------------------------------------------------------------
QUERIES = {
    "aircraft": """
        SELECT a.*,
               e.ev_year
          FROM aircraft a
          LEFT OUTER JOIN events e
            ON (a.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY a.ev_id,
                 a.aircraft_key;
    """,
    "dt_aircraft": """
        SELECT d.*,
               e.ev_year
          FROM dt_aircraft d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.col_name,
                 d.code;
    """,
    "dt_events": """
        SELECT d.*,
               e.ev_year
          FROM dt_events d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.col_name,
                 d.code;
    """,
    "dt_flight_crew": """
        SELECT d.*,
               e.ev_year
          FROM dt_flight_crew d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.crew_no,
                 d.col_name,
                 d.code;
    """,
    "engines": """
        SELECT d.*,
               e.ev_year
          FROM engines d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.eng_no;
    """,
    "events": """
        SELECT *
          FROM events
         WHERE ev_state IN (SELECT state
                              FROM io_states
                             WHERE country = 'USA')
           AND ev_year >= 1982
         ORDER BY ev_id;
    """,
    "events_sequence": """
        SELECT d.*,
               e.ev_year
          FROM events_sequence d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.occurrence_no;
    """,
    "findings": """
        SELECT f.*,
               e.ev_year
          FROM findings f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.finding_no;
    """,
    "flight_crew": """
        SELECT f.*,
               e.ev_year
          FROM flight_crew f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.crew_no;
    """,
    "flight_time": """
        SELECT f.*,
               e.ev_year
          FROM flight_time f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.crew_no,
                 f.flight_type,
                 f.flight_craft;
    """,
    "injury": """
        SELECT i.*,
               e.ev_year
          FROM injury i
          LEFT OUTER JOIN events e
            ON (i.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY i.ev_id,
                 i.aircraft_key,
                 i.inj_person_category,
                 i.injury_level;
    """,
    "io_app_faaus1982": """
        SELECT *
          FROM io_app_faaus1982
        ORDER BY ev_id;
    """,
    "io_countries": """
        SELECT *
          FROM io_countries
        ORDER BY country;
    """,
    "io_fatalities_us_1982": """
        SELECT *
          FROM io_fatalities_us_1982
        ORDER BY ev_id;
    """,
    "io_lat_lng": """
        SELECT *
          FROM io_lat_lng
        ORDER BY id;
    """,
    "io_lat_lng_issues": """
        SELECT l.*,
               e.ev_year
          FROM io_lat_lng_issues l
          LEFT OUTER JOIN events e
            ON (l.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY l.ev_id;
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
    "io_us_1982": """
        SELECT *
          FROM io_us_1982
        ORDER BY ev_id;
    """,
    "narratives": """
        SELECT n.*,
               e.ev_year
          FROM narratives n
          LEFT OUTER JOIN events e
            ON (n.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY n.ev_id,
                 n.aircraft_key;
    """,
    "ntsb_admin": """
        SELECT n.*,
               e.ev_year
          FROM ntsb_admin n
          LEFT OUTER JOIN events e
            ON (n.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY n.ev_id;
    """,
    "occurrences": """
        SELECT o.*,
               e.ev_year
          FROM occurrences o
          LEFT OUTER JOIN events e
            ON (o.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY o.ev_id,
                 o.aircraft_key,
                 o.occurrence_no;
    """,
    "seq_of_events": """
        SELECT s.*,
               e.ev_year
          FROM seq_of_events s
          LEFT OUTER JOIN events e
            ON (s.ev_id = e.ev_id)
        WHERE e.ev_state IN (SELECT state
                               FROM io_states
                              WHERE country = 'USA')
          AND e.ev_year >= 1982
        ORDER BY s.ev_id,
                 s.aircraft_key,
                 s.occurrence_no,
                 s.seq_event_no,
                 s.group_code;
    """,
}

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)


# ------------------------------------------------------------------
# Filter the data frame.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
def _apply_filter_controls():
    global DF  # pylint: disable=global-statement

    # noinspection PyUnboundLocalVariable
    if FILTER_YEAR_FROM or FILTER_YEAR_TO:
        DF = DF.loc[
            (DF["ev_year"] >= FILTER_YEAR_FROM) & (DF["ev_year"] <= FILTER_YEAR_TO)
        ]


# ------------------------------------------------------------------
# Read and filter the data.
# ------------------------------------------------------------------
def _get_data():
    global DF  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement

    PG_CONN = _get_postgres_connection()

    DF = pd.read_sql(QUERIES[CHOICE_TABLE_SELECTION], con=_get_engine())  # type: ignore

    if not (
        CHOICE_TABLE_SELECTION
        in [
            "io_countries",
            "io_processed_files",
            "io_lat_lng",
            "io_states",
        ]
    ):
        if CHOICE_FILTER_DATA:
            _apply_filter_controls()


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
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data():
    if CHOICE_DATA_PROFILE:
        st.subheader(f"Profiling of the database table `{CHOICE_TABLE_SELECTION}`")
        _present_data_data_profile()

    if CHOICE_DETAILS:
        st.subheader(f"The database table `{CHOICE_TABLE_SELECTION}` in detail")
        st.dataframe(DF)


# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
def _present_data_data_profile():
    # noinspection PyUnboundLocalVariable
    if CHOICE_DATA_PROFILE_TYPE == "explorative":
        profile_report = ProfileReport(
            DF,
            explorative=True,
        )
    else:
        profile_report = ProfileReport(
            DF,
            minimal=True,
        )

    st_profile_report(profile_report)

    # noinspection PyUnboundLocalVariable
    if CHOICE_DATA_PROFILE_FILE:
        if not os.path.isdir(SETTINGS.pandas_profile_dir):
            os.mkdir(SETTINGS.pandas_profile_dir)
        profile_report.to_file(
            os.path.join(
                SETTINGS.pandas_profile_dir,
                CHOICE_TABLE_SELECTION + "_" + CHOICE_DATA_PROFILE_TYPE,  # type: ignore
            )
        )


# ------------------------------------------------------------------
# Setup the filter controls.
# ------------------------------------------------------------------
def _setup_filter_controls():
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_YEAR_TO  # pylint: disable=global-statement

    st.sidebar.markdown("""---""")

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**`Filter data ?`**",
        value=True,
    )

    if CHOICE_FILTER_DATA:
        FILTER_YEAR_FROM, FILTER_YEAR_TO = st.sidebar.slider(
            label="Select a time frame",
            help="Data available from 1982 to the current year.",
            min_value=1982,
            max_value=datetime.date.today().year,
            value=(2008, datetime.date.today().year),
        )


# ------------------------------------------------------------------
# Setup the page.
# ------------------------------------------------------------------
def _setup_page():
    st.set_page_config(layout="wide")
    st.header("Profiling Data for the US since 1982")


# ------------------------------------------------------------------
# Setup the sidebar.
# ------------------------------------------------------------------
def _setup_sidebar():
    _setup_task_controls()
    _setup_filter_controls()


# ------------------------------------------------------------------
# Setup the task controls.
# ------------------------------------------------------------------
def _setup_task_controls():
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_FILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_TABLE_SELECTION  # pylint: disable=global-statement

    CHOICE_DATA_PROFILE = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**`Show data profile`**",
        value=False,
    )

    if CHOICE_DATA_PROFILE:
        CHOICE_DATA_PROFILE_TYPE = st.sidebar.radio(
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

        if SETTINGS.is_runtime_environment_local:
            CHOICE_DATA_PROFILE_FILE = st.sidebar.checkbox(
                help="Export the Pandas profile into a file.",
                label="Export profile to file",
                value=False,
            )

    st.sidebar.markdown("""---""")

    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the selected detailed data.",
        label="**`Show details`**",
        value=True,
    )

    st.sidebar.markdown("""---""")

    CHOICE_TABLE_SELECTION = st.sidebar.radio(
        help="Available database tables and views for profiling.",
        index=5,
        label="**`Database table`**",
        options=(QUERIES.keys()),
    )


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
_setup_page()

_setup_sidebar()

_get_data()

_present_data()
