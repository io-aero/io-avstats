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
import streamlit as st
import utils  # type: ignore  # pylint: disable=import-error
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from psycopg2.extensions import connection
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

CHOICE_BOX_PLOTS: bool | None = None

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

CHOICE_CHARTS_TYPE_D_NA: bool | None = None
CHOICE_CHARTS_TYPE_D_NA_MAX: float | None = None
CHOICE_CHARTS_TYPE_D_NA_NO: int | None = None
CHOICE_CHARTS_TYPE_EY_AOC: bool | None = None
CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_EY_IL: bool | None = None
CHOICE_CHARTS_TYPE_EY_MPF: bool | None = None
CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_EY_NA: bool | None = None
CHOICE_CHARTS_TYPE_EY_NA_I_1_OG: float | None = None
CHOICE_CHARTS_TYPE_EY_NA_I_2_OG: float | None = None
CHOICE_CHARTS_TYPE_EY_PF: bool | None = None
CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD: float | None = None
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
CHOICE_CHARTS_TYPE_TE_MPF: bool | None = None
CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TE_NA: bool | None = None
CHOICE_CHARTS_TYPE_TE_NA_I_1_OG: float | None = None
CHOICE_CHARTS_TYPE_TE_NA_I_2_OG: float | None = None
CHOICE_CHARTS_TYPE_TE_PF: bool | None = None
CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TE_PSS: bool | None = None
CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TE_T: bool | None = None
CHOICE_CHARTS_TYPE_TE_TLP: bool | None = None
CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TF_FP: bool | None = None
CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD: float | None = None
CHOICE_CHARTS_TYPE_TF_SFP: bool | None = None

CHOICE_DATA_GRAPHS_DISTANCES: bool | None = None
CHOICE_DATA_GRAPHS_TOTALS: bool | None = None
CHOICE_DATA_GRAPHS_YEARS: bool | None = None
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DATA_PROFILE_TYPE: str | None = None
CHOICE_DETAILS: bool | None = None

CHOICE_EXTENDED_VERSION: bool | None = None

CHOICE_FILTER_DATA: bool | None = None

CHOICE_HORIZONTAL_BAR_CHARTS: bool | None = None

CHOICE_MAP: bool | None = None
CHOICE_MAP_MAP_STYLE: str | None = None
CHOICE_MAP_MAP_STYLE_DEFAULT = "open-street-map"

CHOICE_PIE_CHARTS: bool | None = None

CHOICE_RUN_ANALYSIS: bool | None = None

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

CHOICE_VIOLIN_PLOTS: bool | None = None

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
FILTER_DEFINING_PHASES: list[str] = []
FILTER_DESCRIPTION_MAIN_PHASES: list[str] = []
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
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats/"

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

# ------------------------------------------------------------------
# Configuration parameters.
# ------------------------------------------------------------------
SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AERO",
    settings_files=["settings.io_aero.toml"],
)
START_TIME: int = 0

