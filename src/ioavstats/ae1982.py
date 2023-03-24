# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Aviation Event Analysis."""
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
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from psycopg2.extensions import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore
from ydata_profiling import ProfileReport  # type: ignore

# SettingWithCopyWarning
pd.options.mode.chained_assignment: str | None = None  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "ae1982"

CHARTS_LEGEND_N_A = "n/a"
CHARTS_LEGEND_N_A_DESC = "no data"
CHARTS_LEGEND_THRESHOLD = "below threshold"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_ABOUT: bool | None = None
CHOICE_ACTIVE_FILTERS: bool | None = None
CHOICE_ACTIVE_FILTERS_TEXT: str = ""

CHOICE_CHARTS_LEGEND_IL_FATAL = "fatal"
CHOICE_CHARTS_LEGEND_IL_MINOR = "minor"
CHOICE_CHARTS_LEGEND_IL_NONE = "none"
CHOICE_CHARTS_LEGEND_IL_N_A = CHARTS_LEGEND_N_A
CHOICE_CHARTS_LEGEND_IL_SERIOUS = "serious"
CHOICE_CHARTS_LEGEND_NAME_NONE = "None"
CHOICE_CHARTS_LEGEND_SFP_091X = "General Operations (Parts 091x)"
CHOICE_CHARTS_LEGEND_SFP_121 = "Regular Scheduled Air Carriers (Parts 121)"
CHOICE_CHARTS_LEGEND_SFP_135 = "Charter Type Services (Parts 135)"
CHOICE_CHARTS_LEGEND_SFP_OTHER = "Other FAR Operations Parts"
CHOICE_CHARTS_LEGEND_T_ACC = "Accident"
CHOICE_CHARTS_LEGEND_T_INC = "Incident"

CHOICE_CHARTS_TYPE_EY_AOC: bool | None = None
CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_EY_IL: bool | None = None
CHOICE_CHARTS_TYPE_EY_PSS: bool | None = None
CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_EY_T: bool | None = None
CHOICE_CHARTS_TYPE_EY_TLP: bool | None = None
CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_FY_FP: bool | None = None
CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_FY_SFP: bool | None = None
CHOICE_CHARTS_TYPE_N_AOC: list[tuple[str, str]] = []
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
    (
        CHOICE_CHARTS_LEGEND_IL_N_A,
        CHARTS_LEGEND_N_A,
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
CHOICE_CHARTS_TYPE_N_SFP: list[tuple[str, str]] = [
    (
        CHOICE_CHARTS_LEGEND_SFP_091X,
        "is_far_part_091x",
    ),
    (
        CHOICE_CHARTS_LEGEND_SFP_135,
        "is_far_part_135",
    ),
    (
        CHOICE_CHARTS_LEGEND_SFP_121,
        "is_far_part_121",
    ),
]
CHOICE_CHARTS_TYPE_TE_AOC: bool | None = None
CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TE_IL: bool | None = None
CHOICE_CHARTS_TYPE_TE_PSS: bool | None = None
CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TE_T: bool | None = None
CHOICE_CHARTS_TYPE_TE_TLP: bool | None = None
CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TF_FP: bool | None = None
CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TF_SFP: bool | None = None

CHOICE_DATA_GRAPHS_YEARS: bool | None = None
CHOICE_DATA_GRAPHS_TOTALS: bool | None = None
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None

CHOICE_EXTENDED_VERSION: bool | None = None

CHOICE_FILTER_DATA: bool | None = None

CHOICE_HORIZONTAL_BAR_CHARTS: bool | None = None

CHOICE_MAP: bool | None = None
CHOICE_MAP_MAP_STYLE: str | None = None
CHOICE_MAP_MAP_STYLE_DEFAULT: str = "outdoors-v12"
CHOICE_MAP_RADIUS: float | None = 1609.347 * 2

CHOICE_PIE_CHARTS: bool | None = None

CHOICE_TOTALS_CHARTS_DETAILS: bool | None = None
CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS: bool | None = None
CHOICE_TOTALS_CHARTS_HEIGHT: float | None = None
CHOICE_TOTALS_CHARTS_HEIGHT_DEFAULT: float = 500
CHOICE_TOTALS_CHARTS_WIDTH: float | None = None
CHOICE_TOTALS_CHARTS_WIDTH_DEFAULT: float = 1000

CHOICE_UG_APP: bool | None = None
CHOICE_UG_DATA_PROFILE: bool | None = None
CHOICE_UG_DETAILS: bool | None = None
CHOICE_UG_MAP: bool | None = None
CHOICE_UG_YEARS_CHARTS_EY_AOC: bool | None = None
CHOICE_UG_YEARS_CHARTS_EY_IL: bool | None = None
CHOICE_UG_YEARS_CHARTS_EY_PSS: bool | None = None
CHOICE_UG_YEARS_CHARTS_EY_T: bool | None = None
CHOICE_UG_YEARS_CHARTS_EY_TLP: bool | None = None
CHOICE_UG_YEARS_CHARTS_FY_FP: bool | None = None
CHOICE_UG_YEARS_CHARTS_FY_SFP: bool | None = None

CHOICE_YEARS_CHARTS_DETAILS: bool | None = None
CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS: bool | None = None
CHOICE_YEARS_CHARTS_DETAILS_TOTAL_ROWS: bool | None = None
CHOICE_YEARS_CHARTS_HEIGHT: float | None = None
CHOICE_YEARS_CHARTS_HEIGHT_DEFAULT: float = 500
CHOICE_YEARS_CHARTS_WIDTH: float | None = None
CHOICE_YEARS_CHARTS_WIDTH_DEFAULT: float = 1000

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
DF_FILTERED_ROWS = 0
DF_UNFILTERED: DataFrame = DataFrame()
DF_UNFILTERED_ROWS = 0

EVENT_TYPE_DESC: str

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_CICTT_CODES: list[str] = []
FILTER_EV_HIGHEST_INJURY: list[str] = []
FILTER_EV_HIGHEST_INJURY_DEFAULT: list[str] = ["fatal"]
FILTER_EV_TYPE: list[str] = []
FILTER_EV_TYPE_DEFAULT = [CHOICE_CHARTS_LEGEND_T_ACC]
FILTER_EV_YEAR_INCOMPATIBLE = 2008
FILTER_EV_YEAR_FROM: int | None = None
FILTER_EV_YEAR_TO: int | None = None
FILTER_FAR_PARTS: list[str] = []
FILTER_FAR_PARTS_DEFAULT = [
    "091",
    "091F",
    "091K",
    "121",
    "135",
]
FILTER_FINDING_CODES: list[str] = []
FILTER_INJ_F_GRND_FROM: int | None = None
FILTER_INJ_F_GRND_TO: int | None = None
FILTER_INJ_TOT_F_FROM: int | None = None
FILTER_INJ_TOT_F_TO: int | None = None
FILTER_LATLONG_ACQ: list[str] = []
FILTER_NO_AIRCRAFT_FROM: int | None = None
FILTER_NO_AIRCRAFT_TO: int | None = None
FILTER_OCCURRENCE_CODES: list[str] = []
FILTER_PREVENTABLE_EVENTS: list[str] = []
FILTER_TLL_PARAMETERS: list[str] = []
FILTER_US_AVIATION: list[str] = []
FILTER_US_AVIATION_COUNTRY = "Event Country USA"
FILTER_US_AVIATION_DEPARTURE = "US Departure"
FILTER_US_AVIATION_DESTINATION = "US Destination"
FILTER_US_AVIATION_OPERATOR = "US Operator"
FILTER_US_AVIATION_OWNER = "US Owner"
FILTER_US_AVIATION_REGISTRATION = "US Registration"
FILTER_US_AVIATION_DEFAULT: list[str] = [
    FILTER_US_AVIATION_COUNTRY,
    FILTER_US_AVIATION_DEPARTURE,
    FILTER_US_AVIATION_DESTINATION,
    FILTER_US_AVIATION_OPERATOR,
    FILTER_US_AVIATION_OWNER,
    FILTER_US_AVIATION_REGISTRATION,
]
FILTER_US_STATES: list[str] = []

FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

HOST_CLOUD: bool | None = None

IS_TIMEKEEPING = False

LAST_READING: int = 0
# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"

MAP_STYLE_PREFIX = "mapbox://styles/mapbox/"
MODE_STANDARD: bool | None = None

OPTIONS_EV_HIGHEST_INJURY = {
    "FATL": "fatal",
    "MINR": "minor",
    "NONE": "none",
    "SERS": "serious",
    "UNKN": "unknown",
    "n/a": CHARTS_LEGEND_N_A_DESC,
}

OPTIONS_EV_TYPE = {
    "ACC": "Accident",
    "INC": "Incident",
    "n/a": CHARTS_LEGEND_N_A_DESC,
}

OPTIONS_LATLONG_ACQ = {
    "CITY": "computed on US city basis",
    "COUN": "computed on US country basis",
    "ERRA": "invalid latitude",
    "ERRO": "invalid longitude",
    "EST": "estimated (NTSB)",
    "LALO": "computed on lat. & long. basis",
    "LOLA": "computed on lat. & long. basis after swap",
    "MEAS": "measured (NTSB)",
    "NONE": "none",
    "NREC": "not recorded (NTSB)",
    "STAT": "computed on US state basis",
    "ZIP": "computed on US zip code basis",
}

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
) -> DataFrame:
    """Filter the data frame."""
    _print_timestamp(f"_apply_filter() - {len(df_unfiltered):>6} - Start")

    df_filtered = df_unfiltered

    # noinspection PyUnboundLocalVariable
    if FILTER_ACFT_CATEGORIES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["acft_categories"].apply(
                lambda x: bool(set(x) & set(FILTER_ACFT_CATEGORIES))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_ACFT_CATEGORIES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_CICTT_CODES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["cictt_codes"].apply(
                lambda x: x in FILTER_CICTT_CODES  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_CICTT_CODES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_EV_HIGHEST_INJURY:
        # noinspection PyUnboundLocalVariable
        filter_ev_highest_injury_key = []
        for selected in FILTER_EV_HIGHEST_INJURY:
            for key, data in OPTIONS_EV_HIGHEST_INJURY.items():
                if selected == data:
                    filter_ev_highest_injury_key.append(key)
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["ev_highest_injury"].isin(filter_ev_highest_injury_key))
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_EV_HIGHEST_INJURY"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_EV_TYPE:
        # noinspection PyUnboundLocalVariable
        filter_ev_type_key = []
        for selected in FILTER_EV_TYPE:
            for key, data in OPTIONS_EV_TYPE.items():
                if selected == data:
                    filter_ev_type_key.append(key)
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[(df_filtered["ev_type"].isin(filter_ev_type_key))]
        _print_timestamp(f"_apply_filter() - {len(df_filtered):>6} - FILTER_EV_TYPE")

    # noinspection PyUnboundLocalVariable
    if FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= FILTER_EV_YEAR_FROM)
            & (df_filtered["ev_year"] <= FILTER_EV_YEAR_TO)
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_EV_YEAR_FROM/TO"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FAR_PARTS:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["far_parts"].apply(
                lambda x: x in FILTER_FAR_PARTS  # type: ignore
            )
        ]
        _print_timestamp(f"_apply_filter() - {len(df_filtered):>6} - FILTER_FAR_PARTS")

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDING_CODES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["finding_codes"].apply(
                lambda x: bool(set(x) & set(FILTER_FINDING_CODES))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDING_CODES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_INJ_F_GRND_FROM or FILTER_INJ_F_GRND_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["inj_f_grnd"] >= FILTER_INJ_F_GRND_FROM)
            & (df_filtered["inj_f_grnd"] <= FILTER_INJ_F_GRND_TO)
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_INJ_F_GRND_FROM/TO"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_INJ_TOT_F_FROM or FILTER_INJ_TOT_F_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["inj_tot_f"] >= FILTER_INJ_TOT_F_FROM)
            & (df_filtered["inj_tot_f"] <= FILTER_INJ_TOT_F_TO)
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_INJ_TOT_F_FROM/TO"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_LATLONG_ACQ:
        filter_latlong_acq_key = []
        for selected in FILTER_LATLONG_ACQ:
            for key, data in OPTIONS_LATLONG_ACQ.items():
                if selected == data:
                    filter_latlong_acq_key.append(key)
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["latlong_acq"].isin(filter_latlong_acq_key))
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_LATLONG_ACQ"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_NO_AIRCRAFT_FROM or FILTER_NO_AIRCRAFT_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["no_aircraft"] >= FILTER_NO_AIRCRAFT_FROM)
            & (df_filtered["no_aircraft"] <= FILTER_NO_AIRCRAFT_TO)
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - filter_no_aircraft_from/to"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_OCCURRENCE_CODES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            df_filtered["occurrence_codes"].apply(
                lambda x: bool(set(x) & set(FILTER_OCCURRENCE_CODES))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_OCCURRENCE_CODES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_PREVENTABLE_EVENTS:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["preventable_events"].isin(FILTER_PREVENTABLE_EVENTS))
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_PREVENTABLE_EVENTS"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_TLL_PARAMETERS:
        df_filtered = df_filtered.loc[
            (df_filtered["tll_parameters"].isin(FILTER_TLL_PARAMETERS))
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_LOGICAL_PARAMETERS_AND"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_US_AVIATION:
        df_filtered = _apply_filter_us_aviation(df_filtered, FILTER_US_AVIATION)
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_US_AVIATION"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_US_STATES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (df_filtered["state"].isin(_get_prepared_us_states(FILTER_US_STATES)))
        ]
        _print_timestamp(f"_apply_filter() - {len(df_filtered):>6} - FILTER_STATE")

    _print_timestamp(f"_apply_filter() - {len(df_filtered):>6} - End")

    return df_filtered


