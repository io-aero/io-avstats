# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Fatal Aviation Accidents in the US since 2008."""
import datetime

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

MAP_STYLE = "mapbox://styles/mapbox/light-v9"

PITCH = 30

# ------------------------------------------------------------------
# Query regarding the aircraft fatalities in the US since 2008.
# ------------------------------------------------------------------
QUERY_FAAUS2008 = """
    SELECT ev_year,
           inj_tot_f fatalities,
           COALESCE(io_state, ev_state) state,
           COALESCE(io_city, ev_city) city,
           COALESCE(io_site_zipcode, ev_site_zipcode) zip,
           COALESCE(io_dec_latitude, dec_latitude) dec_latitude,
           COALESCE(io_dec_longitude, dec_longitude) dec_longitude,
           ev_id event_id,
           ntsb_no
     FROM io_fatalities_us_2008
    WHERE COALESCE(io_dec_latitude, dec_latitude) IS NOT NULL
      AND COALESCE(io_dec_longitude, dec_longitude) IS NOT NULL
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
choice_filter_data = st.sidebar.checkbox(
    label="**`Filter data ?`**",
    value=False,
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

    filter_states = st.sidebar.text_input(
        label="Select one or more states",
        help="One or more USPS abbreviations - "
        + "all U.S. states if no selection has been made.",
    )

choice_data_profile = st.sidebar.checkbox(
    label="**`Show data profile`**",
    value=False,
    help="Pandas profiling of the dataset.",
)

choice_details = st.sidebar.checkbox(
    label="**`Show details`**",
    value=False,
    help="Tabular representation of the selected detailed data.",
)

choice_histogram = st.sidebar.checkbox(
    label="**`Show histogram`**", value=False, help="Fatal accidents per year."
)

if choice_histogram:
    width = st.sidebar.slider("Histogram width", 1, 25, 11)
    height = st.sidebar.slider("Histogram height", 1, 25, 5)

choice_map = st.sidebar.checkbox(
    label="**`Show US map`**",
    value=False,
    help="Display of fatal accident events on a map of the USA.",
)

if choice_map:
    RADIUS = st.sidebar.number_input(
        label="Accident radius in meters",
        value=RADIUS,
        help="Radius for displaying the fatal accident events - "
        + "default value is 2 miles.",
    )

# ------------------------------------------------------------------
# Read and filter data.
# ------------------------------------------------------------------
pg_conn = _get_postgres_connection()

df_faa = pd.read_sql(QUERY_FAAUS2008, con=_get_engine())

if choice_filter_data:
    # noinspection PyUnboundLocalVariable
    if filter_states:
        # noinspection PyUnboundLocalVariable
        df_faa_states = df_faa.loc[
            (df_faa["state"].isin(filter_states.upper().split(",")))
        ]
    else:
        df_faa_states = df_faa

    # noinspection PyUnboundLocalVariable
    if filter_year_from or filter_year_to:
        df_faa_states_year = df_faa_states.loc[
            (df_faa["ev_year"] >= filter_year_from)
            & (df_faa["ev_year"] <= filter_year_to)
        ]
    else:
        df_faa_states_year = df_faa_states
else:
    df_faa_states_year = df_faa

# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
if choice_data_profile:
    st.subheader("Profiling of the filtered data set")
    df_faa_states_year_profile = ProfileReport(
        df_faa_states_year,
        # correlations={
        #     "auto": {"calculate": True},
        #     "cramers": {"calculate": True},
        #     "kendall": {"calculate": True},
        #     "pearson": {"calculate": True},
        #     "phi_k": {"calculate": True},
        #     "recoded": {"calculate": False},
        #     "spearman": {"calculate": False},
        # },
        explorative=True,
        # minimal=True,
    )
    st_profile_report(df_faa_states_year_profile)


# ------------------------------------------------------------------
# Present details.
# ------------------------------------------------------------------
if choice_details:
    st.subheader("The filtered data set in detail")
    st.dataframe(df_faa_states_year)

# ------------------------------------------------------------------
# Present the yearly fatal accidents.
# ------------------------------------------------------------------
if choice_histogram:
    st.subheader("Number of fatal accidents per year")
    # noinspection PyUnboundLocalVariable
    fig, ax = plt.subplots(figsize=(width, height))
    sns.histplot(df_faa_states_year["ev_year"], discrete=True)
    plt.xlabel("Year")
    st.pyplot(fig)

# ------------------------------------------------------------------
# Present the US map.
# ------------------------------------------------------------------
if choice_map:
    st.subheader("Depicting the fatal accidents on a map of the USA")
    faa_layer = pdk.Layer(
        type=LAYER_TYPE,
        auto_highlight=True,
        data=df_faa_states_year,
        get_fill_color=[255, 0, 0],
        get_position=["dec_longitude", "dec_latitude"],
        get_radius=RADIUS,
        pickable=True,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style=MAP_STYLE,
            initial_view_state=_sql_query_us_ll(pg_conn, QUERY_US_LL),
            layers=[faa_layer],
        )
    )
