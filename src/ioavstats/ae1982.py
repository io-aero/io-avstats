# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Aviation Events in the US since 1982."""
import ast
import datetime
import time

import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import psycopg2
import pydeck as pdk  # type: ignore
import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

pd.options.mode.chained_assignment: str | None = None  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "ae1982"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_ABOUT: bool | None = None
CHOICE_CHARTS: bool | None = None
CHOICE_CHARTS_DETAILS: bool | None = None
CHOICE_CHARTS_HEIGHT: float | None = None
CHOICE_CHARTS_TYPE_EYIL: bool | None = None
CHOICE_CHARTS_TYPE_EYT: bool | None = None
CHOICE_CHARTS_TYPE_FYFP: bool | None = None
CHOICE_CHARTS_TYPE_TEIL: bool | None = None
CHOICE_CHARTS_TYPE_TET: bool | None = None
CHOICE_CHARTS_TYPE_TFFP: bool | None = None
CHOICE_CHARTS_WIDTH: float | None = None
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None
CHOICE_FILTER_CONDITIONS: bool | None = None
CHOICE_FILTER_CONDITIONS_TEXT: str = ""
CHOICE_FILTER_DATA: bool | None = None
CHOICE_MAP: bool | None = None
CHOICE_MAP_MAP_STYLE: str | None = None
CHOICE_MAP_RADIUS: float | None = 1609.347 * 2

COLOR_LEVEL_1 = "#15535f"  # peacock
COLOR_LEVEL_2 = "#47a3b5"  # aqua
COLOR_LEVEL_3 = "#fadc82"  # yellow
COLOR_LEVEL_4 = "#f1a638"  # orange

COUNTRY_USA = "USA"

DF_FILTERED: DataFrame = DataFrame()
DF_FILTERED_CHARTS_EYIL: DataFrame = DataFrame()
DF_FILTERED_CHARTS_EYT: DataFrame = DataFrame()
DF_FILTERED_CHARTS_FYFP: DataFrame = DataFrame()
DF_FILTERED_CHARTS_TEIL: list[int] = []
DF_FILTERED_CHARTS_TET: list[int] = []
DF_FILTERED_CHARTS_TFFP: list[int] = []
DF_UNFILTERED: DataFrame = DataFrame()

EVENT_TYPE_DESC: str

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_EV_HIGHEST_INJURY: list[str] = []
FILTER_EV_TYPE: list[str] = []
FILTER_EV_YEAR_FROM: int | None = None
FILTER_EV_YEAR_TO: int | None = None
FILTER_FAR_PARTS: list[str] = []
FILTER_FINDING_CODES: list[str] = []
FILTER_INJ_F_GRND_FROM: int | None = None
FILTER_INJ_F_GRND_TO: int | None = None
FILTER_INJ_TOT_F_FROM: int | None = None
FILTER_INJ_TOT_F_TO: int | None = None
FILTER_IS_ALTITUDE_LOW: bool | None = None
FILTER_IS_DEST_COUNTRY_USA: bool | None = None
FILTER_IS_DPRT_COUNTRY_USA: bool | None = None
FILTER_IS_NARRATIVE_STALL: bool | None = None
FILTER_IS_SPIN_STALL: bool | None = None
FILTER_LATLONG_ACQ: list[str] = []
FILTER_OCCURRENCE_CODES: list[str] = []
FILTER_STATE: list[str] = []
FILTER_US_AVIATION: list[str] = []
FILTER_US_AVIATION_COUNTRY = "Event Country USA"
FILTER_US_AVIATION_DEPARTURE = "US Departure"
FILTER_US_AVIATION_DESTINATION = "US Destination"
FILTER_US_AVIATION_OPERATOR = "US Operator"
FILTER_US_AVIATION_OWNER = "US Owner"
FILTER_US_AVIATION_REGISTRATION = "US Registration"

IS_TIMEKEEPING = False

LAST_READING: int = 0
# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"

MAP_STYLE_PREFIX = "mapbox://styles/mapbox/"

PG_CONN: connection | None = None
#  Up/down angle relative to the maps plane,
#  with 0 being looking directly at the map
PITCH = 30