# Magnification level of the map, usually between
# 0 (representing the whole world) and
# 24 (close to individual buildings)
ZOOM = 4


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
    if FILTER_DEFINING_PHASES:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["phase_codes_defining"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_DEFINING_PHASES)))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_DEFINING_PHASES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_DESCRIPTION_MAIN_PHASES:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[
            (
                df_filtered["description_main_phase_defining"].isin(
                    FILTER_DESCRIPTION_MAIN_PHASES
                )
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_DESCRIPTION_MAIN_PHASES"
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
    return dataframe.to_csv().encode("utf-8")


# ------------------------------------------------------------------
# Read the data.
# ------------------------------------------------------------------
@st.cache_resource
def _get_data() -> DataFrame:
    _print_timestamp("_get_data() - Start")

    return pd.read_sql(
        con=utils.get_engine(SETTINGS),
        sql="""
            SELECT ev_id,
                   acft_categories,
                   cictt_codes,
                   country,
                   dec_latitude,
                   dec_longitude,
                   description_main_phase_defining,
                   CASE WHEN inj_tot_f = 0 THEN 'non-fatal'
                        ELSE 'fatal'
                   END dot_color,     
                   ev_highest_injury,
                   ev_type,
                   ev_year,
                   UPPER(city) event_city,
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
                   nearest_airport_distance,
                   nearest_airport_ident,
                   nearest_airport_servcity,
                   no_aircraft,
                   ntsb_no,
                   occurrence_codes,
                   phase_codes_defining,
                   preventable_events,
                   state,
                   tll_parameters
             FROM io_app_ae1982
            ORDER BY ev_id;
""",
    )


# ------------------------------------------------------------------
# Prepare the codes.
# ------------------------------------------------------------------
def _get_prepared_codes(list_in: list) -> list[str]:
    list_out = []

    for elem in list_in:
        (_, code) = elem.split(" - ")
        list_out.append(code)

    _print_timestamp("_get_prepared_codes()")

    return list_out


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
    ug_text = """
#### User guide: Application
"""

    ug_text += f"""
This application allows you to perform data analysis tasks on aviation accident and incident data provided by 
[NTSB]( https://www.ntsb.gov/Pages/home.aspx).
The National Transportation Safety Board (NTSB) is an independent Federal agency charged by Congress with investigating 
every civil aviation accident in the United States and significant accidents in other modes of transportation – railroad, 
highway, marine and pipeline.
For each aviation accident and incident, the NTSB provides the relevant data in the form of MS Access databases.

The databases provided on the [NTSB website](https://data.ntsb.gov/avdata) come in three versions:
- **Pre2008**: contains data for events that occurred before the year 2008,
- **avall**: on the first of each month, the data for events since 2008 are made available here,
- **up[01|08|15|22][JAN|...|DEC]**: at the 1st, 8th, 15th and 22nd of each month these update files contain the changes
since the previous update file.

The application processes data regarding
- the events (`events`),
- the aircraft involved (`aircraft`),
- the event sequences (`events_sequence`),
- the findings (`findings`), and
- the reports of involved parties (`narratives`).

The application provides the following tools:

- **Data Graphs - Distances**: Provides graphical evaluation options for questions regarding distances,
- **Data Graphs - Totals**: Provides graphical evaluation options for total summaries,
- **Data Graphs - Years**: Provides graphical analysis options for year-based analysis,
- **Data Profiles**: Allows detailed analysis of data characteristics,
- **Detailed Data**: Shows the detailed data involved,
- **Filter**: A large number of filter options allow the evaluation of the data with any granularity,
- **Map**: Shows the event locations on a map. 

Where appropriate, the application allows you to print the displayed graphics or upload detailed data in **csv** format.

Further information on the application can be found [here]({LINK_GITHUB_PAGES}).

If you encounter any problem in the application, documentation or data, we would appreciate it if you would notify us 
[here](https://github.com/io-aero/io-avstats/issues) so that we can make any necessary correction. 
Also suggestions for improvement or enhancements are welcome. 
"""

    st.warning(ug_text)


# ------------------------------------------------------------------
# Creates the user guide for years charts.
# ------------------------------------------------------------------
def _get_user_guide_chart(
    chart_id: str,
    chart_title: str,
) -> None:
    ug_text = _get_user_guide_chart_header(
        chart_id,
        chart_title,
    )

    ug_text = _get_user_guide_chart_data_basis(chart_id, ug_text)

    match chart_id:
        case "d_na":
            ug_text += _get_user_guide_distances_chart_footer(
                chart_id,
                chart_title,
            )
        # pylint: disable=line-too-long
        case "ey_aoc" | "ey_il" | "ey_mpf" | "ey_na" | "ey_pf" | "ey_pss" | "ey_t" | "ey_tlp" | "fy_fp" | "fy_sfp":
            ug_text += _get_user_guide_years_chart_footer(
                chart_id,
                chart_title,
            )
        # pylint: disable=line-too-long
        case "te_aoc" | "te_il" | "te_mpf" | "te_na" | "te_pf" | "te_pss" | "te_t" | "te_tlp" | "tf_fp" | "tf_sfp":
            ug_text += _get_user_guide_totals_chart_footer(
                chart_id,
                chart_title,
            )

    st.warning(ug_text)


# ------------------------------------------------------------------
# Creates the description of the data basis.
# ------------------------------------------------------------------
def _get_user_guide_chart_data_basis(chart_id, ug_text):
    ug_text = (
        ug_text
        + """
##### Data basis

"""
    )

    match chart_id:
        case "d_na" | "ey_na" | "te_na":
            ug_text += """
For airport data, the [this FAA publication](https://adds-faa.opendata.arcgis.com/datasets/faa::airports-1/explore?location=0.158824%2C-1.633886%2C2.00) is used with the following selection:         
- Airports in the U.S. states.
- Airports contained in the National Plan of Integrated Airport Systems (NPIAS).

Of the events, only those that occurred in U.S. states are included.

**Hint**: A violin plot is two KDE (kernel density estimation) plots aligned on an axis. 
Any "negative" values are an artifact of KDEs. 
They are estimations of values in the data. 
This does not mean that there are negative data, rather that the data contain values very close to negative values, namely 0. 
And thus there is a non-zero estimated probability of selecting a negative value from the dataset. 
"""

        case "ey_aoc" | "te_aoc":
            ug_text += """
- In the database table **events_sequence** there are the columns **defining_code** and **eventsoe_no**. 
- The values from **eventsoe_no** are used to determine the CICTT code in case **defining_code** equals TRUE via the tables 
**io_sequence_of_events** and **io_aviation_occurrence_categories**. 
- Depending on the number of aircraft involved in the event, several rows may be assigned to the same event in the 
**events_sequence** table. However, this is only critical if it results in different CICTT codes for the same event.
"""

        case "ey_il" | "te_il":
            ug_text += """
- In the database table **events** there is a column **ev_highest_injury** which contains the highest injury level per event. 
- The available database categories are **`FATL`** (fatal injury), **`MINR`** (minor injury), **`NONE`** (no injury) and **`SERS`** (serious injury). 
- If there is no information about the injuries, then the event appears in the category **`n/a`** (not available).
"""

        case "ey_mpf" | "te_mpf":
            ug_text += """
- An event can have several entries in the database table **events_sequence** assigned to it.      
- The **phase_no** column contains the flight phase at the time of the event. 
- The flight phases can be marked as defining events in the **defining_ev** column.
- In the database table **io_md_codes_phase**, each flight phase is assigned a main flight phase.
- From this information, the main flight phases for the aircraft involved in the event can be determined.
"""
        case "ey_pf" | "te_pf":
            ug_text += """
- An event can have several entries in the database table **events_sequence** assigned to it.      
- The **phase_no** column contains the flight phase at the time of the event. 
- The flight phases can be marked as defining events in the **defining_ev** column. 
- From this information, the flight phases for the aircraft involved in the event can be determined.
"""

        case "ey_pss" | "te_pss":
            ug_text += """
- **Airborne Collision Avoidance**: Accident was a mid-air collision
- **Forced landing**: Aircraft in degraded control state ? Aircraft is pitch/roll controllable
- **Spin / stall prevention and recovery**: Aircraft is pitch/roll controllable ? Aircraft in aerodynamic spin or stall
- **Terrain collision avoidance**: Aircraft altitude too low ? Aircraft is pitch/roll controllable ? Aircraft can climb

- **not available**: None of the criteria listed above
"""
        case "ey_t" | "te_t":
            ug_text += """
- In the database table **events** there is a column **ev_type** which contains the type of the event. 
- The available database categories are **`ACC`** (Accident) and **`INC`** (Incident). 
- If there is no information about the event type, then the event appears in the category **`n/a`** (not available).
"""
        case "ey_tlp" | "te_tlp":
            ug_text += """
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
            ug_text += """
- In the database table **aircraft** there is the column **far_part** which contains the FAR operations parts.
- In the database table **events** there is a column **inj_tot_f** which contains the number of fatalities per event.
- Several FAR operations parts can be assigned to the same event, depending on the number of aircraft involved. However, this is only critical if the FAR operation parts are different.
"""
        case "fy_sfp" | "tf_sfp":
            ug_text += """
- In the database table **aircraft** there is the column **far_part** which contains the FAR operations parts.
- In the database table **events** there is a column **inj_tot_f** which contains the number of fatalities per event.
- Several FAR operations parts can be assigned to the same event, depending on the number of aircraft involved. However, this is only critical if the FAR operation parts are different.
"""
        case _:
            ug_text += f"""
### Coming soon ... (chart_id={chart_id})    
"""

    return ug_text


# ------------------------------------------------------------------
# Create the generic header section.
# ------------------------------------------------------------------
def _get_user_guide_chart_header(
    chart_id: str,
    chart_title: str,
) -> str:
    chart_type = "n/a"
    chart_type_1 = "n/a"

    if "d_" in chart_id:
        chart_type = "Box Plot and Violin Plot"
        chart_type_1 = "Only the distance figures are shown here."
    elif "ey_" in chart_id or "fy_" in chart_id:
        chart_type = "Bar Chart"
        chart_type_1 = "Here are the data grouped by year."
    elif "te_" in chart_id or "tf_" in chart_id:
        chart_type = "Pie Chart and Horizontal Bar Chart"
        chart_type_1 = "Only the total figures are shown here."

    return f"""
#### User guide: {chart_type} - {chart_title}

{chart_type_1}
"""


# ------------------------------------------------------------------
# Creates the user guide for the 'Show data profile' task.
# ------------------------------------------------------------------
def _get_user_guide_data_profile() -> None:
    ug_text = """
#### User guide: Show Data Profile

This task performs a data analysis of the underlying database view **io_app_ae1982**. This is done with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/). You can select either the explorative or the minimal version. Depending on the size of the selected data, there may be delayed response times, with the exploratory version again requiring significantly more computational effort than the minimal version.
For further explanations please consult the documentation of **Pandas Profiling**. The result of the data analysis can also be downloaded as **HTML** file if desired.
"""

    st.warning(ug_text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def _get_user_guide_details() -> None:
    ug_text = """
#### User guide: Show details

This task provides the data of the underlying database view **io_app_ae1982** in a table format for display and upload as **csv** file. The rows to be displayed are limited to the chosen filter options. The order of data display is based on the ascending event identification. The database columns of the selected rows are always displayed in full.

##### Usage tips

- **Column sorting**: sort columns by clicking on their headers.
- **Column resizing**: resize columns by dragging and dropping column header borders.
- **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
- **Search**: search through data by clicking a table, using hotkeys ('? Cmd + F' or 'Ctrl + F') to bring up the search bar, and using the search bar to filter data.
- **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
"""

    st.warning(ug_text)


# ------------------------------------------------------------------
# Creates the user guide for the map.
# ------------------------------------------------------------------
def _get_user_guide_map() -> None:
    ug_text = """
#### User guide: Map

The dots on the interactive map show the locations where the selected events took place. By default, the map is focused on the center of the United States. You can move around the map and zoom in and out. Each point on the map contains an interactive popup with additional information such as latitude and longitude or number of fatalities. 

##### Usage tips

- If you hover your mouse over the dots in the map, event related extra information will be shown.
- **Download map as png** (camera symbol): the map can be downloaded as an image file.
- **Zoom out**, **Zoom in**, **Home** (plus, minus and cross symbols): the map can changed in size and focus.
- **View fullscreen** (double arrow): shows the map in fullscreen mode.
"""

    st.warning(ug_text)


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _get_user_guide_distances_chart_footer(
    _chart_id: str,
    _chart_title: str,
) -> str:
    return """
##### Usage tips

- The left side displays the data points underlying the chart.
- If you hover your mouse over the dots in the left, the exact distance in miles will be shown.
- If you hover your mouse over the figure in the right, statistical key figures will be shown.
- **View fullscreen** (double arrow): shows the distances chart in fullscreen mode.
"""


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _get_user_guide_totals_chart_footer(
    chart_id: str,
    _chart_title: str,
) -> str:
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
- **View fullscreen** (double arrow): shows the totals chart in fullscreen mode.
"""


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _get_user_guide_years_chart_footer(
    chart_id: str,
    _chart_title: str,
) -> str:
    objects = (
        "fatalities"
        if chart_id
        in [
            "fy_fp",
            "fy_sfp",
        ]
        else "events"
    )

    ug_text = f"""
##### Usage tips years chart

- If you hover your mouse over the bars, the exact number of {objects} will be shown.
- By clicking on the icons in the legend, you can hide the underlying categories in the chart. 
- **Download chart as png** (camera symbol): the chart can be downloaded as an image file.
- **Zoom out**, **Zoom in**, **Autoscale** (plus, minus and cross symbols): the chart can be resized.
- **Reset axes** (home symbol): reset the axis of the chart.
- **View fullscreen** (double arrow): shows the chart in fullscreen mode.

##### Usage tips detailed data

- **Column sorting**: sort columns by clicking on their headers.
- **Column resizing**: resize columns by dragging and dropping column header borders.
- **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
- **Search**: search through data by clicking a table, using hotkeys ('? Cmd + F' or 'Ctrl + F') to bring up the search bar, 
and using the search bar to filter data.
- **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
"""

    ug_text += """
##### Detailed chart data

If you have selected the checkbox **`Show detailed chart data`** in the filter options, then you get the data underlying 
the chart displayed in a tabular form. 
With the button **Download the chart data** this data can be loaded into a local **csv** file. 
"""

    return ug_text


# ------------------------------------------------------------------
# Prepare the chart data: Distance to the Nearest Airport.
# ------------------------------------------------------------------
def _prep_data_chart_d_na(
    df_filtered: DataFrame,
) -> DataFrame:
    global CHOICE_CHARTS_TYPE_D_NA_NO  # pylint: disable=global-statement

    df_chart_data = _apply_filter_incompatible(df_filtered)

    if CHOICE_CHARTS_TYPE_D_NA_MAX:
        df_chart_data = df_chart_data[
            df_chart_data["nearest_airport_distance"] <= CHOICE_CHARTS_TYPE_D_NA_MAX
        ]

    df_chart_data = df_chart_data.nearest_airport_distance.dropna()

    (CHOICE_CHARTS_TYPE_D_NA_NO,) = df_chart_data.shape

    return _prep_distance_chart(
        df_chart_data,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Number of Events per Year by
# CICTT Codes.
# ------------------------------------------------------------------
def _prep_data_chart_ey_aoc(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_ey_il(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
# Prepare the chart data: Events per Year by Main Phases of Flight.
# ------------------------------------------------------------------
def _prep_data_chart_ey_mpf(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "ev_year",
            "description_main_phase_defining",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    names = []

    for description_main_phase_defining in (
        FILTER_DESCRIPTION_MAIN_PHASES
        if FILTER_DESCRIPTION_MAIN_PHASES
        else _sql_query_description_main_phase()
    ):
        if (
            description_main_phase_defining
            in df_chart.description_main_phase_defining.values
        ):
            names.append(
                (description_main_phase_defining, description_main_phase_defining)
            )

    for name, name_df in names:
        df_chart[name] = np.where(
            df_chart.description_main_phase_defining == name_df, 1, 0
        )

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Nearest Airport.
# ------------------------------------------------------------------
def _prep_data_chart_ey_na(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    df_chart = df_filtered[
        [
            "ev_year",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    interval_1 = f"Up to {CHOICE_CHARTS_TYPE_EY_NA_I_1_OG:.2f} miles"
    interval_2 = f"Up to {CHOICE_CHARTS_TYPE_EY_NA_I_2_OG:.2f} miles"
    interval_3 = f"Above {CHOICE_CHARTS_TYPE_EY_NA_I_2_OG:.2f} miles"

    names = [
        (interval_1, interval_1),
        (interval_2, interval_2),
        (interval_3, interval_3),
    ]

    intervals: list[str | None] = []

    for _index, row in df_filtered.iterrows():
        if row.nearest_airport_distance <= CHOICE_CHARTS_TYPE_EY_NA_I_1_OG:
            intervals.append(interval_1)
        elif row.nearest_airport_distance <= CHOICE_CHARTS_TYPE_EY_NA_I_2_OG:
            intervals.append(interval_2)
        elif row.nearest_airport_servcity is None:
            intervals.append(None)
        else:
            intervals.append(interval_3)

    df_chart["intervals"] = intervals

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.intervals == name_df, 1, 0)

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Events per Year by Phases of Flight.
# ------------------------------------------------------------------
def _prep_data_chart_ey_pf(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
    df_chart = df_filtered[
        [
            "ev_year",
            "phase_codes_defining",
        ]
    ]

    df_chart.rename(
        columns={
            "ev_year": "year",
        },
        inplace=True,
    )

    names = []

    for phase_desc in (
        FILTER_DEFINING_PHASES
        if FILTER_DEFINING_PHASES
        else _sql_query_md_codes_phase()
    ):
        desc, phase = phase_desc.split(" - ")
        if phase in df_chart.phase_codes_defining.values:
            names.append((desc, phase))

    for name, name_df in names:
        df_chart[name] = np.where(df_chart.phase_codes_defining == name_df, 1, 0)

    return names, df_chart.groupby("year", as_index=False).sum(numeric_only=True)


# ------------------------------------------------------------------
# Prepare the chart data: Number of Preventable Events per Year by
# Safety Systems.
# ------------------------------------------------------------------
def _prep_data_chart_ey_pss(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_ey_t(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_ey_tlp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_fy_fp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_fy_sfp(
    df_filtered: DataFrame,
) -> tuple[list[tuple[str, str]], DataFrame]:
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
def _prep_data_chart_te_aoc(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
def _prep_data_chart_te_il(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
# Prepare the chart data: Total Events by Main Phases of Flight.
# ------------------------------------------------------------------
def _prep_data_chart_te_mpf(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "description_main_phase_defining",
        ]
    ]

    name_value = []
    total_pie = 0

    for name in (
        FILTER_DESCRIPTION_MAIN_PHASES
        if FILTER_DESCRIPTION_MAIN_PHASES
        else _sql_query_description_main_phase()
    ):
        df_chart[name] = np.where(
            df_chart.description_main_phase_defining == name, 1, 0
        )
        value = df_chart[name].sum(numeric_only=True)
        if value > 0:
            name_value.append((name, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Phases of Flight.
# ------------------------------------------------------------------
def _prep_data_chart_te_na(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    df_filtered = _apply_filter_incompatible(df_filtered)

    interval_1 = f"Up to {CHOICE_CHARTS_TYPE_TE_NA_I_1_OG:.2f} miles"
    interval_2 = f"Up to {CHOICE_CHARTS_TYPE_TE_NA_I_2_OG:.2f} miles"
    interval_3 = f"Above {CHOICE_CHARTS_TYPE_TE_NA_I_2_OG:.2f} miles"

    total_interval_1 = 0
    total_interval_2 = 0
    total_interval_3 = 0

    for _index, row in df_filtered.iterrows():
        if row.nearest_airport_servcity is None:
            continue

        if row.nearest_airport_distance <= CHOICE_CHARTS_TYPE_TE_NA_I_1_OG:
            total_interval_1 += 1
        elif row.nearest_airport_distance <= CHOICE_CHARTS_TYPE_TE_NA_I_2_OG:
            total_interval_2 += 1
        else:
            total_interval_3 += 1

    total_pie = total_interval_1 + total_interval_2 + total_interval_3

    name_value = [
        (interval_1, total_interval_1),
        (interval_2, total_interval_2),
        (interval_3, total_interval_3),
    ]

    return _prep_totals_chart(
        total_pie,
        name_value,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Events by Phases of Flight.
# ------------------------------------------------------------------
def _prep_data_chart_te_pf(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
    df_filtered = _apply_filter_incompatible(df_filtered)

    df_chart = df_filtered[
        [
            "phase_codes_defining",
        ]
    ]

    name_value = []
    total_pie = 0

    for phase_desc in (
        FILTER_DEFINING_PHASES
        if FILTER_DEFINING_PHASES
        else _sql_query_md_codes_phase()
    ):
        desc, phase = phase_desc.split(" - ")
        df_chart[phase] = np.where(df_chart.phase_codes_defining == phase, 1, 0)
        value = df_chart[phase].sum(numeric_only=True)
        if value > 0:
            name_value.append((desc, value))
            total_pie += value

    return _prep_totals_chart(
        total_pie,
        name_value,
        CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Prepare the chart data: Total Preventable Events by Safety Systems.
# ------------------------------------------------------------------
def _prep_data_chart_te_pss(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
def _prep_data_chart_te_t(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
def _prep_data_chart_te_tlp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
def _prep_data_chart_tf_fp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
def _prep_data_chart_tf_sfp(
    df_filtered: DataFrame,
) -> tuple[list[str], list[int], dict[str, str], DataFrame]:
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
# Prepare the distance chart.
# ------------------------------------------------------------------
def _prep_distance_chart(
    chart_data: DataFrame,
) -> DataFrame:
    return chart_data


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
        use_container_width=True,
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
            help="The upload includes the detailed years chart data.",
            label="Download the years chart data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the bar charts.
# ------------------------------------------------------------------
def _present_bar_charts() -> None:
    # Fatalities per Year by FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FY_FP:
        _present_chart_fy_fp()

    # Fatalities per Year by Selected FAR Operations Parts
    if CHOICE_CHARTS_TYPE_FY_SFP:
        _present_chart_fy_sfp()

    # Events per Year by CICTT Codes
    if CHOICE_CHARTS_TYPE_EY_AOC:
        _present_chart_ey_aoc()

    # Events per Year by Event Types
    if CHOICE_CHARTS_TYPE_EY_T:
        _present_chart_ey_t()

    # Events per Year by Injury Level
    if CHOICE_CHARTS_TYPE_EY_IL:
        _present_chart_ey_il()

    # Events per Year by Main Phases of Flight
    if CHOICE_CHARTS_TYPE_EY_MPF:
        _present_chart_ey_mpf()

    # Events per Year by Nearest Airport
    if CHOICE_CHARTS_TYPE_EY_NA:
        _present_chart_ey_na()

    # Events per Year by Phases of Flight
    if CHOICE_CHARTS_TYPE_EY_PF:
        _present_chart_ey_pf()

    # Preventable Events per Year by Safety Systems
    if CHOICE_CHARTS_TYPE_EY_PSS:
        _present_chart_ey_pss()

    # Events per Year by Top Level Logical Parameters
    if CHOICE_CHARTS_TYPE_EY_TLP:
        _present_chart_ey_tlp()


# ------------------------------------------------------------------
# Present chart: Events per Year by CICTT Codes.
# ------------------------------------------------------------------
def _present_chart_ey_aoc() -> None:
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
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_aoc(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Injury Levels.
# ------------------------------------------------------------------
def _present_chart_ey_il() -> None:
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
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )
    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_il(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Main Phases of Flight.
# ------------------------------------------------------------------
def _present_chart_ey_mpf() -> None:
    chart_id = "ey_mpf"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Main Phases of Flight"

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )

    with col2:
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_mpf(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Nearest Airport.
# ------------------------------------------------------------------
def _present_chart_ey_na() -> None:
    chart_id = "ey_na"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Nearest Airport"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )
    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_na(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Phases of Flight.
# ------------------------------------------------------------------
def _present_chart_ey_pf() -> None:
    chart_id = "ey_pf"
    chart_title = f"Number of {EVENT_TYPE_DESC}s per Year by Phases of Flight"
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )
    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_pf(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Preventable Events per Year by Safety Systems.
# ------------------------------------------------------------------
def _present_chart_ey_pss() -> None:
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
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_pss(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_PSS_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Event Types.
# ------------------------------------------------------------------
def _present_chart_ey_t() -> None:
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
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )
    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )
    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_t(DF_FILTERED),
    )


# ------------------------------------------------------------------
# Present chart: Events per Year by Top Logical Parameters.
# ------------------------------------------------------------------
def _present_chart_ey_tlp() -> None:
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
        choice_ug = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_ey_tlp(DF_FILTERED),
        CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_EY_TLP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Number of Fatalities per Year by
# FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fy_fp() -> None:
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
        choice_ug_years_charts_fy_fp = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug_years_charts_fy_fp:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_fy_fp(DF_FILTERED),
        CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD / 100
        if CHOICE_CHARTS_TYPE_FY_FP_THRESHOLD
        else 0.0,
    )


# ------------------------------------------------------------------
# Present chart: Number of Fatalities per Year by
# Selected FAR Operations Parts.
# ------------------------------------------------------------------
def _present_chart_fy_sfp() -> None:
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
        choice_ug_years_charts_fy_sfp = st.checkbox(
            help="Explanations and operating instructions related to this years chart.",
            key=chart_title,
            label="**User guide: Years chart**",
            value=False,
        )

    if choice_ug_years_charts_fy_sfp:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    _present_bar_chart(
        chart_id,
        chart_title,
        _prep_data_chart_fy_sfp(DF_FILTERED),
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
            if CHOICE_EXTENDED_VERSION:
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

    # ------------------------------------------------------------------
    # Run analysis.
    # ------------------------------------------------------------------

    if CHOICE_RUN_ANALYSIS:
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

        if CHOICE_DATA_GRAPHS_DISTANCES and (CHOICE_BOX_PLOTS or CHOICE_VIOLIN_PLOTS):
            _present_distance_charts()
            _print_timestamp("_present_data() - CHOICE_DATA_GRAPHS_DISTANCE")

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
            label="**User guide: Show data profile**",
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
        help="The upload includes a profile report from the dataframe "
        + "after applying the filter options.",
        label="Download the profile report",
        mime="text/html",
    )


# ------------------------------------------------------------------
# Present details.
# ------------------------------------------------------------------
def _present_details() -> None:
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
                label="**User guide: Show details**",
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
            help="The upload includes all data " + "after applying the filter options.",
            label="Download the detailed data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the distance chart.
# ------------------------------------------------------------------
def _present_distance_chart(
    chart_id: str,
    chart_title: str,
    chart_data: DataFrame,
) -> None:
    chart_title_int = chart_title.replace(
        "{no_rows}", str(CHOICE_CHARTS_TYPE_D_NA_NO)
    ).replace("{event_type}", EVENT_TYPE_DESC + "s")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title_int}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        choice_charts_ug = st.checkbox(
            help="Explanations and operating instructions related to this distance chart(s).",
            key=chart_title_int,
            label="**User guide: Distance chart**",
            value=False,
        )

    if choice_charts_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title_int,
        )

    if CHOICE_BOX_PLOTS:
        fig = px.box(
            chart_data,
            notched=True,
            points="all",
            title=chart_title_int,
            y="nearest_airport_distance",
        )
        fig.update_layout(
            yaxis_title="Distance (mi)",
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    if CHOICE_VIOLIN_PLOTS:
        fig = px.violin(
            chart_data,
            points="all",
            title=chart_title_int,
            y="nearest_airport_distance",
        )
        fig.update_layout(
            yaxis_title="Distance (mi)",
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# ------------------------------------------------------------------
# Present the distance charts.
# ------------------------------------------------------------------
def _present_distance_charts() -> None:
    # Distance to the nearest airport
    if CHOICE_CHARTS_TYPE_D_NA:
        _present_distance_chart(
            "d_na",
            "Distance to the Nearest Airport ({no_rows} {event_type})",
            _prep_data_chart_d_na(DF_FILTERED),
        )


# ------------------------------------------------------------------
# Present the events on the US map.
# ------------------------------------------------------------------
def _present_map() -> None:
    global CHOICE_UG_MAP  # pylint: disable=global-statement

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                + 'font-weight: normal;border-radius:2%;">Map of '
                + EVENT_TYPE_DESC
                + "s"
                + "</p>",
                unsafe_allow_html=True,
            )

    with col2:
        CHOICE_UG_MAP = st.checkbox(
            help="Explanations and operating instructions related to the map.",
            key="Show Map",
            label="**User guide: Map**",
            value=False,
        )

    if CHOICE_UG_MAP:
        _get_user_guide_map()

    # noinspection PyUnboundLocalVariable
    df_filtered_map = DF_FILTERED.loc[
        (DF_FILTERED["dec_latitude"].notna() & DF_FILTERED["dec_longitude"].notna())
    ]

    fig = px.scatter_mapbox(
        df_filtered_map,
        center=_sql_query_us_ll(),
        color="dot_color",
        color_discrete_map={"non-fatal": "MediumBlue", "fatal": "Red"},
        hover_data={
            "dot_color": False,
            "event_city": True,
            "ev_id": True,
            "ntsb_no": True,
            "inj_tot_f": True,
        },
        labels={
            "dec_latitude": "Latitude",
            "dec_longitude": "Longitude",
            "ev_id": "Event",
            "event_city": "City",
            "inj_tot_f": "Fatalities",
            "ntsb_no": "NTSB No.",
        },
        lat="dec_latitude",
        lon="dec_longitude",
        title=f"Map of {EVENT_TYPE_DESC}s",
        zoom=ZOOM,
    )

    fig.update_layout(
        mapbox_style=CHOICE_MAP_MAP_STYLE
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ------------------------------------------------------------------
# Present the totals chart.
# ------------------------------------------------------------------
def _present_totals_chart(
    chart_id: str,
    chart_title: str,
    chart_data: tuple[list[str], list[int], dict[str, str], DataFrame],
) -> None:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
            + f'font-weight: normal;border-radius:2%;">{chart_title}</p>',
            unsafe_allow_html=True,
        )
    with col2:
        choice_charts_ug = st.checkbox(
            help="Explanations and operating instructions related to this totals chart(s).",
            key=chart_title,
            label="**User guide: Totals chart**",
            value=False,
        )

    if choice_charts_ug:
        _get_user_guide_chart(
            chart_id,
            chart_title,
        )

    names, values, color_discrete_map, df_sum = chart_data

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
            use_container_width=True,
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
            use_container_width=True,
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
    # Total Fatalities by FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TF_FP:
        _present_totals_chart(
            "tf_fp",
            "Total Number of Fatalities by FAR Operations Parts",
            _prep_data_chart_tf_fp(DF_FILTERED),
        )

    # Total Fatalities by Selected FAR Operations Parts
    if CHOICE_CHARTS_TYPE_TF_SFP:
        _present_totals_chart(
            "tf_sfp",
            "Total Number of Fatalities by Selected FAR Operations Parts",
            _prep_data_chart_tf_sfp(DF_FILTERED),
        )

    # Total Events by CICTT Code
    if CHOICE_CHARTS_TYPE_TE_AOC:
        _present_totals_chart(
            "te_aoc",
            f"Total Number of {EVENT_TYPE_DESC}s by CICTT Codes",
            _prep_data_chart_te_aoc(DF_FILTERED),
        )

    # Total Events by Event Types
    if CHOICE_CHARTS_TYPE_TE_T:
        _present_totals_chart(
            "te_t",
            f"Total Number of {EVENT_TYPE_DESC}s by Event Types",
            _prep_data_chart_te_t(DF_FILTERED),
        )

    # Total Events by Highest Injury Levels
    if CHOICE_CHARTS_TYPE_TE_IL:
        _present_totals_chart(
            "te_il",
            f"Total Number of {EVENT_TYPE_DESC}s by Highest Injury Levels",
            _prep_data_chart_te_il(DF_FILTERED),
        )

    # Total Events by Main Phases of Flight
    if CHOICE_CHARTS_TYPE_TE_MPF:
        _present_totals_chart(
            "te_mpf",
            f"Total Number of {EVENT_TYPE_DESC}s by Main Phases of Flight",
            _prep_data_chart_te_mpf(DF_FILTERED),
        )

    # Total Events by Nearest Airport
    if CHOICE_CHARTS_TYPE_TE_NA:
        _present_totals_chart(
            "te_na",
            f"Total Number of {EVENT_TYPE_DESC}s by Nearest Airport",
            _prep_data_chart_te_na(DF_FILTERED),
        )

    # Total Events by Phases of Flight
    if CHOICE_CHARTS_TYPE_TE_PF:
        _present_totals_chart(
            "te_pf",
            f"Total Number of {EVENT_TYPE_DESC}s by Phases of Flight",
            _prep_data_chart_te_pf(DF_FILTERED),
        )

    # Total Preventable Events by Safety Systems
    if CHOICE_CHARTS_TYPE_TE_PSS:
        _present_totals_chart(
            "te_pss",
            f"Total Number of Preventable {EVENT_TYPE_DESC}s by Safety Systems",
            _prep_data_chart_te_pss(DF_FILTERED),
        )

    # Total Events by Top Level logical Parameter
    if CHOICE_CHARTS_TYPE_TE_TLP:
        _present_totals_chart(
            "te_tlp",
            f"Total Number of {EVENT_TYPE_DESC}s  by Top Level Logical Parameters",
            _prep_data_chart_te_tlp(DF_FILTERED),
        )


# ------------------------------------------------------------------
# Print a timestamp.
# ------------------------------------------------------------------
# pylint: disable=too-many-statements
def _print_timestamp(identifier: str) -> None:
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
    global CHOICE_ACTIVE_FILTERS_TEXT  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_CICTT_CODES  # pylint: disable=global-statement
    global FILTER_DEFINING_PHASES  # pylint: disable=global-statement
    global FILTER_DESCRIPTION_MAIN_PHASES  # pylint: disable=global-statement
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

    st.sidebar.divider()

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

        st.sidebar.divider()

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

        st.sidebar.divider()

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

    st.sidebar.divider()

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

    st.sidebar.divider()

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

        st.sidebar.divider()

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
        st.sidebar.divider()

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

        st.sidebar.divider()

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

    st.sidebar.divider()

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
        st.sidebar.divider()

        FILTER_DESCRIPTION_MAIN_PHASES = st.sidebar.multiselect(
            help="Here, data can be limited to selected main phases of flight.",
            label="**Main phases of flight:**",
            options=_sql_query_description_main_phase(),
        )
        _print_timestamp("_setup_filter - FILTER_DESCRIPTION_MAIN_PHASES - 1")
        if FILTER_DESCRIPTION_MAIN_PHASES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Main Phases of flight**: **`{','.join(FILTER_DESCRIPTION_MAIN_PHASES)}`**"
            )
        st.sidebar.divider()

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
        st.sidebar.divider()

    if CHOICE_EXTENDED_VERSION:
        FILTER_DEFINING_PHASES = st.sidebar.multiselect(
            help="Here, data can be limited to selected events sequence phases (phases of flight).",
            label="**Phases of flight:**",
            options=_sql_query_md_codes_phase(),
        )
        _print_timestamp("_setup_filter - FILTER_DEFINING_PHASES - 1")
        if FILTER_DEFINING_PHASES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Phases of flight**: **`{','.join(FILTER_DEFINING_PHASES)}`**"
            )
        st.sidebar.divider()

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

    st.sidebar.divider()

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

        st.sidebar.divider()

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

    st.sidebar.divider()

    _print_timestamp("_setup_filter - End")


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page() -> None:
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

    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        + f'font-weight: normal;border-radius:2%;">Aviation {EVENT_TYPE_DESC} Analysis - Year '
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
            label="**User guide: Application**",
            value=False,
        )


# ------------------------------------------------------------------
# Set up the sidebar.
# ------------------------------------------------------------------
def _setup_sidebar() -> None:
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
    global CHOICE_BOX_PLOTS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_D_NA  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_D_NA_MAX  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_AOC  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_AOC_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_IL  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_MPF  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_NA  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_NA_I_1_OG  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_NA_I_2_OG  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_PF  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD  # pylint: disable=global-statement
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
    global CHOICE_CHARTS_TYPE_TE_MPF  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_NA  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_NA_I_1_OG  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_NA_I_2_OG  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PF  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PSS  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_PSS_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_T  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_TLP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TE_TLP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_FP  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_FP_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_CHARTS_TYPE_TF_SFP  # pylint: disable=global-statement
    global CHOICE_DATA_GRAPHS_DISTANCES  # pylint: disable=global-statement
    global CHOICE_DATA_GRAPHS_TOTALS  # pylint: disable=global-statement
    global CHOICE_DATA_GRAPHS_YEARS  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_EXTENDED_VERSION  # pylint: disable=global-statement
    global CHOICE_HORIZONTAL_BAR_CHARTS  # pylint: disable=global-statement
    global CHOICE_MAP  # pylint: disable=global-statement
    global CHOICE_MAP_MAP_STYLE  # pylint: disable=global-statement
    global CHOICE_PIE_CHARTS  # pylint: disable=global-statement
    global CHOICE_RUN_ANALYSIS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_DETAILS_TOTAL_COLS  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_TOTALS_CHARTS_WIDTH  # pylint: disable=global-statement
    global CHOICE_VIOLIN_PLOTS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS_TOTAL_COLS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_DETAILS_TOTAL_ROWS  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_HEIGHT  # pylint: disable=global-statement
    global CHOICE_YEARS_CHARTS_WIDTH  # pylint: disable=global-statement

    # --------------------------------------------------------------
    # Run the Data Analysis.
    # --------------------------------------------------------------
    # pylint: disable=line-too-long
    CHOICE_RUN_ANALYSIS = st.sidebar.checkbox(
        help="""
    For efficiency reasons, it is very useful to define the parameter settings and filter conditions first and then run the selected data analysis.        """,
        key="CHOICE_RUN_ANALYSIS",
        label="**Run the Data Analysis**",
        value=False,
    )

    st.sidebar.divider()

    # ----------------------------------------------------------
    # Extended Version.
    # ----------------------------------------------------------
    CHOICE_EXTENDED_VERSION = st.sidebar.checkbox(
        help="The extended version has more complex filtering and processing options.",
        label="**Extended Version**",
        value=False,
    )

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Map.
    # --------------------------------------------------------------
    CHOICE_MAP = st.sidebar.checkbox(
        help="Display the events on a map (after filtering the data).",
        label="**Show Map**",
        value=False,
    )

    if CHOICE_MAP:
        CHOICE_MAP_MAP_STYLE = st.sidebar.radio(
            help="""
- **carto-positron**: light base map
- **open-street-map**: default representation
- **stamen-terrain**: focused on terrain representation
- **stamen-toner**: black and white representation
- **stamen-watercolor**: focused on water representation
- **white-bg**: pure white background
""",
            index=1,
            label="Map style",
            options=(
                [
                    "carto-positron",
                    "open-street-map",
                    "stamen-terrain",
                    "stamen-toner",
                    "stamen-watercolor",
                    "white-bg",
                ]
            ),
        )

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Data Graph - Years.
    # --------------------------------------------------------------
    CHOICE_DATA_GRAPHS_YEARS = st.sidebar.checkbox(
        help="Events or fatalities per year (after filtering the data).",
        label="**Show Data Graphs - Years**",
        value=False,
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

            st.sidebar.divider()

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
            value=False,
        )

        CHOICE_CHARTS_TYPE_EY_AOC = st.sidebar.checkbox(
            help="Events per year by CICTT codes (after filtering the data).",
            label=f"{EVENT_TYPE_DESC}s per Year by CICTT Codes",
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
                label=f"{EVENT_TYPE_DESC}s per Year by Event Types",
                value=False,
            )
            CHOICE_CHARTS_TYPE_EY_IL = st.sidebar.checkbox(
                help="Events per year by highest injury level (after filtering the data).",
                label=f"{EVENT_TYPE_DESC}s per Year by Highest Injury Levels",
                value=False,
            )

            CHOICE_CHARTS_TYPE_EY_MPF = st.sidebar.checkbox(
                help="Events per year by main phases of flight (after filtering the data).",
                label=f"{EVENT_TYPE_DESC}s per Year by Main Phases of Flight",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_EY_MPF:
                CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_EY_MPF_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

            # pylint: disable=line-too-long
            CHOICE_CHARTS_TYPE_EY_NA = st.sidebar.checkbox(
                help="Events per year by distance to the nearest airport (after filtering the data).",
                label=f"{EVENT_TYPE_DESC}s per Year by Nearest Airport",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_EY_NA:
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    CHOICE_CHARTS_TYPE_EY_NA_I_1_OG = col1.number_input(
                        help="Upper limit first interval",
                        key="CHOICE_CHARTS_TYPE_EY_NA_I_1_OG",
                        label="Upper limit 1",
                        max_value=100.0,
                        min_value=0.0,
                        value=0.5,
                    )
                with col2:
                    CHOICE_CHARTS_TYPE_EY_NA_I_2_OG = col2.number_input(
                        help="Upper limit first interval",
                        key="CHOICE_CHARTS_TYPE_EY_NA_I_2_OG",
                        label="Upper limit 2",
                        max_value=100.0,
                        min_value=0.0,
                        value=5.0,
                    )
                if CHOICE_CHARTS_TYPE_EY_NA_I_2_OG <= CHOICE_CHARTS_TYPE_EY_NA_I_1_OG:
                    # pylint: disable=line-too-long
                    st.error(
                        "##### Error: Events per Year by Nearest Airport: The upper limit 2 must be greater than the upper limit 1."
                    )
                    st.stop()

            CHOICE_CHARTS_TYPE_EY_PF = st.sidebar.checkbox(
                help="Events per year by phases of flight (after filtering the data).",
                label=f"{EVENT_TYPE_DESC}s per Year by Phases of Flight",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_EY_PF:
                CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_EY_PF_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

        CHOICE_CHARTS_TYPE_EY_PSS = st.sidebar.checkbox(
            help="Preventable events per year by safety systems (after filtering the data).",
            label=f"Preventable {EVENT_TYPE_DESC}s per Year by Safety Systems",
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

        CHOICE_CHARTS_TYPE_EY_TLP = st.sidebar.checkbox(
            help="Events per year by top level logical parameters (after filtering the data).",
            label=f"{EVENT_TYPE_DESC}s per Year by Top Level Logical Parameters",
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

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Data Graph - Totals.
    # --------------------------------------------------------------
    CHOICE_DATA_GRAPHS_TOTALS = st.sidebar.checkbox(
        help=f"Total {EVENT_TYPE_DESC}s or fatalities (after filtering the data).",
        label="**Show Data Graphs - Totals**",
        value=False,
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

        st.sidebar.divider()

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
            value=False,
        )

        CHOICE_CHARTS_TYPE_TE_AOC = st.sidebar.checkbox(
            help="Total events by CICTT codes (after filtering the data).",
            label=f"Total {EVENT_TYPE_DESC}s by CICTT Codes",
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
                label=f"Total {EVENT_TYPE_DESC}s by Event Types",
                value=False,
            )
            CHOICE_CHARTS_TYPE_TE_IL = st.sidebar.checkbox(
                help="Total events by highest injury levels (after filtering the data).",
                label=f"Total {EVENT_TYPE_DESC}s by Highest Injury Levels",
                value=False,
            )

            CHOICE_CHARTS_TYPE_TE_MPF = st.sidebar.checkbox(
                help="Total events by main phases of flight (after filtering the data).",
                label=f"Total {EVENT_TYPE_DESC}s by Main Phases of Flight",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TE_MPF:
                CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_TE_MPF_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

            CHOICE_CHARTS_TYPE_TE_NA = st.sidebar.checkbox(
                help="Total events by distance to the nearest airport (after filtering the data).",
                label=f"Total {EVENT_TYPE_DESC}s by Nearest Airport",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TE_NA:
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    CHOICE_CHARTS_TYPE_TE_NA_I_1_OG = col1.number_input(
                        help="Upper limit first interval",
                        key="CHOICE_CHARTS_TYPE_TE_NA_I_1_OG",
                        label="Upper limit 1",
                        max_value=100.0,
                        min_value=0.0,
                        value=0.5,
                    )
                with col2:
                    CHOICE_CHARTS_TYPE_TE_NA_I_2_OG = col2.number_input(
                        help="Upper limit first interval",
                        key="CHOICE_CHARTS_TYPE_TE_NA_I_2_OG",
                        label="Upper limit 2",
                        max_value=100.0,
                        min_value=0.0,
                        value=5.0,
                    )
                if CHOICE_CHARTS_TYPE_TE_NA_I_2_OG <= CHOICE_CHARTS_TYPE_TE_NA_I_1_OG:
                    # pylint: disable=line-too-long
                    st.error(
                        "##### Error: Total Events by Nearest Airport: The upper limit 2 must be greater than the upper limit 1."
                    )
                    st.stop()

            CHOICE_CHARTS_TYPE_TE_PF = st.sidebar.checkbox(
                help="Total events by phases of flight (after filtering the data).",
                label=f"Total {EVENT_TYPE_DESC}s by Phases of Flight",
                value=False,
            )
            if CHOICE_CHARTS_TYPE_TE_PF:
                CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD = st.sidebar.number_input(
                    help="Threshold percentage for combined display",
                    key="CHOICE_CHARTS_TYPE_TE_PF_THRESHOLD",
                    label="Threshold value in %",
                    max_value=20.0,
                    min_value=0.0,
                    value=1.5,
                )

        CHOICE_CHARTS_TYPE_TE_PSS = st.sidebar.checkbox(
            help="Total preventable events by safety systems (after filtering the data).",
            label=f"Total Preventable {EVENT_TYPE_DESC}s by Safety Systems",
            value=False,
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

        CHOICE_CHARTS_TYPE_TE_TLP = st.sidebar.checkbox(
            help="Total events by top level logical parameters (after filtering the data).",
            label=f"Total {EVENT_TYPE_DESC}s by Top Level Logical Parameters",
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

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Data Graph - Distances.
    # --------------------------------------------------------------
    CHOICE_DATA_GRAPHS_DISTANCES = st.sidebar.checkbox(
        help="Distances (after filtering the data).",
        label="**Show Data Graphs - Distances**",
        value=False,
    )

    if CHOICE_DATA_GRAPHS_DISTANCES:
        CHOICE_BOX_PLOTS = st.sidebar.checkbox(
            help="Presenting distances with box plots.",
            key="CHOICE_BOX_PLOTS",
            label="Show box plots",
            value=False,
        )
        CHOICE_VIOLIN_PLOTS = st.sidebar.checkbox(
            help="Presenting distances with violin plots.",
            key="CHOICE_VIOLIN_PLOTS",
            label="Show voline plots",
            value=True,
        )

        st.sidebar.divider()

        # pylint: disable=line-too-long
        CHOICE_CHARTS_TYPE_D_NA = st.sidebar.checkbox(
            help="Distance in miles from the place of the event to the nearest airport (after filtering the data).",
            label="Distance to the Nearest Airport",
            value=False,
        )
        if CHOICE_CHARTS_TYPE_D_NA:
            CHOICE_CHARTS_TYPE_D_NA_MAX = st.sidebar.number_input(
                help="Maximum distance in miles",
                key="CHOICE_CHARTS_TYPE_D_NA_MAX",
                label="Maximum distance in miles",
                max_value=5000.0,
                step=5.0,
                value=100.0,
            )

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Data Profile.
    # --------------------------------------------------------------
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

    st.sidebar.divider()

    # --------------------------------------------------------------
    # Show Detailed Data.
    # --------------------------------------------------------------
    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed data.",
        label="**Show Detailed Data**",
        value=False,
    )

    st.sidebar.divider()


# ------------------------------------------------------------------
# Execute a query that returns the list of aircraft categories.
# ------------------------------------------------------------------
def _sql_query_acft_categories() -> list[str]:
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
# Execute a query that returns the list of descriptions of main phases
# of flight.
# ------------------------------------------------------------------
def _sql_query_description_main_phase() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT DISTINCT description_main_phase
          FROM io_md_codes_phase;
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
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MAX(inj_tot_f)
          FROM io_app_ae1982;
"""
        )
        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of phases.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_phase() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', phase_code), ',' ORDER BY 1)
          FROM io_md_codes_phase;
"""
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of occurrence codes.
# ------------------------------------------------------------------
def _sql_query_occurrence_codes() -> list[str]:
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
def _sql_query_us_ll() -> dict[str, float]:
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
        return {"lat": result[0], "lon": result[1]}  # type: ignore


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
    global DF_FILTERED  # pylint: disable=global-statement
    global DF_UNFILTERED  # pylint: disable=global-statement
    global EVENT_TYPE_DESC  # pylint: disable=global-statement
    global HOST_CLOUD  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement
    global START_TIME  # pylint: disable=global-statement

    # Start time measurement.
    START_TIME = time.time_ns()

    if "HOST_CLOUD" in st.session_state:
        EVENT_TYPE_DESC = "Event"
        HOST_CLOUD = st.session_state["HOST_CLOUD"]
    else:
        host = utils.get_args()
        EVENT_TYPE_DESC = "Accident"
        HOST_CLOUD = bool(host == "Cloud")
        st.session_state["HOST_CLOUD"] = HOST_CLOUD

    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Favicon.ico?raw=true",
        page_title="ae1982 by IO-Aero",
    )

    st.sidebar.markdown("##  [IO-Aero Website](https://www.io-aero.com)")

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Logo.png?raw=true",
        width=200,
    )

    PG_CONN = utils.get_postgres_connection()
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
        + f" {f'{time.time_ns() - START_TIME:,}':>20} ns - Total runtime for application {APP_ID:<10}",
        flush=True,
    )


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

_streamlit_flow()
