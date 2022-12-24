# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Fatal Aviation Accidents in the US since 2008."""
import datetime
import os

import pandas as pd
import psycopg2
import pydeck as pdk  # type: ignore
import seaborn as sns  # type: ignore
import streamlit as st
from dynaconf import Dynaconf  # type: ignore
from matplotlib import pyplot as plt  # type: ignore
from pandas import DataFrame
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
CHOICE_DATA_PROFILE = None
CHOICE_DATA_PROFILE_FILE = None
CHOICE_DATA_PROFILE_TYPE = None
CHOICE_DETAILS = None
CHOICE_FILTER_DATA = None
CHOICE_HISTOGRAM = None
CHOICE_HISTOGRAM_HEIGHT = None
CHOICE_HISTOGRAM_WIDTH = None
CHOICE_MAP = None
CHOICE_MAP_MAP_STYLE = None

DF_FAA_FILTERED: DataFrame = DataFrame()

FILTER_ACFT_CATEGORIES = ""
FILTER_ALT_LOW = None
FILTER_FAR_PARTS = ""
FILTER_FINDING_CODES = ""
FILTER_LATLONG_ACQ = None
FILTER_NARR_STALL = None
FILTER_OCCURRENCE_CODES = ""
FILTER_SPIN_STALL = None
FILTER_STATES = ""
FILTER_YEAR_FROM = None
FILTER_YEAR_TO = None

# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"

MAP_STYLE_PREFIX = "mapbox://styles/mapbox/"

PITCH = 30

# ------------------------------------------------------------------
# Query regarding the aircraft fatalities in the US since 2008.
# ------------------------------------------------------------------
QUERY_FAAUS2008 = """
    SELECT *
     FROM io_app_faaus2008
    ORDER BY ev_id;
"""

QUERY_US_LL = """
    SELECT dec_latitude,
           dec_longitude
      FROM io_countries
     WHERE country = 'USA'
"""

CHOICE_MAP_RADIUS = 1609.347 * 2

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)

ZOOM = 4.4