# ------------------------------------------------------------------
# Filter the data frame - Incompatible data.
# ------------------------------------------------------------------
def _apply_filter_incompatible(df_filtered):
    if FILTER_EV_YEAR_FROM < FILTER_EV_YEAR_INCOMPATIBLE:
        year_from = FILTER_EV_YEAR_INCOMPATIBLE
    else:
        year_from = FILTER_EV_YEAR_FROM

    if FILTER_EV_YEAR_TO < FILTER_EV_YEAR_INCOMPATIBLE:
        year_to = FILTER_EV_YEAR_INCOMPATIBLE
    else:
        year_to = FILTER_EV_YEAR_TO

    if year_from != FILTER_EV_YEAR_FROM or year_to != FILTER_EV_YEAR_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= year_from) & (df_filtered["ev_year"] <= year_to)
        ]

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
def _convert_df_2_csv(dataframe: DataFrame) -> bytes:
    """Convert a dataframe to csv data."""
    return dataframe.to_csv().encode("utf-8")


# ------------------------------------------------------------------
# Read the data.
# ------------------------------------------------------------------
@st.cache_resource
def _get_data() -> DataFrame:
    """Read the data."""
    _print_timestamp("_get_data() - Start")

    return pd.read_sql(
        con=_get_engine(),
        sql="""
            SELECT ev_id,
                   acft_categories,
                   cictt_codes,
                   country,
                   dec_latitude,
                   dec_longitude,
                   ev_highest_injury,
                   ev_type,
                   ev_year,
                   far_parts,
                   finding_codes,
                   inj_f_grnd,
                   inj_tot_f,
                   is_dest_country_usa,
                   is_dprt_country_usa,
                   is_far_part_091x,
                   is_far_part_121,
                   is_far_part_135,
                   is_oper_country_usa,
                   is_owner_country_usa,
                   is_regis_country_usa,
                   latlong_acq,
                   no_aircraft,
                   ntsb_no,
                   occurrence_codes,
                   preventable_events,
                   state,
                   tll_parameters
             FROM io_app_ae1982
            ORDER BY ev_id;
    """,
    )


# ------------------------------------------------------------------
# Create a simple user PostgreSQL database engine.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def _get_engine() -> Engine:
    """Create a simple user PostgreSQL database engine."""
    print(
        f"[engine  ] User connect request host={SETTINGS.postgres_host} "
        + f"port={SETTINGS.postgres_connection_port} "
        + f"dbname={SETTINGS.postgres_dbname} "
        + f"user={SETTINGS.postgres_user_guest}"
    )

    return create_engine(
        f"postgresql://{SETTINGS.postgres_user_guest}:"
        + f"{SETTINGS.postgres_password_guest}@"
        + f"{SETTINGS.postgres_host}:"
        + f"{SETTINGS.postgres_connection_port}/"
        + f"{SETTINGS.postgres_dbname}",
    )


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def _get_postgres_connection() -> connection:
    """Create a PostgreSQL connection."""
    print(
        f"[psycopg2] User connect request host={SETTINGS.postgres_host} "
        + f"port={SETTINGS.postgres_connection_port} "
        + f"dbname={SETTINGS.postgres_dbname} "
        + f"user={SETTINGS.postgres_user_guest}"
    )

    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Prepare the US states.
# ------------------------------------------------------------------
def _get_prepared_us_states(list_in: list) -> list[str]:
    list_out = []

    for elem in list_in:
        (_, code) = elem.split(" - ")
        list_out.append(code)

    return list_out