# ------------------------------------------------------------------
# Configuration parameters.
# ------------------------------------------------------------------
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
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# @st.experimental_memo
def _apply_filter(
    df_unfiltered: DataFrame,
    filter_acft_categories: list | None,
    filter_ev_highest_injury: list | None,
    filter_ev_type: list | None,
    filter_ev_year_from: int | None,
    filter_ev_year_to: int | None,
    filter_far_parts: list | None,
    filter_finding_codes: list | None,
    filter_inj_f_grnd_from: int | None,
    filter_inj_f_grnd_to: int | None,
    filter_inj_tot_f_from: int | None,
    filter_inj_tot_f_to: int | None,
    filter_is_altitude_low: bool | None,
    filter_is_dest_country_usa: bool | None,
    filter_is_dprt_country_usa: bool | None,
    filter_is_narrative_stall: bool | None,
    filter_is_spin_stall: bool | None,
    filter_latlong_acq: list | None,
    filter_occurrence_codes: list | None,
    filter_state: list | None,
    filter_us_aviation: list | None,
) -> DataFrame:
    """Filter the data frame."""
    _print_timestamp("_apply_filter() - Start")

    df_filtered = df_unfiltered

    # noinspection PyUnboundLocalVariable
    if filter_acft_categories:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["acft_categories"].apply(
                lambda x: bool(set(x) & set(filter_acft_categories))  # type: ignore
            )
        ]
        _print_timestamp("_apply_filter() - filter_acft_categories")

    # noinspection PyUnboundLocalVariable
    if filter_is_altitude_low:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["is_altitude_low"] == True)  # noqa: E712
        ]
        _print_timestamp("_apply_filter() - filter_is_altitude_low")

    # noinspection PyUnboundLocalVariable
    if filter_is_dest_country_usa:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["is_dest_country_usa"] == True)  # noqa: E712
        ]
        _print_timestamp("_apply_filter() - filter_is_dest_country_usa")

    # noinspection PyUnboundLocalVariable
    if filter_is_dprt_country_usa:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["is_dprt_country_usa"] == True)  # noqa: E712
        ]
        _print_timestamp("_apply_filter() - filter_is_dprt_country_usa")

    # noinspection PyUnboundLocalVariable
    if filter_ev_highest_injury:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["ev_highest_injury"].isin(filter_ev_highest_injury))
        ]
        _print_timestamp("_apply_filter() - filter_ev_highest_injury")

    # noinspection PyUnboundLocalVariable
    if filter_ev_type:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[(df_filtered["ev_type"].isin(filter_ev_type))]
        _print_timestamp("_apply_filter() - filter_ev_type")

    # noinspection PyUnboundLocalVariable
    if filter_ev_year_from or filter_ev_year_to:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= FILTER_EV_YEAR_FROM)
            & (df_filtered["ev_year"] <= FILTER_EV_YEAR_TO)
        ]
        _print_timestamp("_apply_filter() - filter_ev_year_from")

    # noinspection PyUnboundLocalVariable
    if filter_far_parts:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["far_parts"].apply(
                lambda x: bool(set(x) & set(filter_far_parts))  # type: ignore
            )
        ]
        _print_timestamp("_apply_filter() - filter_far_parts")

    # noinspection PyUnboundLocalVariable
    if filter_finding_codes:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["finding_codes"].apply(
                lambda x: bool(set(x) & set(filter_finding_codes))  # type: ignore
            )
        ]
        _print_timestamp("_apply_filter() - filter_finding_codes")

    # noinspection PyUnboundLocalVariable
    if filter_inj_f_grnd_from or filter_inj_f_grnd_to:
        df_filtered = df_filtered.loc[
            (df_filtered["inj_f_grnd"] >= filter_inj_f_grnd_from)
            & (df_filtered["inj_f_grnd"] <= filter_inj_f_grnd_to)
        ]
        _print_timestamp("_apply_filter() - filter_inj_f_grnd_from")

    # noinspection PyUnboundLocalVariable
    if filter_inj_tot_f_from or filter_inj_tot_f_to:
        df_filtered = df_filtered.loc[
            (df_filtered["inj_tot_f"] >= filter_inj_tot_f_from)
            & (df_filtered["inj_tot_f"] <= filter_inj_tot_f_to)
        ]
        _print_timestamp("_apply_filter() - filter_inj_tot_f_from")

    # noinspection PyUnboundLocalVariable
    if filter_latlong_acq:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["latlong_acq"].isin(filter_latlong_acq))
        ]
        _print_timestamp("_apply_filter() - filter_latlong_acq")

    # noinspection PyUnboundLocalVariable
    if filter_is_narrative_stall:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["is_narrative_stall"] == True)  # noqa: E712
        ]
        _print_timestamp("_apply_filter() - filter_is_narrative_stall")

    # noinspection PyUnboundLocalVariable
    if filter_occurrence_codes:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["occurrence_codes"].apply(
                lambda x: bool(set(x) & set(filter_occurrence_codes))  # type: ignore
            )
        ]
        _print_timestamp("_apply_filter() - filter_occurrence_codes")

    # noinspection PyUnboundLocalVariable
    if filter_is_spin_stall:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            # pylint: disable=singleton-comparison
            (df_filtered["is_spin_stall"] == True)  # noqa: E712
        ]
        _print_timestamp("_apply_filter() - filter_is_spin_stall")

    # noinspection PyUnboundLocalVariable
    if filter_state:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[(df_filtered["state"].isin(filter_state))]
        _print_timestamp("_apply_filter() - filter_state")

    # noinspection PyUnboundLocalVariable
    if filter_us_aviation:
        df_filtered = _apply_filter_us_aviation(df_filtered, filter_us_aviation)

    _print_timestamp("_apply_filter() - End")

    return df_filtered