# ------------------------------------------------------------------
# Filter the data frame.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
def _apply_filter_controls():
    global DF_FAA_FILTERED  # pylint: disable=global-statement

    # noinspection PyUnboundLocalVariable
    if FILTER_YEAR_FROM or FILTER_YEAR_TO:
        df_faa_year = df_faa.loc[
            (df_faa["ev_year"] >= FILTER_YEAR_FROM)
            & (df_faa["ev_year"] <= FILTER_YEAR_TO)
        ]
    else:
        df_faa_year = df_faa
    # noinspection PyUnboundLocalVariable
    if FILTER_ACFT_CATEGORIES:
        # noinspection PyUnboundLocalVariable
        df_faa_acft_categories = df_faa_year.loc[
            (
                df_faa_year["acft_category"].isin(
                    FILTER_ACFT_CATEGORIES.upper().split(",")
                )
            )
        ]
    else:
        df_faa_acft_categories = df_faa_year
    # noinspection PyUnboundLocalVariable
    if FILTER_FAR_PARTS:
        # noinspection PyUnboundLocalVariable
        df_faa_far_parts = df_faa_acft_categories.loc[
            (
                df_faa_acft_categories["far_part"].isin(
                    FILTER_FAR_PARTS.upper().split(",")
                )
            )
        ]
    else:
        df_faa_far_parts = df_faa_acft_categories
    # noinspection PyUnboundLocalVariable
    if FILTER_FINDING_CODES:
        # noinspection PyUnboundLocalVariable
        df_faa_finding_codes = df_faa_far_parts.loc[
            (
                df_faa_far_parts["finding_code"].isin(
                    FILTER_FINDING_CODES.upper().split(",")
                )
            )
        ]
    else:
        df_faa_finding_codes = df_faa_far_parts
    # noinspection PyUnboundLocalVariable
    if FILTER_OCCURRENCE_CODES:
        # noinspection PyUnboundLocalVariable
        df_faa_occurrence_codes = df_faa_finding_codes.loc[
            (
                df_faa_finding_codes["occurrence_code"].isin(
                    FILTER_OCCURRENCE_CODES.upper().split(",")
                )
            )
        ]
    else:
        df_faa_occurrence_codes = df_faa_finding_codes
    # noinspection PyUnboundLocalVariable
    if FILTER_STATES:
        # noinspection PyUnboundLocalVariable
        df_faa_states = df_faa_occurrence_codes.loc[
            (df_faa_occurrence_codes["state"].isin(FILTER_STATES.upper().split(",")))
        ]
    else:
        df_faa_states = df_faa_occurrence_codes
    # noinspection PyUnboundLocalVariable
    if FILTER_LATLONG_ACQ:
        # noinspection PyUnboundLocalVariable
        df_faa_latlong_acq = df_faa_states.loc[
            (df_faa_states["latlong_acq"] == FILTER_LATLONG_ACQ)
        ]
    else:
        df_faa_latlong_acq = df_faa_states
    # noinspection PyUnboundLocalVariable
    if FILTER_SPIN_STALL:
        # noinspection PyUnboundLocalVariable
        df_faa_spin_stall = df_faa_latlong_acq.loc[
            # pylint: disable=singleton-comparison
            (df_faa_latlong_acq["spin_stall"] == True)  # noqa: E712
        ]
    else:
        df_faa_spin_stall = df_faa_latlong_acq
    # noinspection PyUnboundLocalVariable
    if FILTER_ALT_LOW:
        # noinspection PyUnboundLocalVariable
        df_faa_alt_low = df_faa_spin_stall.loc[
            # pylint: disable=singleton-comparison
            (df_faa_spin_stall["alt_low"] == True)  # noqa: E712
        ]
    else:
        df_faa_alt_low = df_faa_spin_stall
    # noinspection PyUnboundLocalVariable
    if FILTER_NARR_STALL:
        # noinspection PyUnboundLocalVariable
        df_faa_narr_stall = df_faa_alt_low.loc[
            # pylint: disable=singleton-comparison
            (df_faa_alt_low["narr_stall"] == True)  # noqa: E712
        ]
    else:
        df_faa_narr_stall = df_faa_alt_low
    DF_FAA_FILTERED = df_faa_narr_stall


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
# Present data profile.
# ------------------------------------------------------------------
def _present_data_profile():
    st.subheader("Profiling of the filtered data set")

    # noinspection PyUnboundLocalVariable
    if CHOICE_DATA_PROFILE_TYPE == "explorative":
        df_faa_states_year_profile = ProfileReport(
            DF_FAA_FILTERED,
            explorative=True,
        )
    else:
        df_faa_states_year_profile = ProfileReport(
            DF_FAA_FILTERED,
            minimal=True,
        )

    st_profile_report(df_faa_states_year_profile)

    # noinspection PyUnboundLocalVariable
    if CHOICE_DATA_PROFILE_FILE:
        if not os.path.isdir(SETTINGS.pandas_profile_dir):
            os.mkdir(SETTINGS.pandas_profile_dir)
        df_faa_states_year_profile.to_file(
            os.path.join(
                SETTINGS.pandas_profile_dir,
                "faaus2008_" + CHOICE_DATA_PROFILE_TYPE,  # type: ignore
            )
        )


# ------------------------------------------------------------------
# Present the yearly fatal accidents.
# ------------------------------------------------------------------
def _present_histogram():
    st.subheader("Number of fatal accidents per year")

    # noinspection PyUnboundLocalVariable
    fig, _ax = plt.subplots(figsize=(CHOICE_HISTOGRAM_WIDTH, CHOICE_HISTOGRAM_HEIGHT))

    sns.histplot(DF_FAA_FILTERED["ev_year"], discrete=True)

    plt.xlabel("Year")

    st.pyplot(fig)