# ------------------------------------------------------------------
# Creates the user guide for the whole application.
# ------------------------------------------------------------------
def _get_user_guide_app() -> None:
    """Creates the user guide for the whole application."""
    text = """
#### User guide: ae1982 Application
"""

    if not MODE_STANDARD:
        text += """
**Important**: You are using a very limited version of this application. 
You are welcome to request the use of the free full version of this application [here](https://www.io-aero.com/analytics) on IO-Aero's website.
        """

    text += f"""
The **ae1982** application allows you to perform data analysis tasks on aviation accident and incident data provided by 
[NTSB]( https://www.ntsb.gov/Pages/home.aspx).
The National Transportation Safety Board (NTSB) is an independent Federal agency charged by Congress with investigating 
every civil aviation accident in the United States and significant accidents in other modes of transportation – railroad, 
highway, marine and pipeline.
For each aviation accident and incident, the NTSB provides the relevant data in the form of MS Access databases.

The databases provided on the [NTSB website](https://data.ntsb.gov/avdata) come in three versions:
- **Pre2008**: contains all data for events that occurred before the year 2008,
- **avall**: on the first of each month, the data for all events since 2008 are made available here,
- **up[01|08|15|22][JAN|...|DEC]**: at the 1st, 8th, 15th and 22nd of each month these update files contain the changes
since the previous update file.

The **ae1982** application processes data regarding
- the events (`events`),
- the event sequences (`events_sequence`),
- the aircraft involved (`aircraft`),
- the reports of involved parties (`narratives`), and
- the findings (`findings`).

The **ae1982** application provides the following tools:

- **Filter**: A large number of filter options allow the evaluation of the data with any granularity,
- **Data Graphs - Years**: Provides graphical analysis options for year-based analysis,
- **Data Graphs - Totals**: Provides graphical evaluation options for total summaries,
- **Data Profiles**: Allows detailed analysis of data characteristics,
- **Detailed Data**: Shows the detailed data involved,
- **Map**: Shows the event locations on a map. 

Where appropriate, the **ae1982** application allows you to print the displayed graphics or download detailed data in **csv** format.

Further information on the **ae1982** application can be found [here]({LINK_GITHUB_PAGES}).

If you encounter any problem in the application, documentation or data, we would appreciate it if you would notify us 
[here](https://github.com/io-aero/io-avstats-shared/issues) so that we can make any necessary correction. 
Also suggestions for improvement or enhancements are welcome. 
"""

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for years charts.
# ------------------------------------------------------------------
def _get_user_guide_chart(
    chart_id: str,
    chart_title: str,
) -> None:
    """Creates the user guide for years charts."""
    text = _get_user_guide_chart_header(
        chart_id,
        chart_title,
    )

    match chart_id:
        case "ey_aoc" | "te_aoc":
            text += """
##### Data basis

- In the database table **events_sequence** there are the columns **defining_code** and **eventsoe_no**. 
- The values from **eventsoe_no** are used to determine the CICTT code in case **defining_code** equals TRUE via the tables 
**io_sequence_of_events** and **io_aviation_occurrence_categories**. 
- Depending on the number of aircraft involved in the event, several rows may be assigned to the same event in the 
**events_sequence** table. However, this is only critical if it results in different CICTT codes for the same event.

##### Possible double counting since 2008 as of 02/01/2013

```
ev_id          ev_year    aircraft_key    eventsoe_no
20080505X00589    2008    1               200
20080505X00589    2008    2               230
20080829X01354    2008    1               260
20080829X01354    2008    2               100
20090202X21409    2009    1               250
20090202X21409    2009    2               490
20091010X63931    2009    1               250
20091010X63931    2009    2               240
20100317X00948    2010    1               260
20100317X00948    2010    2               070
20100704X92306    2010    1               380
20100704X92306    2010    2               200
20100803X25950    2010    1               200
20100803X25950    2010    2               900
20101022X34140    2010    1               190
20101022X34140    2010    2               100
20101022X34140    2010    3               100
20110904X00636    2011    1               250
20110904X00636    2011    2               440
20111019X85758    2011    1               900
20111019X85758    2011    2               260
20120523X33839    2012    1               230
20120523X33839    2012    2               200
20120529X21628    2012    1               230
20120529X21628    2012    2               200
20120705X51659    2012    1               320
20120705X51659    2012    2               900
20120811X13221    2012    1               000
20120811X13221    2012    2               900
20121027X42304    2012    1               230
20121027X42304    2012    2               200
20121118X14342    2012    1               220
20121118X14342    2012    2               200
20140425X84104    2014    1               100
20140425X84104    2014    2               260
20150210X11721    2015    1               230
20150210X11721    2015    2               200
20150416X33824    2015    1               260
20150416X33824    2015    2               320
20150508X60256    2015    1               230
20150508X60256    2015    2               200
20151123X43413    2015    1               200
20151123X43413    2015    2               402
20160413X30204    2016    1               320
20160413X30204    2016    2               100
20160413X94401    2016    1               320
20160413X94401    2016    2               070
20160418X44917    2016    1               100
20160418X44917    2016    2               260
20171019X45158    2017    1               200
20171019X45158    2017    2               490
20180403X00427    2018    1               200
20180403X00427    2018    2               490
20200603X55158    2019    1               080
20200603X55158    2019    2               200
20201023102180    2020    2               230
20201030102217    2020    2               230
20210219102650    2021    2               900
20210311102742    2021    2               333
20210726103541    2021    1               200
20210726103541    2021    2               270
20210822103737    2021    2               333
20220111104514    2022    1               200
20220111104514    2022    2               900
20220309104755    2022    2               240
20220818105763    2022    2               250
20220826105805    2022    2               341
20221121106336    2022    1               200
20221121106336    2022    2               250
```
            """
        case "ey_il" | "te_il":
            text += """
##### Data basis

- In the database table **events** there is a column **ev_highest_injury** which contains the highest injury level per event. 
- The available database categories are **`FATL`** (fatal injury), **`MINR`** (minor injury), **`NONE`** (no injury) and **`SERS`** (serious injury). 
- If there is no information about the injuries, then the event appears in the category **`n/a`** (not available).
            """
        case "ey_pss" | "te_pss":
            text += """
##### Data basis

- **Airborne Collision Avoidance**: Accident was a mid-air collision
- **Forced landing**: Aircraft in degraded control state ? Aircraft is pitch/roll controllable
- **Spin / stall prevention and recovery**: Aircraft is pitch/roll controllable ? Aircraft in aerodynamic spin or stall
- **Terrain collision avoidance**: Aircraft altitude too low ? Aircraft is pitch/roll controllable ? Aircraft can climb

- **not available**: None of the criteria listed above
"""
        case "ey_t" | "te_t":
            text += """
##### Data basis

- In the database table **events** there is a column **ev_type** which contains the type of the event. 
- The available database categories are **`ACC`** (Accident) and **`INC`** (Incident). 
- If there is no information about the event type, then the event appears in the category **`n/a`** (not available).
                    """
        case "ey_tlp" | "te_tlp":
            text += """
##### Data basis

- **Aerodynamic spin / stall**: [Angle of attack ? Aerodynamic stall/spin ? (Loss of control in flight ? “Stall in narrative”)] ?¬Controlled flight into terrain/obj (CFIT) ?¬Collision avoidance alert
- **Airborne Collision Avoidance**: Accident was a mid-air collision
- **Aircraft can climb**: ¬(Aircraft power plant ? Fuel system ? Engine out control ? Ice/rain protection system ? Fuel ? Emergency descent ? Fuel contamination ? Fuel exhaustion ? Fuel related ? Fuel starvation ? Loss of engine power (partial) ? Loss of engine power (total) ? Loss of lift ? Off field or emergency landing ? Powerplant/sys comp malf/fail ? Uncontained engine failure ? Main rotor system ? Propeller system) ? ¬ “Aerodynamic stall/spin”
- **Aircraft has degraded control failure**: (Aircraft power plant ? Fuel system ? Engine out control ? Ice/rain protection system ? Fuel ? Emergency descent ? Fuel contamination ? Fuel exhaustion ? Fuel related ? Fuel starvation ? Loss of engine power (partial) ? Loss of engine power (total) ? Loss of lift ? Off field or emergency landing ? Powerplant/sys comp malf/fail ? Uncontained engine failure ? Main rotor system ? Propeller system) ? “Attitude is controllable”
- **Altitude too low**: [(Object/animal/substance ?¬Birdstrike) ? Terrain ? Altitude ? Descent rate ? Descent/approach/glide path ? Approach-IFR final approach ? Initial climb ? Maneuvering-low alt flying ? Collision avoidance alert ? Controlled flight into terr/obj (CFIT) ? Low altitude operation/event] ?¬ Mid-air collision ?¬ “Aerodynamic stall/spin”
- **Attitude is controllable**: ¬(Conditions/weather phenomena (general) ? Turbulence ? Dust devil/whirlwind ? Microburst ? Updraft ? Aircraft wake turb encounter ? Downdraft ? Gusts ? High wind ? Windshear ? Empennage structure ? Wing structure ? Conducive to structural icing ? Aircraft structural failure ? Flight control sys malf/fail ? Mast bumping ? Structural icing ? Part(s) separation from AC ? CG or Weight Distribution)
- **Forced landing**: Aircraft in degraded control state ? Aircraft is pitch/roll controllable
- **Midair collision**: Accident was a mid-air collision
- **Pilot is able to perform maneuver**: ¬(Impairment/incapacitation ? Visual function)
- **Spin / stall prevention and recovery**: Aircraft is pitch/roll controllable ? Aircraft in aerodynamic spin or stall
- **Stall in narrative**: Stall is mentioned in the narrative.
- **Terrain collision avoidance**: Aircraft altitude too low ? Aircraft is pitch/roll controllable ? Aircraft can climb

- **not available**: None of the criteria listed above
"""
        case "fy_fp" | "tf_fp":
            text += """
##### Data basis

- In the database table **aircraft** there is the column **far_part** which contains the FAR operations parts.
- In the database table **events** there is a column **inj_tot_f** which contains the number of fatalities per event.
- Several FAR operations parts can be assigned to the same event, depending on the number of aircraft involved. However, this is only critical if the FAR operation parts are different.

##### Possible double counting since 2008 as of 02/01/2013

```
ev_id         |ev_year|aircraft_key|far_part|inj_tot_f|
--------------+-------+------------+--------+---------+
20090808X42846|   2009|           1|091     |        9|
20090808X42846|   2009|           2|135     |        9|
20111004X45824|   2011|           1|NUSN    |        1|
20111004X45824|   2011|           2|        |        1|
20150707X22207|   2015|           1|091     |        2|
20150707X22207|   2015|           2|ARMF    |        2|
20160831X62719|   2016|           1|135     |        5|
20160831X62719|   2016|           2|091     |        5|
20180107X10632|   2017|           1|NUSN    |        1|
20180107X10632|   2017|           2|NUSC    |        1|
20180614X22730|   2018|           1|091     |        1|
20180614X22730|   2018|           2|135     |        1|
20180804X53521|   2018|           1|UNK     |        1|
20180804X53521|   2018|           2|PUBU    |        1|
20190826X90719|   2019|           1|NUSC    |        7|
20190826X90719|   2019|           2|NUSN    |        7|
20200731X11938|   2020|           1|135     |        7|
20200731X11938|   2020|           2|091     |        7|
20200827X15154|   2020|           1|135     |        2|
20200827X15154|   2020|           2|091     |        2|
20210715103483|   2020|           1|NUSN    |        5|
20210715103483|   2020|           2|129     |        5|
20211221104432|   2021|           1|135     |        2|
20211221104432|   2021|           2|103     |        2|
```
                    """
        case "fy_sfp" | "tf_sfp":
            text += """
##### Data basis

- In the database table **aircraft** there is the column **far_part** which contains the FAR operations parts.
- In the database table **events** there is a column **inj_tot_f** which contains the number of fatalities per event.
- Several FAR operations parts can be assigned to the same event, depending on the number of aircraft involved. However, this is only critical if the FAR operation parts are different.

##### Possible double counting since 2008 as of 02/01/2013

```
ev_id         |ev_year|aircraft_key|far_part|inj_tot_f|
--------------+-------+------------+--------+---------+
20090808X42846|   2009|           1|091     |        9|
20090808X42846|   2009|           2|135     |        9|
20111004X45824|   2011|           1|NUSN    |        1|
20111004X45824|   2011|           2|        |        1|
20150707X22207|   2015|           1|091     |        2|
20150707X22207|   2015|           2|ARMF    |        2|
20160831X62719|   2016|           1|135     |        5|
20160831X62719|   2016|           2|091     |        5|
20180107X10632|   2017|           1|NUSN    |        1|
20180107X10632|   2017|           2|NUSC    |        1|
20180614X22730|   2018|           1|091     |        1|
20180614X22730|   2018|           2|135     |        1|
20180804X53521|   2018|           1|UNK     |        1|
20180804X53521|   2018|           2|PUBU    |        1|
20190826X90719|   2019|           1|NUSC    |        7|
20190826X90719|   2019|           2|NUSN    |        7|
20200731X11938|   2020|           1|135     |        7|
20200731X11938|   2020|           2|091     |        7|
20200827X15154|   2020|           1|135     |        2|
20200827X15154|   2020|           2|091     |        2|
20210715103483|   2020|           1|NUSN    |        5|
20210715103483|   2020|           2|129     |        5|
20211221104432|   2021|           1|135     |        2|
20211221104432|   2021|           2|103     |        2|
```
                            """
        case _:
            text += f"""
                ### Coming soon ... (chart_id={chart_id})    
                    """

    match chart_id:
        case "ey_aoc" | "ey_il" | "ey_pss" | "ey_t" | "ey_tlp" | "fy_fp" | "fy_sfp":
            text += _get_user_guide_years_chart_footer(
                chart_id,
                chart_title,
            )
        case "te_aoc" | "te_il" | "te_pss" | "te_t" | "te_tlp" | "tf_fp" | "tf_sfp":
            text += _get_user_guide_totals_chart_footer(
                chart_id,
                chart_title,
            )

    st.warning(text)


