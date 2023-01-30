# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Aviation Events in the US since 1982."""
import datetime
import time
from operator import itemgetter

import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import psycopg2
import pydeck as pdk  # type: ignore
import streamlit as st
import user_guide  # type: ignore
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from pandas_profiling import ProfileReport  # type: ignore
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore

# SettingWithCopyWarning
pd.options.mode.chained_assignment: str | None = None  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "ae1982"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_ABOUT: bool | None = None
CHOICE_ACTIVE_FILTERS: bool | None = None
CHOICE_ACTIVE_FILTERS_TEXT: str = ""

CHOICE_CHARTS: bool | None = None
CHOICE_CHARTS_DETAILS: bool | None = None
CHOICE_CHARTS_HEIGHT: float | None = None
CHOICE_CHARTS_HEIGHT_DEFAULT: float = 500

CHOICE_CHARTS_LEGEND_FP_091X = "General Operations (Parts 091x)"
CHOICE_CHARTS_LEGEND_FP_121 = "Regular Scheduled Air Carriers (Parts 121)"
CHOICE_CHARTS_LEGEND_FP_135 = "Charter Type Services (Parts 135)"

CHOICE_CHARTS_LEGEND_IL_FATAL = "Fatal"
CHOICE_CHARTS_LEGEND_IL_MINOR = "Minor"
CHOICE_CHARTS_LEGEND_IL_NONE = "None"
CHOICE_CHARTS_LEGEND_IL_SERIOUS = "Serious"

CHOICE_CHARTS_LEGEND_LP_ALTITUDE_CONTROLLABLE = "Aircraft can climb"
CHOICE_CHARTS_LEGEND_LP_ALTITUDE_LOW = "Altitude too low"
CHOICE_CHARTS_LEGEND_LP_ATTITUDE = "Attitude is controllable"
CHOICE_CHARTS_LEGEND_LP_EMERGENCY = "Aircraft has degraded control failure"
CHOICE_CHARTS_LEGEND_LP_MIDAIR = "Midair collision"
CHOICE_CHARTS_LEGEND_LP_NARRATIVE = "Stall in narrative"
CHOICE_CHARTS_LEGEND_LP_PILOT = "Pilot is able to perform maneuver"
CHOICE_CHARTS_LEGEND_LP_RSS_AIRBORNE = "Airborne collision avoidance"
CHOICE_CHARTS_LEGEND_LP_RSS_FORCED = "Forced landing"
CHOICE_CHARTS_LEGEND_LP_RSS_SPIN = "Spin / stall prevention and recovery"
CHOICE_CHARTS_LEGEND_LP_RSS_TERRAIN = "Terrain collision avoidance"
CHOICE_CHARTS_LEGEND_LP_SPIN = "Aerodynamic spin / stall"

CHOICE_CHARTS_LEGEND_RSS_AIRBORNE = "Airborne Collision Avoidance"
CHOICE_CHARTS_LEGEND_RSS_FORCED = "Forced Landing"
CHOICE_CHARTS_LEGEND_RSS_SPIN = "Spin Stall Prevention and Recovery"
CHOICE_CHARTS_LEGEND_RSS_TERRAIN = "Terrain Collision Avoidance"

CHOICE_CHARTS_LEGEND_T_ACC = "Accident"
CHOICE_CHARTS_LEGEND_T_INC = "Incident"

CHOICE_CHARTS_TYPE_EY_AOC: bool | None = None
CHOICE_CHARTS_TYPE_EY_IL: bool | None = None
CHOICE_CHARTS_TYPE_EY_RSS: bool | None = None
CHOICE_CHARTS_TYPE_EY_T: bool | None = None
CHOICE_CHARTS_TYPE_EY_TLP: bool | None = None
CHOICE_CHARTS_TYPE_FY_FP: bool | None = None

CHOICE_CHARTS_TYPE_N_AOC: list[tuple[str, str]] = [
    (
        "LOC-I",
        "LOC-I",
    ),
    (
        "UNK",
        "UNK",
    ),
    (
        "SCF-PP",
        "SCF-PP",
    ),
    (
        "CFIT",
        "CFIT",
    ),
    (
        "OTHR",
        "OTHR",
    ),
    (
        "UIMC",
        "UIMC",
    ),
    (
        "SCF-NP",
        "SCF-NP",
    ),
    (
        "FUEL",
        "FUEL",
    ),
    (
        "LALT",
        "LALT",
    ),
    (
        "MAC",
        "MAC",
    ),
    (
        "CTOL",
        "CTOL",
    ),
]

CHOICE_CHARTS_TYPE_N_IL: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_IL_FATAL,
        "FATL",
    ),
    (
        CHOICE_CHARTS_LEGEND_IL_SERIOUS,
        "SERS",
    ),
    (
        CHOICE_CHARTS_LEGEND_IL_MINOR,
        "MINR",
    ),
    (
        CHOICE_CHARTS_LEGEND_IL_NONE,
        "NONE",
    ),
]

CHOICE_CHARTS_TYPE_N_RSS: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_RSS_TERRAIN,
        "is_rss_terrain_collision_avoidance",
    ),
    (
        CHOICE_CHARTS_LEGEND_RSS_SPIN,
        "is_rss_spin_stall_prevention_and_recovery",
    ),
    (
        CHOICE_CHARTS_LEGEND_RSS_FORCED,
        "is_rss_forced_landing",
    ),
    (
        CHOICE_CHARTS_LEGEND_RSS_AIRBORNE,
        "is_midair_collision",
    ),
]

CHOICE_CHARTS_TYPE_N_T: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_T_ACC,
        "ACC",
    ),
    (
        CHOICE_CHARTS_LEGEND_T_INC,
        "INC",
    ),
]

CHOICE_CHARTS_TYPE_N_TLP: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_LP_ATTITUDE,
        "is_attitude_controllable",
    ),
    (
        CHOICE_CHARTS_LEGEND_LP_ALTITUDE_CONTROLLABLE,
        "is_altitude_controllable",
    ),
    (
        CHOICE_CHARTS_LEGEND_LP_ALTITUDE_LOW,
        "is_altitude_low",
    ),
    (
        CHOICE_CHARTS_LEGEND_LP_EMERGENCY,
        "is_emergency_landing",
    ),
    (
        CHOICE_CHARTS_LEGEND_LP_SPIN,
        "is_spin_stall",
    ),
    (
        CHOICE_CHARTS_LEGEND_LP_PILOT,
        "is_pilot_issue",
    ),
]

CHOICE_CHARTS_TYPE_N_FP: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_FP_091X,
        "is_far_part_091x",
    ),
    (
        CHOICE_CHARTS_LEGEND_FP_135,
        "is_far_part_135",
    ),
    (
        CHOICE_CHARTS_LEGEND_FP_121,
        "is_far_part_121",
    ),
]