# ------------------------------------------------------------------
# Present the US map.
# ------------------------------------------------------------------
def _present_map():
    st.subheader("Depicting the fatal accidents on a map of the USA")

    faa_layer = pdk.Layer(
        auto_highlight=True,
        data=DF_FAA_FILTERED,
        get_fill_color=[255, 0, 0],
        get_position=["dec_longitude", "dec_latitude"],
        get_radius=CHOICE_MAP_RADIUS,
        pickable=True,
        type=LAYER_TYPE,
    )

    # noinspection PyUnboundLocalVariable
    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=_sql_query_us_ll(pg_conn, QUERY_US_LL),
            layers=[faa_layer],
            map_style=MAP_STYLE_PREFIX + CHOICE_MAP_MAP_STYLE,  # type: ignore
            tooltip={
                "html": "<table><tbody>"
                + "<tr><td><b>Event Id</b></td><td>{ev_id}</td></tr>"
                + "<tr><td><b>NTSB No</b></td><td>{ntsb_no}</td></tr>"
                + "<tr><td><b>Fatalities</b></td><td>{fatalities}</td></tr>"
                + "<tr><td><b>Latitude</b></td><td>{dec_latitude}</td></tr>"
                + "<tr><td><b>Longitude</b></td><td>{dec_longitude}</td></tr>"
                + "<tr><td><b>Aquired</b></td><td>{latlong_acq}</td></tr>"
                + "</tbody></table>"
            },
        )
    )


# ------------------------------------------------------------------
# Setup the filter controls.
# ------------------------------------------------------------------
def _setup_filter_controls():
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_ALT_LOW  # pylint: disable=global-statement
    global FILTER_FAR_PARTS  # pylint: disable=global-statement
    global FILTER_FINDING_CODES  # pylint: disable=global-statement
    global FILTER_LATLONG_ACQ  # pylint: disable=global-statement
    global FILTER_NARR_STALL  # pylint: disable=global-statement
    global FILTER_OCCURRENCE_CODES  # pylint: disable=global-statement
    global FILTER_SPIN_STALL  # pylint: disable=global-statement
    global FILTER_STATES  # pylint: disable=global-statement
    global FILTER_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_YEAR_TO  # pylint: disable=global-statement

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**`Filter data ?`**",
        value=True,
    )

    if CHOICE_FILTER_DATA:
        FILTER_YEAR_FROM, FILTER_YEAR_TO = st.sidebar.slider(
            label="Select a time frame",
            help="Data available from 2008 to the current year.",
            min_value=2008,
            max_value=datetime.date.today().year,
            value=(2008, datetime.date.today().year),
        )

        FILTER_ACFT_CATEGORIES = st.sidebar.text_input(
            label="Select one or more aircraft categories",
            help="One or more aircraft categories - "
            + "all aircraft categories if no selection has been made.",
        )

        FILTER_FAR_PARTS = st.sidebar.text_input(
            label="Select one or more FAR parts",
            help="One or more FAR parts - "
            + "all FAR parts if no selection has been made.",
        )

        FILTER_FINDING_CODES = st.sidebar.text_input(
            label="Select one or more finding codes",
            help="One or more finding codes - "
            + "all finding codes if no selection has been made.",
        )

        FILTER_OCCURRENCE_CODES = st.sidebar.text_input(
            label="Select one or more occurrence codes",
            help="One or more occurrence codes - "
            + "all occurrence codes if no selection has been made.",
        )

        FILTER_STATES = st.sidebar.text_input(
            label="Select one or more states",
            help="One or more USPS abbreviations - "
            + "all U.S. states if no selection has been made.",
        )

        FILTER_LATLONG_ACQ = st.sidebar.selectbox(
            label="Select optionally a latitude and longitude determination method",
            help="`EST`means estimated - `MEAS`means measured using GPS.",
            options=(
                "",
                "EST",
                "MEAS",
            ),
        )

        FILTER_SPIN_STALL = st.sidebar.checkbox(
            help="Filters only events with `spin_stall` equals `True`.",
            label="Only events with aerodynamic spin stalls?",
        )

        FILTER_ALT_LOW = st.sidebar.checkbox(
            help="Filters only events with `alt_low` equals `True`.",
            label="Only events with altitude too low?",
        )

        FILTER_NARR_STALL = st.sidebar.checkbox(
            help="Filters only events with `narr_stall` equals `True`.",
            label="Only events stalled according to narrative?",
        )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Setup the controls.