# ------------------------------------------------------------------
# Create the generic header section.
# ------------------------------------------------------------------
def _get_user_guide_chart_header(
    chart_id: str,
    chart_title: str,
) -> str:
    """Create the generic header section."""
    chart_type = (
        "Bar"
        if "ey_" in chart_id or "fy_" in chart_id
        else "Pie"
        if CHOICE_PIE_CHARTS
        else "Horizontal bar"
    )
    chart_type_1 = (
        "Here are the data grouped by year."
        if "ey_" in chart_id or "fy_" in chart_id
        else "Only the total figures are shown here."
    )
    return f"""
#### User guide: {chart_type} chart - {chart_title}

{chart_type_1}
"""


# ------------------------------------------------------------------
# Creates the user guide for the 'Show data profile' task.
# ------------------------------------------------------------------
def _get_user_guide_data_profile() -> None:
    """Creates the user guide for the 'Show data profile' task."""
    text = """
#### User guide: Show Data Profile

This task performs a data analysis of the underlying database view **io_app_ae1982**. This is done with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/). You can select either the explorative or the minimal version. Depending on the size of the selected data, there may be delayed response times, with the exploratory version again requiring significantly more computational effort than the minimal version.
For further explanations please consult the documentation of **Pandas Profiling**. The result of the data analysis can also be downloaded as **HTML** file if desired.
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def _get_user_guide_details() -> None:
    """Creates the user guide for the 'Show details' task."""
    text = """
#### User guide: Show details

This task provides the data of the underlying database view **io_app_ae1982** in a table format for display and download as **csv** file. The rows to be displayed are limited to the chosen filter options. The order of data display is based on the ascending event identification. The database columns of the selected rows are always displayed in full.

##### Usage tips

- **Column sorting**: sort columns by clicking on their headers.
- **Column resizing**: resize columns by dragging and dropping column header borders.
- **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
- **Search**: search through data by clicking a table, using hotkeys ('? Cmd + F' or 'Ctrl + F') to bring up the search bar, and using the search bar to filter data.
- **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the map.
# ------------------------------------------------------------------
def _get_user_guide_map() -> None:
    """Creates the user guide for the map."""
    text = """
#### User guide: Map

###TODO
"""

    st.warning(text)


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _get_user_guide_totals_chart_footer(
    chart_id: str,
    _chart_title: str,
) -> str:
    """Create the generic footer section."""
    objects = (
        "fatalities"
        if chart_id
        in [
            "tf_fp",
            "tf_sfp",
        ]
        else "events"
    )
    return f"""
##### Usage tips

- If you hover your mouse over the slices, the exact number of {objects} will be shown.
- By clicking on the icons in the legend, you can hide the underlying categories in the totals chart. 
- **`View fullscreen`** (double arrow): shows the totals chart in fullscreen mode.
    """


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _get_user_guide_years_chart_footer(
    chart_id: str,
    _chart_title: str,
) -> str:
    """Create the generic footer section."""
    objects = (
        "fatalities"
        if chart_id
        in [
            "fy_fp",
            "fy_sfp",
        ]
        else "events"
    )

    text = f"""
##### Usage tips years chart

- If you hover your mouse over the bars, the exact number of {objects} will be shown.
- By clicking on the icons in the legend, you can hide the underlying categories in the bar chart. 
- **`Download plot as png`** (camera symbol): the bar chart can be downloaded as an image file.
- **`Zoom out`**, **`Zoom in`**, **`Autoscale`** (plus, minus and cross symbols): the bar chart can be downloaded as an image file.
- **`Reset axes`** (home symbol): reset the axis of the bar chart.
- **`View fullscreen`** (double arrow): shows the bar chart in fullscreen mode.

##### Usage tips detailed data

- **Column sorting**: sort columns by clicking on their headers.
- **Column resizing**: resize columns by dragging and dropping column header borders.
- **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
- **Search**: search through data by clicking a table, using hotkeys ('? Cmd + F' or 'Ctrl + F') to bring up the search bar, 
and using the search bar to filter data.
- **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
        """

    if MODE_STANDARD:
        text += """
##### Detailed chart data

If you have selected the checkbox **`Show detailed chart data`** in the filter options, then you get the data underlying 
the chart displayed in a tabular form. 
With the button **`Download the chart data`** this data can be loaded into a local **csv** file. 
    """

    return text


# ------------------------------------------------------------------
# Prepare the chart data: Number of Events per Year by
# CICTT Codes.
# ------------------------------------------------------------------
def _prep_data_charts_ey_aoc(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Events per Year by CICTT Codes."""
    df_filtered = _apply_filter_incompatible(df_filtered)

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

    names = []

    for cictt_code in (
        FILTER_CICTT_CODES if FILTER_CICTT_CODES else _sql_query_cictt_codes()
    ):
        if cictt_code in df_chart.cictt_codes.values:
            names.append((cictt_code, cictt_code))

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.cictt_codes == name_df, 1, 0)

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Injury Level.
# ------------------------------------------------------------------
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

    return CHOICE_CHARTS_TYPE_N_IL, df_chart.groupby("year", as_index=False).sum(
        numeric_only=True
    )


# ------------------------------------------------------------------
# Prepare the chart data: Number of Preventable Events per Year by
# Safety Systems.
# ------------------------------------------------------------------
def _prep_data_charts_ey_pss(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Preventable Events per Year by Safety
    Systems."""
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "ev_year",
            "preventable_events",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    names = []

    for preventable_events in (
        FILTER_PREVENTABLE_EVENTS
        if FILTER_PREVENTABLE_EVENTS
        else _sql_query_preventable_events()
    ):
        if preventable_events in df_chart.preventable_events.values:
            names.append((preventable_events, preventable_events))

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.preventable_events == name_df, 1, 0)

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Event Types.
# ------------------------------------------------------------------
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

    return CHOICE_CHARTS_TYPE_N_T, df_chart.groupby("year", as_index=False).sum(
        numeric_only=True
    )


