# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Aviation Accidents in the US since 1982."""
import datetime
import time

import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import psycopg2
import pydeck as pdk  # type: ignore
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
APP_ID = "aaus1982"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_CHART_TYPE_ACCIDENTS_YEAR = "Accidents per year"
CHOICE_CHART_TYPE_FATALITIES_YEAR = "Fatalities per year"
CHOICE_CHART_TYPE_FATALITIES_YEAR_FAR_PART = "Fatalities per year & Far part"
CHOICE_CHARTS: bool | None = None
CHOICE_CHARTS_DETAILS: bool | None = None
CHOICE_CHARTS_HEIGHT: float | None = None
CHOICE_CHARTS_WIDTH: float | None = None
CHOICE_CHARTS_TYPES: list[str] = []
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None
CHOICE_FILTER_DATA: bool | None = None
CHOICE_MAP: bool | None = None
CHOICE_MAP_MAP_STYLE: str | None = None
CHOICE_MAP_RADIUS: float | None = 1609.347 * 2

DF_FILTERED: DataFrame = DataFrame()
DF_FILTERED_CHARTS_YEAR: DataFrame = DataFrame()
DF_UNFILTERED: DataFrame = DataFrame()

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_ALT_LOW: bool | None = None
FILTER_FAR_PARTS: list[str] = []
FILTER_FATALITIES_FROM: int | None = None
FILTER_FATALITIES_TO: int | None = None
FILTER_FINDING_CODES: list[str] = []
FILTER_LATLONG_ACQ: str | None = None
FILTER_NARR_STALL: bool | None = None
FILTER_OCCURRENCE_CODES: list[str] = []
FILTER_SPIN_STALL: bool | None = None
FILTER_US_STATES: list[str] = []
FILTER_YEAR_FROM: int | None = None
FILTER_YEAR_TO: int | None = None


# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"

MAP_STYLE_PREFIX = "mapbox://styles/mapbox/"

PG_CONN: Connection | None = None
#  Up/down angle relative to the map�s plane,
#  with 0 being looking directly at the map
PITCH = 30

# ------------------------------------------------------------------
# Query regarding the aircraft accidents in the US since 1982.
# ------------------------------------------------------------------
QUERY_ACFT_CATEGORIES = """
    SELECT string_agg(DISTINCT acft_category, ',' ORDER BY acft_category)
      FROM aircraft
     WHERE acft_category IS NOT NULL
     ORDER BY 1;
"""

QUERY_AAUS1982 = """
    SELECT *
     FROM io_app_aaus1982
    ORDER BY ev_id;
"""

QUERY_FAR_PARTS = """
    SELECT string_agg(DISTINCT far_part, ',' ORDER BY far_part)
      FROM aircraft
    WHERE far_part IS NOT NULL
    ORDER BY 1;
"""

QUERY_FINDING_CODES = """
    SELECT string_agg(DISTINCT finding_code, ',' ORDER BY finding_code)
      FROM (SELECT CASE WHEN substring(finding_code, 1, 8) = '01062012' THEN 'PARAMS_ALT'
                        WHEN substring(finding_code, 1, 8) = '01062037' THEN 'PARAMS_DEC_RATE'
                        WHEN substring(finding_code, 1, 8) = '01062040' THEN 'PARAMS_DEC_APP'
                        WHEN substring(finding_code, 1, 8) = '01062042' THEN 'PARAMS_AoA'
                        WHEN substring(finding_code, 1, 6) = '030210' THEN 'ENV_TER'
                        WHEN substring(finding_code, 1, 6) = '030220' THEN 'ENV_OAS'
                        ELSE finding_code
                    END finding_code
              FROM findings
             WHERE (substring(finding_code, 1, 8) IN ('01062012', '01062037', '01062040', '01062042')
                OR substring(finding_code, 1, 6) IN ('030210', '030220'))
               AND finding_code IS NOT NULL) f
"""  # noqa: E501

QUERY_MAX_FATALITIES = """
    SELECT MAX(fatalities)
      FROM io_app_aaus1982;
"""