# ------------------------------------------------------------------
def _setup_controls():
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_FILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_HISTOGRAM  # pylint: disable=global-statement
    global CHOICE_HISTOGRAM_HEIGHT  # pylint: disable=global-statement
    global CHOICE_HISTOGRAM_WIDTH  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_MAP_RADIUS  # pylint: disable=global-statement

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
        CHOICE_DATA_PROFILE_FILE = st.sidebar.checkbox(
            help="Export the Pandas profile into a file.",
            label="Export profile to file",
            value=False,
        )

    st.sidebar.markdown("""---""")

    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the selected detailed data.",
        label="**`Show details`**",
        value=False,
    )

    st.sidebar.markdown("""---""")

    CHOICE_HISTOGRAM = st.sidebar.checkbox(
        help="Fatal accidents per year.",
        label="**`Show histogram`**",
        value=False,
    )

    if CHOICE_HISTOGRAM:
        CHOICE_HISTOGRAM_WIDTH = st.sidebar.slider("Histogram width", 1, 25, 11)
        CHOICE_HISTOGRAM_HEIGHT = st.sidebar.slider("Histogram height", 1, 25, 5)

    st.sidebar.markdown("""---""")

    CHOICE_MAP = st.sidebar.checkbox(
        help="Display of fatal accident events on a map of the USA.",
        label="**`Show US map`**",
        value=False,
    )

    if CHOICE_MAP:
        CHOICE_MAP_MAP_STYLE = st.sidebar.radio(
            help="""
light: designed to provide geographic context while highlighting the data -
outdoors: focused on wilderness locations with curated tilesets -
streets: emphasizes accurate, legible styling of road and transit networks.
        """,
            index=1,
            label="Map style",
            options=(
                [
                    "light-v11",
                    "outdoors-v12",
                    "streets-v12",
                ]
            ),
        )
        CHOICE_MAP_RADIUS = st.sidebar.slider(
            label="Accident radius in meters",
            help="Radius for displaying the fatal accident events - "
            + "default value is 2 miles.",
            min_value=10,
            max_value=1609 * 4,
            value=(1609 * 2),
        )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Run the US latitude and longitude query.
# ------------------------------------------------------------------
def _sql_query_us_ll(conn: connection, query: str) -> pdk.ViewState:
    """Run t.he US latitude and longitude query.

    Args:
        conn (connection): Database connection.
        query (str): Database query.

    Returns:
        pdk.ViewState: Screen focus.
    """
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchone()
        return pdk.ViewState(
            latitude=result[0],  # type: ignore
            longitude=result[1],  # type: ignore
            pitch=PITCH,
            zoom=ZOOM,
        )


# ------------------------------------------------------------------
# Setup the page.
# ------------------------------------------------------------------
st.set_page_config(layout="wide")
st.header("Fatal Aviation Accidents in the US since 2008")

# ------------------------------------------------------------------
# Setup the sidebar.
# ------------------------------------------------------------------
_setup_controls()
_setup_filter_controls()

# ------------------------------------------------------------------
# Read and filter the data.
# ------------------------------------------------------------------
pg_conn = _get_postgres_connection()

df_faa = pd.read_sql(QUERY_FAAUS2008, con=_get_engine())

if CHOICE_FILTER_DATA:
    _apply_filter_controls()
else:
    DF_FAA_FILTERED = df_faa

# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
if CHOICE_DATA_PROFILE:
    _present_data_profile()

if CHOICE_DETAILS:
    st.subheader("The filtered data set in detail")
    st.dataframe(DF_FAA_FILTERED)

if CHOICE_HISTOGRAM:
    _present_histogram()

if CHOICE_MAP:
    _present_map()