# ------------------------------------------------------------------
# Prepare the chart data: Number of Events per Year by
# Top Level Logical Parameters.
# ------------------------------------------------------------------
def _prep_data_charts_ey_tlp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Number of Events per Year by Top Level Logical
    Parameters."""
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "ev_year",
            "tll_parameters",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    names = []

    for tll_parameters in (
        FILTER_TLL_PARAMETERS if FILTER_TLL_PARAMETERS else _sql_query_tll_parameters()
    ):
        if tll_parameters in df_chart.tll_parameters.values:
            names.append((tll_parameters, tll_parameters))

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.tll_parameters == name_df, 1, 0)

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Fatalities per Year under
# FAR Operations Parts.
# ------------------------------------------------------------------
def _prep_data_charts_fy_fp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Fatalities per Year under FAR Operations
    Parts."""
    df_chart = df_filtered[
        [
            "ev_year",
            "inj_tot_f",
            "far_parts",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    if FILTER_FAR_PARTS:
        names = []
    else:
        names = [(CHOICE_CHARTS_LEGEND_NAME_NONE, CHOICE_CHARTS_LEGEND_NAME_NONE)]

    for far_part in FILTER_FAR_PARTS if FILTER_FAR_PARTS else _sql_query_far_parts():
        if far_part in df_chart.far_parts.values:
            names.append((far_part, far_part))

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.far_parts == name_df, df_chart.inj_tot_f, 0)

    del df_chart["inj_tot_f"]

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Fatalities per Year under
# Selected FAR Operations Parts.
# ------------------------------------------------------------------
def _prep_data_charts_fy_sfp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    """Prepare the chart data: Fatalities per Year under Selected FAR
    Operations Parts."""
    df_chart = df_filtered[
        [
            "ev_year",
            "inj_tot_f",
            "is_far_part_091x",
            "is_far_part_121",
            "is_far_part_135",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    for name, name_df in CHOICE_CHARTS_TYPE_N_SFP:
        df_chart[name] = np.where(df_chart[name_df], df_chart.inj_tot_f, 0)
        if name_df in [
            "is_far_part_091x",
            "is_far_part_121",
            "is_far_part_135",
        ]:
            del df_chart[name_df]

    del df_chart["inj_tot_f"]

    return CHOICE_CHARTS_TYPE_N_SFP, df_chart.groupby("year", as_index=False).sum(
        numeric_only=True
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by CICTT Codes.
# ------------------------------------------------------------------
def _prep_data_charts_te_aoc(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    #   """Prepare the chart data: Total Events by CICTT Codes."""
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "cictt_codes",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in FILTER_CICTT_CODES if FILTER_CICTT_CODES else _sql_query_cictt_codes():
        df_chart[name] = np.where(df_chart.cictt_codes == name, 1, 0)
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            if name == "":
                name = CHOICE_CHARTS_LEGEND_NAME_NONE
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Highest Injury Levels.
# ------------------------------------------------------------------
def _prep_data_charts_te_il(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Preventable Events by Safety Systems.
# ------------------------------------------------------------------
def _prep_data_charts_te_pss(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    """Prepare the chart data: Total Preventable Events by Safety Systems."""
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "preventable_events",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in (
        FILTER_PREVENTABLE_EVENTS
        if FILTER_PREVENTABLE_EVENTS
        else _sql_query_preventable_events()
    ):
        df_chart[name] = np.where(df_chart.preventable_events == name, 1, 0)
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Event Types.
# ------------------------------------------------------------------
def _prep_data_charts_te_t(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by
# Top Level Logical Parameters.
# ------------------------------------------------------------------
def _prep_data_charts_te_tlp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    """Prepare the chart data: Total Events by Top Level Logical Parameters."""
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "tll_parameters",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in (
        FILTER_TLL_PARAMETERS if FILTER_TLL_PARAMETERS else _sql_query_tll_parameters()
    ):
        df_chart[name] = np.where(df_chart.tll_parameters == name, 1, 0)
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Fatalities by
# FAR Operations Parts.
# ------------------------------------------------------------------
def _prep_data_charts_tf_fp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    """Prepare the chart data: Total Fatalities by FAR Operations Parts."""
    df_chart = df_filtered[
        [
            "far_parts",
            "inj_tot_f",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in FILTER_FAR_PARTS if FILTER_FAR_PARTS else _sql_query_far_parts():
        df_chart[name] = np.where(df_chart.far_parts == name, df_chart.inj_tot_f, 0)
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Fatalities by
# Selected FAR Operations Parts.
# ------------------------------------------------------------------
def _prep_data_charts_tf_sfp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    """Prepare the chart data: Total Fatalities by Selected FAR Operations
    Parts."""
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

    for name, name_df in CHOICE_CHARTS_TYPE_N_SFP:
        df_chart[name] = np.where(df_chart[name_df], df_chart.inj_tot_f, 0)
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
    )


# ------------------------------------------------------------------
# Prepare the totals chart.
# ------------------------------------------------------------------
def _prep_totals_chart(
    total_pie: int,
    name_value: list[tuple[str, int]],
    threshold: float | None = 0.0,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    value_threshold = total_pie * threshold if threshold else 0.0

    name_sum_adj = []
    total_pie_adj_threshold = 0

    for name, value in name_value:
        if value < value_threshold:
            total_pie_adj_threshold += value
        else:
            name_sum_adj.append(
                (CHARTS_LEGEND_N_A_DESC if name == CHARTS_LEGEND_N_A else name, value)
            )

    if total_pie_adj_threshold > 0:
        for name, value in name_value:
            if value < value_threshold:
                name_value.remove((name, value))
        name_sum_adj.append((CHARTS_LEGEND_THRESHOLD, total_pie_adj_threshold))

    name_sum_adj.sort(key=itemgetter(1), reverse=True)

    color_discrete_map = {}
    color_no = 0
    df_chart = pd.DataFrame()
    names = []
    values = []

    for name, value in name_sum_adj:
        df_chart[name] = [value]
        names.append(name)
        values.append(value)
        color_discrete_map[name] = (
            COLOR_MAP[color_no % COLOR_MAP_SIZE]
            if name
            not in [
                CHARTS_LEGEND_N_A,
                CHARTS_LEGEND_N_A_DESC,
                CHOICE_CHARTS_LEGEND_SFP_OTHER,
                CHOICE_CHARTS_LEGEND_IL_N_A,
                CHOICE_CHARTS_LEGEND_NAME_NONE,
            ]
            else COLOR_MAP_NONE
        )
        if name not in [
            CHARTS_LEGEND_N_A,
            CHARTS_LEGEND_N_A_DESC,
            CHOICE_CHARTS_LEGEND_SFP_OTHER,
            CHOICE_CHARTS_LEGEND_IL_N_A,
            CHOICE_CHARTS_LEGEND_NAME_NONE,
        ]:
            color_no += 1

    return names, values, color_discrete_map, df_chart


# ------------------------------------------------------------------
# Present the chart: Events per Year by CICTT Codes.
# ------------------------------------------------------------------
def _present_bar_chart(
    chart_id: str,
    chart_title: str,
    prep_result,
    threshold: float | None = 0.0,
):
    """Present the chart: Events per Year by CICTT Codes."""
    names, df_filtered_charts = prep_result

    if threshold and threshold > 0.0:
        name_value_dict: dict[str, int] = {}
        total_pie = 0
        for name_df in df_filtered_charts:
            if name_df != "year":
                value = df_filtered_charts[name_df].sum(axis=0, numeric_only=True)
                name_value_dict[name_df] = value
                total_pie += value
        value_threshold = total_pie * threshold if threshold else 0.0
        for name_df, value in name_value_dict.items():
            if value >= value_threshold:
                continue
            if CHARTS_LEGEND_THRESHOLD not in df_filtered_charts:
                df_filtered_charts.rename(
                    columns={
                        name_df: CHARTS_LEGEND_THRESHOLD,
                    },
                    inplace=True,
                )
                names.append((CHARTS_LEGEND_THRESHOLD, CHARTS_LEGEND_THRESHOLD))
                continue
            df_filtered_charts[CHARTS_LEGEND_THRESHOLD] = (
                df_filtered_charts[CHARTS_LEGEND_THRESHOLD]
                + df_filtered_charts[name_df]
            )
            del df_filtered_charts[name_df]

    name_value_list: list[tuple[str, int]] = []

    for name_df in df_filtered_charts:
        if name_df != "year":
            value = df_filtered_charts[name_df].sum(axis=0, numeric_only=True)
            name_value_list.append((name_df, value))

    name_value_list.sort(key=itemgetter(1), reverse=True)

    color_discrete_map = {}
    color_no = 0

    for name, value in name_value_list:
        color_discrete_map[name] = (
            COLOR_MAP[color_no % COLOR_MAP_SIZE]
            if name
            not in [
                CHARTS_LEGEND_N_A,
                CHARTS_LEGEND_N_A_DESC,
                CHOICE_CHARTS_LEGEND_SFP_OTHER,
                CHOICE_CHARTS_LEGEND_IL_N_A,
                CHOICE_CHARTS_LEGEND_NAME_NONE,
            ]
            else COLOR_MAP_NONE
        )
        if name not in [
            CHARTS_LEGEND_N_A,
            CHARTS_LEGEND_N_A_DESC,
            CHOICE_CHARTS_LEGEND_SFP_OTHER,
            CHOICE_CHARTS_LEGEND_IL_N_A,
            CHOICE_CHARTS_LEGEND_NAME_NONE,
        ]:
            color_no += 1

    data = []
    details = []

    for name, _name_df in names:
        if name not in df_filtered_charts:
            continue
        color = color_discrete_map[name]
        data.append(
            go.Bar(
                marker={"color": color},
                name=CHARTS_LEGEND_N_A_DESC if name == CHARTS_LEGEND_N_A else name,
                x=df_filtered_charts["year"],
                y=df_filtered_charts[name],
            )
        )
        details.append(name)

    fig = go.Figure(
        data,
    )

    fig.update_layout(
        bargap=0.05,
        barmode="stack",
        height=CHOICE_YEARS_CHARTS_HEIGHT
        if CHOICE_YEARS_CHARTS_HEIGHT
        else CHOICE_YEARS_CHARTS_HEIGHT_DEFAULT,
        width=CHOICE_YEARS_CHARTS_WIDTH
        if CHOICE_YEARS_CHARTS_WIDTH
        else CHOICE_YEARS_CHARTS_WIDTH_DEFAULT,
        title=chart_title,
        xaxis={"title": {"text": "Year"}},
        yaxis={
            "title": {
                "text": "Fatalities"
                if chart_id in ["fy_fp", "fy_sfp"]
                else EVENT_TYPE_DESC + "s"
            }
        },
    )

    st.plotly_chart(
        fig,
    )

    if CHOICE_YEARS_CHARTS_DETAILS:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + 'font-weight: normal;border-radius:2%;">Detailed Years Chart Data</p>',
            unsafe_allow_html=True,
        )
        details.insert(0, "year")
        if CHARTS_LEGEND_N_A in df_filtered_charts:
            df_filtered_charts.rename(
                columns={
                    CHARTS_LEGEND_N_A: CHARTS_LEGEND_N_A_DESC,
                },
                inplace=True,
            )
        if CHOICE_YEARS_CHARTS_DETAILS_TOTAL_ROWS:
            df_filtered_charts.loc[len(df_filtered_charts)] = df_filtered_charts.sum(
                axis=0, numeric_only=True
            )
            df_filtered_charts.year.iloc[-1] = "Total"
        if CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS:
            df_filtered_charts["Total"] = df_filtered_charts.iloc[:, :].sum(
                axis=1, numeric_only=True
            )
        st.dataframe(df_filtered_charts)
        st.download_button(
            data=_convert_df_2_csv(df_filtered_charts),
            file_name=APP_ID + "_chart_detail_" + chart_id + ".csv",
            help="The download includes the detailed years chart data.",
            label="Download the years chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the bar charts.
# ------------------------------------------------------------------
def _present_bar_charts() -> None:
    """Present the bar charts."""
    # Fatalities per Year by FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FY_FP:
        _present_chart_fy_fp()

    # Fatalities per Year by Selected FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FY_SFP:
        _present_chart_fy_sfp()

    # Events per Year by CICTT Codes
    if CHOICE_CHARTS_TYPE_EY_AOC:
        _present_chart_ey_aoc()

    # Events per Year by Injury Level
    if CHOICE_CHARTS_TYPE_EY_IL:
        _present_chart_ey_il()

    # Events per Year by Event Types
    if CHOICE_CHARTS_TYPE_EY_T:
        _present_chart_ey_t()

    # Events per Year by Top Level Logical Parameters
    if CHOICE_CHARTS_TYPE_EY_TLP:
        _present_chart_ey_tlp()

    # Preventable Events per Year by Safety Systems
    if CHOICE_CHARTS_TYPE_EY_PSS:
        _present_chart_ey_pss()


# ------------------------------------------------------------------
# Present chart: Events per Year by CICTT Codes.
# ------------------------------------------------------------------
def _present_chart_ey_aoc() -> None:
    """Present chart: Events per Year by CICTT Codes."""
    global CHOICE_UG_YEARS_CHARTS_EY_AOC  # pylint: disable=global-statement

    chart_id = "ey_aoc"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by CICTT Codes"

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )

    with col2:
        CHOICE_UG_YEARS_CHARTS_EY_AOC = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )

    if CHOICE_UG_YEARS_CHARTS_EY_AOC:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_aoc(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Injury Levels.
# ------------------------------------------------------------------
def _present_chart_ey_il() -> None:
    """Present chart: Events per Year by Injury Levels."""
    global CHOICE_UG_YEARS_CHARTS_EY_IL  # pylint: disable=global-statement

    chart_id = "ey_il"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Injury Levels"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_UG_YEARS_CHARTS_EY_IL = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )
    if CHOICE_UG_YEARS_CHARTS_EY_IL:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_il(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Preventable Events per Year by Safety Systems.
# ------------------------------------------------------------------
def _present_chart_ey_pss() -> None:
    """Present chart: Preventable Events per Year by Safety Systems."""
    global CHOICE_UG_YEARS_CHARTS_EY_PSS  # pylint: disable=global-statement

    chart_id = "ey_pss"
    chart_title = f"Number of Preventable {EVENT_TYPE_DESC}s per Year by Safety Systems"

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )

    with col2:
        CHOICE_UG_YEARS_CHARTS_EY_PSS = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )

    if CHOICE_UG_YEARS_CHARTS_EY_PSS:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_pss(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Event Types.
# ------------------------------------------------------------------
def _present_chart_ey_t() -> None:
    """Present chart: Events per Year by Event Types."""
    global CHOICE_UG_YEARS_CHARTS_EY_T  # pylint: disable=global-statement

    chart_id = "ey_t"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Event Types"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_UG_YEARS_CHARTS_EY_T = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )
    if CHOICE_UG_YEARS_CHARTS_EY_T:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )
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
    global CHOICE_UG_YEARS_CHARTS_EY_TLP  # pylint: disable=global-statement

    chart_id = "ey_tlp"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Top Logical Parameters"

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )

    with col2:
        CHOICE_UG_YEARS_CHARTS_EY_TLP = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )

    if CHOICE_UG_YEARS_CHARTS_EY_TLP:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_ey_tlp(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Number of Fatalities per Year by
# FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fy_fp() -> None:
    """Present chart: Number of Fatalities per Year by FAR Operations Parts."""
    global CHOICE_UG_YEARS_CHARTS_FY_FP  # pylint: disable=global-statement

    chart_id = "fy_fp"
    chart_title = "Number of Fatalities per Year by FAR Operations Parts"

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )

    with col2:
        CHOICE_UG_YEARS_CHARTS_FY_FP = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )

    if CHOICE_UG_YEARS_CHARTS_FY_FP:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_fy_fp(DF_FILTERED),
        CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Number of Fatalities per Year by
# Selected FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fy_sfp() -> None:
    """Present chart: Number of Fatalities per Year by Selected FAR Operations
    Parts."""
    global CHOICE_UG_YEARS_CHARTS_FY_SFP  # pylint: disable=global-statement

    chart_id = "fy_sfp"
    chart_title = "Number of Fatalities per Year by Selected FAR Operations Parts"

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        CHOICE_UG_YEARS_CHARTS_FY_SFP = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User Guide: Years chart**",
            value=False,
        )

    if CHOICE_UG_YEARS_CHARTS_FY_SFP:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_charts_fy_sfp(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data() -> None:
    global DF_FILTERED_ROWS  # pylint: disable=global-statement
    global DF_UNFILTERED_ROWS  # pylint: disable=global-statement

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
        _get_user_guide_app()

    (DF_UNFILTERED_ROWS, _) = DF_UNFILTERED.shape
    if DF_UNFILTERED_ROWS == 0:
        st.error("##### Error: There are no data available.")
        st.stop()

    (DF_FILTERED_ROWS, _) = DF_FILTERED.shape
    if DF_FILTERED_ROWS == 0:
        st.error("##### Error: No data has been selected.")
        st.stop()

    if CHOICE_MAP:
        _present_map()
        _print_timestamp("_present_data() - CHOICE_MAP")

    if CHOICE_DATA_GRAPHS_YEARS:
        _present_bar_charts()
        _print_timestamp("_present_data() - CHOICE_DATA_GRAPHS_YEARS")

    if CHOICE_DATA_GRAPHS_TOTALS and (
        CHOICE_HORIZONTAL_BAR_CHARTS or CHOICE_PIE_CHARTS
    ):
        _present_totals_charts()
        _print_timestamp("_present_data() - CHOICE_DATA_GRAPHS_TOTALS")

    if CHOICE_DATA_PROFILE:
        _present_data_profile()
        _print_timestamp("_present_data() - CHOICE_DATA_PROFILE")

    if CHOICE_DETAILS:
        _present_details()
        _print_timestamp("_present_data() - CHOICE_DETAILS")

    _print_timestamp("_present_data() - End")


# ------------------------------------------------------------------
# Present data profile.
# ------------------------------------------------------------------
def _present_data_profile() -> None:
    """Present data profile."""
    global CHOICE_UG_DATA_PROFILE  # pylint: disable=global-statement

    col1, col2 = st.columns(
        [
            2,
            1,
        ]
    )

    with col1:
        # pylint: disable=line-too-long
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + 'font-weight: normal;border-radius:2%;">Profiling of the Filtered io_app_ae1982 data</p>',
            unsafe_allow_html=True,
        )

    with col2:
        CHOICE_UG_DATA_PROFILE = st.checkbox(
            help="Explanations and operating instructions related to profiling "
            + "of the database view **io_app_ae1982",
            label="**User Guide: Show data profile**",
            value=False,
        )

    if CHOICE_UG_DATA_PROFILE:
        _get_user_guide_data_profile()

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
    global CHOICE_UG_DETAILS  # pylint: disable=global-statement

    if CHOICE_DETAILS:
        col1, col2 = st.columns(
            [
                2,
                1,
            ]
        )

        with col1:
            # pylint: disable=line-too-long
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                + 'font-weight: normal;border-radius:2%;">Detailed data from DB view io_app_ae1982</p>',
                unsafe_allow_html=True,
            )

        with col2:
            CHOICE_UG_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed view.",
                label="**User Guide: Show details**",
                value=False,
            )

        if CHOICE_UG_DETAILS:
            _get_user_guide_details()

        # pylint: disable=line-too-long
        st.write(
            f"No {EVENT_TYPE_DESC.lower() + 's'} unfiltered: {DF_UNFILTERED_ROWS} - filtered: {DF_FILTERED_ROWS}"
        )

        st.dataframe(DF_FILTERED)

        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED),
            file_name=APP_ID + "_data_detail.csv",
            help="The download includes all data "
            + "after applying the filter options.",
            label="Download the detailed data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the events on the US map.
# ------------------------------------------------------------------
def _present_map() -> None:
    """Present the events on the US map."""
    global CHOICE_UG_MAP  # pylint: disable=global-statement

    col1, col2 = st.columns([2, 1])

    with col1:
        if MODE_STANDARD:
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                + 'font-weight: normal;border-radius:2%;">Map of '
                + EVENT_TYPE_DESC
                + "s"
                + "</p>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                + 'font-weight: normal;border-radius:2%;">Map of Fatal Accidents in the US</p>',
                unsafe_allow_html=True,
            )

    with col2:
        CHOICE_UG_MAP = st.checkbox(
            help="Explanations and operating instructions related to the map.",
            key="Show Map",
            label="**User Guide: Map**",
            value=False,
        )

    if CHOICE_UG_MAP:
        _get_user_guide_map()

    # noinspection PyUnboundLocalVariable
    df_filtered_map = DF_FILTERED.loc[
        (DF_FILTERED["dec_latitude"].notna() & DF_FILTERED["dec_longitude"].notna())
    ]

    faa_layer = pdk.Layer(
        auto_highlight=True,
        data=df_filtered_map,
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
# Present the totals chart.
# ------------------------------------------------------------------
def _present_totals_chart(
    chart_id: str,
    chart_title: str,
    pie_chart_data: tuple[list[str], list[int], dict[str, str], DataFrame],
) -> None:
    """Present the totals chart."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        choice_pie_charts_ug = st.checkbox(
            help="Explanations and operating instructions related to this totals chart(s).",
            key=chart_title,
            label="**User Guide: Totals chart**",
            value=False,
        )

    if choice_pie_charts_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    names, values, color_discrete_map, df_sum = pie_chart_data

    if CHOICE_HORIZONTAL_BAR_CHARTS:
        names_new = []
        for categ in names:
            names_new.append(categ + ":")
        if values:
            fig = px.bar(
                color=names,
                color_discrete_map=color_discrete_map,
                orientation="h",
                title=chart_title,
                x=values,
                y=names_new,
            )
        else:
            fig = px.bar(
                color=names,
                color_discrete_map=color_discrete_map,
                orientation="h",
                title=chart_title,
                y=names_new,
            )
        fig.update_layout(
            bargap=0.05,
            barmode="stack",
            height=CHOICE_TOTALS_CHARTS_HEIGHT
            if CHOICE_TOTALS_CHARTS_HEIGHT
            else CHOICE_TOTALS_CHARTS_HEIGHT_DEFAULT,
            width=CHOICE_TOTALS_CHARTS_WIDTH
            if CHOICE_TOTALS_CHARTS_WIDTH
            else CHOICE_TOTALS_CHARTS_WIDTH_DEFAULT,
            showlegend=False,
            title=chart_title,
            xaxis={
                "title": {
                    "text": "Fatalities"
                    if chart_id in ["tf_fp", "tf_sfp"]
                    else EVENT_TYPE_DESC + "s"
                }
            },
            yaxis={"title": {"text": " "}},
        )
        st.plotly_chart(
            fig,
        )

    if CHOICE_PIE_CHARTS:
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

    if CHOICE_TOTALS_CHARTS_DETAILS:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + 'font-weight: normal;border-radius:2%;">Detailed Totals Chart Data</p>',
            unsafe_allow_html=True,
        )
        if CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS:
            df_sum["Total"] = df_sum.sum(axis=1, numeric_only=True)
        st.dataframe(df_sum)


# ------------------------------------------------------------------
# Present the totals charts.
# ------------------------------------------------------------------
def _present_totals_charts() -> None:
    """Present the totals charts."""
    # Total Fatalities by FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TF_FP:
        _present_totals_chart(
            "tf_fp",
            "Total Number of Fatalities by FAR Operations Parts",
            _prep_data_charts_tf_fp(DF_FILTERED),
        )

    # Total Fatalities by Selected FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TF_SFP:
        _present_totals_chart(
            "tf_sfp",
            "Total Number of Fatalities by Selected FAR Operations Parts",
            _prep_data_charts_tf_sfp(DF_FILTERED),
        )

    # Total Events by CICTT Code
    if CHOICE_CHARTS_TYPE_TE_AOC:
        _present_totals_chart(
            "te_aoc",
            f"Total Number of {EVENT_TYPE_DESC}s by CICTT Codes",
            _prep_data_charts_te_aoc(DF_FILTERED),
        )

    # Total Events by Highest Injury Levels
    if CHOICE_CHARTS_TYPE_TE_IL:
        _present_totals_chart(
            "te_il",
            f"Total Number of {EVENT_TYPE_DESC}s by Highest Injury Levels",
            _prep_data_charts_te_il(DF_FILTERED),
        )

    # Total Events by Event Types
    if CHOICE_CHARTS_TYPE_TE_T:
        _present_totals_chart(
            "te_t",
            f"Total Number of {EVENT_TYPE_DESC}s by Event Types",
            _prep_data_charts_te_t(DF_FILTERED),
        )

    # Total Events by Top Level logical Parameter
    if CHOICE_CHARTS_TYPE_TE_TLP:
        _present_totals_chart(
            "te_tlp",
            f"Total Number of {EVENT_TYPE_DESC}s  by Top Level Logical Parameters",
            _prep_data_charts_te_tlp(DF_FILTERED),
        )

    # Total Preventable Events by Safety Systems
    if CHOICE_CHARTS_TYPE_TE_PSS:
        _present_totals_chart(
            "te_pss",
            f"Total Number of Preventable {EVENT_TYPE_DESC}s by Safety Systems",
            _prep_data_charts_te_pss(DF_FILTERED),
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
    global FILTER_NO_AIRCRAFT_FROM  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_TO  # pylint: disable=global-statement
    global FILTER_OCCURRENCE_CODES  # pylint: disable=global-statement
    global FILTER_PREVENTABLE_EVENTS  # pylint: disable=global-statement
    global FILTER_TLL_PARAMETERS  # pylint: disable=global-statement
    global FILTER_US_AVIATION  # pylint: disable=global-statement
    global FILTER_US_STATES  # pylint: disable=global-statement

    _print_timestamp("_setup_filter - Start")

    if MODE_STANDARD:
        CHOICE_FILTER_DATA = st.sidebar.checkbox(
            help="""
            The following filter options can be used to limit the data to be processed.
            All selected filter options are applied simultaneously, i.e. they are linked
            to a logical **`and`**.
            """,
            label="**Filter Data ?**",
            value=True,
        )

        if not CHOICE_FILTER_DATA:
            return
    else:
        CHOICE_FILTER_DATA = True
        st.sidebar.markdown("**Filter Data:**")

    CHOICE_ACTIVE_FILTERS_TEXT = ""

    if MODE_STANDARD:
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
            default=FILTER_EV_TYPE_DEFAULT,
            help="""
            Here, the data can be limited to selected event types.
            Those events are selected whose event type matches.
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

    if not MODE_STANDARD:
        FILTER_EV_TYPE = FILTER_EV_TYPE_DEFAULT
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Event type(s)**: **`{','.join(FILTER_EV_TYPE)}`**"
        )

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
        FILTER_FAR_PARTS = FILTER_FAR_PARTS_DEFAULT
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **FAR operations parts**: **`{','.join(FILTER_FAR_PARTS)}`**"
        )
        FILTER_EV_HIGHEST_INJURY = FILTER_EV_HIGHEST_INJURY_DEFAULT
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Highest injury level(s)**: **`{','.join(FILTER_EV_HIGHEST_INJURY)}`**"
        )
        FILTER_US_AVIATION = FILTER_US_AVIATION_DEFAULT
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **US aviation criteria**: **`{','.join(FILTER_US_AVIATION)}`**"
        )
        return

    if CHOICE_EXTENDED_VERSION:
        FILTER_FAR_PARTS = st.sidebar.multiselect(
            help="""
            Under which FAR operations parts the event was conducted.
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
        default=FILTER_EV_HIGHEST_INJURY_DEFAULT,
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
            Here, the data can be limited to selected acquisition methods.
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

    FILTER_PREVENTABLE_EVENTS = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to events that could be prevented if an appropriate safety system were available.
        """,
        label="**Preventable events:**",
        options=_sql_query_preventable_events(),
    )
    _print_timestamp("_setup_filter - FILTER_PREVENTABLE_EVENTS - 1")

    if FILTER_PREVENTABLE_EVENTS:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Preventable events**: **`{','.join(FILTER_PREVENTABLE_EVENTS)}`**"
        )
        _print_timestamp("_setup_filter - FILTER_PREVENTABLE_EVENTS - 2")

    st.sidebar.markdown("""---""")

    FILTER_US_STATES = st.sidebar.multiselect(
        help="Here, data can be limited to selected U.S. states.",
        label="**State(s) in the US:**",
        options=_sql_query_us_states(),
    )

    if FILTER_US_STATES:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **State(s) in the US**: **`{','.join(FILTER_US_STATES)}`**"
        )

    _print_timestamp("_setup_filter - FILTER_STATES - 1")

    if CHOICE_EXTENDED_VERSION:
        FILTER_TLL_PARAMETERS = st.sidebar.multiselect(
            help="""
            Top logical parameters that are applied when filtering.
            """,
            label="**Top logical parameter(s):**",
            options=_sql_query_tll_parameters(),
        )
        _print_timestamp("_setup_filter - FILTER_TLL_PARAMETERS - 1")

        if FILTER_TLL_PARAMETERS:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + "\n- **Top logical parameter(s)**: **"
                + f"`{','.join(FILTER_TLL_PARAMETERS)}`**"
            )
            _print_timestamp("_setup_filter - FILTER_TLL_PARAMETERS - 2")

        st.sidebar.markdown("""---""")

    FILTER_US_AVIATION = st.sidebar.multiselect(
        default=FILTER_US_AVIATION_DEFAULT,
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

    if FILTER_EV_TYPE == [CHOICE_CHARTS_LEGEND_T_ACC]:
        EVENT_TYPE_DESC = "Accident"
    elif FILTER_EV_TYPE == [CHOICE_CHARTS_LEGEND_T_INC]:
        EVENT_TYPE_DESC = "Incident"
    else:
        EVENT_TYPE_DESC = "Event"

    if MODE_STANDARD:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
            + f'font-weight: normal;border-radius:2%;">Aviation {EVENT_TYPE_DESC} Analysis - Year '
            + f"{FILTER_EV_YEAR_FROM} until {FILTER_EV_YEAR_TO}</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
            + 'font-weight: normal;border-radius:2%;">US Aviation Fatal Accidents - Year '
            + f"{FILTER_EV_YEAR_FROM} until {FILTER_EV_YEAR_TO}</p>",
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
            label="**User Guide: Application**",
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
    global CHOICE_CHARTS_TYPE_EY_AOC  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_IL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_PSS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_T  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_TLP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_FY_FP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_FY_SFP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_AOC  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_IL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PSS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_T  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_TLP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_FP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_SFP  # pylint: disable=global-statement
    global CHOICE_DATA_GRAPHS_TOTALS  # pylint: disable=global-statement
    global CHOICE_DATA_GRAPHS_YEARS  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_EXTENDED_VERSION  # pylint: disable=global-statement
    global CHOICE_HORIZONTAL_BAR_CHARTS  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_MAP_RADIUS  # pylint: disable=global-statement
    global CHOICE_PIE_CHARTS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_WIDTH  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS_TOTAL_ROWS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_WIDTH  # pylint: disable=global-statement

    if MODE_STANDARD:
        CHOICE_EXTENDED_VERSION = st.sidebar.checkbox(
            help="The extended version has more complex filtering and processing options.",
            label="**Extended Version**",
            value=False,
        )

        st.sidebar.markdown("""---""")

    CHOICE_MAP = st.sidebar.checkbox(
        help="Display the events on a map (after filtering the data).",
        label="**Show Map**",
        value=not MODE_STANDARD,
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

    CHOICE_DATA_GRAPHS_YEARS = st.sidebar.checkbox(
        help="Events or fatalities per year (after filtering the data).",
        label="**Show Data Graphs - Years**",
        value=not MODE_STANDARD,
    )

    if CHOICE_DATA_GRAPHS_YEARS:
        if CHOICE_EXTENDED_VERSION:
            CHOICE_YEARS_CHARTS_HEIGHT = st.sidebar.slider(
                key="CHOICE_YEARS_CHARTS_HEIGHT",
                label="Chart height (px)",
                min_value=100,
                max_value=1000,
                value=CHOICE_YEARS_CHARTS_HEIGHT_DEFAULT,
            )
            CHOICE_YEARS_CHARTS_WIDTH = st.sidebar.slider(
                key="CHOICE_YEARS_CHARTS_WIDTH",
                label="Chart width (px)",
                min_value=100,
                max_value=2000,
                value=CHOICE_YEARS_CHARTS_WIDTH_DEFAULT,
            )

            CHOICE_YEARS_CHARTS_DETAILS = st.sidebar.checkbox(
                help="Tabular representation of the of the data underlying the charts.",
                key="CHOICE_YEARS_CHARTS_DETAILS",
                label="Show detailed chart data",
                value=False,
            )
            if CHOICE_YEARS_CHARTS_DETAILS:
                CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS = st.sidebar.checkbox(
                    help="Sums all columns of the detailed data table.",
                    key="CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS",
                    label="Sum all columns",
                    value=False,
                )
                CHOICE_YEARS_CHARTS_DETAILS_TOTAL_ROWS = st.sidebar.checkbox(
                    help="Sums all rows of the detailed data table.",
                    label="Sum all rows",
                    value=False,
                )

            st.sidebar.markdown("""---""")

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_FY_FP = st.sidebar.checkbox(
                help="Fatalities per year by FAR Operations Parts (after filtering the data).",
                label="Fatalities per Year by FAR Operations Parts",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_FY_FP:
                CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

        CHOICE_CHARTS_TYPE_FY_SFP = st.sidebar.checkbox(
            help="Fatalities per year by selected FAR Operations Parts (after filtering the data).",
            label="Fatalities per Year by Selected FAR Operations Parts",
            value=not MODE_STANDARD,
        )
        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_EY_AOC = st.sidebar.checkbox(
                help="Events per year by CICTT codes (after filtering the data).",
                label="Events per Year by CICTT Codes",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_EY_AOC:
                CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
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

        CHOICE_CHARTS_TYPE_EY_PSS = st.sidebar.checkbox(
            help="Preventable events per year by safety systems (after filtering the data).",
            label="Preventable Events per Year by Safety Systems",
            value=False,
        )
        if CHOICE_CHARTS_TYPE_EY_PSS:
            CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD = st.sidebar.number_input(
                help="Threshold percentage for combined display",
                key="CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD",
                label="Threshold value in %",
                max_value=20.0,
                min_value=0.0,
                value=0.5,
            )

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_EY_TLP = st.sidebar.checkbox(
                help="Events per year by top level logical parameters (after filtering the data).",
                label="Events per Year by Top Level Logical Parameters",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_EY_TLP:
                CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

    st.sidebar.markdown("""---""")

    CHOICE_DATA_GRAPHS_TOTALS = st.sidebar.checkbox(
        help="Total Events or fatalities (after filtering the data).",
        label="**Show Data Graphs - Totals**",
        value=not MODE_STANDARD,
    )

    if CHOICE_DATA_GRAPHS_TOTALS:
        CHOICE_PIE_CHARTS = st.sidebar.checkbox(
            help="Presenting totals with pie charts.",
            key="CHOICE_PIE_CHARTS",
            label="Show pie charts",
            value=True,
        )
        CHOICE_HORIZONTAL_BAR_CHARTS = st.sidebar.checkbox(
            help="Presenting totals with horizontal bar charts.",
            key="CHOICE_HORIZONTAL_BAR_CHARTS",
            label="Show horizontal bar charts",
            value=False,
        )
        if CHOICE_HORIZONTAL_BAR_CHARTS:
            if CHOICE_EXTENDED_VERSION:
                CHOICE_TOTALS_CHARTS_HEIGHT = st.sidebar.slider(
                    key="CHOICE_TOTALS_CHARTS_HEIGHT",
                    label="Chart height (px)",
                    min_value=100,
                    max_value=1000,
                    value=CHOICE_TOTALS_CHARTS_HEIGHT_DEFAULT,
                )
                CHOICE_TOTALS_CHARTS_WIDTH = st.sidebar.slider(
                    key="CHOICE_TOTALS_CHARTS_WIDTH",
                    label="Chart width (px)",
                    min_value=100,
                    max_value=2000,
                    value=CHOICE_TOTALS_CHARTS_WIDTH_DEFAULT,
                )
        if CHOICE_EXTENDED_VERSION:
            CHOICE_TOTALS_CHARTS_DETAILS = st.sidebar.checkbox(
                help="Tabular representation of the of the data underlying the charts.",
                key="CHOICE_TOTALS_CHARTS_DETAILS",
                label="Show detailed chart data",
                value=False,
            )
            if CHOICE_TOTALS_CHARTS_DETAILS:
                CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS = st.sidebar.checkbox(
                    help="Sums all columns of the detailed data table.",
                    key="CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS",
                    label="Sum all columns",
                    value=True,
                )

        st.sidebar.markdown("""---""")

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_TF_FP = st.sidebar.checkbox(
                help="Total fatalities by FAR operations parts (after filtering the data).",
                label="Total Fatalities by FAR Operations Parts",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TF_FP:
                CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

        CHOICE_CHARTS_TYPE_TF_SFP = st.sidebar.checkbox(
            help="Total fatalities by selected FAR operations parts (after filtering the data).",
            label="Total Fatalities by Selected FAR Operations Parts",
            value=not MODE_STANDARD,
        )

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_TE_AOC = st.sidebar.checkbox(
                help="Total events by CICTT codes (after filtering the data).",
                label="Total Events by CICTT Codes",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TE_AOC:
                CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_TE_AOC_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
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

        CHOICE_CHARTS_TYPE_TE_PSS = st.sidebar.checkbox(
            help="Total preventable events by safety systems (after filtering the data).",
            label="Total Preventable Events by Safety Systems",
            value=not MODE_STANDARD,
        )
        if CHOICE_CHARTS_TYPE_TE_PSS:
            CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD = st.sidebar.number_input(
                help="Threshold percentage for combined display",
                key="CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD",
                label="Threshold value in %",
                max_value=20.0,
                min_value=0.0,
                value=0.5,
            )

        if MODE_STANDARD:
            CHOICE_CHARTS_TYPE_TE_TLP = st.sidebar.checkbox(
                help="Total events by top level logical parameters (after filtering the data).",
                label="Total Events by Top Level Logical Parameters",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TE_TLP:
                CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

    st.sidebar.markdown("""---""")

    if MODE_STANDARD:
        CHOICE_DATA_PROFILE = st.sidebar.checkbox(
            help="Profiling of the filtered dataset.",
            label="**Show Data Profile**",
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
            label="**Show Detailed Data**",
            value=True,
        )

        st.sidebar.markdown("""---""")


# ------------------------------------------------------------------
# Execute a query that returns the list of aircraft categories.
# ------------------------------------------------------------------
def _sql_query_acft_categories() -> list[str]:
    """Execute a query that returns a list of aircraft categories."""
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
def _sql_query_cictt_codes() -> list[str]:
    """Execute a query that returns a list of CICTT codes."""
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT DISTINCT cictt_codes
          FROM io_app_ae1982;
        """
        )

        data = []

        for row in cur:
            data.append(row[0])

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of injury levels
# ------------------------------------------------------------------
def _sql_query_ev_highest_injury() -> list[str]:
    """Execute a query that returns a list of injury levels."""
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT string_agg(DISTINCT CASE WHEN ev_highest_injury IS NULL THEN 'n/a' ELSE ev_highest_injury END, ',' ORDER BY CASE WHEN ev_highest_injury IS NULL THEN 'n/a' ELSE ev_highest_injury END)
          FROM io_app_ae1982;
        """
        )

        keys = (cur.fetchone()[0]).split(",")  # type: ignore

        data = []

        for key in keys:
            data.append(OPTIONS_EV_HIGHEST_INJURY[key])

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of event types
# ------------------------------------------------------------------
def _sql_query_ev_type() -> list[str]:
    """Execute a query that returns a list of event types."""
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT string_agg(DISTINCT CASE WHEN ev_type IS NULL THEN 'n/a' ELSE ev_type END, ',' ORDER BY CASE WHEN ev_type IS NULL THEN 'n/a' ELSE ev_type END)
          FROM io_app_ae1982;
        """
        )

        keys = (cur.fetchone()[0]).split(",")  # type: ignore

        data = []

        for key in keys:
            data.append(OPTIONS_EV_TYPE[key])

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of FAR Operations Parts.
# ------------------------------------------------------------------
def _sql_query_far_parts() -> list[str]:
    """Execute a query that returns a list of FAR Operations Parts."""
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT DISTINCT far_parts
          FROM io_app_ae1982;
        """
        )

        data = []

        for row in cur:
            data.append(row[0])

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of finding codes.
# ------------------------------------------------------------------
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
def _sql_query_latlong_acq() -> list[str]:
    """Execute a query that returns a list of latitude / longitude acquisition.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(DISTINCT latlong_acq, ',' ORDER BY latlong_acq)
          FROM io_app_ae1982;
        """
        )

        keys = (cur.fetchone()[0]).split(",")  # type: ignore

        data = []

        for key in keys:
            data.append(OPTIONS_LATLONG_ACQ[key])

        return sorted(data)


# ------------------------------------------------------------------
# Determine the maximum number of fatalities on ground.
# ------------------------------------------------------------------
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
# Execute a query that returns the list of preventable event
# categories.
# ------------------------------------------------------------------
def _sql_query_preventable_events() -> list[str]:
    """Execute a query that returns a list of preventable event categories.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT DISTINCT preventable_events
          FROM io_app_ae1982;
        """
        )

        data = []

        for row in cur:
            data.append(row[0])

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of top level logical
# parameters.
# ------------------------------------------------------------------
def _sql_query_tll_parameters() -> list[str]:
    """Execute a query that returns a list of top_level_logical_parameters.

    Returns:
        list[str]: Query results in a list.
    """
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT DISTINCT tll_parameters
          FROM io_app_ae1982;
        """
        )

        data = []

        for row in cur:
            data.append(row[0])

        return sorted(data)


# ------------------------------------------------------------------
# Run the US latitude and longitude query.
# ------------------------------------------------------------------
def _sql_query_us_ll(pitch: int, zoom: float) -> pdk.ViewState:
    """Run the US latitude and longitude query."""
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
def _sql_query_us_states() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            # pylint: disable=line-too-long
            """
        SELECT string_agg(CONCAT(state_name, ' - ', state), ',' ORDER BY state)
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
    global HOST_CLOUD  # pylint: disable=global-statement
    global MODE_STANDARD  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement
    global START_TIME  # pylint: disable=global-statement
    global DF_UNFILTERED  # pylint: disable=global-statement

    # Start time measurement.
    START_TIME = time.time_ns()

    print(
        str(datetime.datetime.now())
        + "                         - Start application "
        + APP_ID,
        flush=True,
    )

    if "HOST_CLOUD" in st.session_state and "MODE_STANDARD" in st.session_state:
        HOST_CLOUD = st.session_state["HOST_CLOUD"]
        MODE_STANDARD = st.session_state["MODE_STANDARD"]
    else:
        (host, mode) = utils.get_args()
        HOST_CLOUD = bool(host == "Cloud")
        st.session_state["HOST_CLOUD"] = HOST_CLOUD
        MODE_STANDARD = bool(mode == "Std")
        st.session_state["MODE_STANDARD"] = MODE_STANDARD

    print(
        str(datetime.datetime.now())
        + f"                         - MODE_STANDARD={MODE_STANDARD}",
        flush=True,
    )

    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Favicon.ico?raw=true",
        page_title="ae1982 by IO-Aero",
    )

    if MODE_STANDARD:
        col1, col2 = st.sidebar.columns(2)
        col1.markdown("##  [IO-Aero Website](https://www.io-aero.com)")
        url = "http://" + ("members.io-aero.com:8080" if HOST_CLOUD else "localhost:8598")
        col2.markdown(f"##  [Member Menu]({url})")
    else:
        st.sidebar.markdown("## [IO-Aero Website](https://www.io-aero.com)")

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    if MODE_STANDARD:
        utils.has_access(HOST_CLOUD, APP_ID)

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