CHOICE_CHARTS_TYPE_TE_AOC: bool | None = None
CHOICE_CHARTS_TYPE_TE_IL: bool | None = None
CHOICE_CHARTS_TYPE_TE_RSS: bool | None = None
CHOICE_CHARTS_TYPE_TE_T: bool | None = None
CHOICE_CHARTS_TYPE_TE_TLP: bool | None = None
CHOICE_CHARTS_TYPE_TF_FP: bool | None = None

CHOICE_CHARTS_UG_EY_AOC: bool | None = None
CHOICE_CHARTS_UG_EY_IL: bool | None = None
CHOICE_CHARTS_UG_EY_RSS: bool | None = None
CHOICE_CHARTS_UG_EY_T: bool | None = None
CHOICE_CHARTS_UG_EY_TLP: bool | None = None
CHOICE_CHARTS_UG_FY_FP: bool | None = None
CHOICE_CHARTS_UG_TE_AOC: bool | None = None
CHOICE_CHARTS_UG_TE_IL: bool | None = None
CHOICE_CHARTS_UG_TE_RSS: bool | None = None
CHOICE_CHARTS_UG_TE_T: bool | None = None
CHOICE_CHARTS_UG_TE_TLP: bool | None = None
CHOICE_CHARTS_UG_TF_FP: bool | None = None

CHOICE_CHARTS_WIDTH: float | None = None
CHOICE_CHARTS_WIDTH_DEFAULT: float = 1000
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None
CHOICE_EXTENDED_VERSION: bool | None = None
CHOICE_FILTER_DATA: bool | None = None

CHOICE_MAP: bool | None = None
CHOICE_MAP_MAP_STYLE: str | None = None
CHOICE_MAP_MAP_STYLE_DEFAULT: str = "outdoors-v12"
CHOICE_MAP_RADIUS: float | None = 1609.347 * 2

CHOICE_UG_APP: bool | None = None
CHOICE_UG_CHART_FY_FP: bool | None = None

COLOR_HEADER: str = "#357f8f"
COLOR_MAP: list[str] = [
    "#15535f",  # peacock
    "#47a3b5",  # aqua
    "#fadc82",  # yellow
    "#f18c2c",  # orange
    "#778b4a",  # olive
    "#eb6081",  # raspberry
    "#c4e5f4",  # pale blue
    "#d43724",  # red
    "#bcd284",  # pale green
    "#5f4b8b",  # purple
    "#f8d2d5",  # pink
    "#795339",  # brown
    "#40484f",  # charcoal
]
COLOR_MAP_NONE = "#000000"  # black
COLOR_MAP_SIZE = len(COLOR_MAP)

COUNTRY_USA = "USA"

DF_FILTERED: DataFrame = DataFrame()
DF_UNFILTERED: DataFrame = DataFrame()

EVENT_TYPE_DESC: str

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_CICTT_CODES: list[str] = []
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
FILTER_LATLONG_ACQ: list[str] = []
FILTER_LOGICAL_PARAMETERS_AND: list[str] = []
FILTER_LOGICAL_PARAMETERS_OR: list[str] = []
FILTER_NO_AIRCRAFT_FROM: int | None = None
FILTER_NO_AIRCRAFT_TO: int | None = None
FILTER_OCCURRENCE_CODES: list[str] = []
FILTER_RSS: list[str] = []
FILTER_STATE: list[str] = []
FILTER_US_AVIATION: list[str] = []
FILTER_US_AVIATION_COUNTRY = "Event Country USA"
FILTER_US_AVIATION_DEPARTURE = "US Departure"
FILTER_US_AVIATION_DESTINATION = "US Destination"
FILTER_US_AVIATION_OPERATOR = "US Operator"
FILTER_US_AVIATION_OWNER = "US Owner"
FILTER_US_AVIATION_REGISTRATION = "US Registration"
FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

IS_TIMEKEEPING = False

LAST_READING: int = 0
# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"


MAP_STYLE_PREFIX = "mapbox://styles/mapbox/"
MODE_STANDARD: bool | None = None

NAME_NONE = "None"

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
START_TIME: int = 0

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
def _apply_filter(
    df_unfiltered: DataFrame,
    filter_acft_categories: list | None,
    filter_cictt_codes: list | None,
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
    filter_latlong_acq: list | None,
    filter_logical_parameters_and: list | None,
    filter_logical_parameters_or: list | None,
    filter_no_aircraft_from: int | None,
    filter_no_aircraft_to: int | None,
    filter_occurrence_codes: list | None,
    filter_rss: list | None,
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
    if filter_cictt_codes:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["cictt_codes"].apply(
                lambda x: bool(set(x) & set(filter_cictt_codes))  # type: ignore
            )
        ]
        _print_timestamp("_apply_filter() - filter_cictt_codes")

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
        _print_timestamp("_apply_filter() - filter_ev_year_from/to")

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
        _print_timestamp("_apply_filter() - filter_inj_f_grnd_from/to")

    # noinspection PyUnboundLocalVariable
    if filter_inj_tot_f_from or filter_inj_tot_f_to:
        df_filtered = df_filtered.loc[
            (df_filtered["inj_tot_f"] >= filter_inj_tot_f_from)
            & (df_filtered["inj_tot_f"] <= filter_inj_tot_f_to)
        ]
        _print_timestamp("_apply_filter() - filter_inj_tot_f_from/to")

    # noinspection PyUnboundLocalVariable
    if filter_latlong_acq:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["latlong_acq"].isin(filter_latlong_acq))
        ]
        _print_timestamp("_apply_filter() - filter_latlong_acq")

    # noinspection PyUnboundLocalVariable
    if filter_logical_parameters_and:
        df_filtered = _apply_filter_logical_params(
            df_filtered,
            filter_logical_parameters_and,
            " & ",
        )

    # noinspection PyUnboundLocalVariable
    if filter_logical_parameters_or:
        df_filtered = _apply_filter_logical_params(
            df_filtered,
            filter_logical_parameters_or,
            " | ",
        )

    # noinspection PyUnboundLocalVariable
    if filter_no_aircraft_from or filter_no_aircraft_to:
        df_filtered = df_filtered.loc[
            (df_filtered["no_aircraft"] >= filter_no_aircraft_from)
            & (df_filtered["no_aircraft"] <= filter_no_aircraft_to)
        ]
        _print_timestamp("_apply_filter() - filter_no_aircraft_from/to")

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
    if filter_rss:
        df_filtered = _apply_filter_rss(df_filtered, filter_rss)

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
# Filter the data frame - Logical parameters.
# ------------------------------------------------------------------
def _apply_filter_logical_params(
    _df_unfiltered: DataFrame,  # pylint: disable=unused-argument
    filter_params: list | None,
    operand: str,
) -> DataFrame:
    """Filter the data frame - US aviation."""
    _print_timestamp("_apply_filter_logical_params() - Start")

    filter_cmd = "_df_unfiltered.loc["
    filter_cmd_or = ""

    if CHOICE_CHARTS_LEGEND_LP_ALTITUDE_CONTROLLABLE in filter_params:  # type: ignore
        filter_cmd += "(_df_unfiltered['is_altitude_controllable'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_ALTITUDE_LOW in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_altitude_low'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_ATTITUDE in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or + "(_df_unfiltered['is_attitude_controllable'] == True)"
        )
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_EMERGENCY in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_emergency_landing'] == True)"
        filter_cmd_or = operand

    if (
        CHOICE_CHARTS_LEGEND_LP_MIDAIR in filter_params  # type: ignore
        or CHOICE_CHARTS_LEGEND_LP_RSS_AIRBORNE in filter_params  # type: ignore
    ):
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_midair_collision'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_NARRATIVE in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_narrative_stall'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_PILOT in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_pilot_issue'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_RSS_AIRBORNE in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_midair_collision'] == True)"
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_RSS_FORCED in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or + "(_df_unfiltered['is_rss_forced_landing'] == True)"
        )
        filter_cmd_or = " | "

    if CHOICE_CHARTS_LEGEND_LP_RSS_SPIN in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or
            + "(_df_unfiltered['is_rss_spin_stall_prevention_and_recovery'] == True)"
        )
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_RSS_TERRAIN in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or
            + "(_df_unfiltered['is_rss_terrain_collision_avoidance'] == True)"
        )
        filter_cmd_or = operand

    if CHOICE_CHARTS_LEGEND_LP_SPIN in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_spin_stall'] == True)"

    filter_cmd += "]"

    df_filtered = eval(filter_cmd)  # pylint: disable=eval-used

    _print_timestamp("_apply_filter_logical_params() - End")

    return df_filtered


