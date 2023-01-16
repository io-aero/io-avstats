# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Profiling Data for the US since 1982."""
import datetime
import time

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
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "pd1982"

# pylint: disable=R0801
CHOICE_ABOUT: bool | None = None
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None
CHOICE_FILTER_DATA: bool | None = None
CHOICE_TABLE_SELECTION: str = ""

DF_FILTERED: DataFrame = DataFrame()
DF_UNFILTERED: DataFrame = DataFrame()

FILTER_YEAR_FROM: int | None = None
FILTER_YEAR_TO: int | None = None

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
    "io_app_ae1982": """
        SELECT *
          FROM io_app_ae1982
        ORDER BY ev_id;
    """,
    "io_countries": """
        SELECT *
          FROM io_countries
        ORDER BY country;
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
@st.experimental_memo
def _apply_filter_controls(
    df_unfiltered: DataFrame, filter_year_from: int | None, filter_year_to: int | None
) -> DataFrame:
    """Filter the data frame.

    Args:
        df_unfiltered (DataFrame): The unfiltered dataframe.
        filter_year_from (int | None): Event year from.
        filter_year_to (int | None): Event year to.

    Returns:
        DataFrame: The filtered dataframe.
    """
    df_filtered = df_unfiltered

    # noinspection PyUnboundLocalVariable
    if filter_year_from or filter_year_to:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= filter_year_from)
            & (df_filtered["ev_year"] <= filter_year_to)
        ]

    return df_filtered


# ------------------------------------------------------------------
# Convert a dataframe to csv data.
# ------------------------------------------------------------------
@st.experimental_memo
def _convert_df_2_csv(dataframe: DataFrame) -> bytes:
    """Convert a dataframe to csv data.

    Args:
        dataframe (DataFrame): The datafarame.

    Returns:
        bytes: The csv data.
    """
    return dataframe.to_csv().encode("utf-8")


# ------------------------------------------------------------------
# Read the data.
# ------------------------------------------------------------------
@st.experimental_memo
def _get_data(table_name: str) -> DataFrame:
    """Read the data.

    Args:
        table_name (str): Name of the database table.

    Returns:
        DataFrame: The unfiltered dataframe.
    """
    global PG_CONN  # pylint: disable=global-statement

    PG_CONN = _get_postgres_connection()  # type: ignore

    return pd.read_sql(QUERIES[table_name], con=_get_engine())  # type: ignore


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
@st.experimental_singleton
def _get_postgres_connection() -> connection:
    """Create a PostgreSQL connection.

    Returns:
        connection: Database connection.
    """
    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Present the chart: Events per Year by Injury Level.
# ------------------------------------------------------------------
def _present_about():
    file_name, processed = _sql_query_last_file_name()

    about_msg = "IO-AVSTATS Application: **pd1982**"
    about_msg = about_msg + "<br/>"
    about_msg = about_msg + f"\nLastest NTSB database: **{file_name} - {processed}**"
    about_msg = about_msg + "<br/>"
    about_msg = (
        about_msg
        + f"\n**:copyright: 2022-{datetime.date.today().year} - "
        + "IO AERONAUTICAL AUTONOMY LABS, LLC**"
    )

    st.markdown(about_msg, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data():
    """Present the filtered data."""
    if CHOICE_DATA_PROFILE:
        st.subheader(f"Profiling of the database table `{CHOICE_TABLE_SELECTION}`")
        _present_data_data_profile()

    _col1, _col2, col3 = st.columns(
        [
            1,
            1,
            1,
        ]
    )

    if CHOICE_ABOUT:
        with col3:
            _present_about()

    if CHOICE_DETAILS:
        st.subheader(f"The database table `{CHOICE_TABLE_SELECTION}` in detail")
        st.dataframe(DF_FILTERED)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED),
            file_name=APP_ID + "_" + CHOICE_TABLE_SELECTION + ".csv",
            help="The download includes all data of the selected table "
            + "after applying the filter options.",
            label="Download all data as CSV file",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the data profile.
# ------------------------------------------------------------------
def _present_data_data_profile():
    """Present the data profile."""
    # noinspection PyUnboundLocalVariable
    if CHOICE_DATA_PROFILE_TYPE == "explorative":
        profile_report = ProfileReport(
            DF_FILTERED,
            explorative=True,
        )
    else:
        profile_report = ProfileReport(
            DF_FILTERED,
            minimal=True,
        )

    st_profile_report(profile_report)

    st.download_button(
        data=profile_report.to_html(),
        file_name=APP_ID + "_" + CHOICE_DATA_PROFILE_TYPE + ".html",
        help="The download includes a profile report from the dataframe "
        + "after applying the filter options.",
        label="Download the profile report",
        mime="text/html",
    )


# ------------------------------------------------------------------
# Set up the filter controls.
# ------------------------------------------------------------------
def _setup_filter_controls():
    """Set up the filter controls."""
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_YEAR_TO  # pylint: disable=global-statement

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**Filter data ?**",
        value=True,
    )

    if CHOICE_FILTER_DATA:
        FILTER_YEAR_FROM, FILTER_YEAR_TO = st.sidebar.slider(
            label="Select a time frame",
            help="Data available from 1982 to the current year.",
            min_value=1982,
            max_value=datetime.date.today().year,
            value=(2008, datetime.date.today().year - 1),
        )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page():
    """Set up the page."""
    global CHOICE_ABOUT  # pylint: disable=global-statement

    st.header(
        f"Profiling Data from Year {FILTER_YEAR_FROM} to {FILTER_YEAR_TO}"
    )

    _col1, _col2, col3 = st.columns(
        [
            1,
            1,
            1,
        ]
    )

    with col3:
        CHOICE_ABOUT = st.checkbox(
            help="Software owner and release information.",
            label="**About this Application**",
            value=False,
        )


# ------------------------------------------------------------------
# Set up the sidebar.
# ------------------------------------------------------------------
def _setup_sidebar():
    """Set up the sidebar."""
    _setup_task_controls()
    _setup_filter_controls()


# ------------------------------------------------------------------
# Set up the task controls.
# ------------------------------------------------------------------
def _setup_task_controls():
    """Set up the task controls."""
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_TABLE_SELECTION  # pylint: disable=global-statement

    CHOICE_DATA_PROFILE = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**Show data profile**",
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

    st.sidebar.markdown("""---""")

    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the selected detailed data.",
        label="**Show details**",
        value=True,
    )

    st.sidebar.markdown("""---""")

    CHOICE_TABLE_SELECTION = st.sidebar.radio(
        help="Available database tables and views for profiling.",
        index=5,
        label="**Database table**",
        options=(QUERIES.keys()),
    )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Determine the last processed update file.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_last_file_name() -> tuple[str, str]:
    """Determine the last processed update file.

    Returns:
        tuple[str, str]: File name and processing date.
    """
    global PG_CONN  # pylint: disable=global-statement

    PG_CONN = _get_postgres_connection()  # type: ignore

    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT file_name, TO_CHAR(first_processed, 'DD.MM.YYYY')
          FROM io_processed_files
         ORDER BY first_processed DESC ;
        """
        )

        return cur.fetchone()  # type: ignore


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
# Start time measurement.
start_time = time.time_ns()

st.set_page_config(layout="wide")

_setup_sidebar()

_setup_page()

DF_UNFILTERED = _get_data(CHOICE_TABLE_SELECTION)

DF_FILTERED = DF_UNFILTERED

if CHOICE_TABLE_SELECTION not in [
    "io_countries",
    "io_processed_files",
    "io_lat_lng",
    "io_states",
]:
    if CHOICE_FILTER_DATA:
        DF_FILTERED = _apply_filter_controls(
            DF_UNFILTERED, FILTER_YEAR_FROM, FILTER_YEAR_TO
        )

_present_data()

# Stop time measurement.
print(
    str(datetime.datetime.now())
    + f" {f'{time.time_ns() - start_time:,}':>20} ns - Total runtime for application "
    + APP_ID,
    flush=True,
)