# ------------------------------------------------------------------
# Filter the data frame - US aviation.
# ------------------------------------------------------------------
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# @st.experimental_memo
def _apply_filter_us_aviation(
    df_unfiltered: DataFrame,  # pylint: disable=unused-argument
    filter_us_aviation: list | None,
) -> DataFrame:
    """Filter the data frame - US aviation."""
    _print_timestamp("_apply_filter_us_aviation() - Start")

    filter_cmd = "df_unfiltered.loc["
    filter_cmd_or = ""

    if FILTER_US_AVIATION_COUNTRY in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['country'] == COUNTRY_USA)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_DESTINATION in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['is_dest_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_DEPARTURE in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['is_dprt_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_OPERATOR in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['is_oper_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_OWNER in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['is_owner_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_REGISTRATION in filter_us_aviation:  # type: ignore
        filter_cmd += filter_cmd_or + "(df_unfiltered['is_regis_country_usa'] == True)"

    filter_cmd += "]"

    df_filtered = eval(filter_cmd)

    _print_timestamp("_apply_filter_us_aviation() - End")

    return df_filtered


# ------------------------------------------------------------------
# Convert a dataframe to csv data.
# ------------------------------------------------------------------
@st.experimental_memo
def _convert_df_2_csv(dataframe: DataFrame) -> bytes:
    """Convert a dataframe to csv data.

    Args:
        dataframe (DataFrame): The dataframe.

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
    _print_timestamp("_get_data() - Start")

    return pd.read_sql(
        """
    SELECT *
     FROM io_app_ae1982
    ORDER BY ev_id;
    """,
        con=_get_engine(),
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
@st.experimental_singleton
def _get_postgres_connection() -> connection:
    """Create a PostgreSQL connection.

    Returns:
        connection: Database connection.
    """
    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Injury Level.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_eyil(
    df_filtered: DataFrame,
) -> DataFrame:
    """Prepare the chart data: Events per Year by Injury Level."""
    df_chart = df_filtered[
        [
            "ev_year",
            "ev_highest_injury",
            "ev_counter",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
            "ev_counter": "events",
        },
        inplace=True,
    )

    df_chart["fatal"] = np.where(df_chart.ev_highest_injury == "FATL", 1, 0)
    df_chart["minor"] = np.where(df_chart.ev_highest_injury == "MINR", 1, 0)
    df_chart["none"] = np.where(df_chart.ev_highest_injury == "NONE", 1, 0)
    df_chart["serious"] = np.where(df_chart.ev_highest_injury == "SERS", 1, 0)

    return df_chart.groupby("year", as_index=False).sum(
        [  # type: ignore
            "fatal",
            "minor",
            "none",
            "serious",
        ],
    )


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Type.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_eyt(
    df_filtered: DataFrame,
) -> DataFrame:
    """Prepare the chart data: Events per Year by Type."""
    df_chart = df_filtered[
        [
            "ev_year",
            "ev_type",
            "ev_counter",
        ]
    ]

    df_chart.loc["ev_year", "ev_counter"] = df_chart.rename(
        columns={
            "ev_year": "year",
            "ev_counter": "events",
        },
        inplace=True,
    )

    df_chart["accidents"] = np.where(df_chart.ev_type == "ACC", 1, 0)
    df_chart["incidents"] = np.where(df_chart.ev_type == "INC", 1, 0)

    return df_chart.groupby("year", as_index=False).sum(
        [  # type: ignore
            "accidents",
            "incidents",
        ],
    )


# ------------------------------------------------------------------
# Prepare the chart data: Fatalities per Year under FAR Operations Parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_fyfp(
    df_filtered: DataFrame,
) -> DataFrame:
    """Prepare the chart data: Fatalities per Year under FAR Operations
    Parts."""
    df_chart = df_filtered[
        [
            "ev_year",
            "is_far_part_091x",
            "is_far_part_121",
            "is_far_part_135",
            "inj_tot_f",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    df_chart["far_part_091x_inj_tot_f"] = np.where(
        df_chart.is_far_part_091x, df_chart.inj_tot_f, 0
    )
    df_chart["far_part_121_inj_tot_f"] = np.where(
        df_chart.is_far_part_121, df_chart.inj_tot_f, 0
    )
    df_chart["far_part_135_inj_tot_f"] = np.where(
        df_chart.is_far_part_135, df_chart.inj_tot_f, 0
    )

    return df_chart.groupby("year", as_index=False).sum(
        [  # type: ignore
            "far_part_091x_inj_tot_f",
            "far_part_121_inj_tot_f",
            "far_part_135_inj_tot_f",
        ],
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Injury Level.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_teil(
    df_filtered: DataFrame,
) -> list[int]:
    """Prepare the chart data: Total Events by Injury Level."""
    df_chart = df_filtered[
        [
            "ev_highest_injury",
        ]
    ]

    df_chart["fatal"] = np.where(df_chart.ev_highest_injury == "FATL", 1, 0)
    df_chart["minor"] = np.where(df_chart.ev_highest_injury == "MINR", 1, 0)
    df_chart["none"] = np.where(df_chart.ev_highest_injury == "NONE", 1, 0)
    df_chart["serious"] = np.where(df_chart.ev_highest_injury == "SERS", 1, 0)

    return [
        df_chart["fatal"].sum(),
        df_chart["minor"].sum(),
        df_chart["none"].sum(),
        df_chart["serious"].sum(),
    ]


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Type.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_tet(
    df_filtered: DataFrame,
) -> list[int]:
    """Prepare the chart data: Total Events by Type."""
    df_chart = df_filtered[
        [
            "ev_type",
        ]
    ]

    df_chart["accidents"] = np.where(df_chart.ev_type == "ACC", 1, 0)
    df_chart["incidents"] = np.where(df_chart.ev_type == "INC", 1, 0)

    return [df_chart["accidents"].sum(), df_chart["incidents"].sum()]


# ------------------------------------------------------------------
# Prepare the chart data: Total Fatalities under FAR Operations Parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_tffp(
    df_filtered: DataFrame,
) -> list[int]:
    """Prepare the chart data: Total Fatalities under FAR Operations Parts."""
    df_chart = df_filtered[
        [
            "is_far_part_091x",
            "is_far_part_121",
            "is_far_part_135",
            "inj_tot_f",
        ]
    ]

    df_chart["far_part_091x_inj_tot_f"] = np.where(
        df_chart.is_far_part_091x, df_chart.inj_tot_f, 0
    )
    df_chart["far_part_121_inj_tot_f"] = np.where(
        df_chart.is_far_part_121, df_chart.inj_tot_f, 0
    )
    df_chart["far_part_135_inj_tot_f"] = np.where(
        df_chart.is_far_part_135, df_chart.inj_tot_f, 0
    )

    return [
        df_chart["far_part_091x_inj_tot_f"].sum(),
        df_chart["far_part_121_inj_tot_f"].sum(),
        df_chart["far_part_135_inj_tot_f"].sum(),
    ]


# ------------------------------------------------------------------
# Present the chart: Events per Year by Injury Level.
# ------------------------------------------------------------------
def _present_chart_eyil() -> None:
    """Present the chart: Events per Year by Injury Level."""
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Highest Injury Level"

    st.subheader(chart_title)

    fig = go.Figure(
        data=[
            go.Bar(
                marker={"color": COLOR_LEVEL_1},
                name="Fatal",
                x=DF_FILTERED_CHARTS_EYIL["year"],
                y=DF_FILTERED_CHARTS_EYIL["fatal"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_2},
                name="Serious",
                x=DF_FILTERED_CHARTS_EYIL["year"],
                y=DF_FILTERED_CHARTS_EYIL["serious"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_3},
                name="Minor",
                x=DF_FILTERED_CHARTS_EYIL["year"],
                y=DF_FILTERED_CHARTS_EYIL["minor"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_4},
                name="None",
                x=DF_FILTERED_CHARTS_EYIL["year"],
                y=DF_FILTERED_CHARTS_EYIL["none"],
            ),
        ],
    )

    fig.update_layout(
        autosize=True,
        bargap=0.05,
        barmode="stack",
        height=CHOICE_CHARTS_HEIGHT,
        title=chart_title,
        width=CHOICE_CHARTS_WIDTH,
        xaxis={"title": {"text": "Year"}},
        yaxis={"title": {"text": EVENT_TYPE_DESC}},
    )

    st.plotly_chart(
        fig,
    )

    if CHOICE_CHARTS_DETAILS:
        st.subheader("Detailed chart data")
        st.dataframe(DF_FILTERED_CHARTS_EYIL)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED_CHARTS_EYIL),
            file_name=APP_ID + "_charts_eyil.csv",
            help="The download includes the detailed chart data.",
            label="Download the chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the chart: Events per Year by Type.
# ------------------------------------------------------------------
def _present_chart_eyt() -> None:
    """Present the chart: Events per Year by Type."""
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Type"

    st.subheader(chart_title)

    fig = go.Figure(
        data=[
            go.Bar(
                marker={"color": COLOR_LEVEL_1},
                name="Accidents",
                x=DF_FILTERED_CHARTS_EYT["year"],
                y=DF_FILTERED_CHARTS_EYT["accidents"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_2},
                name="Incidents",
                x=DF_FILTERED_CHARTS_EYT["year"],
                y=DF_FILTERED_CHARTS_EYT["incidents"],
            ),
        ],
    )

    fig.update_layout(
        bargap=0.05,
        barmode="stack",
        height=CHOICE_CHARTS_HEIGHT,
        title=chart_title,
        width=CHOICE_CHARTS_WIDTH,
        xaxis={"title": {"text": "Year"}},
        yaxis={"title": {"text": EVENT_TYPE_DESC}},
    )

    st.plotly_chart(
        fig,
    )

    if CHOICE_CHARTS_DETAILS:
        st.subheader("Detailed chart data")
        st.dataframe(DF_FILTERED_CHARTS_EYT)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED_CHARTS_EYT),
            file_name=APP_ID + "_charts_eyt.csv",
            help="The download includes the detailed chart data.",
            label="Download the chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the chart: Fatalities per Year under FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fyfp() -> None:
    """Present the chart: Fatalities per Year under FAR Operations Parts."""
    chart_title = "Number of Fatalities per Year by Selected FAR Operations Parts"

    st.subheader(chart_title)

    fig = go.Figure(
        data=[
            go.Bar(
                marker={"color": COLOR_LEVEL_1},
                name="Parts 091x",
                x=DF_FILTERED_CHARTS_FYFP["year"],
                y=DF_FILTERED_CHARTS_FYFP["far_part_091x_inj_tot_f"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_2},
                name="Parts 135",
                x=DF_FILTERED_CHARTS_FYFP["year"],
                y=DF_FILTERED_CHARTS_FYFP["far_part_135_inj_tot_f"],
            ),
            go.Bar(
                marker={"color": COLOR_LEVEL_4},
                name="Parts 121",
                x=DF_FILTERED_CHARTS_FYFP["year"],
                y=DF_FILTERED_CHARTS_FYFP["far_part_121_inj_tot_f"],
            ),
        ],
    )

    fig.update_layout(
        bargap=0.05,
        barmode="stack",
        height=CHOICE_CHARTS_HEIGHT,
        width=CHOICE_CHARTS_WIDTH,
        title=chart_title,
        xaxis={"title": {"text": "Year"}},
        yaxis={"title": {"text": "Fatalities"}},
    )

    st.plotly_chart(
        fig,
    )

    if CHOICE_CHARTS_DETAILS:
        st.subheader("Detailed chart data")
        st.dataframe(DF_FILTERED_CHARTS_FYFP)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED_CHARTS_FYFP),
            file_name=APP_ID + "_charts_fyfp.csv",
            help="The download includes the detailed chart data.",
            label="Download the chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the chart: Total Events by Injury Level.
# ------------------------------------------------------------------
def _present_chart_teil() -> None:
    """Present the chart: Total Events by Injury Level."""
    chart_title = f"Total Number of {EVENT_TYPE_DESC} by Highest Injury Level"

    st.subheader(chart_title)

    fig = px.pie(
        color=[
            "Fatal",
            "Minor",
            "None",
            "Serious",
        ],
        color_discrete_map={
            "Fatal": COLOR_LEVEL_1,
            "Minor": COLOR_LEVEL_3,
            "None": COLOR_LEVEL_4,
            "Serious": COLOR_LEVEL_2,
        },
        hole=0.3,
        names=["Fatal", "Minor", "None", "Serious"],
        title=chart_title,
        values=DF_FILTERED_CHARTS_TEIL,
    )

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the chart: Total Events by Type.
# ------------------------------------------------------------------
def _present_chart_tet() -> None:
    """Present the chart: Total Events by Type."""
    chart_title = f"Total Number of {EVENT_TYPE_DESC} by Type"

    st.subheader(chart_title)

    fig = px.pie(
        color=[
            "Accidents",
            "Incidents",
        ],
        color_discrete_map={"Accidents": COLOR_LEVEL_1, "Incidents": COLOR_LEVEL_2},
        hole=0.3,
        names=["Accidents", "Incidents"],
        title=chart_title,
        values=DF_FILTERED_CHARTS_TET,
    )

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the chart: Fatalities per Year under FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_tffp() -> None:
    """Present the chart: Fatalities per Year under FAR Operations Parts."""
    chart_title = "Total Number of Fatalities by Selected FAR Operations Parts"

    st.subheader(chart_title)

    fig = px.pie(
        color=[
            "Parts 091x",
            "Parts 121",
            "Parts 135",
        ],
        color_discrete_map={
            "Parts 091x": COLOR_LEVEL_1,
            "Parts 121": COLOR_LEVEL_4,
            "Parts 135": COLOR_LEVEL_2,
        },
        hole=0.3,
        names=["Parts 091x", "Parts 121", "Parts 135"],
        title=chart_title,
        values=DF_FILTERED_CHARTS_TFFP,
    )

    st.plotly_chart(
        fig,
    )


# ------------------------------------------------------------------
# Present the charts.
# ------------------------------------------------------------------
def _present_charts() -> None:
    """Present the charts."""
    global DF_FILTERED_CHARTS_EYIL  # pylint: disable=global-statement
    global DF_FILTERED_CHARTS_EYT  # pylint: disable=global-statement
    global DF_FILTERED_CHARTS_FYFP  # pylint: disable=global-statement
    global DF_FILTERED_CHARTS_TEIL  # pylint: disable=global-statement
    global DF_FILTERED_CHARTS_TET  # pylint: disable=global-statement
    global DF_FILTERED_CHARTS_TFFP  # pylint: disable=global-statement

    # Events per Year by Type
    if CHOICE_CHARTS_TYPE_EYT:
        DF_FILTERED_CHARTS_EYT = _prep_data_charts_eyt(DF_FILTERED)
        _present_chart_eyt()

    # Events per Year by Injury Level
    if CHOICE_CHARTS_TYPE_EYIL:
        DF_FILTERED_CHARTS_EYIL = _prep_data_charts_eyil(DF_FILTERED)
        _present_chart_eyil()

    # Fatalities per Year under FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FYFP:
        DF_FILTERED_CHARTS_FYFP = _prep_data_charts_fyfp(DF_FILTERED)
        _present_chart_fyfp()

    # Total Events by Type
    if CHOICE_CHARTS_TYPE_TET:
        DF_FILTERED_CHARTS_TET = _prep_data_charts_tet(DF_FILTERED)
        _present_chart_tet()

    # Total Events by Injury Level
    if CHOICE_CHARTS_TYPE_TEIL:
        DF_FILTERED_CHARTS_TEIL = _prep_data_charts_teil(DF_FILTERED)
        _present_chart_teil()

    # Total Fatalities under FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TFFP:
        DF_FILTERED_CHARTS_TFFP = _prep_data_charts_tffp(DF_FILTERED)
        _present_chart_tffp()


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data() -> None:
    """Present the filtered data."""
    _print_timestamp("_present_data() - Start")

    col1, _col2, col3 = st.columns([1, 1, 1])

    if CHOICE_FILTER_CONDITIONS:
        with col1:
            st.markdown(CHOICE_FILTER_CONDITIONS_TEXT)
            _print_timestamp("_present_data() - CHOICE_FILTER_CONDITIONS")

    if CHOICE_ABOUT:
        with col3:
            utils.present_about(PG_CONN, APP_ID)
            _print_timestamp("_present_data() - CHOICE_ABOUT")

    if CHOICE_CHARTS:
        _present_charts()
        _print_timestamp("_present_data() - CHOICE_CHARTS")

    if CHOICE_DATA_PROFILE:
        _present_data_profile()
        _print_timestamp("_present_data() - CHOICE_DATA_PROFILE")

    if CHOICE_DETAILS or CHOICE_CHARTS_DETAILS:
        _present_details()
        _print_timestamp("_present_data() - CHOICE_DETAILS or CHOICE_CHARTS_DETAILS")

    if CHOICE_MAP:
        _present_map()
        _print_timestamp("_present_data() - CHOICE_MAP")

    _print_timestamp("_present_data() - End")


# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
def _present_data_profile() -> None:
    """Present data profile."""
    st.subheader("Profiling of the filtered data set")

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
        file_name=APP_ID + "_" + CHOICE_DATA_PROFILE_TYPE + ".html",  # type: ignore
        help="The download includes a profile report from the dataframe "
        + "after applying the filter options.",
        label="Download the profile report",
        mime="text/html",
    )


# ------------------------------------------------------------------
# Present details.
# ------------------------------------------------------------------
def _present_details() -> None:
    """Present details."""
    if CHOICE_DETAILS:
        st.subheader("Detailed data from database view **`io_app_ae1982`**")
        st.dataframe(DF_FILTERED)
        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED),
            file_name=APP_ID + ".csv",
            help="The download includes all data "
            + "after applying the filter options.",
            label="Download the detailed data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the accidents on the US map.
# ------------------------------------------------------------------
def _present_map() -> None:
    """Present the accidents on the US map."""
    global DF_FILTERED  # pylint: disable=global-statement

    st.subheader("Depicting the accidents on a map of the USA")

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
                + "<tr><td><b>Fatalities</b></td><td>{inj_tot_f}</td></tr>"
                + "<tr><td><b>Latitude</b></td><td>{dec_latitude}</td></tr>"
                + "<tr><td><b>Longitude</b></td><td>{dec_longitude}</td></tr>"
                + "<tr><td><b>Acquired</b></td><td>{latlong_acq}</td></tr>"
                + "</tbody></table>"
            },
        )
    )


# ------------------------------------------------------------------
# Print a timestamp.
# ------------------------------------------------------------------
# pylint: disable=too-many-statements
def _print_timestamp(identifier: str) -> None:
    """Print a timestamp."""
    global LAST_READING  # pylint: disable=global-statement

    if not IS_TIMEKEEPING:
        return

    if not LAST_READING:
        LAST_READING = start_time

    current_time = time.time_ns()

    # Stop time measurement.
    print(
        str(datetime.datetime.now())
        + f" {f'{current_time - LAST_READING:,}':>20} ns - "
        + f"{APP_ID} - {identifier}",
        flush=True,
    )

    LAST_READING = current_time


# ------------------------------------------------------------------
# Set up the filter controls.
# ------------------------------------------------------------------
# pylint: disable=too-many-statements
def _setup_filter() -> None:
    """Set up the filter controls."""
    global CHOICE_FILTER_CONDITIONS_TEXT  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_EV_HIGHEST_INJURY  # pylint: disable=global-statement
    global FILTER_EV_TYPE  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement
    global FILTER_FAR_PARTS  # pylint: disable=global-statement
    global FILTER_FINDING_CODES  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_FROM  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_TO  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_FROM  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_TO  # pylint: disable=global-statement
    global FILTER_IS_ALTITUDE_LOW  # pylint: disable=global-statement
    global FILTER_IS_DEST_COUNTRY_USA  # pylint: disable=global-statement
    global FILTER_IS_DPRT_COUNTRY_USA  # pylint: disable=global-statement
    global FILTER_IS_NARRATIVE_STALL  # pylint: disable=global-statement
    global FILTER_IS_SPIN_STALL  # pylint: disable=global-statement
    global FILTER_LATLONG_ACQ  # pylint: disable=global-statement
    global FILTER_OCCURRENCE_CODES  # pylint: disable=global-statement
    global FILTER_STATE  # pylint: disable=global-statement
    global FILTER_US_AVIATION  # pylint: disable=global-statement

    _print_timestamp("_setup_filter - Start")

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="""
        The following filter options can be used to limit the data to be processed.
        All selected filter options are applied simultaneously, i.e. they are linked
        to a logical ***`and`**.
        """,
        label="**Filter data ?**",
        value=True,
    )

    if not CHOICE_FILTER_DATA:
        return

    CHOICE_FILTER_CONDITIONS_TEXT = ""

    FILTER_ACFT_CATEGORIES = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to selected aircraft categories.
        """,
        label="**Aircraft categories:**",
        options=_sql_query_acft_categories(),
    )
    _print_timestamp("_setup_filter - FILTER_ACFT_CATEGORIES - 1")

    if FILTER_ACFT_CATEGORIES:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Aircraft categories**: **`{','.join(FILTER_ACFT_CATEGORIES)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_ACFT_CATEGORIES - 2")

    st.sidebar.markdown("""---""")

    FILTER_EV_TYPE = st.sidebar.multiselect(
        default="ACC",
        help="""
        - **`ACC`**: The event was classified as an accident.
        - **`INC`**: The event was classified as an incident.
        """,
        label="**Event type(s):**",
        options=_sql_query_ev_type(),
    )
    _print_timestamp("_setup_filter - FILTER_EV_TYPE - 1")

    if FILTER_EV_TYPE:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Event type(s)**: **`{','.join(FILTER_EV_TYPE)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_EV_TYPE - 2")

    st.sidebar.markdown("""---""")

    FILTER_EV_YEAR_FROM, FILTER_EV_YEAR_TO = st.sidebar.slider(
        help="""
            - **`1982`** is the first year with complete statistics.
            - **`2008`** changes were made to the data collection mode.
            """,
        label="**Event year(s):**",
        min_value=1982,
        max_value=datetime.date.today().year,
        value=(2008, datetime.date.today().year - 1),
    )

    if FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO:
        # pylint: disable=line-too-long
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Event year(s)**: between **`{FILTER_EV_YEAR_FROM}`** and **`{FILTER_EV_YEAR_TO}`**"
        )
        _print_timestamp("_setup_filter - FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO")

    st.sidebar.markdown("""---""")

    FILTER_FAR_PARTS = st.sidebar.multiselect(
        help="""
        Under which FAR operations parts the accident was conducted.
        """,
        label="**FAR operations parts:**",
        options=_sql_query_far_parts(),
    )
    _print_timestamp("_setup_filter - FILTER_FAR_PARTS - 1")

    if FILTER_FAR_PARTS:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **FAR operations parts**: **`{','.join(FILTER_FAR_PARTS)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_FAR_PARTS - 2")

    st.sidebar.markdown("""---""")

    max_inj_f_grnd = _sql_query_max_inj_f_grnd()
    _print_timestamp("_setup_filter - _sql_query_max_inj_f_grnd()")

    FILTER_INJ_F_GRND_FROM, FILTER_INJ_F_GRND_TO = st.sidebar.slider(
        help="""
        Number of fatalities on the ground.
        """,
        label="**Fatalities on ground:**",
        min_value=0,
        max_value=max_inj_f_grnd,
        value=(0, max_inj_f_grnd),
    )

    if FILTER_INJ_F_GRND_FROM or FILTER_INJ_F_GRND_TO:
        # pylint: disable=line-too-long
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Fatalities on ground**: between **`{FILTER_INJ_F_GRND_FROM}`** and **`{FILTER_INJ_F_GRND_TO}`**"
        )
        _print_timestamp(
            "_setup_filter - FILTER_INJ_F_GRND_FROM or FILTER_INJ_F_GRND_TO"
        )

    st.sidebar.markdown("""---""")

    max_inj_tot_f = _sql_query_max_inj_tot_f()
    _print_timestamp("_setup_filter - _sql_query_max_inj_tot_f()")

    FILTER_INJ_TOT_F_FROM, FILTER_INJ_TOT_F_TO = st.sidebar.slider(
        help="""
        Number of total fatalities.
        """,
        label="**Fatalities total:**",
        min_value=0,
        max_value=max_inj_tot_f,
        value=(0, max_inj_tot_f),
    )

    if FILTER_INJ_TOT_F_FROM or FILTER_INJ_TOT_F_TO:
        # pylint: disable=line-too-long
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Fatalities total**: between **`{FILTER_INJ_TOT_F_FROM}`** and **`{FILTER_INJ_TOT_F_TO}`**"
        )
        _print_timestamp("_setup_filter - FILTER_INJ_TOT_F_TO")

    st.sidebar.markdown("""---""")

    FILTER_FINDING_CODES = st.sidebar.multiselect(
        help="""
        Here, data can be limited to selected finding codes.
        """,
        label="**Finding code(s):**",
        options=_sql_query_finding_codes(),
    )
    _print_timestamp("_setup_filter - FILTER_FINDING_CODES - 1")

    if FILTER_FINDING_CODES:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Finding code(s)**: **`{','.join(FILTER_FINDING_CODES)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_FINDING_CODES - 2")

    st.sidebar.markdown("""---""")

    FILTER_EV_HIGHEST_INJURY = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to selected injury levels.
        Those events are selected whose highest injury level matches.
        """,
        label="**Highest injury level(s):**",
        options=_sql_query_ev_highest_injury(),
    )
    _print_timestamp("_setup_filter - FILTER_EV_HIGHEST_INJURY - 1")

    if FILTER_EV_HIGHEST_INJURY:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Highest injury level(s)**: **`{','.join(FILTER_EV_HIGHEST_INJURY)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_EV_HIGHEST_INJURY - 2")

    st.sidebar.markdown("""---""")

    FILTER_IS_SPIN_STALL = st.sidebar.checkbox(
        help="""
        For an aerodynamic spin stall, at least one of the following
        two conditions must be met in the event data:
        - one of the finding codes contains **`PARAMS_AoA' or one of
          the occurrence codes contains **`STALL`**, or
        - one of the occurrence codes contains **`LOC-I`** and there is
          a stall according to the narrative and none of the occurrence
          codes contains **`CAA`** or **`CFIT`**, and none of the occurrence
          codes contains **`CAA`** or **`CFIT`**.
        """,
        label="**Incl. aerodynamic spin stalls ?**",
    )

    if FILTER_IS_SPIN_STALL:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Incl. aerodynamic spin stalls ?**: **`{FILTER_IS_SPIN_STALL}`**"
        )
        _print_timestamp("_setup_filter - FILTER_IS_SPIN_STALL")

    st.sidebar.markdown("""---""")

    # flake8: noqa: E501
    FILTER_IS_ALTITUDE_LOW = st.sidebar.checkbox(
        help="""
        A too low altitude problem exists when the following conditions are met:
        - no occurrence code **`MIDAIR`**` or aerodynamic spin stall is present, and
        - the occurrence code is one of **`CAA`**, **`CFIT`**, **`ENV_TER`**, **`FINAL_APP`**,
          **`INIT_CLIMB`**, **`LALT`**, **`MAN_LALT`**, **`PARAMS_ALT`**, **`PARAMS_DEC_APP`**,
          **`PARAMS_DEC_RATE`** or **`ENV_OAS`** and no occurrence code contains **`BIRD`**.
        """,
        label="**Incl. altitude too low ?**",
    )

    if FILTER_IS_ALTITUDE_LOW:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Incl. altitude too low ?**: **`{FILTER_IS_ALTITUDE_LOW}`**"
        )
        _print_timestamp("_setup_filter - FILTER_IS_ALTITUDE_LOW")

    st.sidebar.markdown("""---""")

    FILTER_IS_NARRATIVE_STALL = st.sidebar.checkbox(
        help="""
        A stall according to narrative is present if the accepted narrative
        contains the text **`STALL`**` in any lower or upper case.
        """,
        label="**Incl. stalled according narrative ?**",
    )

    if FILTER_IS_NARRATIVE_STALL:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Incl. stalled according narrative ?**: **`{FILTER_IS_NARRATIVE_STALL}`**"
        )
        _print_timestamp("_setup_filter - FILTER_IS_NARRATIVE_STALL")

    st.sidebar.markdown("""---""")

    FILTER_LATLONG_ACQ = st.sidebar.multiselect(
        help="""
        - **`EST`**: Latitude and longitude have been estimated.
        - **`MEAS`**: Latitude and longitude have been measured.
        """,
        label="**Latitude / longitude acquisition:**",
        options=_sql_query_latlong_acq(),
    )
    _print_timestamp("_setup_filter - FILTER_LATLONG_ACQ - 1")

    if FILTER_LATLONG_ACQ:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Latitude / longitude acquisition**: **`{','.join(FILTER_LATLONG_ACQ)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_LATLONG_ACQ - 2")

    st.sidebar.markdown("""---""")

    FILTER_OCCURRENCE_CODES = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to selected occurrence codes.
        """,
        label="**Occurrence code(s):**",
        options=_sql_query_occurrence_codes(),
    )
    _print_timestamp("_setup_filter - FILTER_OCCURRENCE_CODES - 1")

    if FILTER_OCCURRENCE_CODES:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Occurrence code(s)**: **`{','.join(FILTER_OCCURRENCE_CODES)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_OCCURRENCE_CODES - 2")

    st.sidebar.markdown("""---""")

    FILTER_IS_DPRT_COUNTRY_USA = st.sidebar.checkbox(
        help="""
        At least one of the aircraft involved in the event took off from the US.
        """,
        label="**Only departure country USA ?**",
    )

    if FILTER_IS_DPRT_COUNTRY_USA:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Only departure country USA ?**: **`{FILTER_IS_DPRT_COUNTRY_USA}`**"
        )
        _print_timestamp("_setup_filter - FILTER_IS_DPRT_COUNTRY_USA")

    st.sidebar.markdown("""---""")

    FILTER_IS_DEST_COUNTRY_USA = st.sidebar.checkbox(
        help="""
        At least one of the aircraft involved in the event has its target in the US.
        """,
        label="**Only destination country USA ?**",
    )

    if FILTER_IS_DEST_COUNTRY_USA:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **Only destination country USA ?**: **`{FILTER_IS_DEST_COUNTRY_USA}`**"
        )
        _print_timestamp("_setup_filter - FILTER_IS_DEST_COUNTRY_USA")

    st.sidebar.markdown("""---""")

    FILTER_STATE = st.sidebar.multiselect(
        help="Here, data can be limited to selected U.S. states.",
        label="**State(s) in the US:**",
        options=_sql_query_us_states(),
    )
    _print_timestamp("_setup_filter - FILTER_STATE - 1")

    if FILTER_STATE:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **State(s) in the US**: **`{','.join(FILTER_STATE)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_STATE - 2")

    st.sidebar.markdown("""---""")

    FILTER_US_AVIATION = st.sidebar.multiselect(
        default=[
            FILTER_US_AVIATION_COUNTRY,
            FILTER_US_AVIATION_DEPARTURE,
            FILTER_US_AVIATION_DESTINATION,
            FILTER_US_AVIATION_OPERATOR,
            FILTER_US_AVIATION_OWNER,
            FILTER_US_AVIATION_REGISTRATION,
        ],
        help="""
        **US aviation** means that either the event occurred on US soil or 
        the departure, destination, owner, operator or registration is US.
        """,
        label="**US aviation criteria:**",
        options=[
            FILTER_US_AVIATION_COUNTRY,
            FILTER_US_AVIATION_DEPARTURE,
            FILTER_US_AVIATION_DESTINATION,
            FILTER_US_AVIATION_OPERATOR,
            FILTER_US_AVIATION_OWNER,
            FILTER_US_AVIATION_REGISTRATION,
        ],
    )
    _print_timestamp("_setup_filter - FILTER_US_AVIATION - 1")

    if FILTER_US_AVIATION:
        CHOICE_FILTER_CONDITIONS_TEXT = (
            CHOICE_FILTER_CONDITIONS_TEXT
            + f"\n- **US aviation criteria**: **`{','.join(FILTER_US_AVIATION)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_US_AVIATION - 2")

    st.sidebar.markdown("""---""")

    _print_timestamp("_setup_filter - End")


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page() -> None:
    """Set up the page."""
    global CHOICE_ABOUT  # pylint: disable=global-statement
    global CHOICE_FILTER_CONDITIONS  # pylint: disable=global-statement
    global EVENT_TYPE_DESC  # pylint: disable=global-statement

    if FILTER_EV_TYPE == ["ACC"]:
        EVENT_TYPE_DESC = "Accidents"
    elif FILTER_EV_TYPE == ["INC"]:
        EVENT_TYPE_DESC = "Incidents"
    else:
        EVENT_TYPE_DESC = "Events"

    st.header(
        f"Aviation {EVENT_TYPE_DESC} between {FILTER_EV_YEAR_FROM} and {FILTER_EV_YEAR_TO}"
    )

    col1, _col2, col3 = st.columns([1, 1, 1])

    if CHOICE_FILTER_DATA:
        with col1:
            CHOICE_FILTER_CONDITIONS = st.checkbox(
                help="Show the selected filter conditions.",
                label="**Show filter conditions**",
                value=False,
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
def _setup_sidebar() -> None:
    """Set up the sidebar."""
    _print_timestamp("_setup_sidebar() - Start")

    _setup_task_controls()
    _print_timestamp("_setup_sidebar() - _setup_task_controls()")

    _setup_filter()
    _print_timestamp("_setup_sidebar() - _setup_filter")

    _print_timestamp("_setup_sidebar() - End")


# ------------------------------------------------------------------
# Set up the task controls.
# ------------------------------------------------------------------
def _setup_task_controls() -> None:
    """Set up the task controls."""
    global CHOICE_CHARTS  # pylint: disable=global-statement
    global CHOICE_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EYIL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EYT  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_FYFP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TEIL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TET  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TFFP  # pylint: disable=global-statement
    global CHOICE_CHARTS_WIDTH  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_MAP_RADIUS  # pylint: disable=global-statement

    CHOICE_CHARTS = st.sidebar.checkbox(
        help="Accidents or fatalities per year (after filtering the data).",
        label="**Show charts**",
        value=True,
    )

    if CHOICE_CHARTS:
        CHOICE_CHARTS_HEIGHT = st.sidebar.slider(
            label="Chart height (px)", min_value=100, max_value=1000, value=500
        )
        CHOICE_CHARTS_WIDTH = st.sidebar.slider(
            label="Chart width (px)", min_value=100, max_value=2000, value=1000
        )

        CHOICE_CHARTS_DETAILS = st.sidebar.checkbox(
            help="Tabular representation of the of the data underlying the charts.",
            label="Show detailed chart data",
            value=False,
        )

        st.sidebar.markdown("""---""")

        CHOICE_CHARTS_TYPE_EYT = st.sidebar.checkbox(
            help="Events per year by event type (after filtering the data).",
            label="Events per Year by Type",
            value=False,
        )
        CHOICE_CHARTS_TYPE_EYIL = st.sidebar.checkbox(
            help="Events per year by highest injury level (after filtering the data).",
            label="Events per Year by Injury Level",
            value=False,
        )
        CHOICE_CHARTS_TYPE_FYFP = st.sidebar.checkbox(
            help="Fatalities per year by selected FAR Operations Parts (after filtering the data).",
            label="Fatalities per Year under FAR Operations Parts",
            value=True,
        )
        CHOICE_CHARTS_TYPE_TET = st.sidebar.checkbox(
            help="Total events by event type (after filtering the data).",
            label="Total Events by Type",
            value=False,
        )
        CHOICE_CHARTS_TYPE_TEIL = st.sidebar.checkbox(
            help="Total events by highest injury level (after filtering the data).",
            label="Total Events by Injury Level",
            value=False,
        )
        CHOICE_CHARTS_TYPE_TFFP = st.sidebar.checkbox(
            help="Total fatalities by selected FAR Operations Parts (after filtering the data).",
            label="Total Fatalities under FAR Operations Parts",
            value=True,
        )

    st.sidebar.markdown("""---""")

    CHOICE_DATA_PROFILE = st.sidebar.checkbox(
        help="Pandas profiling of the filtered dataset.",
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
        help="Tabular representation of the filtered detailed data.",
        label="**Show detailed data**",
        value=False,
    )

    st.sidebar.markdown("""---""")

    CHOICE_MAP = st.sidebar.checkbox(
        help="Display of accident events on a map of the USA "
        + "(after filtering the data).",
        label="**Show US map**",
        value=False,
    )

    if CHOICE_MAP:
        CHOICE_MAP_MAP_STYLE = st.sidebar.radio(
            help="""
light: designed to provide geographic context while highlighting the data -
outdoors: focused on wilderness locations with curated tile sets -
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
        cur.execute(
            """
        SELECT string_agg(DISTINCT acft_category, ',' ORDER BY acft_category)
          FROM aircraft
         WHERE acft_category IS NOT NULL
         ORDER BY 1;
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of injury levels
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_ev_highest_injury() -> list[str]:
    """Execute a query that returns a list of injury levels.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(DISTINCT ev_highest_injury, ',' ORDER BY ev_highest_injury)
          FROM events
         WHERE ev_highest_injury IS NOT NULL
         ORDER BY 1;
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of event types
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_ev_type() -> list[str]:
    """Execute a query that returns a list of event types.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(DISTINCT ev_type, ',' ORDER BY ev_type)
          FROM events
         WHERE ev_type IS NOT NULL
         ORDER BY 1;
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of FAR Operations Parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_far_parts() -> list[str]:
    """Execute a query that returns a list of FAR Operations Parts.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(DISTINCT far_part, ',' ORDER BY far_part)
          FROM aircraft
         WHERE far_part IS NOT NULL
         ORDER BY 1;
        """
        )
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
        # flake8: noqa: E501
        # pylint: disable=line-too-long
        cur.execute(
            """
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
        """
        )  # noqa: E501
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Determine the maximum number of fatalities on ground.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_max_inj_f_grnd() -> int:
    """Determine the maximum number of total fatalities on ground.

    Returns:
        int: Maximum number of fatalities on ground.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MAX(inj_f_grnd)
          FROM io_app_ae1982;
        """
        )
        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Determine the maximum number of fatalities.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_max_inj_tot_f() -> int:
    """Determine the maximum number of total fatalities.

    Returns:
        int: Maximum number of total fatalities.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MAX(inj_tot_f)
          FROM io_app_ae1982;
        """
        )
        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of latitude / longitude
# acquisition
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_latlong_acq() -> list[str]:
    """Execute a query that returns a list of latitude / longitude acquisition.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(DISTINCT latlong_acq, ',' ORDER BY latlong_acq)
          FROM events
         WHERE latlong_acq IS NOT NULL
         ORDER BY 1;
        """
        )
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
        # flake8: noqa: E501
        # pylint: disable=line-too-long
        cur.execute(
            """
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
        """
        )  # noqa: E501
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Run the US latitude and longitude query.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_us_ll(pitch: int, zoom: float) -> pdk.ViewState:
    """Run the US latitude and longitude query.

    Args:
        pitch (int): Up/down angle relative to the maps plane.
        zoom (float): Magnification level of the map.

    Returns:
        pdk.ViewState: Screen focus.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT dec_latitude,
               dec_longitude
          FROM io_countries
         WHERE country = 'USA';
        """
        )
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
        cur.execute(
            """
        SELECT string_agg(DISTINCT state, ',' ORDER BY state)
          FROM io_states
         WHERE country  = 'USA'
         ORDER BY 1;
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
# Start time measurement.
start_time = time.time_ns()

st.set_page_config(layout="wide")

PG_CONN = _get_postgres_connection()
_print_timestamp("_setup_filter - got DB connection")

_setup_sidebar()
_print_timestamp("_setup_sidebar()")

_setup_page()
_print_timestamp("_setup_page()")

DF_UNFILTERED = _get_data()
DF_FILTERED = DF_UNFILTERED
_print_timestamp("_get_data()")

if CHOICE_FILTER_DATA:
    DF_FILTERED = _apply_filter(
        DF_UNFILTERED,
        FILTER_ACFT_CATEGORIES,
        FILTER_EV_HIGHEST_INJURY,
        FILTER_EV_TYPE,
        FILTER_EV_YEAR_FROM,
        FILTER_EV_YEAR_TO,
        FILTER_FAR_PARTS,
        FILTER_FINDING_CODES,
        FILTER_INJ_F_GRND_FROM,
        FILTER_INJ_F_GRND_TO,
        FILTER_INJ_TOT_F_FROM,
        FILTER_INJ_TOT_F_TO,
        FILTER_IS_ALTITUDE_LOW,
        FILTER_IS_DEST_COUNTRY_USA,
        FILTER_IS_DPRT_COUNTRY_USA,
        FILTER_IS_NARRATIVE_STALL,
        FILTER_IS_SPIN_STALL,
        FILTER_LATLONG_ACQ,
        FILTER_OCCURRENCE_CODES,
        FILTER_STATE,
        FILTER_US_AVIATION,
    )
    _print_timestamp("_apply_filter()")

_present_data()
_print_timestamp("_present_data()")

# Stop time measurement.
print(
    str(datetime.datetime.now())
    + f" {f'{time.time_ns() - start_time:,}':>20} ns - Total runtime for application "
    + APP_ID,
    flush=True,
)