# ------------------------------------------------------------------
# Filter the data frame - Required safety systems.
# ------------------------------------------------------------------
def _apply_filter_rss(
    _df_unfiltered: DataFrame,  # pylint: disable=unused-argument
    filter_params: list | None,
) -> DataFrame:
    """Filter the data frame - US aviation."""
    _print_timestamp("_apply_filter_rss() - Start")

    filter_cmd = "_df_unfiltered.loc["
    filter_cmd_or = ""

    if CHOICE_CHARTS_LEGEND_RSS_AIRBORNE in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_midair_collision'] == True)"
        filter_cmd_or = " | "

    if CHOICE_CHARTS_LEGEND_RSS_FORCED in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or + "(_df_unfiltered['is_rss_forced_landing'] == True)"
        )
        filter_cmd_or = " | "

    if CHOICE_CHARTS_LEGEND_RSS_SPIN in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or
            + "(_df_unfiltered['is_rss_spin_stall_prevention_and_recovery'] == True)"
        )
        filter_cmd_or = " | "

    if CHOICE_CHARTS_LEGEND_RSS_TERRAIN in filter_params:  # type: ignore
        filter_cmd += (
            filter_cmd_or
            + "(_df_unfiltered['is_rss_terrain_collision_avoidance'] == True)"
        )

    filter_cmd += "]"

    df_filtered = eval(filter_cmd)  # pylint: disable=eval-used

    _print_timestamp("_apply_filter_rss() - End")

    return df_filtered


