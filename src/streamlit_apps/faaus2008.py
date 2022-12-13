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
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

# ------------------------------------------------------------------
# Global constants.
# ------------------------------------------------------------------
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

RADIUS = 1609.347 * 2

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)

ZOOM = 4.4


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
# Setup the controls.
# ------------------------------------------------------------------
choice_data_profile = st.sidebar.checkbox(
    label="**`Show data profile`**",
    value=False,
    help="Pandas profiling of the dataset.",
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

st.sidebar.markdown("""---""")

choice_details = st.sidebar.checkbox(
    label="**`Show details`**",
    value=False,
    help="Tabular representation of the selected detailed data.",
)

st.sidebar.markdown("""---""")

choice_histogram = st.sidebar.checkbox(
    label="**`Show histogram`**", value=False, help="Fatal accidents per year."
)

if choice_histogram:
    width = st.sidebar.slider("Histogram width", 1, 25, 11)
    height = st.sidebar.slider("Histogram height", 1, 25, 5)

st.sidebar.markdown("""---""")

choice_map = st.sidebar.checkbox(
    label="**`Show US map`**",
    value=False,
    help="Display of fatal accident events on a map of the USA.",
)

if choice_map:
    map_style = st.sidebar.radio(
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
    RADIUS = st.sidebar.slider(
        label="Accident radius in meters",
        help="Radius for displaying the fatal accident events - "
        + "default value is 2 miles.",
        min_value=10,
        max_value=1609 * 4,
        value=(1609 * 2),
    )

st.sidebar.markdown("""---""")

choice_filter_data = st.sidebar.checkbox(
    label="**`Filter data ?`**",
    value=True,
    help="Pandas profiling of the dataset.",
)

if choice_filter_data:
    filter_year_from, filter_year_to = st.sidebar.slider(
        label="Select a time frame",
        help="Data available from 2008 to the current year.",
        min_value=2008,
        max_value=datetime.date.today().year,
        value=(2008, datetime.date.today().year),
    )

    filter_acft_categories = st.sidebar.text_input(
        label="Select one or more aircraft categories",
        help="One or more aircraft categories - "
        + "all aircraft categories if no selection has been made.",
    )

    filter_far_parts = st.sidebar.text_input(
        label="Select one or more FAR parts",
        help="One or more FAR parts - "
        + "all FAR parts if no selection has been made.",
    )

    filter_finding_codes = st.sidebar.text_input(
        label="Select one or more finding codes",
        help="One or more finding codes - "
        + "all finding codes if no selection has been made.",
    )

    filter_occurrence_codes = st.sidebar.text_input(
        label="Select one or more occurrence codes",
        help="One or more occurrence codes - "
        + "all occurrence codes if no selection has been made.",
    )

    filter_states = st.sidebar.text_input(
        label="Select one or more states",
        help="One or more USPS abbreviations - "
        + "all U.S. states if no selection has been made.",
    )

    filter_latlong_acq = st.sidebar.selectbox(
        label="Select optionally a latitude and longitude determination method",
        help="`EST`means estimated - `MEAS`means measured using GPS.",
        options=(
            "",
            "EST",
            "MEAS",
        ),
    )

    filter_spin_stall = st.sidebar.checkbox(
        label="Only events with aerodynamic spin stalls?",
        help="Filters only events with `spin_stall` equals `True`.",
    )

    filter_alt_low = st.sidebar.checkbox(
        label="Only events with altitude too low?",
        help="Filters only events with `alt_low` equals `True`.",
    )

    filter_narr_stall = st.sidebar.checkbox(
        label="Only events stalled according to narrative?",
        help="Filters only events with `narr_stall` equals `True`.",
    )

st.sidebar.markdown("""---""")

# ------------------------------------------------------------------
# Read and filter data.
# ------------------------------------------------------------------
pg_conn = _get_postgres_connection()

df_faa = pd.read_sql(QUERY_FAAUS2008, con=_get_engine())

if choice_filter_data:
    # noinspection PyUnboundLocalVariable
    if filter_year_from or filter_year_to:
        df_faa_year = df_faa.loc[
            (df_faa["ev_year"] >= filter_year_from)
            & (df_faa["ev_year"] <= filter_year_to)
        ]
    else:
        df_faa_year = df_faa

    # noinspection PyUnboundLocalVariable
    if filter_acft_categories:
        # noinspection PyUnboundLocalVariable
        df_faa_acft_categories = df_faa_year.loc[
            (
                df_faa_year["acft_category"].isin(
                    filter_acft_categories.upper().split(",")
                )
            )
        ]
    else:
        df_faa_acft_categories = df_faa_year

    # noinspection PyUnboundLocalVariable
    if filter_far_parts:
        # noinspection PyUnboundLocalVariable
        df_faa_far_parts = df_faa_acft_categories.loc[
            (
                df_faa_acft_categories["far_part"].isin(
                    filter_far_parts.upper().split(",")
                )
            )
        ]
    else:
        df_faa_far_parts = df_faa_acft_categories

    # noinspection PyUnboundLocalVariable
    if filter_finding_codes:
        # noinspection PyUnboundLocalVariable
        df_faa_finding_codes = df_faa_far_parts.loc[
            (
                df_faa_far_parts["finding_code"].isin(
                    filter_finding_codes.upper().split(",")
                )
            )
        ]
    else:
        df_faa_finding_codes = df_faa_far_parts

    # noinspection PyUnboundLocalVariable
    if filter_occurrence_codes:
        # noinspection PyUnboundLocalVariable
        df_faa_occurrence_codes = df_faa_finding_codes.loc[
            (
                df_faa_finding_codes["occurrence_code"].isin(
                    filter_occurrence_codes.upper().split(",")
                )
            )
        ]
    else:
        df_faa_occurrence_codes = df_faa_finding_codes

    # noinspection PyUnboundLocalVariable
    if filter_states:
        # noinspection PyUnboundLocalVariable
        df_faa_states = df_faa_occurrence_codes.loc[
            (df_faa_occurrence_codes["state"].isin(filter_states.upper().split(",")))
        ]
    else:
        df_faa_states = df_faa_occurrence_codes

    # noinspection PyUnboundLocalVariable
    if filter_latlong_acq:
        # noinspection PyUnboundLocalVariable
        df_faa_latlong_acq = df_faa_states.loc[
            (df_faa_states["latlong_acq"] == filter_latlong_acq)
        ]
    else:
        df_faa_latlong_acq = df_faa_states

    # noinspection PyUnboundLocalVariable
    if filter_spin_stall:
        # noinspection PyUnboundLocalVariable
        df_faa_spin_stall = df_faa_latlong_acq.loc[
            (df_faa_latlong_acq["spin_stall"] is True)
        ]
    else:
        df_faa_spin_stall = df_faa_latlong_acq

    # noinspection PyUnboundLocalVariable
    if filter_alt_low:
        # noinspection PyUnboundLocalVariable
        df_faa_alt_low = df_faa_spin_stall.loc[(df_faa_spin_stall["alt_low"] is True)]
    else:
        df_faa_alt_low = df_faa_spin_stall

    # noinspection PyUnboundLocalVariable
    if filter_narr_stall:
        # noinspection PyUnboundLocalVariable
        df_faa_narr_stall = df_faa_alt_low.loc[(df_faa_alt_low["narr_stall"] is True)]
    else:
        df_faa_narr_stall = df_faa_alt_low

    df_faa_filtered = df_faa_narr_stall
else:
    df_faa_filtered = df_faa

# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
if choice_data_profile:
    st.subheader("Profiling of the filtered data set")
    # noinspection PyUnboundLocalVariable
    if choice_data_profile_type == "explorative":
        df_faa_states_year_profile = ProfileReport(
            df_faa_filtered,
            explorative=True,
        )
    else:
        df_faa_states_year_profile = ProfileReport(
            df_faa_filtered,
            minimal=True,
        )
    st_profile_report(df_faa_states_year_profile)
    # noinspection PyUnboundLocalVariable
    if choice_data_profile_file:
        if not os.path.isdir(SETTINGS.pandas_profile_dir):
            os.mkdir(SETTINGS.pandas_profile_dir)
        df_faa_states_year_profile.to_file(
            os.path.join(
                SETTINGS.pandas_profile_dir,
                "faaus2008_" + choice_data_profile_type,  # type: ignore
            )
        )


# ------------------------------------------------------------------
# Present details.
# ------------------------------------------------------------------
if choice_details:
    st.subheader("The filtered data set in detail")
    st.dataframe(df_faa_filtered)

# ------------------------------------------------------------------
# Present the yearly fatal accidents.
# ------------------------------------------------------------------
if choice_histogram:
    st.subheader("Number of fatal accidents per year")
    # noinspection PyUnboundLocalVariable
    fig, ax = plt.subplots(figsize=(width, height))
    sns.histplot(df_faa_filtered["ev_year"], discrete=True)
    plt.xlabel("Year")
    st.pyplot(fig)

# ------------------------------------------------------------------
# Present the US map.
# ------------------------------------------------------------------
if choice_map:
    st.subheader("Depicting the fatal accidents on a map of the USA")
    faa_layer = pdk.Layer(
        auto_highlight=True,
        data=df_faa_filtered,
        get_fill_color=[255, 0, 0],
        get_position=["dec_longitude", "dec_latitude"],
        get_radius=RADIUS,
        pickable=True,
        type=LAYER_TYPE,
    )

    # noinspection PyUnboundLocalVariable
    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=_sql_query_us_ll(pg_conn, QUERY_US_LL),
            layers=[faa_layer],
            map_style=MAP_STYLE_PREFIX + map_style,  # type: ignore
            tooltip={
                "html": "<table><tbody>"
                + "<tr><td><b>Event Id</b></td><td>{ev_id}</td></tr>"
                + "<tr><td><b>NTSB No</b></td><td>{ntsb_no}</td></tr>"
                + "<tr><td><b>Latitude</b></td><td>{dec_latitude}</td></tr>"
                + "<tr><td><b>Longitude</b></td><td>{dec_longitude}</td></tr>"
                + "<tr><td><b>Aquired</b></td><td>{latlong_acq}</td></tr>"
                + "</tbody></table>"
            },
        )
    )