QUERY_OCCURRENCE_CODES = """
    SELECT string_agg(DISTINCT occurrence_code, ',' ORDER BY occurrence_code)
      FROM (SELECT CASE WHEN substring(occurrence_code, 1, 3) = '350' THEN 'INIT_CLIMB'
                        WHEN substring(occurrence_code, 1, 3) = '452' THEN 'MAN_LALT'
                        WHEN substring(occurrence_code, 1, 3) = '502' THEN 'FINAL_APP'
                        WHEN substring(occurrence_code, 4, 6) = '120' THEN 'CFIT'
                        WHEN substring(occurrence_code, 4, 6) = '220' THEN 'LALT'
                        WHEN substring(occurrence_code, 4, 6) = '240' THEN 'LOC-I'
                        WHEN substring(occurrence_code, 4, 6) = '241' THEN 'STALL'
                        WHEN substring(occurrence_code, 4, 6) = '250' THEN 'MIDAIR'
                        WHEN substring(occurrence_code, 4, 6) = '401' THEN 'UIMC'
                        WHEN substring(occurrence_code, 4, 6) = '420' THEN 'CAA'
                        WHEN substring(occurrence_code, 4, 6) = '901' THEN 'BIRD'
                        ELSE occurrence_code
                   END
              FROM events_sequence
             WHERE (substring(occurrence_code, 1, 3) IN ('350', '452', '502')
                OR substring(occurrence_code, 4, 6) IN ('120', '220', '240', '241', '250', '401', '420', '901'))
               AND occurrence_code IS NOT NULL) o
"""  # noqa: E501

QUERY_US_LL = """
    SELECT dec_latitude,
           dec_longitude
      FROM io_countries
     WHERE country = 'USA';
"""

QUERY_US_STATES = """
    SELECT string_agg(DISTINCT state, ',' ORDER BY state)
      FROM io_states
     WHERE country  = 'USA'
     ORDER BY 1;
"""

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)

# Magnification level of the map, usually between
# 0 (representing the whole world) and
# 24 (close to individual buildings)
ZOOM = 4.4


# ------------------------------------------------------------------
# Filter the data frame.
# ------------------------------------------------------------------
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
@st.experimental_memo
def _apply_filter_controls(
    df_unfiltered: DataFrame,
    filter_acft_categories: list | None,
    filter_alt_low: bool | None,
    filter_fatalities_from: int | None,
    filter_fatalities_to: int | None,
    filter_far_parts: list | None,
    filter_finding_codes: list | None,
    filter_latlong_acq: str | None,
    filter_narr_stall: bool | None,
    filter_occurrence_codes: list | None,
    filter_spin_stall: bool | None,
    filter_us_states: list | None,
    filter_year_from: int | None,
    filter_year_to: int | None,
) -> DataFrame:
    """Filter the data frame."""
    df_filtered = df_unfiltered

    # noinspection PyUnboundLocalVariable
    if filter_year_from or filter_year_to:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= FILTER_YEAR_FROM)
            & (df_filtered["ev_year"] <= FILTER_YEAR_TO)
        ]

    # noinspection PyUnboundLocalVariable
    if filter_fatalities_from or filter_fatalities_to:
        df_filtered = df_filtered.loc[
            (df_filtered["fatalities"] >= filter_fatalities_from)
            & (df_filtered["fatalities"] <= filter_fatalities_to)
        ]

    # noinspection PyUnboundLocalVariable
    if filter_acft_categories:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["acft_category"].apply(
                lambda x: bool(set(x) & set(filter_acft_categories))  # type: ignore
            )
        ]

    # noinspection PyUnboundLocalVariable
    if filter_far_parts:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["far_part"].apply(
                lambda x: bool(set(x) & set(filter_far_parts))  # type: ignore
            )
        ]

    # noinspection PyUnboundLocalVariable
    if filter_finding_codes:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["finding_code"].apply(
                lambda x: bool(set(x) & set(filter_finding_codes))  # type: ignore
            )
        ]

    # noinspection PyUnboundLocalVariable
    if filter_occurrence_codes:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["occurrence_code"].apply(
                lambda x: bool(set(x) & set(filter_occurrence_codes))  # type: ignore
            )
        ]

    # noinspection PyUnboundLocalVariable
    if filter_us_states:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[(df_filtered["state"].isin(filter_us_states))]

    # noinspection PyUnboundLocalVariable
    if filter_latlong_acq:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["latlong_acq"] == filter_latlong_acq)
        ]

    # noinspection PyUnboundLocalVariable
    if filter_spin_stall:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["spin_stall"] == True)  # noqa: E712
        ]

    # noinspection PyUnboundLocalVariable
    if filter_alt_low:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["alt_low"] == True)  # noqa: E712
        ]

    # noinspection PyUnboundLocalVariable
    if filter_narr_stall:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["narr_stall"] == True)  # noqa: E712
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
def _get_data() -> DataFrame:
    """Read the data.

    Returns:
        DataFrame: The unfiltered dataframe.
    """
    global PG_CONN  # pylint: disable=global-statement

    PG_CONN = _get_postgres_connection()  # type: ignore

    return pd.read_sql(QUERY_AAUS1982, con=_get_engine())


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
# Prepare the yearly chart data.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_chart_data_year(
    df_filtered: DataFrame,
) -> DataFrame:
    """Prepare the yearly chart data."""
    df_chart = df_filtered[
        [
            "ev_year",
            "fatalities",
            "far_part_091x_fatalities",
            "far_part_121_fatalities",
            "far_part_135_fatalities",
        ]
    ]

    df_chart.loc[:, "accidents"] = 1

    return df_chart.groupby("ev_year", as_index=False).sum(
        [  # type: ignore
            "fatalities",
            "far_part_091x_fatalities",
            "far_part_121_fatalities",
            "far_part_135_fatalities",
        ],
    )