# ------------------------------------------------------------------
# Filter the data frame - US aviation.
# ------------------------------------------------------------------
def _apply_filter_us_aviation(
    _df_unfiltered: DataFrame,  # pylint: disable=unused-argument
    filter_params: list | None,
) -> DataFrame:
    """Filter the data frame - US aviation."""
    _print_timestamp("_apply_filter_us_aviation() - Start")

    filter_cmd = "_df_unfiltered.loc["
    filter_cmd_or = ""

    if FILTER_US_AVIATION_COUNTRY in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['country'] == COUNTRY_USA)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_DESTINATION in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_dest_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_DEPARTURE in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_dprt_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_OPERATOR in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_oper_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_OWNER in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_owner_country_usa'] == True)"
        filter_cmd_or = " | "

    if FILTER_US_AVIATION_REGISTRATION in filter_params:  # type: ignore
        filter_cmd += filter_cmd_or + "(_df_unfiltered['is_regis_country_usa'] == True)"

    filter_cmd += "]"

    df_filtered = eval(filter_cmd)  # pylint: disable=eval-used

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
# Prepare the chart data: Number of Events per Year by
# CICTT Codes.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_ey_aoc(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Events per Year by CICTT Codes."""
    df_chart = df_filtered[
        [
            "ev_year",
            "cictt_codes",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    if FILTER_CICTT_CODES:
        names = []
        for cictt_code in FILTER_CICTT_CODES:
            names.append((cictt_code, cictt_code))
    else:
        names = CHOICE_CHARTS_TYPE_N_AOC

    for name, name_df in names:
        df_chart[name] = np.where(
            df_chart.cictt_codes.apply(lambda x, n=name_df: bool(set(x) & {n})), 1, 0
        )

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Injury Level.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_ey_il(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Events per Year by Injury Level."""
    df_chart = df_filtered[
        [
            "ev_year",
            "ev_highest_injury",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    for name, name_df in CHOICE_CHARTS_TYPE_N_IL:
        df_chart[name] = np.where(df_chart.ev_highest_injury == name_df, 1, 0)

    return CHOICE_CHARTS_TYPE_N_IL, df_chart.groupby("year", as_index=False).sum()


# ------------------------------------------------------------------
# Prepare the chart data: Number of Events per Year by
# Required Safety Systems.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_ey_rss(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Events per Year by Required Safety
    Systems."""
    df_chart = df_filtered[
        [
            "ev_year",
            "is_midair_collision",
            "is_rss_forced_landing",
            "is_rss_spin_stall_prevention_and_recovery",
            "is_rss_terrain_collision_avoidance",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    for name, name_df in CHOICE_CHARTS_TYPE_N_RSS:
        df_chart[name] = np.where(df_chart[name_df], 1, 0)

    return CHOICE_CHARTS_TYPE_N_RSS, df_chart.groupby("year", as_index=False).sum()


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Event Types.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_ey_t(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Events per Year by Event Types."""
    df_chart = df_filtered[
        [
            "ev_year",
            "ev_type",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    for name, name_df in CHOICE_CHARTS_TYPE_N_T:
        df_chart[name] = np.where(df_chart.ev_type == name_df, 1, 0)

    return CHOICE_CHARTS_TYPE_N_T, df_chart.groupby("year", as_index=False).sum()


# ------------------------------------------------------------------
# Prepare the chart data: Number of Events per Year by
# Top Level Logical Parameters.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_ey_tlp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Events per Year by Top Level Logical
    Parameters."""
    df_chart = df_filtered[
        [
            "ev_year",
            "is_altitude_controllable",
            "is_altitude_low",
            "is_attitude_controllable",
            "is_emergency_landing",
            "is_pilot_issue",
            "is_spin_stall",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    for name, name_df in CHOICE_CHARTS_TYPE_N_TLP:
        df_chart[name] = np.where(df_chart[name_df], 1, 0)

    return CHOICE_CHARTS_TYPE_N_TLP, df_chart.groupby("year", as_index=False).sum()


# ------------------------------------------------------------------
# Prepare the chart data: Fatalities per Year under
# FAR Operations Parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_fy_fp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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

    for name, name_df in CHOICE_CHARTS_TYPE_N_FP:
        df_chart[name] = np.where(df_chart[name_df], df_chart.inj_tot_f, 0)

    return CHOICE_CHARTS_TYPE_N_FP, df_chart.groupby("year", as_index=False).sum()


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by CICTT Codes.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_te_aoc(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    #   """Prepare the chart data: Total Events by CICTT Codes."""
    df_chart = df_filtered[
        [
            "cictt_codes",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in _sql_query_cictt_codes():
        df_chart[name] = np.where(
            df_chart.cictt_codes.apply(lambda x, n=name: bool(set(x) & {n})),
            1,
            0,
        )
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(len(df_chart.index), total_pie, name_value, 0.015)


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Highest Injury Levels.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_te_il(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    """Prepare the chart data: Total Events by Highest Injury Levels."""
    df_chart = df_filtered[
        [
            "ev_highest_injury",
        ]
    ]

    name_value = []
    total_pie = 0

    for name, name_df in CHOICE_CHARTS_TYPE_N_IL:
        df_chart[name] = np.where(df_chart.ev_highest_injury == name_df, 1, 0)
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(len(df_chart.index), total_pie, name_value)


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Required Safety Systems.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_te_rss(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    """Prepare the chart data: Total Events by Required Safety Systems."""
    df_chart = df_filtered[
        [
            "is_midair_collision",
            "is_rss_forced_landing",
            "is_rss_spin_stall_prevention_and_recovery",
            "is_rss_terrain_collision_avoidance",
        ]
    ]

    name_value = []
    total_pie = 0

    for name, name_df in CHOICE_CHARTS_TYPE_N_RSS:
        df_chart[name] = np.where(df_chart[name_df], 1, 0)
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(len(df_chart.index), total_pie, name_value)


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Event Types.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_te_t(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    """Prepare the chart data: Total Events by Event Types."""
    df_chart = df_filtered[
        [
            "ev_type",
        ]
    ]

    name_value = []
    total_pie = 0

    for name, name_df in CHOICE_CHARTS_TYPE_N_T:
        df_chart[name] = np.where(df_chart.ev_type == name_df, 1, 0)
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(len(df_chart.index), total_pie, name_value)


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by
# Top Level Logical Parameters.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_te_tlp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    """Prepare the chart data: Total Events by Top Level Logical Parameters."""
    df_chart = df_filtered[
        [
            "is_altitude_controllable",
            "is_altitude_low",
            "is_attitude_controllable",
            "is_emergency_landing",
            "is_pilot_issue",
            "is_spin_stall",
        ]
    ]

    name_value = []
    total_pie = 0

    for name, name_df in CHOICE_CHARTS_TYPE_N_TLP:
        df_chart[name] = np.where(df_chart[name_df], 1, 0)
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(len(df_chart.index), total_pie, name_value)


# ------------------------------------------------------------------
# Prepare the chart data: Total Fatalities under
# FAR Operations Parts.
# ------------------------------------------------------------------
@st.experimental_memo
def _prep_data_charts_tf_fp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str]]:
    """Prepare the chart data: Total Fatalities under FAR Operations Parts."""
    df_chart = df_filtered[
        [
            "is_far_part_091x",
            "is_far_part_121",
            "is_far_part_135",
            "inj_tot_f",
        ]
    ]

    name_value = []
    total_pie = 0

    for name, name_df in CHOICE_CHARTS_TYPE_N_FP:
        df_chart[name] = np.where(df_chart[name_df], df_chart.inj_tot_f, 0)
        value = df_chart[name].sum()
        name_value.append((name, value))
        total_pie += value

    return _prep_pie_chart(total_pie, total_pie, name_value)


# ------------------------------------------------------------------
# Prepare the pie chart.
# ------------------------------------------------------------------
def _prep_pie_chart(
    total_filter: int,
    total_pie: int,
    name_value: list[tuple[str, int]],
    threshold: float = 0,
) -> tuple[list[str], list[int], dict[str, str]]:
    value_threshold = total_pie * threshold

    name_sum_adj = []
    total_pie_adj = 0

    for (name, value) in name_value:
        if value > value_threshold:
            name_sum_adj.append((name, value))
            total_pie_adj += value

    name_sum_adj.sort(key=itemgetter(1), reverse=True)

    color_discrete_map = {}
    color_no = 0
    names = []
    values = []

    for (name, value) in name_sum_adj:
        names.append(name)
        values.append(value)
        color_discrete_map[name] = COLOR_MAP[color_no % COLOR_MAP_SIZE]
        color_no += 1

    if total_pie_adj < total_filter:
        color_discrete_map[NAME_NONE] = COLOR_MAP_NONE
        names.append(NAME_NONE)
        values.append(total_filter - total_pie)

    return names, values, color_discrete_map


# ------------------------------------------------------------------
# Present the chart: Events per Year by CICTT Codes.
# ------------------------------------------------------------------
def _present_bar_chart(chart_id, chart_title, prep_result):
    """Present the chart: Events per Year by CICTT Codes."""
    names, df_filtered_charts = prep_result

    color_no = 0
    data = []
    details = []

    for name, _name_df in names:
        data.append(
            go.Bar(
                marker={"color": COLOR_MAP[color_no % COLOR_MAP_SIZE]},
                name=name,
                x=df_filtered_charts["year"],
                y=df_filtered_charts[name],
            )
        )
        details.append(name)
        color_no += 1

    fig = go.Figure(
        data,
    )

    fig.update_layout(
        bargap=0.05,
        barmode="stack",
        height=CHOICE_CHARTS_HEIGHT
        if CHOICE_CHARTS_HEIGHT
        else CHOICE_CHARTS_HEIGHT_DEFAULT,
        width=CHOICE_CHARTS_WIDTH
        if CHOICE_CHARTS_WIDTH
        else CHOICE_CHARTS_WIDTH_DEFAULT,
        title=chart_title,
        xaxis={"title": {"text": "Year"}},
        yaxis={
            "title": {"text": "Fatalities" if chart_id in ["fyfp"] else EVENT_TYPE_DESC}
        },
    )

    st.plotly_chart(
        fig,
    )

    if CHOICE_CHARTS_DETAILS:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + 'font-weight: bold;border-radius:2%;">Detailed Chart Data</p>',
            unsafe_allow_html=True,
        )
        details.insert(0, "year")
        st.dataframe(
            df_filtered_charts.loc[
                :,
                details,
            ]
        )
        st.download_button(
            data=_convert_df_2_csv(df_filtered_charts),
            file_name=APP_ID + "_charts_" + chart_id + ".csv",
            help="The download includes the detailed chart data.",
            label="Download the chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present chart: Events per Year by CICTT Codes.
# ------------------------------------------------------------------
def _present_chart_ey_aoc() -> None:
    """Present chart: Events per Year by CICTT Codes."""
    global CHOICE_CHARTS_UG_EY_AOC  # pylint: disable=global-statement

    if CHOICE_CHARTS_TYPE_EY_AOC:
        chart_id = "ey_aoc"
        chart_title = f"Number of {EVENT_TYPE_DESC} per Year by CICTT Codes"
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
                unsafe_allow_html=True,
            )
        with col2:
            CHOICE_CHARTS_UG_EY_AOC = st.checkbox(
                help="Explanations and operating instructions related to this bar chart.",
                key=chart_title,
                label="**User Guide Chart**",
                value=False,
            )
        if CHOICE_CHARTS_UG_EY_AOC:
            user_guide.get_ae1982_chart(
                chart_id,
                chart_title,
            ),
        _present_bar_chart(
            chart_id,
            chart_title,
            _prep_data_charts_ey_aoc(DF_FILTERED),
        )


# ------------------------------------------------------------------
# Present chart: Events per Year by Injury Levels.
# ------------------------------------------------------------------
def _present_chart_ey_il() -> None:
    """Present chart: Events per Year by Injury Levels."""
    global CHOICE_CHARTS_UG_EY_IL  # pylint: disable=global-statement

    chart_id = "ey_il"
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Injury Levels"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_CHARTS_UG_EY_IL = st.checkbox(
            help="Explanations and operating instructions related to this bar chart.",
            key=chart_title,
            label="**User Guide Chart**",
            value=False,
        )
    if CHOICE_CHARTS_UG_EY_IL:
        user_guide.get_ae1982_chart(
            chart_id,
            chart_title,
        ),
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_il(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Required Safety Systems.
# ------------------------------------------------------------------
def _present_chart_ey_rss() -> None:
    """Present chart: Events per Year by Required Safety Systems."""
    global CHOICE_CHARTS_UG_EY_RSS  # pylint: disable=global-statement

    chart_id = "ey_rss"
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Required Safety Systems"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_CHARTS_UG_EY_RSS = st.checkbox(
            help="Explanations and operating instructions related to this bar chart.",
            key=chart_title,
            label="**User Guide Chart**",
            value=False,
        )
    if CHOICE_CHARTS_UG_EY_RSS:
        user_guide.get_ae1982_chart(
            chart_id,
            chart_title,
        ),
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_rss(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Event Types.
# ------------------------------------------------------------------
def _present_chart_ey_t() -> None:
    """Present chart: Events per Year by Event Types."""
    global CHOICE_CHARTS_UG_EY_T  # pylint: disable=global-statement

    chart_id = "ey_t"
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Event Types"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_CHARTS_UG_EY_T = st.checkbox(
            help="Explanations and operating instructions related to this bar chart.",
            key=chart_title,
            label="**User Guide Chart**",
            value=False,
        )
    if CHOICE_CHARTS_UG_EY_T:
        user_guide.get_ae1982_chart(
            chart_id,
            chart_title,
        ),
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_t(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Top Logical Parameters.
# ------------------------------------------------------------------
def _present_chart_ey_tlp() -> None:
    """Present chart: Events per Year by Top Logical Parameters."""
    global CHOICE_CHARTS_UG_EY_TLP  # pylint: disable=global-statement

    chart_id = "ey_tlp"
    chart_title = f"Number of {EVENT_TYPE_DESC} per Year by Top Logical Parameters"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_CHARTS_UG_EY_TLP = st.checkbox(
            help="Explanations and operating instructions related to this bar chart.",
            key=chart_title,
            label="**User Guide Chart**",
            value=False,
        )
    if CHOICE_CHARTS_UG_EY_TLP:
        user_guide.get_ae1982_chart(
            chart_id,
            chart_title,
        ),
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_tlp(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Number of Fatalities per Year by
# Selected FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fy_fp() -> None:
    """Present chart: Number of Fatalities per Year by Selected FAR Operations
    Parts."""
    global CHOICE_CHARTS_UG_FY_FP  # pylint: disable=global-statement

    chart_id = "fy_fp"
    chart_title = "Number of Fatalities per Year by Selected FAR Operations Parts"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_CHARTS_UG_FY_FP = st.checkbox(
            help="Explanations and operating instructions related to this bar chart.",
            key=chart_title,
            label="**User Guide Chart**",
            value=False,
        )
    if CHOICE_CHARTS_UG_FY_FP:
        user_guide.get_ae1982_chart(
            chart_id,
            chart_title,
        ),
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_fy_fp(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present the charts.
# ------------------------------------------------------------------
def _present_charts() -> None:
    """Present the charts."""
    # Events per Year by CICTT Codes
    if CHOICE_CHARTS_TYPE_EY_AOC:
        _present_chart_ey_aoc()

    # Events per Year by Injury Level
    if CHOICE_CHARTS_TYPE_EY_IL:
        _present_chart_ey_il()

    # Events per Year by Required Safety Systems
    if CHOICE_CHARTS_TYPE_EY_RSS:
        _present_chart_ey_rss()

    # Events per Year by Event Types
    if CHOICE_CHARTS_TYPE_EY_T:
        _present_chart_ey_t()

    # Events per Year by Top Level Logical Parameters
    if CHOICE_CHARTS_TYPE_EY_TLP:
        _present_chart_ey_tlp()

    # Fatalities per Year under FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FY_FP:
        _present_chart_fy_fp()

    # Total Events by CICTT Code
    if CHOICE_CHARTS_TYPE_TE_AOC:
        _present_pie_chart(
            f"Total Number of {EVENT_TYPE_DESC} by CICTT Codes",
            _prep_data_charts_te_aoc(DF_FILTERED),
        )

    # Total Events by Highest Injury Levels
    if CHOICE_CHARTS_TYPE_TE_IL:
        _present_pie_chart(
            f"Total Number of {EVENT_TYPE_DESC} by Highest Injury Levels",
            _prep_data_charts_te_il(DF_FILTERED),
        )

    # Total Events by Required Safety Systems
    if CHOICE_CHARTS_TYPE_TE_RSS:
        _present_pie_chart(
            f"Total Number of {EVENT_TYPE_DESC}  by Required Safety Systems",
            _prep_data_charts_te_rss(DF_FILTERED),
        )

    # Total Events by Event Types
    if CHOICE_CHARTS_TYPE_TE_T:
        _present_pie_chart(
            f"Total Number of {EVENT_TYPE_DESC} by Event Types",
            _prep_data_charts_te_t(DF_FILTERED),
        )

    # Total Events by Top Level logical Parameter
    if CHOICE_CHARTS_TYPE_TE_TLP:
        _present_pie_chart(
            f"Total Number of {EVENT_TYPE_DESC}  by Top Level Logical Parameters",
            _prep_data_charts_te_tlp(DF_FILTERED),
        )

    # Total Fatalities under FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TF_FP:
        _present_pie_chart(
            "Total Number of Fatalities by Selected FAR Operations Parts",
            _prep_data_charts_tf_fp(DF_FILTERED),
        )


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data() -> None:
    """Present the filtered data."""
    _print_timestamp("_present_data() - Start")

    if CHOICE_ACTIVE_FILTERS:
        st.warning(CHOICE_ACTIVE_FILTERS_TEXT)
        _print_timestamp("_present_data() - CHOICE_ACTIVE_FILTERS")

    if CHOICE_ABOUT:
        _col1, col2 = st.columns(
            [
                1,
                2,
            ]
        )
        with col2:
            if not MODE_STANDARD:
                extension = " - limited version"
            elif CHOICE_EXTENDED_VERSION:
                extension = " - extended version"
            else:
                extension = " (Standard version)"
            utils.present_about(PG_CONN, APP_ID + extension)
            _print_timestamp("_present_data() - CHOICE_ABOUT")

    if CHOICE_UG_APP:
        user_guide.get_ae1982_app()

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
    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
        + 'font-weight: bold;border-radius:2%;">Profiling of the Filtered io_app_ae1982 data</p>',
        unsafe_allow_html=True,
    )

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
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + 'font-weight: bold;border-radius:2%;">Detailed data from DB view io_app_ae1982</p>',
            unsafe_allow_html=True,
        )
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

    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
        + 'font-weight: bold;border-radius:2%;">Depicting the accidents on a map of the USA</p>',
        unsafe_allow_html=True,
    )

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
            map_style=MAP_STYLE_PREFIX
            + (
                CHOICE_MAP_MAP_STYLE
                if CHOICE_MAP_MAP_STYLE
                else CHOICE_MAP_MAP_STYLE_DEFAULT
            ),  # type: ignore
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
# Present the pie chart.
# ------------------------------------------------------------------
def _present_pie_chart(
    chart_title: str, pie_chart_data: tuple[list[str], list[int], dict[str, str]]
) -> None:
    """Present the pie chart."""
    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
        + f'font-weight: bold;border-radius:2%;">{chart_title}</p>',
        unsafe_allow_html=True,
    )

    names, values, color_discrete_map = pie_chart_data

    fig = px.pie(
        color=names,
        color_discrete_map=color_discrete_map,
        hole=0.3,
        names=names,
        title=chart_title,
        values=values,
    )

    st.plotly_chart(
        fig,
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
        LAST_READING = START_TIME

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
    global CHOICE_ACTIVE_FILTERS_TEXT  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_CICTT_CODES  # pylint: disable=global-statement
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
    global FILTER_LATLONG_ACQ  # pylint: disable=global-statement
    global FILTER_LOGICAL_PARAMETERS_AND  # pylint: disable=global-statement
    global FILTER_LOGICAL_PARAMETERS_OR  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_FROM  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_TO  # pylint: disable=global-statement
    global FILTER_OCCURRENCE_CODES  # pylint: disable=global-statement
    global FILTER_RSS  # pylint: disable=global-statement
    global FILTER_STATE  # pylint: disable=global-statement
    global FILTER_US_AVIATION  # pylint: disable=global-statement

    _print_timestamp("_setup_filter - Start")

    if MODE_STANDARD:
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
    else:
        CHOICE_FILTER_DATA = True
        st.sidebar.markdown("**Filter data:**")

    CHOICE_ACTIVE_FILTERS_TEXT = ""

    FILTER_ACFT_CATEGORIES = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to selected aircraft categories.
        """,
        label="**Aircraft categories:**",
        options=_sql_query_acft_categories(),
    )
    _print_timestamp("_setup_filter - FILTER_ACFT_CATEGORIES - 1")

    if FILTER_ACFT_CATEGORIES:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Aircraft categories**: **`{','.join(FILTER_ACFT_CATEGORIES)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_ACFT_CATEGORIES - 2")

    st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
        max_no_aircraft = _sql_query_max_no_aircraft()
        _print_timestamp("_setup_filter - _sql_query_max_no_aircraft()")

        min_no_aircraft = _sql_query_min_no_aircraft()
        _print_timestamp("_setup_filter - _sql_query_min_no_aircraft()")

        FILTER_NO_AIRCRAFT_FROM, FILTER_NO_AIRCRAFT_TO = st.sidebar.slider(
            help="""
            Number of aircraft involved.
            """,
            label="**Aircraft involved:**",
            min_value=min_no_aircraft,
            max_value=max_no_aircraft,
            value=(min_no_aircraft, max_no_aircraft),
        )

        if (
            FILTER_NO_AIRCRAFT_FROM
            and FILTER_NO_AIRCRAFT_FROM != min_no_aircraft
            or FILTER_NO_AIRCRAFT_TO
            and FILTER_NO_AIRCRAFT_TO != max_no_aircraft
        ):
            # pylint: disable=line-too-long
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Aircraft involved**: between **`{FILTER_NO_AIRCRAFT_FROM}`** and **`{FILTER_NO_AIRCRAFT_TO}`**"
            )
            _print_timestamp(
                "_setup_filter - FILTER_NO_AIRCRAFT_FROM or FILTER_NO_AIRCRAFT_TO"
            )

        st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
        FILTER_CICTT_CODES = st.sidebar.multiselect(
            help="""
            Here, data can be limited to selected CICTT codes.
            """,
            label="**CICTT code(s):**",
            options=_sql_query_cictt_codes(),
        )
        _print_timestamp("_setup_filter - FILTER_CICTT_CODES - 1")

        if FILTER_CICTT_CODES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **CICTT code(s)**: **`{','.join(FILTER_CICTT_CODES)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_CICTT_CODES - 2")

        st.sidebar.markdown("""---""")

    if MODE_STANDARD:
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
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
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
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Event year(s)**: between **`{FILTER_EV_YEAR_FROM}`** and **`{FILTER_EV_YEAR_TO}`**"
        )
        _print_timestamp("_setup_filter - FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO")

    st.sidebar.markdown("""---""")

    if not MODE_STANDARD:
        return

    if CHOICE_EXTENDED_VERSION:
        FILTER_FAR_PARTS = st.sidebar.multiselect(
            help="""
            Under which FAR operations parts the accident was conducted.
            """,
            label="**FAR operations parts:**",
            options=_sql_query_far_parts(),
        )
        _print_timestamp("_setup_filter - FILTER_FAR_PARTS - 1")

        if FILTER_FAR_PARTS:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **FAR operations parts**: **`{','.join(FILTER_FAR_PARTS)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_FAR_PARTS - 2")

        st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
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

        if (
            FILTER_INJ_F_GRND_FROM
            and FILTER_INJ_F_GRND_FROM != 0
            or FILTER_INJ_F_GRND_TO
            and FILTER_INJ_F_GRND_TO != max_inj_f_grnd
        ):
            # pylint: disable=line-too-long
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Fatalities on ground**: between **`{FILTER_INJ_F_GRND_FROM}`** and **`{FILTER_INJ_F_GRND_TO}`**"
            )
            _print_timestamp(
                "_setup_filter - FILTER_INJ_F_GRND_FROM or FILTER_INJ_F_GRND_TO"
            )

    if CHOICE_EXTENDED_VERSION:
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

        if (
            FILTER_INJ_TOT_F_FROM
            and FILTER_INJ_TOT_F_FROM != 0
            or FILTER_INJ_TOT_F_TO
            and FILTER_INJ_TOT_F_TO != max_inj_tot_f
        ):
            # pylint: disable=line-too-long
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Fatalities total**: between **`{FILTER_INJ_TOT_F_FROM}`** and **`{FILTER_INJ_TOT_F_TO}`**"
            )
            _print_timestamp("_setup_filter - FILTER_INJ_TOT_F_TO")

    if (
        FILTER_INJ_F_GRND_FROM
        or FILTER_INJ_F_GRND_TO
        or FILTER_INJ_TOT_F_FROM
        or FILTER_INJ_TOT_F_TO
    ):
        st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
        FILTER_FINDING_CODES = st.sidebar.multiselect(
            help="""
            Here, data can be limited to selected finding codes.
            """,
            label="**Finding code(s):**",
            options=_sql_query_finding_codes(),
        )
        _print_timestamp("_setup_filter - FILTER_FINDING_CODES - 1")

        if FILTER_FINDING_CODES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding code(s)**: **`{','.join(FILTER_FINDING_CODES)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_FINDING_CODES - 2")

        st.sidebar.markdown("""---""")

    FILTER_EV_HIGHEST_INJURY = st.sidebar.multiselect(
        default="FATL",
        help="""
        Here, the data can be limited to selected injury levels.
        Those events are selected whose highest injury level matches.
        """,
        label="**Highest injury level(s):**",
        options=_sql_query_ev_highest_injury(),
    )
    _print_timestamp("_setup_filter - FILTER_EV_HIGHEST_INJURY - 1")

    if FILTER_EV_HIGHEST_INJURY:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Highest injury level(s)**: **`{','.join(FILTER_EV_HIGHEST_INJURY)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_EV_HIGHEST_INJURY - 2")

    st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
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
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Latitude / longitude acquisition**: **`{','.join(FILTER_LATLONG_ACQ)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_LATLONG_ACQ - 2")

        st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
        logical_params_options = [
            CHOICE_CHARTS_LEGEND_LP_SPIN,
            CHOICE_CHARTS_LEGEND_LP_RSS_AIRBORNE,
            CHOICE_CHARTS_LEGEND_LP_ALTITUDE_CONTROLLABLE,
            CHOICE_CHARTS_LEGEND_LP_EMERGENCY,
            CHOICE_CHARTS_LEGEND_LP_ALTITUDE_LOW,
            CHOICE_CHARTS_LEGEND_LP_ATTITUDE,
            CHOICE_CHARTS_LEGEND_LP_RSS_FORCED,
            CHOICE_CHARTS_LEGEND_LP_MIDAIR,
            CHOICE_CHARTS_LEGEND_LP_PILOT,
            CHOICE_CHARTS_LEGEND_LP_RSS_SPIN,
            CHOICE_CHARTS_LEGEND_LP_NARRATIVE,
            CHOICE_CHARTS_LEGEND_LP_RSS_TERRAIN,
        ]

        FILTER_LOGICAL_PARAMETERS_AND = st.sidebar.multiselect(
            help="""
            Logical parameters that are applied when filtering with a logical AND.
            """,
            label="**Logical parameter(s AND):**",
            options=logical_params_options,
        )
        _print_timestamp("_setup_filter - FILTER_LOGICAL_PARAMETERS_AND - 1")

        if FILTER_LOGICAL_PARAMETERS_AND:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + "\n- **Logical parameters (OR)**: **"
                + f"`{','.join(FILTER_LOGICAL_PARAMETERS_AND)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_LOGICAL_PARAMETERS_AND - 2")

        FILTER_LOGICAL_PARAMETERS_OR = st.sidebar.multiselect(
            help="""
            Logical parameters that are applied when filtering with a logical OR.
            """,
            label="**Logical parameter(s OR):**",
            options=logical_params_options,
        )
        _print_timestamp("_setup_filter - FILTER_LOGICAL_PARAMETERS_OR - 1")

        if FILTER_LOGICAL_PARAMETERS_OR:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Logical parameters (OR)**: **`{','.join(FILTER_LOGICAL_PARAMETERS_OR)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_LOGICAL_PARAMETERS_OR - 2")

        st.sidebar.markdown("""---""")

    if CHOICE_EXTENDED_VERSION:
        FILTER_OCCURRENCE_CODES = st.sidebar.multiselect(
            help="""
            Here, the data can be limited to selected occurrence codes.
            """,
            label="**Occurrence code(s):**",
            options=_sql_query_occurrence_codes(),
        )
        _print_timestamp("_setup_filter - FILTER_OCCURRENCE_CODES - 1")

        if FILTER_OCCURRENCE_CODES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Occurrence code(s)**: **`{','.join(FILTER_OCCURRENCE_CODES)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_OCCURRENCE_CODES - 2")

        st.sidebar.markdown("""---""")

    FILTER_RSS = st.sidebar.multiselect(
        help="""
        **High level safety system save requirements.
        """,
        label="**Required safety system(s):**",
        options=[
            CHOICE_CHARTS_LEGEND_RSS_AIRBORNE,
            CHOICE_CHARTS_LEGEND_RSS_FORCED,
            CHOICE_CHARTS_LEGEND_RSS_SPIN,
            CHOICE_CHARTS_LEGEND_RSS_TERRAIN,
        ],
    )
    _print_timestamp("_setup_filter - FILTER_RSS - 1")

    if FILTER_RSS:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Required safety system criteria**: **`{','.join(FILTER_RSS)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_RSS - 2")

    st.sidebar.markdown("""---""")

    FILTER_STATE = st.sidebar.multiselect(
        help="Here, data can be limited to selected U.S. states.",
        label="**State(s) in the US:**",
        options=_sql_query_us_states(),
    )
    _print_timestamp("_setup_filter - FILTER_STATE - 1")

    if FILTER_STATE:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
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
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
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
    global CHOICE_ACTIVE_FILTERS  # pylint: disable=global-statement
    global CHOICE_UG_APP  # pylint: disable=global-statement
    global EVENT_TYPE_DESC  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement

    FILTER_EV_YEAR_FROM = FILTER_EV_YEAR_FROM if FILTER_EV_YEAR_FROM else 1982
    FILTER_EV_YEAR_TO = (
        FILTER_EV_YEAR_TO if FILTER_EV_YEAR_TO else datetime.date.today().year - 1
    )

    if FILTER_EV_TYPE == ["ACC"]:
        EVENT_TYPE_DESC = "Accidents"
    elif FILTER_EV_TYPE == ["INC"]:
        EVENT_TYPE_DESC = "Incidents"
    else:
        EVENT_TYPE_DESC = "Events"

    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        + f'font-weight: bold;border-radius:2%;">Aviation {EVENT_TYPE_DESC} between '
        + f"{FILTER_EV_YEAR_FROM} and {FILTER_EV_YEAR_TO}</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    if CHOICE_FILTER_DATA:
        with col1:
            CHOICE_ACTIVE_FILTERS = st.checkbox(
                help="Show the selected filter conditions.",
                label="**Show Active Filter(s)**",
                value=False,
            )

    with col2:
        CHOICE_ABOUT = st.checkbox(
            help="Software owner and release information.",
            label="**About this Application**",
            value=False,
        )

    with col3:
        CHOICE_UG_APP = st.checkbox(
            help="Explanations and operating instructions related to the whole application.",
            label="**User Guide Application**",
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
    global CHOICE_CHARTS_TYPE_EY_AOC  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_IL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_RSS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_T  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_TLP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_FY_FP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_AOC  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_IL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_RSS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_T  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_TLP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_FP  # pylint: disable=global-statement
    global CHOICE_CHARTS_WIDTH  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_EXTENDED_VERSION  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_MAP_RADIUS  # pylint: disable=global-statement

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    if MODE_STANDARD:
        CHOICE_EXTENDED_VERSION = st.sidebar.checkbox(
            help="The extended version has more complex filtering and processing options.",
            label="**Extended Version**",
            value=False,
        )

        st.sidebar.markdown("""---""")

    CHOICE_CHARTS = st.sidebar.checkbox(
        help="Accidents or fatalities per year (after filtering the data).",
        label="**Show charts**",
        value=True,
    )

    if CHOICE_CHARTS:
        if MODE_STANDARD:
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

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_EY_AOC = st.sidebar.checkbox(
                help="Events per year by CICTT codes (after filtering the data).",
                label="Events per Year by CICTT Codes",
                value=False,
            )
            CHOICE_CHARTS_TYPE_EY_T = st.sidebar.checkbox(
                help="Events per year by event types (after filtering the data).",
                label="Events per Year by Event Types",
                value=False,
            )
            CHOICE_CHARTS_TYPE_EY_IL = st.sidebar.checkbox(
                help="Events per year by highest injury level (after filtering the data).",
                label="Events per Year by Highest Injury Levels",
                value=False,
            )
            CHOICE_CHARTS_TYPE_EY_RSS = st.sidebar.checkbox(
                help="Events per year by required security systems (after filtering the data).",
                label="Events per Year by Required Security Systems",
                value=False,
            )
            CHOICE_CHARTS_TYPE_EY_TLP = st.sidebar.checkbox(
                help="Events per year by top level logical parameters (after filtering the data).",
                label="Events per Year by Top Level Logical Parameters",
                value=False,
            )

        CHOICE_CHARTS_TYPE_FY_FP = st.sidebar.checkbox(
            help="Fatalities per year by selected FAR Operations Parts (after filtering the data).",
            label="Fatalities per Year under FAR Operations Parts",
            value=True,
        )

        st.sidebar.markdown("""---""")

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_TE_AOC = st.sidebar.checkbox(
                help="Total events by CICTT codes (after filtering the data).",
                label="Total Events by CICTT Codes",
                value=False,
            )
            CHOICE_CHARTS_TYPE_TE_T = st.sidebar.checkbox(
                help="Total events by event types (after filtering the data).",
                label="Total Events by Event Types",
                value=False,
            )
            CHOICE_CHARTS_TYPE_TE_IL = st.sidebar.checkbox(
                help="Total events by highest injury levels (after filtering the data).",
                label="Total Events by Highest Injury Levels",
                value=False,
            )
            CHOICE_CHARTS_TYPE_TE_RSS = st.sidebar.checkbox(
                help="Total events by required safety systems (after filtering the data).",
                label="Total Events by Required Safety Systems",
                value=False,
            )
            CHOICE_CHARTS_TYPE_TE_TLP = st.sidebar.checkbox(
                help="Total events by top level logical parameters (after filtering the data).",
                label="Total Events by Top Level Logical Parameters",
                value=False,
            )

        CHOICE_CHARTS_TYPE_TF_FP = st.sidebar.checkbox(
            help="Total fatalities by selected FAR operations parts (after filtering the data).",
            label="Total Fatalities under FAR Operations Parts",
            value=True,
        )

    st.sidebar.markdown("""---""")

    if MODE_STANDARD:
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

    if MODE_STANDARD:
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
        if MODE_STANDARD:
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
            label="Event radius in meters",
            help="Radius for displaying the events - " + "default value is 2 miles.",
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
         WHERE acft_category IS NOT NULL;
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of CICTT codes.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_cictt_codes() -> list[str]:
    """Execute a query that returns a list of CICTT codes.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(cictt_code, ',' ORDER BY cictt_code)
          FROM io_aviation_occurrence_categories;
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
         WHERE ev_highest_injury IS NOT NULL;
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
         WHERE ev_type IS NOT NULL;
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
         WHERE far_part IS NOT NULL;
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
         WHERE latlong_acq IS NOT NULL;
        """
        )
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
# Determine the maximum number of involved aircraft.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_max_no_aircraft() -> int:
    """Determine the maximum number of involved aircraft.

    Returns:
        int: Maximum number of involved aircraft.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MAX(no_aircraft)
          FROM io_app_ae1982;
        """
        )
        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Determine the minimum number of involved aircraft.
# ------------------------------------------------------------------
@st.experimental_memo
def _sql_query_min_no_aircraft() -> int:
    """Determine the minimum number of involved aircraft.

    Returns:
        int: Maximum number of involved aircraft.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MIN(no_aircraft)
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
         WHERE country  = 'USA';
        """
        )
        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
def _streamlit_flow() -> None:
    """Streamlit flow."""
    global DF_FILTERED  # pylint: disable=global-statement
    global MODE_STANDARD  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement
    global START_TIME  # pylint: disable=global-statement
    global DF_UNFILTERED  # pylint: disable=global-statement

    # Start time measurement.
    START_TIME = time.time_ns()

    if "MODE_STANDARD" in st.session_state:
        MODE_STANDARD = st.session_state["MODE_STANDARD"]
    else:
        mode = utils.get_args()
        print(f"command line argument mode={mode}")
        MODE_STANDARD = bool(mode == "Std")
        st.session_state["MODE_STANDARD"] = MODE_STANDARD

    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png",
        page_title="ae1982 by IO-Aero",
    )

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
            FILTER_CICTT_CODES,
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
            FILTER_LATLONG_ACQ,
            FILTER_LOGICAL_PARAMETERS_AND,
            FILTER_LOGICAL_PARAMETERS_OR,
            FILTER_NO_AIRCRAFT_FROM,
            FILTER_NO_AIRCRAFT_TO,
            FILTER_OCCURRENCE_CODES,
            FILTER_RSS,
            FILTER_STATE,
            FILTER_US_AVIATION,
        )
        _print_timestamp("_apply_filter()")

    _present_data()
    _print_timestamp("_present_data()")

    # Stop time measurement.
    print(
        str(datetime.datetime.now())
        + f" {f'{time.time_ns() - START_TIME:,}':>20} ns - Total runtime for application "
        + APP_ID,
        flush=True,
    )


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

_streamlit_flow()