# ------------------------------------------------------------------
# Present the chart accidents per year.
# ------------------------------------------------------------------
def _present_chart_accidents_year():
    """Present the chart accidents per year."""
    st.subheader("Number of accidents per year")

    fig = px.bar(
        DF_FILTERED_CHARTS_YEAR,
        labels={"ev_year": "Year", "accidents": "Accidents"},
        x="ev_year",
        y="accidents",
    )

    fig.update_layout(bargap=0, height=CHOICE_CHARTS_HEIGHT, width=CHOICE_CHARTS_WIDTH)

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the chart fatalities per year.
# ------------------------------------------------------------------
def _present_chart_fatalities_year():
    """Present the chart accidents per year."""
    st.subheader("Number of fatalities per year")

    fig = px.bar(
        DF_FILTERED_CHARTS_YEAR,
        labels={"ev_year": "Year", "fatalities": "Fatalities"},
        x="ev_year",
        y="fatalities",
    )

    fig.update_layout(
        bargap=0,
    )

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the chart fatalities per year -
# only with selected FAR parts involved.
# ------------------------------------------------------------------
def _present_chart_fatalities_year_far_part():
    """Present the chart fatalities per year - only with selected FAR parts involved."""
    st.subheader(
        "Number of fatalities per year - only with selected FAR parts involved"
    )

    fig = go.Figure(
        data=[
            go.Bar(
                marker={"color": "#636EFA"},
                name="Parts 91, 91F, 91K",
                x=DF_FILTERED_CHARTS_YEAR["ev_year"],
                y=DF_FILTERED_CHARTS_YEAR["far_part_091x_fatalities"],
            ),
            go.Bar(
                marker={"color": "#00CC96"},
                name="Part 135",
                x=DF_FILTERED_CHARTS_YEAR["ev_year"],
                y=DF_FILTERED_CHARTS_YEAR["far_part_135_fatalities"],
            ),
            go.Bar(
                marker={"color": "#EF553B"},
                name="Part 121",
                x=DF_FILTERED_CHARTS_YEAR["ev_year"],
                y=DF_FILTERED_CHARTS_YEAR["far_part_121_fatalities"],
            ),
        ],
    )

    fig.update_layout(
        bargap=0,
        barmode="stack",
    )

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the charts.
# ------------------------------------------------------------------
def _present_charts():
    """Present the charts."""
    global DF_FILTERED_CHARTS_YEAR  # pylint: disable=global-statement

    if CHOICE_CHART_TYPE_ACCIDENTS_YEAR in CHOICE_CHARTS_TYPES:
        DF_FILTERED_CHARTS_YEAR = _prep_chart_data_year(DF_FILTERED)
        _present_chart_accidents_year()

    if CHOICE_CHART_TYPE_FATALITIES_YEAR in CHOICE_CHARTS_TYPES:
        DF_FILTERED_CHARTS_YEAR = _prep_chart_data_year(DF_FILTERED)
        _present_chart_fatalities_year()

    if CHOICE_CHART_TYPE_FATALITIES_YEAR_FAR_PART in CHOICE_CHARTS_TYPES:
        DF_FILTERED_CHARTS_YEAR = _prep_chart_data_year(DF_FILTERED)
        _present_chart_fatalities_year_far_part()


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data():
    """Present the filtered data."""
    if CHOICE_CHARTS:
        _present_charts()

    if CHOICE_DATA_PROFILE:
        st.subheader("Profiling of the filtered data set")
        _present_data_profile()

    if CHOICE_DETAILS or CHOICE_CHARTS_DETAILS:
        _present_details()

    if CHOICE_MAP:
        st.subheader("Depicting the accidents on a map of the USA")
        _present_map()


# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
def _present_data_profile():
    """Present data profile."""
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
# Present details.
# ------------------------------------------------------------------
def _present_details():
    """Present details."""
    if CHOICE_DETAILS:
        st.subheader("Detailed data from database view **`io_app_aaus1982`**")
        st.dataframe(DF_FILTERED)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED),
            file_name=APP_ID + ".csv",
            help="The download includes all data "
            + "after applying the filter options.",
            label="Download the detailed data",
            mime="text/csv",
        )

    if CHOICE_CHARTS_DETAILS:
        if (
            CHOICE_CHART_TYPE_ACCIDENTS_YEAR
            or CHOICE_CHART_TYPE_FATALITIES_YEAR
            or CHOICE_CHART_TYPE_FATALITIES_YEAR_FAR_PART
        ):
            st.subheader("Aggregated chart data per year")
            st.dataframe(DF_FILTERED_CHARTS_YEAR)
            st.download_button(
                data=_convert_df_2_csv(DF_FILTERED_CHARTS_YEAR),
                file_name=APP_ID + "_charts_year.csv",
                help="The download includes the aggregated chart data per year.",
                label="Download the chart data",
                mime="text/csv",
            )


# ------------------------------------------------------------------
# Present the accidents on the US map.
# ------------------------------------------------------------------
def _present_map():
    """Present the accidents on the US map."""
    global DF_FILTERED  # pylint: disable=global-statement

    # noinspection PyUnboundLocalVariable
    DF_FILTERED = DF_FILTERED.loc[
        (DF_FILTERED["dec_latitude"].notna() & DF_FILTERED["dec_longitude"].notna())
    ]

    faa_layer = pdk.Layer(
        auto_highlight=True,
        data=DF_FILTERED,
        get_fill_color=[255, 0, 0],
        get_position=["dec_longitude", "dec_latitude"],
        get_radius=CHOICE_MAP_RADIUS,
        pickable=True,
        type=LAYER_TYPE,
    )

    # noinspection PyUnboundLocalVariable
    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=_sql_query_us_ll(PITCH, ZOOM),
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
# Set up the filter controls.
# ------------------------------------------------------------------
def _setup_filter_controls():
    """Set up the filter controls."""
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_ALT_LOW  # pylint: disable=global-statement
    global FILTER_FAR_PARTS  # pylint: disable=global-statement
    global FILTER_FATALITIES_FROM  # pylint: disable=global-statement
    global FILTER_FATALITIES_TO  # pylint: disable=global-statement
    global FILTER_FINDING_CODES  # pylint: disable=global-statement
    global FILTER_LATLONG_ACQ  # pylint: disable=global-statement
    global FILTER_NARR_STALL  # pylint: disable=global-statement
    global FILTER_OCCURRENCE_CODES  # pylint: disable=global-statement
    global FILTER_SPIN_STALL  # pylint: disable=global-statement
    global FILTER_US_STATES  # pylint: disable=global-statement
    global FILTER_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_YEAR_TO  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement

    PG_CONN = _get_postgres_connection()

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="Special filter options required.",
        label="**`Filter data ?`**",
        value=True,
    )

    if CHOICE_FILTER_DATA:
        FILTER_YEAR_FROM, FILTER_YEAR_TO = st.sidebar.slider(
            label="Select a time frame",
            help="Filter over year from to.",
            min_value=1982,
            max_value=datetime.date.today().year,
            value=(2008, datetime.date.today().year - 1),
        )

        FILTER_ACFT_CATEGORIES = st.sidebar.multiselect(
            help="Filtering via selected aircraft categories.",
            label="Select one or more aircraft categories",
            options=_sql_query_acft_categories(),
        )

        FILTER_FAR_PARTS = st.sidebar.multiselect(
            help="Filtering via selected FAR parts.",
            label="Select one or more FAR parts",
            options=_sql_query_far_parts(),
        )

        max_fatalities = _sql_query_max_fatalities()

        FILTER_FATALITIES_FROM, FILTER_FATALITIES_TO = st.sidebar.slider(
            label="Filtering over an interval of number of fatalities.",
            min_value=0,
            max_value=max_fatalities,
            value=(1, max_fatalities),
        )

        FILTER_FINDING_CODES = st.sidebar.multiselect(
            help="Filtering via selected finding codes.",
            label="Select one or more finding codes",
            options=_sql_query_finding_codes(),
        )

        FILTER_OCCURRENCE_CODES = st.sidebar.multiselect(
            help="Filtering via selected occurrence codes.",
            label="Select one or more occurrence codes",
            options=_sql_query_occurrence_codes(),
        )

        FILTER_US_STATES = st.sidebar.multiselect(
            help="Filtering via selected occurrence USPS abbreviations.",
            label="Select one or more states",
            options=_sql_query_us_states(),
        )

        FILTER_LATLONG_ACQ = st.sidebar.selectbox(
            help="Filtering via a specific latitude and longitude "
            + "determination method.",
            label="Select optionally a latitude and longitude determination method",
            options=(
                "",
                "EST",
                "MEAS",
            ),
        )

        FILTER_SPIN_STALL = st.sidebar.checkbox(
            help="Filtering only events with `spin_stall` equals `True`.",
            label="Only events with aerodynamic spin stalls?",
        )

        FILTER_ALT_LOW = st.sidebar.checkbox(
            help="Filtering only events with `alt_low` equals `True`.",
            label="Only events with altitude too low?",
        )

        FILTER_NARR_STALL = st.sidebar.checkbox(
            help="Filtering only events with `narr_stall` equals `True`.",
            label="Only events stalled according to narrative?",
        )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page():
    """Set up the page."""
    st.set_page_config(layout="wide")
    st.header("Aviation Accidents in the US since 1982")


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
    global CHOICE_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPES  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_CHARTS  # pylint: disable=global-statement
    global CHOICE_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_CHARTS_WIDTH  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_MAP_RADIUS  # pylint: disable=global-statement

    CHOICE_CHARTS = st.sidebar.checkbox(
        help="Accidents or fatalities per year (after filtering the data).",
        label="**`Show charts`**",
        value=False,
    )

    if CHOICE_CHARTS:
        CHOICE_CHARTS_TYPES = st.sidebar.multiselect(
            default=CHOICE_CHART_TYPE_FATALITIES_YEAR_FAR_PART,
            label="Select one or more chart types",
            options=(
                CHOICE_CHART_TYPE_ACCIDENTS_YEAR,
                CHOICE_CHART_TYPE_FATALITIES_YEAR,
                CHOICE_CHART_TYPE_FATALITIES_YEAR_FAR_PART,
            ),
        )

        CHOICE_CHARTS_HEIGHT = st.sidebar.slider(
            label="Chart height", min_value=100, max_value=1000, value=250
        )
        CHOICE_CHARTS_WIDTH = st.sidebar.slider(
            label="Chart width", min_value=100, max_value=1000, value=250
        )

        CHOICE_CHARTS_DETAILS = st.sidebar.checkbox(
            help="Tabular representation of the of the data underlying the charts.",
            label="**`Show detailed chart data`**",
            value=False,
        )

    st.sidebar.markdown("""---""")

    CHOICE_DATA_PROFILE = st.sidebar.checkbox(
        help="Pandas profiling of the filtered dataset.",
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

    st.sidebar.markdown("""---""")

    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed data.",
        label="**`Show detailed data`**",
        value=False,
    )

    st.sidebar.markdown("""---""")

    CHOICE_MAP = st.sidebar.checkbox(
        help="Display of accident events on a map of the USA "
        + "(after filtering the data).",
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
            help="Radius for displaying the accident events - "
            + "default value is 2 miles.",
            min_value=10,
            max_value=1609 * 4,
            value=(1609 * 2),
        )

    st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Execute a query that returns the list of aircraft categories.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_acft_categories() -> list[str]:
    """Execute a query that returns a list of aircraft categories.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_ACFT_CATEGORIES)
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Determine the maximum number of fatalities.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_max_fatalities() -> int:
    """Determine the maximum number of fatalities.

    Returns:
        int: Maximum number of fatalities.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_MAX_FATALITIES)
        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of FAR parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_far_parts() -> list[str]:
    """Execute a query that returns a list of FAR part.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_FAR_PARTS)
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of finding codes.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_finding_codes() -> list[str]:
    """Execute a query that returns a list of finding codes.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_FINDING_CODES)
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of occurrence codes.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_occurrence_codes() -> list[str]:
    """Execute a query that returns a list of occurrence codes.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_OCCURRENCE_CODES)
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Run the US latitude and longitude query.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_us_ll(pitch: int, zoom: float) -> pdk.ViewState:
    """Run the US latitude and longitude query.

    Args:
        pitch (int): Up/down angle relative to the map�s plane.
        zoom (float): Magnification level of the map.

    Returns:
        pdk.ViewState: Screen focus.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_US_LL)
        result = cur.fetchone()
        return pdk.ViewState(
            latitude=result[0],  # type: ignore
            longitude=result[1],  # type: ignore
            pitch=pitch,
            zoom=zoom,
        )


# ------------------------------------------------------------------
# Execute a query that returns the list of US states.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_us_states() -> list[str]:
    """Execute a query that returns a list of US states.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(QUERY_US_STATES)
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
# Start time measurement.
start_time = time.time_ns()

_setup_page()

_setup_sidebar()

DF_UNFILTERED = _get_data()

DF_FILTERED = DF_UNFILTERED

if CHOICE_FILTER_DATA:
    DF_FILTERED = _apply_filter_controls(
        DF_UNFILTERED,
        FILTER_ACFT_CATEGORIES,
        FILTER_ALT_LOW,
        FILTER_FATALITIES_FROM,
        FILTER_FATALITIES_TO,
        FILTER_FAR_PARTS,
        FILTER_FINDING_CODES,
        FILTER_LATLONG_ACQ,
        FILTER_NARR_STALL,
        FILTER_OCCURRENCE_CODES,
        FILTER_SPIN_STALL,
        FILTER_US_STATES,
        FILTER_YEAR_FROM,
        FILTER_YEAR_TO,
    )

_present_data()

# Stop time measurement.
print(
    str(datetime.datetime.now())
    + f" {f'{time.time_ns() - start_time:,}':>20} ns - Total runtime for application "
    + APP_ID,
    flush=True,
)
