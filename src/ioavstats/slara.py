# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Association Rule Analysis."""
import datetime
import time

import numpy
import pandas as pd
import plotly.express as px  # type: ignore
import psycopg2
import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from mlxtend.frequent_patterns import apriori  # type: ignore
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth  # type: ignore
from mlxtend.frequent_patterns import fpmax  # type: ignore
from pandas import DataFrame
from psycopg2.extensions import connection
from pyECLAT import ECLAT  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from streamlit_pandas_profiling import st_profile_report  # type: ignore
from ydata_profiling import ProfileReport  # type: ignore

# SettingWithCopyWarning
pd.options.mode.chained_assignment: str | None = None  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "slara"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_ABOUT: bool | None = None
CHOICE_ACTIVE_FILTERS: bool | None = None
CHOICE_ACTIVE_FILTERS_TEXT: str = ""
CHOICE_ALG_APRIORI: bool | None = None
CHOICE_ALG_ECLAT: bool | None = None
CHOICE_ALG_FPGROWTH: bool | None = None
CHOICE_ALG_FPMAX: bool | None = None
CHOICE_ALG_METRIC: str | None = None
CHOICE_ALG_COMBINATIONS_CURRENT: int = 0
CHOICE_ALG_COMBINATIONS_MAX: int = 0
CHOICE_ALG_COMBINATIONS_MIN: int = 0
CHOICE_ALG_MIN_SUPPORT: float | None = None
CHOICE_ALG_MIN_THRESHOLD: float | None = None

CHOICE_FILTER_DATA_EVENTS_SEQUENCE: bool | None = None
CHOICE_FILTER_DATA_FINDINGS: bool | None = None
CHOICE_FILTER_DATA_OTHER: bool | None = None

CHOICE_RUN_ALGORITHMS: bool | None = None

CHOICE_SHOW_ASSOCIATION_RULES: bool | None = None
CHOICE_SHOW_BINARY_DATA_ECLAT: bool | None = None
CHOICE_SHOW_FILTERED_RAW_DATA: bool | None = None
CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE: bool | None = None
CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE_TYPE: str | None = None
CHOICE_SHOW_FREQUENT_ITEMSETS: bool | None = None
CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT: bool | None = None
CHOICE_SHOW_ONE_HOT_ENCODED_DATA: bool | None = None
CHOICE_SHOW_TRANSACTION_DATA: bool | None = None

CHOICE_UG_APP: bool | None = None

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

COUNTRY_USA = "USA"

DF_ASSOCIATION_RULES_APRIORI: DataFrame = DataFrame()
DF_ASSOCIATION_RULES_ECLAT: DataFrame = DataFrame()
DF_ASSOCIATION_RULES_FPGROWTH: DataFrame = DataFrame()
DF_ASSOCIATION_RULES_FPMAX: DataFrame = DataFrame()
DF_BINARY_DATA_ECLAT: DataFrame = DataFrame()
DF_BINARY_DATA_ONE_HOT_ENCODED: DataFrame = DataFrame()
DF_FREQUENT_ITEMSETS_APRIORI: DataFrame = DataFrame()
DF_FREQUENT_ITEMSETS_ECLAT: DataFrame = DataFrame()
DF_FREQUENT_ITEMSETS_FPGROWTH: DataFrame = DataFrame()
DF_FREQUENT_ITEMSETS_FPMAX: DataFrame = DataFrame()
DF_ITEM_DISTRIBUTION_ECLAT_EXT: DataFrame = DataFrame()
DF_RAW_DATA_FILTERED: DataFrame = DataFrame()
DF_RAW_DATA_FILTERED_ROWS = 0
DF_RAW_DATA_UNFILTERED: DataFrame = DataFrame()
DF_RAW_DATA_UNFILTERED_ROWS = 0
DF_TRANSACTION_DATA: DataFrame = DataFrame()
DF_TRANSACTION_DATA_ECLAT: DataFrame = DataFrame()

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_EV_HIGHEST_INJURY: list[str] = []
FILTER_EV_HIGHEST_INJURY_DEFAULT: list[str] = ["fatal"]
FILTER_EV_TYPE: list[str] = []
FILTER_EV_TYPE_DEFAULT = ["Accident"]
FILTER_EV_YEAR_INCOMPATIBLE = 2008
FILTER_EV_YEAR_FROM: int | None = None
FILTER_EV_YEAR_TO: int | None = None
FILTER_EVENTS_SEQUENCE_EVENTSOES: list[str] = []
FILTER_EVENTS_SEQUENCE_PHASES: list[str] = []
FILTER_FINDINGS_CATEGORIES: list[str] = []
FILTER_FINDINGS_MODIFIERS: list[str] = []
FILTER_FINDINGS_SECTIONS: list[str] = []
FILTER_FINDINGS_SUBCATEGORIES: list[str] = []
FILTER_FINDINGS_SUBSECTIONS: list[str] = []
FILTER_INJ_F_GRND_FROM: int | None = None
FILTER_INJ_F_GRND_TO: int | None = None
FILTER_INJ_TOT_F_FROM: int | None = None
FILTER_INJ_TOT_F_TO: int | None = None
FILTER_NO_AIRCRAFT_FROM: int | None = None
FILTER_NO_AIRCRAFT_TO: int | None = None
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

ITEMS_FROM_ES_EVENTSOE_CODES_ALL: bool | None = None
ITEMS_FROM_ES_EVENTSOE_CODES_FALSE: bool | None = None
ITEMS_FROM_ES_EVENTSOE_CODES_TRUE: bool | None = None
ITEMS_FROM_ES_OCCURRENCE_CODES_ALL: bool | None = None
ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE: bool | None = None
ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE: bool | None = None
ITEMS_FROM_ES_PHASE_CODES_ALL: bool | None = None
ITEMS_FROM_ES_PHASE_CODES_FALSE: bool | None = None
ITEMS_FROM_ES_PHASE_CODES_TRUE: bool | None = None
ITEMS_FROM_F_CATEGORY_CODES_ALL: bool | None = None
ITEMS_FROM_F_CATEGORY_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_CATEGORY_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_CATEGORY_CODES_NONE: bool | None = None
ITEMS_FROM_F_FINDING_CODES_ALL: bool | None = None
ITEMS_FROM_F_FINDING_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_FINDING_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_FINDING_CODES_NONE: bool | None = None
ITEMS_FROM_F_MODIFIER_CODES_ALL: bool | None = None
ITEMS_FROM_F_MODIFIER_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_MODIFIER_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_MODIFIER_CODES_NONE: bool | None = None
ITEMS_FROM_F_SECTION_CODES_ALL: bool | None = None
ITEMS_FROM_F_SECTION_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_SECTION_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_SECTION_CODES_NONE: bool | None = None
ITEMS_FROM_F_SUBCATEGORY_CODES_ALL: bool | None = None
ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_SUBCATEGORY_CODES_NONE: bool | None = None
ITEMS_FROM_F_SUBSECTION_CODES_ALL: bool | None = None
ITEMS_FROM_F_SUBSECTION_CODES_CAUSE: bool | None = None
ITEMS_FROM_F_SUBSECTION_CODES_FACTOR: bool | None = None
ITEMS_FROM_F_SUBSECTION_CODES_NONE: bool | None = None

LAST_READING: int = 0
# LAYER_TYPE = "HexagonLayer"
LAYER_TYPE = "ScatterplotLayer"
LEGEND_N_A = "n/a"
LEGEND_N_A_DESC = "no data"
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"

MD_CODES_CATEGORY: dict[str, str] = {}
MD_CODES_EVENTSOE: dict[str, str] = {}
MD_CODES_MODIFIER: dict[str, str] = {}
MD_CODES_PHASE: dict[str, str] = {}
MD_CODES_SECTION: dict[str, str] = {}
MD_CODES_SUBCATEGORY: dict[str, str] = {}
MD_CODES_SUBSECTION: dict[str, str] = {}

OPTIONS_EV_HIGHEST_INJURY = {
    "FATL": "fatal",
    "MINR": "minor",
    "NONE": "none",
    "SERS": "serious",
    "UNKN": "unknown",
    "n/a": LEGEND_N_A_DESC,
}

OPTIONS_EV_TYPE = {
    "ACC": "Accident",
    "INC": "Incident",
    "n/a": LEGEND_N_A_DESC,
}

PG_CONN: connection | None = None

# ------------------------------------------------------------------
# Configuration parameters.
# ------------------------------------------------------------------
SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)
START_TIME: int = 0


# ------------------------------------------------------------------
# Apply the algorithms.
# ------------------------------------------------------------------
def _apply_algorithm() -> None:
    global DF_ASSOCIATION_RULES_APRIORI  # pylint: disable=global-statement
    global DF_ASSOCIATION_RULES_FPGROWTH  # pylint: disable=global-statement
    global DF_ASSOCIATION_RULES_FPMAX  # pylint: disable=global-statement
    global DF_BINARY_DATA_ONE_HOT_ENCODED  # pylint: disable=global-statement
    global DF_FREQUENT_ITEMSETS_APRIORI  # pylint: disable=global-statement
    global DF_FREQUENT_ITEMSETS_FPGROWTH  # pylint: disable=global-statement
    global DF_FREQUENT_ITEMSETS_FPMAX  # pylint: disable=global-statement

    if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
        if (
            CHOICE_SHOW_ASSOCIATION_RULES
            or CHOICE_SHOW_FREQUENT_ITEMSETS
            or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
            or CHOICE_SHOW_ONE_HOT_ENCODED_DATA
            or CHOICE_SHOW_TRANSACTION_DATA
        ):
            _create_transaction_data()
            if (
                CHOICE_SHOW_ASSOCIATION_RULES
                or CHOICE_SHOW_FREQUENT_ITEMSETS
                or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
                or CHOICE_SHOW_ONE_HOT_ENCODED_DATA
            ):
                DF_BINARY_DATA_ONE_HOT_ENCODED = (
                    DF_TRANSACTION_DATA["items"].str.join("|").str.get_dummies()
                )
                if (
                    CHOICE_SHOW_ASSOCIATION_RULES
                    or CHOICE_SHOW_FREQUENT_ITEMSETS
                    or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
                ):
                    if CHOICE_ALG_APRIORI:
                        DF_FREQUENT_ITEMSETS_APRIORI = (
                            _create_frequent_itemsets_apriori(
                                DF_BINARY_DATA_ONE_HOT_ENCODED,
                                CHOICE_ALG_MIN_SUPPORT,
                            )
                        )
                        # pylint: disable=line-too-long
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_APRIORI  - _create_frequent_itemsets_apriori"
                        )
                        DF_ASSOCIATION_RULES_APRIORI = association_rules(
                            DF_FREQUENT_ITEMSETS_APRIORI,
                            CHOICE_ALG_METRIC,
                            CHOICE_ALG_MIN_THRESHOLD,
                        )
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_APRIORI  - association_rules"
                        )
                    if CHOICE_ALG_FPGROWTH:
                        DF_FREQUENT_ITEMSETS_FPGROWTH = (
                            _create_frequent_itemsets_fpgrowth(
                                DF_BINARY_DATA_ONE_HOT_ENCODED,
                                CHOICE_ALG_MIN_SUPPORT,
                            )
                        )
                        # pylint: disable=line-too-long
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_FPGROWTH - _create_frequent_itemsets_fpgrowth"
                        )
                        DF_ASSOCIATION_RULES_FPGROWTH = association_rules(
                            DF_FREQUENT_ITEMSETS_FPGROWTH,
                            CHOICE_ALG_METRIC,
                            CHOICE_ALG_MIN_THRESHOLD,
                        )
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_FPGROWTH - association_rules"
                        )
                    if CHOICE_ALG_FPMAX:
                        DF_FREQUENT_ITEMSETS_FPMAX = _create_frequent_itemsets_fpmax(
                            DF_BINARY_DATA_ONE_HOT_ENCODED,
                            CHOICE_ALG_MIN_SUPPORT,
                        )
                        # pylint: disable=line-too-long
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_FPMAX    - _create_frequent_itemsets_fpmax"
                        )
                        DF_ASSOCIATION_RULES_FPMAX = association_rules(
                            DF_FREQUENT_ITEMSETS_FPMAX,
                            CHOICE_ALG_METRIC,
                            CHOICE_ALG_MIN_THRESHOLD,
                            support_only=True,
                        )
                        _print_timestamp(
                            "_apply_algorithm() - CHOICE_ALG_FPMAX    - association_rules"
                        )

        return

    if CHOICE_ALG_ECLAT:
        if (
            CHOICE_SHOW_ASSOCIATION_RULES
            or CHOICE_SHOW_BINARY_DATA_ECLAT
            or CHOICE_SHOW_FREQUENT_ITEMSETS
            or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
            or CHOICE_SHOW_TRANSACTION_DATA
        ):
            _create_transaction_data_eclat()
            if (
                CHOICE_SHOW_ASSOCIATION_RULES
                or CHOICE_SHOW_BINARY_DATA_ECLAT
                or CHOICE_SHOW_FREQUENT_ITEMSETS
                or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
            ):
                _apply_algorithm_eclat()

    _print_timestamp("_apply_algorithm()")


# ------------------------------------------------------------------
# Apply the Eclat Algorithm.
# ------------------------------------------------------------------
def _apply_algorithm_eclat() -> None:
    global CHOICE_ALG_COMBINATIONS_CURRENT  # pylint: disable=global-statement
    global CHOICE_ALG_COMBINATIONS_MAX  # pylint: disable=global-statement
    global CHOICE_ALG_COMBINATIONS_MIN  # pylint: disable=global-statement
    global DF_ASSOCIATION_RULES_ECLAT  # pylint: disable=global-statement
    global DF_BINARY_DATA_ECLAT  # pylint: disable=global-statement
    global DF_FREQUENT_ITEMSETS_ECLAT  # pylint: disable=global-statement
    global DF_ITEM_DISTRIBUTION_ECLAT_EXT  # pylint: disable=global-statement

    eclat = ECLAT(DF_TRANSACTION_DATA_ECLAT, CHOICE_ALG_MIN_SUPPORT)

    # --------------------------------------------------------------------------
    if CHOICE_SHOW_BINARY_DATA_ECLAT:
        DF_BINARY_DATA_ECLAT = eclat.df_bin

    # --------------------------------------------------------------------------
    if (
        CHOICE_SHOW_ASSOCIATION_RULES
        or CHOICE_SHOW_FREQUENT_ITEMSETS
        or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
    ):
        CHOICE_ALG_COMBINATIONS_CURRENT = max(eclat.df_bin.astype(int).sum(axis=1))

        # ----------------------------------------------------------------------
        if (
            CHOICE_SHOW_FREQUENT_ITEMSETS
            or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
        ):
            items_total = eclat.df_bin.astype(int).sum(axis=0)
            items_transactions_gross = pd.DataFrame(
                {
                    "item": items_total.index,
                    "item_description": " ",
                    "transactions": items_total.values,
                }
            )
            DF_FREQUENT_ITEMSETS_ECLAT = items_transactions_gross.loc[
                items_transactions_gross["item"] > " "
            ]
            df_item_distribution_eclat_ext = _get_description_items(
                DF_FREQUENT_ITEMSETS_ECLAT
            )

            DF_ITEM_DISTRIBUTION_ECLAT_EXT = df_item_distribution_eclat_ext.sort_values(
                "transactions", ascending=False
            )

        # ----------------------------------------------------------------------
        if CHOICE_SHOW_ASSOCIATION_RULES:
            CHOICE_ALG_COMBINATIONS_MIN = min(
                CHOICE_ALG_COMBINATIONS_MIN, CHOICE_ALG_COMBINATIONS_CURRENT
            )
            CHOICE_ALG_COMBINATIONS_MAX = min(
                CHOICE_ALG_COMBINATIONS_MAX, CHOICE_ALG_COMBINATIONS_CURRENT
            )

            _, rule_supports = eclat.fit(
                min_support=CHOICE_ALG_MIN_SUPPORT,
                min_combination=CHOICE_ALG_COMBINATIONS_MIN,
                max_combination=CHOICE_ALG_COMBINATIONS_MAX,
                separator=" & ",
                verbose=True,
            )

            DF_ASSOCIATION_RULES_ECLAT = pd.DataFrame(
                rule_supports.items(), columns=["Item", "Support"]
            ).sort_values(by=["Support"], ascending=False)

    _print_timestamp("_apply_algorithm_eclat()")


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
    if FILTER_EVENTS_SEQUENCE_EVENTSOES:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_eventsoe_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_EVENTS_SEQUENCE_EVENTSOES, "ee")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_EVENTS_SEQUENCE_EVENTSOES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_EVENTS_SEQUENCE_PHASES:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_phase_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_EVENTS_SEQUENCE_PHASES, "ep")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_EVENTS_SEQUENCE_PHASES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDINGS_CATEGORIES:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_category_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_FINDINGS_CATEGORIES, "fc")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDINGS_CATEGORIES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDINGS_MODIFIERS:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_modifier_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_FINDINGS_MODIFIERS, "fm")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDINGS_MODIFIERS"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDINGS_SECTIONS:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_section_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_FINDINGS_SECTIONS, "fs")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDINGS_SECTIONS"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDINGS_SUBCATEGORIES:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_subcategory_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_FINDINGS_SUBCATEGORIES, "fsc")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDINGS_SUBCATEGORIES"
        )

    # noinspection PyUnboundLocalVariable
    if FILTER_FINDINGS_SUBSECTIONS:
        # noinspection PyUnboundLocalVariable
        # pylint: disable=line-too-long
        df_filtered = df_filtered.loc[
            df_filtered["all_subsection_codes"].apply(
                lambda x: bool(set(x) & set(_get_prepared_codes(FILTER_FINDINGS_SUBSECTIONS, "fss")))  # type: ignore
            )
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_FINDINGS_SUBSECTIONS"
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
    if FILTER_NO_AIRCRAFT_FROM or FILTER_NO_AIRCRAFT_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["no_aircraft"] >= FILTER_NO_AIRCRAFT_FROM)
            & (df_filtered["no_aircraft"] <= FILTER_NO_AIRCRAFT_TO)
        ]
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - filter_no_aircraft_from/to"
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

    _print_timestamp("_apply_filter_incompatible()")

    return df_filtered


# ------------------------------------------------------------------
# Filter the data frame - US aviation.
# ------------------------------------------------------------------
def _apply_filter_us_aviation(
    _df_unfiltered: DataFrame,  # pylint: disable=unused-argument
    filter_params: list | None,
) -> DataFrame:
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

    _print_timestamp("_apply_filter_us_aviation()")

    return df_filtered


# ------------------------------------------------------------------
# Create the external association rules including the descriptions.
# ------------------------------------------------------------------
def _create_df_association_rules_ext(df_int: DataFrame) -> DataFrame:
    df_ext = df_int.copy()

    df_ext.insert(1, "antecedents_description", "")
    df_ext.insert(3, "consequents_description", "")

    for idx in df_ext.index:
        df_ext["antecedents_description"][idx] = _get_items_description(
            df_ext["antecedents"][idx]
        )
        df_ext["consequents_description"][idx] = _get_items_description(
            df_ext["consequents"][idx]
        )

    _print_timestamp("_create_df_association_rules_ext()")

    return df_ext


# ------------------------------------------------------------------
# Create the external association rules including the descriptions.
# ------------------------------------------------------------------
def _create_df_association_rules_ext_eclat(df_int: DataFrame) -> DataFrame:
    df_ext = df_int.copy()

    df_ext.insert(1, "Item_description", "")

    for idx in df_ext.index:
        items = df_ext["Item"][idx].split(" & ")
        df_ext["Item_description"][idx] = _get_items_description(items)

    _print_timestamp("_create_df_association_rules_ext_eclat()")

    return df_ext


# ------------------------------------------------------------------
# Create frequent itemsets with the Apriori Algorithm.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _create_frequent_itemsets_apriori(
    df_binary_data_one_hot_encoded: DataFrame, min_support: float | None
) -> DataFrame:
    df_frequent_itemsets = apriori(
        df_binary_data_one_hot_encoded,
        min_support=min_support,
        use_colnames=True,
    )

    if df_frequent_itemsets.empty:
        # pylint: disable=line-too-long
        st.error(
            "##### Error: The selected Apriori Algorithm did not find any data with the given items and parameters."
        )
        st.stop()

    _print_timestamp("_create_frequent_itemsets_apriori()")

    return df_frequent_itemsets


# ------------------------------------------------------------------
# Create frequent itemsets with the FP-Growth Algorithm.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _create_frequent_itemsets_fpgrowth(
    df_binary_data_one_hot_encoded: DataFrame, min_support: float | None
) -> DataFrame:
    df_frequent_itemsets = fpgrowth(
        df_binary_data_one_hot_encoded,
        min_support=min_support,
        use_colnames=True,
    )

    if df_frequent_itemsets.empty:
        # pylint: disable=line-too-long
        st.error(
            "##### Error: The selected FP-Growth Algorithm did not find any data with the given items and parameters."
        )
        st.stop()

    _print_timestamp("_create_frequent_itemsets_fpgrowth()")

    return df_frequent_itemsets


# ------------------------------------------------------------------
# Create frequent itemsets with the FP-Max Algorithm.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _create_frequent_itemsets_fpmax(
    df_binary_data_one_hot_encoded: DataFrame, min_support: float | None
) -> DataFrame:
    df_frequent_itemsets = fpmax(
        df_binary_data_one_hot_encoded,
        min_support=min_support,
        use_colnames=True,
    )

    if df_frequent_itemsets.empty:
        # pylint: disable=line-too-long
        st.error(
            "##### Error: The selected FP-Max Algorithm did not find any data with the given items and parameters."
        )
        st.stop()

    _print_timestamp("_create_frequent_itemsets_fpmax()")

    return df_frequent_itemsets


# ------------------------------------------------------------------
# Create the transaction dataframe.
# ------------------------------------------------------------------
def _create_transaction_data() -> None:
    transaction_cmd = "("

    if ITEMS_FROM_ES_EVENTSOE_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_eventsoe_codes']"
    else:
        if ITEMS_FROM_ES_EVENTSOE_CODES_FALSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_eventsoe_false_codes']"
        if ITEMS_FROM_ES_EVENTSOE_CODES_TRUE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_eventsoe_true_codes']"

    if ITEMS_FROM_ES_OCCURRENCE_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_occurrence_codes']"
    else:
        if ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_occurrence_false_codes']"
        if ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_occurrence_true_codes']"

    if ITEMS_FROM_ES_PHASE_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_phase_codes']"
    else:
        if ITEMS_FROM_ES_PHASE_CODES_FALSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_phase_false_codes']"
        if ITEMS_FROM_ES_PHASE_CODES_TRUE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_phase_true_codes']"

    if ITEMS_FROM_F_CATEGORY_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_category_codes']"
    else:
        if ITEMS_FROM_F_CATEGORY_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_category_cause_codes']"
        if ITEMS_FROM_F_CATEGORY_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_category_factor_codes']"
        if ITEMS_FROM_F_CATEGORY_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_category_none_codes']"

    if ITEMS_FROM_F_FINDING_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_finding_codes']"
    else:
        if ITEMS_FROM_F_FINDING_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_finding_cause_codes']"
        if ITEMS_FROM_F_FINDING_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_finding_factor_codes']"
        if ITEMS_FROM_F_FINDING_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_finding_none_codes']"

    if ITEMS_FROM_F_MODIFIER_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_modifier_codes']"
    else:
        if ITEMS_FROM_F_MODIFIER_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_modifier_cause_codes']"
        if ITEMS_FROM_F_MODIFIER_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_modifier_factor_codes']"
        if ITEMS_FROM_F_MODIFIER_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_modifier_none_codes']"

    if ITEMS_FROM_F_SECTION_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_section_codes']"
    else:
        if ITEMS_FROM_F_SECTION_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_section_cause_codes']"
        if ITEMS_FROM_F_SECTION_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_section_factor_codes']"
        if ITEMS_FROM_F_SECTION_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_section_none_codes']"

    if ITEMS_FROM_F_SUBCATEGORY_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_subcategory_codes']"
    else:
        if ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subcategory_cause_codes']"
        if ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subcategory_factor_codes']"
        if ITEMS_FROM_F_SUBCATEGORY_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subcategory_none_codes']"

    if ITEMS_FROM_F_SUBSECTION_CODES_ALL:
        transaction_cmd += (
            "" if transaction_cmd == "(" else " + "
        ) + "DF_RAW_DATA_FILTERED['all_subsection_codes']"
    else:
        if ITEMS_FROM_F_SUBSECTION_CODES_CAUSE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subsection_cause_codes']"
        if ITEMS_FROM_F_SUBSECTION_CODES_FACTOR:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subsection_factor_codes']"
        if ITEMS_FROM_F_SUBSECTION_CODES_NONE:
            transaction_cmd += (
                "" if transaction_cmd == "(" else " + "
            ) + "DF_RAW_DATA_FILTERED['all_subsection_none_codes']"

    transaction_cmd += ")"

    if transaction_cmd == "()":
        # pylint: disable=line-too-long
        st.error("##### Error: No items selected - transaction data.")
        st.stop()

    DF_TRANSACTION_DATA["items"] = eval(transaction_cmd)  # pylint: disable=eval-used

    _print_timestamp("_create_transaction_data()")


# ------------------------------------------------------------------
# Create the transaction dataframe - Eclat Algorithm.
# ------------------------------------------------------------------
def _create_transaction_data_eclat() -> None:
    global DF_TRANSACTION_DATA_ECLAT  # pylint: disable=global-statement

    # ------------------------------------------------------------------
    # Create the empty dataframe.
    # ------------------------------------------------------------------

    max_cols = _sql_query_max_array_length()

    (max_rows, _) = DF_RAW_DATA_FILTERED.shape

    DF_TRANSACTION_DATA_ECLAT = DataFrame(numpy.empty([max_rows, max_cols], dtype=str))

    # ------------------------------------------------------------------
    # Create the concat command.
    # ------------------------------------------------------------------

    cmd_concat = "[] "

    if ITEMS_FROM_ES_EVENTSOE_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_eventsoe_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_ES_EVENTSOE_CODES_FALSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_eventsoe_false_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_ES_EVENTSOE_CODES_TRUE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_eventsoe_true_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_ES_OCCURRENCE_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_occurrence_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_occurrence_false_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_occurrence_true_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_ES_PHASE_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_phase_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_ES_PHASE_CODES_FALSE:
            cmd_concat += " + DF_RAW_DATA_FILTERED['all_phase_false_codes'][_idx_row_s]"
        if ITEMS_FROM_ES_PHASE_CODES_TRUE:
            cmd_concat += " + DF_RAW_DATA_FILTERED['all_phase_true_codes'][_idx_row_s]"

    if ITEMS_FROM_F_CATEGORY_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_category_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_CATEGORY_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_category_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_CATEGORY_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_category_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_CATEGORY_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_category_none_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_F_FINDING_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_finding_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_FINDING_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_finding_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_FINDING_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_finding_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_FINDING_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_finding_none_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_F_MODIFIER_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_modifier_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_MODIFIER_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_modifier_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_MODIFIER_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_modifier_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_MODIFIER_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_modifier_none_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_F_SECTION_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_section_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_SECTION_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_section_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SECTION_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_section_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SECTION_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_section_none_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_F_SUBCATEGORY_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_subcategory_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subcategory_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subcategory_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SUBCATEGORY_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subcategory_none_codes'][_idx_row_s]"
            )

    if ITEMS_FROM_F_SUBSECTION_CODES_ALL:
        cmd_concat += " + DF_RAW_DATA_FILTERED['all_subsection_codes'][_idx_row_s]"
    else:
        if ITEMS_FROM_F_SUBSECTION_CODES_CAUSE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subsection_cause_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SUBSECTION_CODES_FACTOR:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subsection_factor_codes'][_idx_row_s]"
            )
        if ITEMS_FROM_F_SUBSECTION_CODES_NONE:
            cmd_concat += (
                " + DF_RAW_DATA_FILTERED['all_subsection_none_codes'][_idx_row_s]"
            )

    if cmd_concat == "[] ":
        # pylint: disable=line-too-long
        st.error("##### Error: No items selected - transaction data Eclat Algorithm.")
        st.stop()

    _idx_row_d = 0

    for _idx_row_s in DF_RAW_DATA_FILTERED.index:
        column_list = eval(cmd_concat)  # pylint: disable=eval-used
        for idx_col, column in enumerate(column_list):
            DF_TRANSACTION_DATA_ECLAT.iat[_idx_row_d, idx_col] = column
        _idx_row_d += 1

    _print_timestamp("_create_transaction_data_eclat()")


# ------------------------------------------------------------------
# Get the item descriptions.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _get_description_items(df_int: DataFrame) -> DataFrame:
    df_ext = df_int.copy()

    for idx in df_ext.index:
        df_ext["item_description"][idx] = _get_item_description(df_ext["item"][idx])

    _print_timestamp("_get_description_items()")

    return df_ext


# ------------------------------------------------------------------
# Get the itemset descriptions.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _get_description_itemsets(df_int: DataFrame) -> DataFrame:
    df_ext = df_int.copy()

    df_ext["itemsets_description"] = ""

    for idx in df_ext.index:
        df_ext["itemsets_description"][idx] = _get_items_description(
            df_ext["itemsets"][idx]
        )

    _print_timestamp("_get_description_itemsets()")

    return df_ext


# ------------------------------------------------------------------
# Create a simple user PostgreSQL database engine.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def _get_engine() -> Engine:
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
# Determine the item description.
# ------------------------------------------------------------------
def _get_item_description(item: str) -> str:
    [part_1, part_2, part_3] = item.split("_")

    match part_1:
        case "ee":
            attribute = "eventsoe no"
            description = [MD_CODES_EVENTSOE[part_2]]
        case "eo":
            attribute = "occurrence code"
            description = [
                MD_CODES_PHASE[part_2[:3]],
                MD_CODES_EVENTSOE[part_2[3:]],
            ]
        case "ep":
            attribute = "phase no"
            description = [MD_CODES_PHASE[part_2]]
        case "fc":
            attribute = "category no"
            description = [MD_CODES_CATEGORY[part_2]]
        case "ff":
            attribute = "finding code"
            description = [
                MD_CODES_CATEGORY[part_2[:2]],
                MD_CODES_SUBCATEGORY[part_2[:4]],
                MD_CODES_SECTION[part_2[:6]],
                MD_CODES_SUBSECTION[part_2[:8]],
                MD_CODES_MODIFIER[part_2[8:]],
            ]
        case "fm":
            attribute = "modifier no"
            description = [MD_CODES_MODIFIER[part_2]]
        case "fs":
            attribute = "section no"
            description = [
                MD_CODES_CATEGORY[part_2[:2]],
                MD_CODES_SUBCATEGORY[part_2[:4]],
                MD_CODES_SECTION[part_2[:6]],
            ]
        case "fsc":
            attribute = "subcategory no"
            description = [
                MD_CODES_CATEGORY[part_2[:2]],
                MD_CODES_SUBCATEGORY[part_2[:4]],
            ]
        case "fss":
            attribute = "subsection no"
            description = [
                MD_CODES_CATEGORY[part_2[:2]],
                MD_CODES_SUBCATEGORY[part_2[:4]],
                MD_CODES_SECTION[part_2[:6]],
                MD_CODES_SUBSECTION[part_2[:8]],
            ]
        case _:
            attribute = "??? " + part_1
            description = ["??? " + part_2]

    if part_1 in ["ee", "eo", "ep"]:
        match part_3:
            case "a":
                variant = "not relevant"
            case "f":
                variant = "no defining event"
            case "t":
                variant = "defining event"
            case _:
                variant = "??? " + part_3
    elif part_1 in ["fc", "ff", "fm", "fs", "fsc", "fss"]:
        match part_3:
            case "a":
                variant = "not relevant"
            case "c":
                variant = "case"
            case "f":
                variant = "factor"
            case "n":
                variant = "neither cause nor factor"
            case _:
                variant = "??? " + part_3
    else:
        variant = "??? " + part_3

    return attribute + " | " + " - ".join(description) + " | " + variant


# ------------------------------------------------------------------
# Determine the itemset description.
# ------------------------------------------------------------------
def _get_items_description(itemset: list[str]) -> list[str]:
    descriptions = []

    for item in itemset:
        if item != "":
            descriptions.append(_get_item_description(item))

    return descriptions


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# pylint: disable=R0801
@st.cache_resource
def _get_postgres_connection() -> connection:
    print(
        f"[psycopg2] User connect request host={SETTINGS.postgres_host} "
        + f"port={SETTINGS.postgres_connection_port} "
        + f"dbname={SETTINGS.postgres_dbname} "
        + f"user={SETTINGS.postgres_user_guest}"
    )

    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Prepare the codes.
# ------------------------------------------------------------------
def _get_prepared_codes(list_in: list, prefix: str) -> list[str]:
    list_out = []

    for elem in list_in:
        (_, code) = elem.split(" - ")
        list_out.append(prefix + "_" + code + "_a")

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

    _print_timestamp("_get_prepared_us_states()")

    return list_out


# ------------------------------------------------------------------
# Read the raw data.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _get_raw_data() -> DataFrame:
    return pd.read_sql(
        con=_get_engine(),
        sql="""
            SELECT ev_id,
                   acft_categories,
                   all_category_cause_codes,
                   all_category_codes,
                   all_category_factor_codes,
                   all_category_none_codes,
                   all_eventsoe_codes,
                   all_eventsoe_false_codes,
                   all_eventsoe_true_codes,
                   all_finding_cause_codes,
                   all_finding_codes,
                   all_finding_factor_codes,
                   all_finding_none_codes,
                   all_modifier_cause_codes,
                   all_modifier_codes,
                   all_modifier_factor_codes,
                   all_modifier_none_codes,
                   all_occurrence_codes,
                   all_occurrence_false_codes,
                   all_occurrence_true_codes,
                   all_phase_codes,
                   all_phase_false_codes,
                   all_phase_true_codes,
                   all_section_cause_codes,
                   all_section_codes,
                   all_section_factor_codes,
                   all_section_none_codes,
                   all_subcategory_cause_codes,
                   all_subcategory_codes,
                   all_subcategory_factor_codes,
                   all_subcategory_none_codes,
                   all_subsection_cause_codes,
                   all_subsection_codes,
                   all_subsection_factor_codes,
                   all_subsection_none_codes,
                   country,
                   ev_highest_injury,
                   ev_type,
                   ev_year,
                   inj_f_grnd,
                   inj_tot_f,
                   is_dest_country_usa,
                   is_dprt_country_usa,
                   is_oper_country_usa,
                   is_owner_country_usa,
                   is_regis_country_usa,
                   no_aircraft,
                   ntsb_no,
                   state
             FROM io_app_ae1982
            WHERE (ARRAY_LENGTH(all_finding_codes, 1)    > 0 
               OR  ARRAY_LENGTH(all_occurrence_codes, 1) > 0) 
              AND  ev_year >= 2008
            ORDER BY ev_id;
    """,
    )


# ------------------------------------------------------------------
# Creates the user guide for the whole application.
# ------------------------------------------------------------------
def _get_user_guide_app() -> None:
    text = """
#### User guide: slara Application
"""

    text += """
Association rule analysis is a data mining technique used to discover relationships between items or events in large datasets. 
It identifies patterns or co-occurrences that frequently appear together in a transactional database.

###### Basic Concepts and Terminology

The following terms are commonly used in association rule analysis:

- **Item**: An element or attribute of interest in the dataset.
- **Transaction**: A collection of items that occur together.
- **Support**: The frequency with which an item or itemset appears in the dataset: ```(Item A + Item B) / (Entire dataset)```.
- **Confidence**: The likelihood that a rule is correct or true, given the occurrence of the antecedent and consequent in the dataset: ```(Item A + Item B)/ (Item A)```.
- **Lif**t: A measure of how often the antecedent and consequent occur together than expected by chance: ```(Confidence) / (item B)/ (Entire dataset)```.

###### Data Preprocessing

Before performing association rule analysis, it is necessary to preprocess the data. 
This involves data cleaning, transformation, and formatting to ensure that the data is in a suitable format for analysis.

Data preprocessing steps may include:

- Removing duplicate or irrelevant data,
- Handling missing or incomplete data,
- Converting data to a suitable format (e.g., binary or numerical),
- Discretizing continuous variables into categorical variables,
- Scaling or normalizing data.

###### Measures For Evaluating Association Rules 

Association rule analysis generates a large number of potential rules, and it is important to evaluate and select the most relevant rules.
The following measures are commonly used to evaluate association rules: 

- **Support**: Rules with high support are more significant as they occur more frequently in the dataset.
- **Confidence**: Rules with high confidence are more reliable, as they have a higher probability of being true.
- **Lift**: Rules with high lift indicate a strong association between the antecedent and consequent, as they occur together more frequently than expected by chance.
"""

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task -
# binary data.
# ------------------------------------------------------------------
def _get_user_guide_details_binary_data() -> None:
    text = """
#### User guide: Binary data

This task provides the binary data in a table format for display and download as **csv** file.
Every row represents a transaction.
Columns are possible categories that might appear in every transaction.
Every cell contains one of two possible values:

- 0 - the category was not included in the transaction,
- 1 - the transaction contains the category.  

To avoid memory problems in the web browser, the display is limited to the first 100 rows and columns.
The **csv** download is not limited, but may not be processable with MS Excel.
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show data profile' task.
# ------------------------------------------------------------------
def _get_user_guide_data_profile(data_type: str) -> None:
    text = f"""
#### User guide: {data_type} profile

This task performs a data analysis of the underlying {data_type.lower()}. This is done with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/). You can select either the explorative or the minimal version. Depending on the size of the selected data, there may be delayed response times, with the exploratory version again requiring significantly more computational effort than the minimal version.
For further explanations please consult the documentation of **Pandas Profiling**. The result of the data analysis can also be downloaded as **HTML** file if desired.
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task -
# association rules.
# ------------------------------------------------------------------
def _get_user_guide_details_association_rules() -> None:
    text = """
#### User guide: Association rules

This task provides the detailed association rules in a table format for display and download as **csv** file. 

The table comes with columns "antecedents" and "consequents" that store itemsets, plus the scoring metric columns:

- "antecedent support", 
- "consequent support",
- "support", 
- "confidence", 
- "lift",
- "leverage", 
- "conviction"

of all rules for which metric(rule) >= `min_threshold`.

For usage examples, please see http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task -
# binary data one-hot encoded.
# ------------------------------------------------------------------
def _get_user_guide_details_binary_data_one_hot_encoded() -> None:
    text = """
#### User guide: One-hot encoded data details

This task provides the detailed one-hot encoded data in a table format for display and download as **csv** file. 
To avoid memory problems in the web browser, the display is limited to the first 100 rows and columns.
The **csv** download is not limited, but may not be processable with MS Excel.
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task -
# frequent itemsets.
# ------------------------------------------------------------------
def _get_user_guide_details_frequent_itemsets() -> None:
    text = """
#### User guide: Frequent itemsets

This task provides the detailed frequent itemsets in a table format for display and download as **csv** file. 

The table comes with columns ['support', 'itemsets'] of all itemsets that are >= `min_support`.

For usage examples, please see http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task -
# frequent itemsets - tree map.
# ------------------------------------------------------------------
def _get_user_guide_details_frequent_itemsets_tree_map() -> None:
    text = """
#### User guide: Frequent itemsets tree map

TODO
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task - raw data.
# ------------------------------------------------------------------
def _get_user_guide_details_raw_data() -> None:
    text = """
#### User guide: Raw data details

This task provides the detailed raw data in a table format for display and download as **csv** file. 
The rows to be displayed are limited to the chosen filter options. 
The order of data display is based on the ascending event identification. 

The database columns of the selected rows are always displayed in full.
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task - standard.
# ------------------------------------------------------------------
def _get_user_guide_details_standard() -> str:
    return """

##### Usage tips

- **Column sorting**: sort columns by clicking on their headers.
- **Column resizing**: resize columns by dragging and dropping column header borders.
- **Table (height, width) resizing**: resize tables by dragging and dropping the bottom right corner of tables.
- **Search**: search through data by clicking a table, using hotkeys ('Ctrl + F') to bring up the search bar, and using the search bar to filter data.
- **Copy to clipboard**: select one or multiple cells, copy them to clipboard, and paste them into your favorite spreadsheet software.
    """


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task - transaction data.
# ------------------------------------------------------------------
def _get_user_guide_details_transaction_data() -> None:
    text = """
#### User guide: Transaction data details

This task provides the detailed transaction data in a table format for display and download as **csv** file.
The order of data display is based on the ascending event identification of the raw data. 
    """

    st.warning(text + _get_user_guide_details_standard())


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def _get_user_guide_items_events_sequence() -> None:
    text = """
#### User guide: Items from events_sequence

From the database table **events_sequence** the following attributes are available as items for the Association Rule Analysis:

- **Eventsoe no** - events sequence
- **Phase no** - event phase
- **Occurrence code** - the combination of **Phase no** and **Eventsoe no**.
- **Defining** - identification of the defining event

The following rules apply when selecting items:

- **Occurrence code** includes **Phase no** and **Eventsoe no**
- **All** includes **Defining** and **Not defining**

The application tries to prevent a redundant selection of items!
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def _get_user_guide_items_findings() -> None:
    text = """
#### User guide: Items from findings

From the database table **findings** the following attributes are available as items for the Association Rule Analysis:

- **Category no** - category
- **Subategory no** - subcategory
- **Section no** - section
- **Subsection no** - subsection
- **Modifier no** - modifier
- **Finding code** - the combination of **Category no**, **Subcategory no**, **Section no**, **Subsection no** and **Modifier no**.
- **Cause factor** - identification of cause or factor

The following rules apply when selecting items:
- **Finding code** includes **Category no**, **Subcategory no**, **Section no**, **Subsection no** and **Modifier no**
- **All** includes **Cause**, **Factor** and **Not cause or factor**

The application tries to prevent a redundant selection of items!
    """

    st.warning(text)


# ------------------------------------------------------------------
# Present association rule details.
# ------------------------------------------------------------------
def _present_details_association_rules(
    algorithm: str, df_association_rules: DataFrame
) -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed association rules '
            + algorithm
            + " Algorithm</p>",
            unsafe_allow_html=True,
        )

    # pylint: disable=line-too-long
    with col2:
        choice_ug_rules_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed association rules view.",
            key="CHOICE_UG_RULES_DETAILS_" + algorithm.upper().replace("-", ""),
            label="**User Guide: Association rule details**",
            value=False,
        )

    if choice_ug_rules_details:
        _get_user_guide_details_association_rules()

    if CHOICE_ALG_ECLAT:
        df_rules_ext = _create_df_association_rules_ext_eclat(df_association_rules)
    else:
        df_rules_ext = _create_df_association_rules_ext(df_association_rules)

    (no_rows, _) = df_rules_ext.shape

    st.write(f"No association rules: {no_rows}")

    if CHOICE_ALG_ECLAT:
        st.dataframe(df_rules_ext.sort_values("Support", ascending=False))
    else:
        st.dataframe(df_rules_ext.sort_values("support", ascending=False))

    st.download_button(
        data=df_rules_ext.to_csv().encode("utf-8"),
        file_name=APP_ID
        + f"_association_rules_{algorithm.lower().replace('-','')}_detail.csv",
        help="The download includes all association rules.",
        label="**Download the association rules**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_association_rules()")


# ------------------------------------------------------------------
# Present binary data.
# ------------------------------------------------------------------
def _present_details_binary_data() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Binary data Eclat Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_binary_data = st.checkbox(
            help="Explanations and operating instructions related to the detailed one-hot encoded data view.",
            key="CHOICE_UG_BINARY_DATA",
            label="**User Guide: Binary data**",
            value=False,
        )

    if choice_ug_binary_data:
        _get_user_guide_details_binary_data()

    (no_rows, no_cols) = DF_BINARY_DATA_ECLAT.shape

    st.write(f"No transactions: {no_rows} - no columns: {no_cols}")

    st.dataframe(DF_BINARY_DATA_ECLAT.iloc[:100, :100])

    st.download_button(
        data=DF_BINARY_DATA_ECLAT.to_csv().encode("utf-8"),
        file_name=APP_ID + "_binary_data.csv",
        help="The download includes all binary data.",
        label="**Download the binary data**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_binary_data()")


# ------------------------------------------------------------------
# Present binary data one-hot encoded.
# ------------------------------------------------------------------
def _present_details_binary_data_one_hot_encoded() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed one-hot encoded data Non-Eclat Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_binary_data_one_hot_encoded = st.checkbox(
            help="Explanations and operating instructions related to the detailed one-hot encoded data view.",
            key="CHOICE_UG_BINARY_DATA_ONE_HOT_ENCODED",
            label="**User Guide: Binary data one-hot encoded**",
            value=False,
        )

    if choice_ug_binary_data_one_hot_encoded:
        _get_user_guide_details_binary_data_one_hot_encoded()

    (no_rows, no_cols) = DF_BINARY_DATA_ONE_HOT_ENCODED.shape

    st.write(f"No transactions: {no_rows} - no columns: {no_cols}")

    st.dataframe(DF_BINARY_DATA_ONE_HOT_ENCODED.iloc[:100, :100])

    st.download_button(
        data=DF_BINARY_DATA_ONE_HOT_ENCODED.to_csv().encode("utf-8"),
        file_name=APP_ID + "_binary_data_one_hot_encoded.csv",
        help="The download includes all one-hot encoded data.",
        label="**Download the one-hot encoded data**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_binary_data_one_hot_encoded()")


# ------------------------------------------------------------------
# Present frequent itemset details - Apriori Algorithm.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets_apriori() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed frequent itemsets Apriori Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_frequent_itemsets_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed frequent itemsets view.",
            key="CHOICE_UG_FREQUENT_ITEMSETS_DETAILS_APRIORI",
            label="**User Guide: Frequent itemset details**",
            value=False,
        )

    if choice_ug_frequent_itemsets_details:
        _get_user_guide_details_frequent_itemsets()

    df_frequent_itemsets_ext = _get_description_itemsets(DF_FREQUENT_ITEMSETS_APRIORI)

    (no_rows, _) = df_frequent_itemsets_ext.shape

    st.write(f"No frequent itemsets: {no_rows}")

    st.dataframe(df_frequent_itemsets_ext.sort_values("support", ascending=False))

    st.download_button(
        data=df_frequent_itemsets_ext.to_csv().encode("utf-8"),
        file_name=APP_ID + "_frequent_itemsets_apriori_detail.csv",
        help="The download includes all frequent itemsets.",
        label="**Download the frequent itemsets**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_frequent_itemsets_apriori()")


# ------------------------------------------------------------------
# Present frequent itemset details - Eclat Algorithm.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets_eclat() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed frequent itemsets Eclat Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_frequent_itemsets_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed frequent itemsets view.",
            key="CHOICE_UG_FREQUENT_ITEMSETS_DETAILS_ECLAT",
            label="**User Guide: Frequent itemset details**",
            value=False,
        )

    if choice_ug_frequent_itemsets_details:
        _get_user_guide_details_frequent_itemsets()

    df_frequent_itemsets_ext = _get_description_items(DF_FREQUENT_ITEMSETS_ECLAT)

    (no_rows, _) = df_frequent_itemsets_ext.shape

    st.write(
        f"No frequent itemsets: {no_rows} - max. combinations: {CHOICE_ALG_COMBINATIONS_CURRENT}"
    )

    st.dataframe(df_frequent_itemsets_ext.sort_values("transactions", ascending=False))

    st.download_button(
        data=df_frequent_itemsets_ext.to_csv().encode("utf-8"),
        file_name=APP_ID + "_frequent_itemsets_eclat_detail.csv",
        help="The download includes all frequent itemsets.",
        label="**Download the frequent itemsets**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_frequent_itemsets_eclat()")


# ------------------------------------------------------------------
# Present frequent itemset details - FP-Growth Algorithm.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets_fpgrowth() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed frequent itemsets FP-Growth Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_frequent_itemsets_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed frequent itemsets view.",
            key="CHOICE_UG_FREQUENT_ITEMSETS_DETAILS_FPGROWTH",
            label="**User Guide: Frequent itemset details**",
            value=False,
        )

    if choice_ug_frequent_itemsets_details:
        _get_user_guide_details_frequent_itemsets()

    df_frequent_itemsets_ext = _get_description_itemsets(DF_FREQUENT_ITEMSETS_FPGROWTH)

    (no_rows, _) = df_frequent_itemsets_ext.shape

    st.write(f"No frequent itemsets: {no_rows}")

    st.dataframe(df_frequent_itemsets_ext.sort_values("support", ascending=False))

    st.download_button(
        data=df_frequent_itemsets_ext.to_csv().encode("utf-8"),
        file_name=APP_ID + "_frequent_itemsets_fpgrowth_detail.csv",
        help="The download includes all frequent itemsets.",
        label="**Download the frequent itemsets**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_frequent_itemsets_fpgrowth()")


# ------------------------------------------------------------------
# Present frequent itemset details - FP-Max Algorithm.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets_fpmax() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed frequent itemsets FP-Max Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_frequent_itemsets_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed frequent itemsets view.",
            key="CHOICE_UG_FREQUENT_ITEMSETS_DETAILS_FPMAX",
            label="**User Guide: Frequent itemset details**",
            value=False,
        )

    if choice_ug_frequent_itemsets_details:
        _get_user_guide_details_frequent_itemsets()

    df_frequent_itemsets_ext = _get_description_itemsets(DF_FREQUENT_ITEMSETS_FPMAX)

    (no_rows, _) = df_frequent_itemsets_ext.shape

    st.write(f"No frequent itemsets: {no_rows}")

    st.dataframe(df_frequent_itemsets_ext.sort_values("support", ascending=False))

    st.download_button(
        data=df_frequent_itemsets_ext.to_csv().encode("utf-8"),
        file_name=APP_ID + "_frequent_itemsets_fpmax_detail.csv",
        help="The download includes all frequent itemsets.",
        label="**Download the frequent itemsets**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_frequent_itemsets_fpmax()")


# ------------------------------------------------------------------
# Present the frequent itemsets tree_map.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets_tree_map_eclat() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Frequent itemsets tree map Eclat Algorithm</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_item_distribution_tree_map = st.checkbox(
            help="Explanations and operating instructions related to the frequent itemset tree map view.",
            key="CHOICE_UG_ITEM_DISTRIBUTION_TREE_MAP",
            label="**User Guide: Frequent itemsets tree map**",
            value=False,
        )

    if choice_ug_item_distribution_tree_map:
        _get_user_guide_details_frequent_itemsets_tree_map()

    DF_ITEM_DISTRIBUTION_ECLAT_EXT["all"] = "All"

    fig = px.treemap(
        DF_ITEM_DISTRIBUTION_ECLAT_EXT.head(50),
        color=DF_ITEM_DISTRIBUTION_ECLAT_EXT["transactions"].head(50),
        color_continuous_scale="Blues",
        hover_data={
            "item_description": True,
            "transactions": True,
        },
        path=[px.Constant("all"), "item"],
        values="transactions",
    )

    st.plotly_chart(fig)

    _print_timestamp("_present_details_frequent_itemsets_tree_map_eclat()")


# ------------------------------------------------------------------
# Present raw data details.
# ------------------------------------------------------------------
def _present_details_raw_data() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Filtered detailed raw data</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_raw_data_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed raw data view.",
            key="CHOICE_UG_RAW_DATA_DETAILS",
            label="**User Guide: Raw data details**",
            value=False,
        )

    if choice_ug_raw_data_details:
        _get_user_guide_details_raw_data()

    # pylint: disable=line-too-long
    st.write(
        f"No itemsets unfiltered: {DF_RAW_DATA_UNFILTERED_ROWS} - filtered: {DF_RAW_DATA_FILTERED_ROWS}"
    )

    st.dataframe(DF_RAW_DATA_FILTERED)

    st.download_button(
        data=DF_RAW_DATA_FILTERED.to_csv().encode("utf-8"),
        file_name=APP_ID + "_raw_data_detail.csv",
        help="The download includes all raw data "
        + "after applying the filter options.",
        label="**Download the detailed raw data**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_raw_data()")


# ------------------------------------------------------------------
# Present transaction data details.
# ------------------------------------------------------------------
def _present_details_transaction_data(
    algorithm: str, df_transaction_data: DataFrame
) -> None:
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
            + 'font-weight: normal;border-radius:2%;">Detailed transaction data  '
            + algorithm
            + " Algorithm</p>",
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_transaction_data_details = st.checkbox(
            help="Explanations and operating instructions related to the detailed transaction data view.",
            key="CHOICE_UG_TRANSACTION_DATA_DETAILS" + algorithm,
            label="**User Guide: Transaction data details**",
            value=False,
        )

    if choice_ug_transaction_data_details:
        _get_user_guide_details_transaction_data()

    (no_rows, _) = df_transaction_data.shape

    st.write(f"No transactions: {no_rows}")

    st.dataframe(df_transaction_data)

    st.download_button(
        data=df_transaction_data.to_csv().encode("utf-8"),
        file_name=APP_ID + "_transaction_data_detail.csv",
        help="The download includes all transaction data.",
        label="**Download the detailed transaction data**",
        mime="text/csv",
    )

    _print_timestamp("_present_details_transaction_data()")


# ------------------------------------------------------------------
# Present raw data profile.
# ------------------------------------------------------------------
def _present_profile_raw_data() -> None:
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
            + 'font-weight: normal;border-radius:2%;">Profile of the filtered raw data</p>',
            unsafe_allow_html=True,
        )

    with col2:
        choice_ug_raw_data_profile = st.checkbox(
            help="Explanations and operating instructions related to profiling "
            + "of the database view **io_app_ae1982",
            key="CHOICE_UG_RAW_DATA_PROFILE",
            label="**User Guide: Raw data profile**",
            value=False,
        )

    if choice_ug_raw_data_profile:
        _get_user_guide_data_profile("Raw data")

    # noinspection PyUnboundLocalVariable
    if CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE_TYPE == "explorative":
        profile_report = ProfileReport(
            DF_RAW_DATA_FILTERED,
            explorative=True,
        )
    else:
        profile_report = ProfileReport(
            DF_RAW_DATA_FILTERED,
            minimal=True,
        )

    st_profile_report(profile_report)

    # pylint: disable=line-too-long
    st.download_button(
        data=profile_report.to_html(),
        file_name=APP_ID + "_raw_data_profile_" + CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE_TYPE + ".html",  # type: ignore
        help="The download includes a profile report from the dataframe "
        + "after applying the filter options.",
        label="**Download the raw data profile report**",
        mime="text/html",
    )

    _print_timestamp("_present_profile_raw_data()")


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_results() -> None:
    # ------------------------------------------------------------------
    # User guide.
    # ------------------------------------------------------------------

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
            utils.present_about(PG_CONN, APP_ID)
            _print_timestamp("_present_data() - CHOICE_ABOUT")

    if CHOICE_UG_APP:
        _get_user_guide_app()

    _setup_filter_events_sequence()

    _setup_filter_findings()

    # ------------------------------------------------------------------
    # Raw data.
    # ------------------------------------------------------------------

    if CHOICE_SHOW_FILTERED_RAW_DATA:
        _present_details_raw_data()

        if CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE:
            _present_profile_raw_data()

    # ------------------------------------------------------------------
    # Run algorithms.
    # ------------------------------------------------------------------

    if CHOICE_RUN_ALGORITHMS:
        # pylint: disable=too-many-boolean-expressions
        if (
            CHOICE_SHOW_ASSOCIATION_RULES
            or CHOICE_SHOW_BINARY_DATA_ECLAT
            or CHOICE_SHOW_FREQUENT_ITEMSETS
            or CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT
            or CHOICE_SHOW_ONE_HOT_ENCODED_DATA
            or CHOICE_SHOW_TRANSACTION_DATA
        ):
            _apply_algorithm()

        # ------------------------------------------------------------------
        # Transaction data.
        # ------------------------------------------------------------------

        if CHOICE_SHOW_TRANSACTION_DATA:
            if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
                _present_details_transaction_data("Non-Eclat", DF_TRANSACTION_DATA)
            if CHOICE_ALG_ECLAT:
                _present_details_transaction_data("Eclat", DF_TRANSACTION_DATA_ECLAT)

        # ------------------------------------------------------------------
        # One-hot encoded data / binary data .
        # ------------------------------------------------------------------

        if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
            if CHOICE_SHOW_ONE_HOT_ENCODED_DATA:
                _present_details_binary_data_one_hot_encoded()

        if CHOICE_ALG_ECLAT:
            if CHOICE_SHOW_BINARY_DATA_ECLAT:
                _present_details_binary_data()

        # ------------------------------------------------------------------
        # Frequent itemsets.
        # ------------------------------------------------------------------

        if CHOICE_SHOW_FREQUENT_ITEMSETS:
            if CHOICE_ALG_APRIORI:
                _present_details_frequent_itemsets_apriori()
            if CHOICE_ALG_ECLAT:
                _present_details_frequent_itemsets_eclat()
            if CHOICE_ALG_FPGROWTH:
                _present_details_frequent_itemsets_fpgrowth()
            if CHOICE_ALG_FPMAX:
                _present_details_frequent_itemsets_fpmax()

        if CHOICE_ALG_ECLAT:
            if CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT:
                _present_details_frequent_itemsets_tree_map_eclat()

        # ------------------------------------------------------------------
        # Association rules.
        # ------------------------------------------------------------------

        if CHOICE_SHOW_ASSOCIATION_RULES:
            if CHOICE_ALG_APRIORI:
                _present_details_association_rules(
                    "Apriori", DF_ASSOCIATION_RULES_APRIORI
                )
            if CHOICE_ALG_ECLAT:
                _present_details_association_rules("Eclat", DF_ASSOCIATION_RULES_ECLAT)
            if CHOICE_ALG_FPGROWTH:
                _present_details_association_rules(
                    "FP-Growth", DF_ASSOCIATION_RULES_FPGROWTH
                )
            if CHOICE_ALG_FPMAX:
                _present_details_association_rules("FP-Max", DF_ASSOCIATION_RULES_FPMAX)


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
    global CHOICE_FILTER_DATA_EVENTS_SEQUENCE  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA_FINDINGS  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA_OTHER  # pylint: disable=global-statement
    global FILTER_ACFT_CATEGORIES  # pylint: disable=global-statement
    global FILTER_EV_HIGHEST_INJURY  # pylint: disable=global-statement
    global FILTER_EV_TYPE  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement
    global FILTER_EVENTS_SEQUENCE_EVENTSOES  # pylint: disable=global-statement
    global FILTER_EVENTS_SEQUENCE_PHASES  # pylint: disable=global-statement
    global FILTER_FINDINGS_CATEGORIES  # pylint: disable=global-statement
    global FILTER_FINDINGS_MODIFIERS  # pylint: disable=global-statement
    global FILTER_FINDINGS_SECTIONS  # pylint: disable=global-statement
    global FILTER_FINDINGS_SUBCATEGORIES  # pylint: disable=global-statement
    global FILTER_FINDINGS_SUBSECTIONS  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_FROM  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_TO  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_FROM  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_TO  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_FROM  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_TO  # pylint: disable=global-statement
    global FILTER_US_AVIATION  # pylint: disable=global-statement
    global FILTER_US_STATES  # pylint: disable=global-statement

    CHOICE_FILTER_DATA_EVENTS_SEQUENCE = st.sidebar.checkbox(
        help="""
        The following filter options can be used to limit the data to be processed.
        All selected filter options are applied simultaneously, i.e. they are linked
        to a logical **`and`**.
        """,
        label="**Filter Events Sequence ?**",
        value=False,
    )

    if CHOICE_FILTER_DATA_EVENTS_SEQUENCE:
        FILTER_EVENTS_SEQUENCE_EVENTSOES = st.sidebar.multiselect(
            help="Here, data can be limited to selected events sequence eventsoes.",
            label="**Eventsoes:**",
            options=_sql_query_md_codes_eventsoe(),
        )
        if FILTER_EVENTS_SEQUENCE_EVENTSOES:
            # pylint: disable=line-too-long
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Events sequence eventsoes**: **`{','.join(FILTER_EVENTS_SEQUENCE_EVENTSOES)}`**"
            )

        FILTER_EVENTS_SEQUENCE_PHASES = st.sidebar.multiselect(
            help="Here, data can be limited to selected events sequence phases.",
            label="**Phases:**",
            options=_sql_query_md_codes_phase(),
        )
        if FILTER_EVENTS_SEQUENCE_PHASES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Events sequence phases**: **`{','.join(FILTER_EVENTS_SEQUENCE_PHASES)}`**"
            )

    CHOICE_FILTER_DATA_FINDINGS = st.sidebar.checkbox(
        help="""
        The following filter options can be used to limit the data to be processed.
        All selected filter options are applied simultaneously, i.e. they are linked
        to a logical **`and`**.
        """,
        label="**Filter Findings ?**",
        value=False,
    )

    if CHOICE_FILTER_DATA_FINDINGS:
        FILTER_FINDINGS_CATEGORIES = st.sidebar.multiselect(
            help="Here, data can be limited to selected finding categories.",
            label="**Categories:**",
            options=_sql_query_md_codes_category(),
        )
        if FILTER_FINDINGS_CATEGORIES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding categories**: **`{','.join(FILTER_FINDINGS_CATEGORIES)}`**"
            )

        FILTER_FINDINGS_SUBCATEGORIES = st.sidebar.multiselect(
            help="Here, data can be limited to selected finding subcategories.",
            label="**Subcategories:**",
            options=_sql_query_md_codes_subcategory(),
        )
        if FILTER_FINDINGS_SUBCATEGORIES:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding subcategories**: **`{','.join(FILTER_FINDINGS_SUBCATEGORIES)}`**"
            )

        FILTER_FINDINGS_SECTIONS = st.sidebar.multiselect(
            help="Here, data can be limited to selected finding sections.",
            label="**Sections:**",
            options=_sql_query_md_codes_section(),
        )
        if FILTER_FINDINGS_SECTIONS:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding sections**: **`{','.join(FILTER_FINDINGS_SECTIONS)}`**"
            )

        FILTER_FINDINGS_SUBSECTIONS = st.sidebar.multiselect(
            help="Here, data can be limited to selected finding subsections.",
            label="**Subsections:**",
            options=_sql_query_md_codes_subsection(),
        )
        if FILTER_FINDINGS_SUBSECTIONS:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding subsections**: **`{','.join(FILTER_FINDINGS_SUBSECTIONS)}`**"
            )

        FILTER_FINDINGS_MODIFIERS = st.sidebar.multiselect(
            help="Here, data can be limited to selected finding modifiers.",
            label="**Modifiers:**",
            options=_sql_query_md_codes_modifier(),
        )
        if FILTER_FINDINGS_MODIFIERS:
            CHOICE_ACTIVE_FILTERS_TEXT = (
                CHOICE_ACTIVE_FILTERS_TEXT
                + f"\n- **Finding modifiers**: **`{','.join(FILTER_FINDINGS_MODIFIERS)}`**"
            )

        st.sidebar.markdown("""---""")

    CHOICE_FILTER_DATA_OTHER = st.sidebar.checkbox(
        help="""
        The following filter options can be used to limit the data to be processed.
        All selected filter options are applied simultaneously, i.e. they are linked
        to a logical **`and`**.
        """,
        label="**Filter Other Criteria ?**",
        value=True,
    )

    if not CHOICE_FILTER_DATA_OTHER:
        return

    CHOICE_ACTIVE_FILTERS_TEXT = ""

    FILTER_ACFT_CATEGORIES = st.sidebar.multiselect(
        help="""
        Here, the data can be limited to selected aircraft categories.
        """,
        label="**Aircraft categories:**",
        options=_sql_query_acft_categories(),
    )

    if FILTER_ACFT_CATEGORIES:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Aircraft categories**: **`{','.join(FILTER_ACFT_CATEGORIES)}`**"
        )

    st.sidebar.markdown("""---""")

    max_no_aircraft = _sql_query_max_no_aircraft()

    min_no_aircraft = _sql_query_min_no_aircraft()

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

    st.sidebar.markdown("""---""")

    FILTER_EV_TYPE = st.sidebar.multiselect(
        default=FILTER_EV_TYPE_DEFAULT,
        help="""
        Here, the data can be limited to selected event types.
        Those events are selected whose event type matches.
        """,
        label="**Event type(s):**",
        options=_sql_query_ev_type(),
    )

    if FILTER_EV_TYPE:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Event type(s)**: **`{','.join(FILTER_EV_TYPE)}`**"
        )

    st.sidebar.markdown("""---""")

    FILTER_EV_YEAR_FROM, FILTER_EV_YEAR_TO = st.sidebar.slider(
        help="""
            - **`2008`** changes were made to the data collection mode.
            """,
        label="**Event year(s):**",
        min_value=2008,
        max_value=datetime.date.today().year,
        value=(2008, datetime.date.today().year - 1),
    )

    if FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO:
        # pylint: disable=line-too-long
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Event year(s)**: between **`{FILTER_EV_YEAR_FROM}`** and **`{FILTER_EV_YEAR_TO}`**"
        )

    st.sidebar.markdown("""---""")

    max_inj_f_grnd = _sql_query_max_inj_f_grnd()

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

    max_inj_tot_f = _sql_query_max_inj_tot_f()

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

    if (
        FILTER_INJ_F_GRND_FROM
        or FILTER_INJ_F_GRND_TO
        or FILTER_INJ_TOT_F_FROM
        or FILTER_INJ_TOT_F_TO
    ):
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

    if FILTER_EV_HIGHEST_INJURY:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Highest injury level(s)**: **`{','.join(FILTER_EV_HIGHEST_INJURY)}`**"
        )

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

    if FILTER_US_AVIATION:
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **US aviation criteria**: **`{','.join(FILTER_US_AVIATION)}`**"
        )

    st.sidebar.markdown("""---""")

    _print_timestamp("_setup_filter")


# ------------------------------------------------------------------
# Set up the filter of table events_sequence.
# ------------------------------------------------------------------
def _setup_filter_events_sequence():
    global ITEMS_FROM_ES_EVENTSOE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_EVENTSOE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_EVENTSOE_CODES_TRUE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_TRUE  # pylint: disable=global-statement

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
            + 'font-weight: normal;border-radius:2%;">Items from database table events_sequence</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_items_events_sequence = st.checkbox(
            help="Explanations for the item selection of database table events_sequence.",
            key="CHOICE_UG_ITEMS_EVENTS_SEQUENCE",
            label="**User Guide: Items from events_sequence****",
            value=False,
        )
    if choice_ug_items_events_sequence:
        _get_user_guide_items_events_sequence()

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    # ------------------------------------------------------------------
    # Occurrence code.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Occurrence code:**")

    with col3:
        ITEMS_FROM_ES_OCCURRENCE_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_ES_OCCURRENCE_CODES_ALL",
            label="**All**",
            value=True,
        )

    with col4:
        ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE = st.checkbox(
            help="Defining event.",
            key="ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE",
            label="**Defining event**",
            value=False,
        )

    with col5:
        ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE = st.checkbox(
            help="No defining event.",
            key="ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE",
            label="**No defining event**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Eventsoe no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Eventsoe no:**")

    with col3:
        ITEMS_FROM_ES_EVENTSOE_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_ES_EVENTSOE_CODES_ALL",
            label="**All**",
            value=False,
        )

    with col4:
        ITEMS_FROM_ES_EVENTSOE_CODES_TRUE = st.checkbox(
            help="Defining event.",
            key="ITEMS_FROM_ES_EVENTSOE_CODES_TRUE",
            label="**Defining event**",
            value=False,
        )

    with col5:
        ITEMS_FROM_ES_EVENTSOE_CODES_FALSE = st.checkbox(
            help="No defining event.",
            key="ITEMS_FROM_ES_EVENTSOE_CODES_FALSE",
            label="**No defining event**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Phase no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Phase no:**")

    with col3:
        ITEMS_FROM_ES_PHASE_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_ES_PHASE_CODES_ALL",
            label="**All**",
            value=False,
        )

    with col4:
        ITEMS_FROM_ES_PHASE_CODES_TRUE = st.checkbox(
            help="Defining event.",
            key="ITEMS_FROM_ES_PHASE_CODES_TRUE",
            label="**Defining event**",
            value=False,
        )

    with col5:
        ITEMS_FROM_ES_PHASE_CODES_FALSE = st.checkbox(
            help="No defining event.",
            key="ITEMS_FROM_ES_PHASE_CODES_FALSE",
            label="**No defining event**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Preventing redundancy.
    # ------------------------------------------------------------------

    if ITEMS_FROM_ES_OCCURRENCE_CODES_ALL:
        if ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Occurrence code** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Occurrence code** already contains the items of the selection **Not defining event**."
            )
            st.stop()

        if (
            ITEMS_FROM_ES_EVENTSOE_CODES_ALL
            or ITEMS_FROM_ES_EVENTSOE_CODES_FALSE
            or ITEMS_FROM_ES_EVENTSOE_CODES_TRUE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Occurrence code** already contains the items of the selection **Eventsoe no**."
            )
            st.stop()

        if (
            ITEMS_FROM_ES_PHASE_CODES_ALL
            or ITEMS_FROM_ES_PHASE_CODES_FALSE
            or ITEMS_FROM_ES_PHASE_CODES_TRUE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Occurrence code** already contains the items of the selection **Phase no**."
            )
            st.stop()

    if ITEMS_FROM_ES_EVENTSOE_CODES_ALL:
        if ITEMS_FROM_ES_EVENTSOE_CODES_TRUE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Eventsoe no** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_EVENTSOE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Eventsoe no** already contains the items of the selection **Not defining event**."
            )
            st.stop()

    if ITEMS_FROM_ES_PHASE_CODES_ALL:
        if ITEMS_FROM_ES_PHASE_CODES_TRUE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Phase no** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_PHASE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Phase no** already contains the items of the selection **Not defining event**."
            )
            st.stop()

    _print_timestamp("_setup_filter_events_sequence()")


# ------------------------------------------------------------------
# Set up the filter of table findings.
# ------------------------------------------------------------------
def _setup_filter_findings():
    global ITEMS_FROM_F_CATEGORY_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_CATEGORY_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_CATEGORY_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_CATEGORY_CODES_NONE  # pylint: disable=global-statement
    global ITEMS_FROM_F_FINDING_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_FINDING_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_FINDING_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_FINDING_CODES_NONE  # pylint: disable=global-statement
    global ITEMS_FROM_F_MODIFIER_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_MODIFIER_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_MODIFIER_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_MODIFIER_CODES_NONE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SECTION_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_SECTION_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SECTION_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_SECTION_CODES_NONE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBCATEGORY_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBCATEGORY_CODES_NONE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBSECTION_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBSECTION_CODES_CAUSE  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBSECTION_CODES_FACTOR  # pylint: disable=global-statement
    global ITEMS_FROM_F_SUBSECTION_CODES_NONE  # pylint: disable=global-statement

    # ------------------------------------------------------------------
    # Items from database table findings.
    # ------------------------------------------------------------------

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
            + 'font-weight: normal;border-radius:2%;">Items from database table findings</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        choice_ug_items_findings = st.checkbox(
            help="Explanations for the item selection of database table findings.",
            key="CHOICE_UG_ITEMS_FINDINGS",
            label="**User Guide: Items from findings**",
            value=False,
        )

    if choice_ug_items_findings:
        _get_user_guide_items_findings()

    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

    # ------------------------------------------------------------------
    # Finding code.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Finding code:**")

    with col3:
        ITEMS_FROM_F_FINDING_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_FINDING_CODES_ALL",
            label="**All**",
            value=True,
        )
    with col4:
        ITEMS_FROM_F_FINDING_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_FINDING_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_FINDING_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_FINDING_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_FINDING_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_FINDING_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Category no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Category no:**")

    with col3:
        ITEMS_FROM_F_CATEGORY_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_CATEGORY_CODES_ALL",
            label="**All**",
            value=False,
        )
    with col4:
        ITEMS_FROM_F_CATEGORY_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_CATEGORY_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_CATEGORY_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_CATEGORY_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_CATEGORY_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_CATEGORY_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Subcategory no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Subcategory no:**")

    with col3:
        ITEMS_FROM_F_SUBCATEGORY_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_SUBCATEGORY_CODES_ALL",
            label="**All**",
            value=False,
        )
    with col4:
        ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_SUBCATEGORY_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_SUBCATEGORY_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Section no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Section no:**")

    with col3:
        ITEMS_FROM_F_SECTION_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_SECTION_CODES_ALL",
            label="**All**",
            value=False,
        )
    with col4:
        ITEMS_FROM_F_SECTION_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_SECTION_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_SECTION_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_SECTION_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_SECTION_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_SECTION_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Subsection no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Subsection no:**")

    with col3:
        ITEMS_FROM_F_SUBSECTION_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_SUBSECTION_CODES_ALL",
            label="**All**",
            value=False,
        )
    with col4:
        ITEMS_FROM_F_SUBSECTION_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_SUBSECTION_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_SUBSECTION_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_SUBSECTION_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_SUBSECTION_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_SUBSECTION_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Modifier no.
    # ------------------------------------------------------------------

    with col1:
        st.markdown("**Modifier no:**")

    with col3:
        ITEMS_FROM_F_MODIFIER_CODES_ALL = st.checkbox(
            help="All.",
            key="ITEMS_FROM_F_MODIFIER_CODES_ALL",
            label="**All**",
            value=False,
        )
    with col4:
        ITEMS_FROM_F_MODIFIER_CODES_CAUSE = st.checkbox(
            help="Cause.",
            key="ITEMS_FROM_F_MODIFIER_CODES_CAUSE",
            label="**Cause**",
            value=False,
        )
    with col5:
        ITEMS_FROM_F_MODIFIER_CODES_FACTOR = st.checkbox(
            help="Factor.",
            key="ITEMS_FROM_F_MODIFIER_CODES_FACTOR",
            label="**Factor**",
            value=False,
        )
    with col6:
        ITEMS_FROM_F_MODIFIER_CODES_NONE = st.checkbox(
            help="Neither cause nor factor.",
            key="ITEMS_FROM_F_MODIFIER_CODES_NONE",
            label="**Neither**",
            value=False,
        )

    # ------------------------------------------------------------------
    # Preventing redundancy.
    # ------------------------------------------------------------------

    if ITEMS_FROM_F_FINDING_CODES_ALL:
        if ITEMS_FROM_F_FINDING_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Finding code** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_FINDING_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Finding code** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_FINDING_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Finding code** already contains the items of the selection **None**."
            )
            st.stop()

        if (
            ITEMS_FROM_F_CATEGORY_CODES_ALL
            or ITEMS_FROM_F_CATEGORY_CODES_CAUSE
            or ITEMS_FROM_F_CATEGORY_CODES_FACTOR
            or ITEMS_FROM_F_CATEGORY_CODES_NONE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Finding code** already contains the items of the selection **Category no**."
            )
            st.stop()

        if (
            ITEMS_FROM_F_SUBCATEGORY_CODES_ALL
            or ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE
            or ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR
            or ITEMS_FROM_F_SUBCATEGORY_CODES_NONE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Finding code** already contains the items of the selection **Subcategory no**."
            )
            st.stop()

        if (
            ITEMS_FROM_F_SECTION_CODES_ALL
            or ITEMS_FROM_F_SECTION_CODES_CAUSE
            or ITEMS_FROM_F_SECTION_CODES_FACTOR
            or ITEMS_FROM_F_SECTION_CODES_NONE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Finding code** already contains the items of the selection **Section no**."
            )
            st.stop()

        if (
            ITEMS_FROM_F_SUBSECTION_CODES_ALL
            or ITEMS_FROM_F_SUBSECTION_CODES_CAUSE
            or ITEMS_FROM_F_SUBSECTION_CODES_FACTOR
            or ITEMS_FROM_F_SUBSECTION_CODES_NONE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Finding code** already contains the items of the selection **Subsection no**."
            )
            st.stop()

        if (
            ITEMS_FROM_F_MODIFIER_CODES_ALL
            or ITEMS_FROM_F_MODIFIER_CODES_CAUSE
            or ITEMS_FROM_F_MODIFIER_CODES_FACTOR
            or ITEMS_FROM_F_MODIFIER_CODES_NONE
        ):
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **Finding code** already contains the items of the selection **Modifier no**."
            )
            st.stop()

    if ITEMS_FROM_F_CATEGORY_CODES_ALL:
        if ITEMS_FROM_F_CATEGORY_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Category no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_CATEGORY_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Category no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_CATEGORY_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Category no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SUBCATEGORY_CODES_ALL:
        if ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subcategory no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subcategory no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBCATEGORY_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subcategory no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SECTION_CODES_ALL:
        if ITEMS_FROM_F_SECTION_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Section no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SECTION_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Section no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SECTION_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Section no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SUBSECTION_CODES_ALL:
        if ITEMS_FROM_F_SUBSECTION_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subsection no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBSECTION_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subsection no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBSECTION_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Subsection no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_MODIFIER_CODES_ALL:
        if ITEMS_FROM_F_MODIFIER_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Modifier no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_MODIFIER_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Modifier no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_MODIFIER_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "##### Error: The selection **All** of **Modifier no** already contains the items of the selection **None**."
            )
            st.stop()

    _print_timestamp("_setup_filter_findings()")


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page() -> None:
    global CHOICE_ABOUT  # pylint: disable=global-statement
    global CHOICE_ACTIVE_FILTERS  # pylint: disable=global-statement
    global CHOICE_UG_APP  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement

    FILTER_EV_YEAR_FROM = FILTER_EV_YEAR_FROM if FILTER_EV_YEAR_FROM else 2008
    FILTER_EV_YEAR_TO = (
        FILTER_EV_YEAR_TO if FILTER_EV_YEAR_TO else datetime.date.today().year - 1
    )

    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        + 'font-weight: normal;border-radius:2%;">Association Rule Analysis - Year '
        + f"{FILTER_EV_YEAR_FROM} until {FILTER_EV_YEAR_TO}</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])

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

    _print_timestamp("_setup_page()")


# ------------------------------------------------------------------
# Set up the sidebar.
# ------------------------------------------------------------------
def _setup_sidebar() -> None:
    _setup_task_controls()

    _setup_filter()


# ------------------------------------------------------------------
# Set up the task controls.
# ------------------------------------------------------------------
def _setup_task_controls() -> None:
    global CHOICE_ALG_APRIORI  # pylint: disable=global-statement
    global CHOICE_ALG_COMBINATIONS_MAX  # pylint: disable=global-statement
    global CHOICE_ALG_COMBINATIONS_MIN  # pylint: disable=global-statement
    global CHOICE_ALG_ECLAT  # pylint: disable=global-statement
    global CHOICE_ALG_FPGROWTH  # pylint: disable=global-statement
    global CHOICE_ALG_FPMAX  # pylint: disable=global-statement
    global CHOICE_ALG_METRIC  # pylint: disable=global-statement
    global CHOICE_ALG_MIN_SUPPORT  # pylint: disable=global-statement
    global CHOICE_ALG_MIN_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_RUN_ALGORITHMS  # pylint: disable=global-statement
    global CHOICE_SHOW_ASSOCIATION_RULES  # pylint: disable=global-statement
    global CHOICE_SHOW_BINARY_DATA_ECLAT  # pylint: disable=global-statement
    global CHOICE_SHOW_FILTERED_RAW_DATA  # pylint: disable=global-statement
    global CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_SHOW_FREQUENT_ITEMSETS  # pylint: disable=global-statement
    global CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT  # pylint: disable=global-statement
    global CHOICE_SHOW_ONE_HOT_ENCODED_DATA  # pylint: disable=global-statement
    global CHOICE_SHOW_TRANSACTION_DATA  # pylint: disable=global-statement

    # pylint: disable=line-too-long
    CHOICE_RUN_ALGORITHMS = st.sidebar.checkbox(
        help="""
For efficiency reasons, it is very useful to define the parameter settings and filter conditions first and then run the selected algorithms.        """,
        key="CHOICE_RUN_ALGORITHMS",
        label="**Run the Algorithms**",
        value=False,
    )

    st.sidebar.markdown("""---""")

    CHOICE_ALG_APRIORI = st.sidebar.checkbox(
        help="""
Apriori is a popular algorithm [1] for extracting frequent itemsets with applications in association rule learning. 
The Apriori Algorithm has been designed to operate on databases containing transactions. 
An itemset is considered as "frequent" if it meets a user-specified support threshold. 
For instance, if the support threshold is set to 0.5 (50%), 
a frequent itemset is defined as a set of items that occur together in at least 50% of all transactions in the database.

**References**

[1] Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.
        """,
        key="CHOICE_ALG_APRIORI",
        label="**Apriori Algorithm**",
        value=False,
    )

    CHOICE_ALG_ECLAT = st.sidebar.checkbox(
        help="""
Unlike the a priori method, the ECLAT method is not based on the calculation of confidence and lift, therefore the ECLAT method is based on the calculation of the support conjunctions of the variables.
        """,
        key="CHOICE_ALG_ECLAT",
        label="**Eclat Algorithm**",
        value=False,
    )

    CHOICE_ALG_FPGROWTH = st.sidebar.checkbox(
        help="""
FP-Growth [1] is an algorithm for extracting frequent itemsets with applications in association rule learning that emerged as a popular alternative to the established Apriori Algorithm [2].

In general, the algorithm has been designed to operate on databases containing transactions. An itemset is considered as "frequent" if it meets a user-specified support threshold. For instance, if the support threshold is set to 0.5 (50%), a frequent itemset is defined as a set of items that occur together in at least 50% of all transactions in the database.

In particular, and what makes it different from the Apriori frequent pattern mining algorithm, FP-Growth is an frequent pattern mining algorithm that does not require candidate generation. Internally, it uses a so-called FP-tree (frequent pattern tree) data structure without generating the candidate sets explicitly, which makes is particularly attractive for large datasets.

**References**

[1] Han, Jiawei, Jian Pei, Yiwen Yin, and Runying Mao. "Mining frequent patterns without candidate generation. "A frequent-pattern tree approach." Data mining and knowledge discovery 8, no. 1 (2004): 53-87.

[2] Agrawal, Rakesh, and Ramakrishnan Srikant. "Fast algorithms for mining association rules." Proc. 20th int. conf. very large data bases, VLDB. Vol. 1215. 1994.
        """,
        key="CHOICE_ALG_FPGROWTH",
        label="**FP-Growth Algorithm**",
        value=False,
    )

    CHOICE_ALG_FPMAX = st.sidebar.checkbox(
        help="""
The Apriori algorithm is among the first and most popular algorithms for frequent itemset generation (frequent itemsets are then used for association rule mining). 
However, the runtime of Apriori can be quite large, especially for datasets with a large number of unique items, as the runtime grows exponentially depending on the number of unique items.

In contrast to Apriori, FP-Growth is a frequent pattern generation algorithm that inserts items into a pattern search tree, which allows it to have a linear increase in runtime with respect to the number of unique items or entries.

FP-Max is a variant of FP-Growth, which focuses on obtaining maximal itemsets. 
An itemset X is said to maximal if X is frequent and there exists no frequent super-pattern containing X. In other words, a frequent pattern X cannot be sub-pattern of larger frequent pattern to qualify for the definition maximal itemset.

**References**

[1] Grahne, G., & Zhu, J. (2003, November). Efficiently using prefix-trees in mining frequent itemsets. In FIMI (Vol. 90).
            """,
        key="CHOICE_ALG_FPMAX",
        label="**FP-Max Algorithm**",
        value=False,
    )

    if (
        CHOICE_ALG_APRIORI
        or CHOICE_ALG_ECLAT
        or CHOICE_ALG_FPGROWTH
        or CHOICE_ALG_FPMAX
    ):
        CHOICE_ALG_MIN_SUPPORT = st.sidebar.number_input(
            help="""
A decimal value 0 and 1 for minimum support of the itemsets returned.
The support is computed as the fraction
`transactions_where_item(s)_occur / total_transactions`.
            """,
            key="CHOICE_ALG_MIN_SUPPORT",
            label="**Minimum support**",
            max_value=1.00,
            min_value=0.01,
            value=0.50,
        )

        if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
            CHOICE_ALG_METRIC = st.sidebar.selectbox(
                help="""
Metric to evaluate if a rule is of interest.
The metrics are computed as follows:

- confidence(A->C) = support(A+C) / support(A), range: [0, 1]\n
- conviction = [1 - support(C)] / [1 - confidence(A->C)], range: [0, inf]\n
- leverage(A->C) = support(A->C) - support(A)*support(C), range: [-1, 1]\n
- lift(A->C) = confidence(A->C) / support(C), range: [0, inf]\n
- support(A->C) = support(A+C) [aka 'support'], range: [0, 1]\n
- zhangs_metric(A->C) = leverage(A->C) / max(support(A->C)*(1-support(A)), support(A)*(support(C)-support(A->C))) range: [-1,1]\n
                    """,
                index=0,
                key="CHOICE_ALG_METRIC",
                label="**Metric**",
                options=[
                    "confidence",
                    "conviction",
                    "leverage",
                    "lift",
                    "support",
                    "zhangs_metric",
                ],
            )

        if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
            CHOICE_ALG_MIN_THRESHOLD = st.sidebar.number_input(
                help="""
Minimal threshold for the evaluation metric,
via the `metric` parameter,
to decide whether a candidate rule is of interest.
            """,
                key="CHOICE_ALG_MIN_THRESHOLD",
                label="**Minimum threshold**",
                max_value=1.00,
                min_value=0.01,
                value=0.80,
            )

    st.sidebar.markdown("""---""")

    CHOICE_SHOW_FILTERED_RAW_DATA = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed raw data.",
        key="CHOICE_RAW_DATA_DETAILS",
        label="**Show Filtered Raw Data**",
        value=False,
    )

    if CHOICE_SHOW_FILTERED_RAW_DATA:
        CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE = st.sidebar.checkbox(
            help="Profiling of the filtered raw dataset.",
            key="CHOICE_RAW_DATA_PROFILE",
            label="**Show Filtered Raw Data Profile**",
            value=False,
        )

        if CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE:
            CHOICE_SHOW_FILTERED_RAW_DATA_PROFILE_TYPE = st.sidebar.radio(
                help="explorative: thorough but also slow - minimal: minimal but faster.",
                index=1,
                key="CHOICE_RAW_DATA_PROFILE_TYPE",
                label="**Data profile type**",
                options=(
                    [
                        "explorative",
                        "minimal",
                    ]
                ),
            )

    CHOICE_SHOW_TRANSACTION_DATA = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed transaction data.",
        key="CHOICE_TRANSACTION_DATA_DETAILS",
        label="**Show Transaction Data**",
        value=False,
    )

    if CHOICE_ALG_APRIORI or CHOICE_ALG_FPGROWTH or CHOICE_ALG_FPMAX:
        CHOICE_SHOW_ONE_HOT_ENCODED_DATA = st.sidebar.checkbox(
            help="Tabular representation of the one-hot encoded data.",
            key="CHOICE_ONE_HOT_ENCODED_DETAILS",
            label="**Show One-Hot Encoded Data**",
            value=False,
        )

    if CHOICE_ALG_ECLAT:
        CHOICE_SHOW_BINARY_DATA_ECLAT = st.sidebar.checkbox(
            help="Tabular representation of the binary data.",
            key="CHOICE_BINARY_DATA",
            label="**Show Binary Data**",
            value=False,
        )

    if (
        CHOICE_ALG_APRIORI
        or CHOICE_ALG_ECLAT
        or CHOICE_ALG_FPGROWTH
        or CHOICE_ALG_FPMAX
    ):
        CHOICE_SHOW_FREQUENT_ITEMSETS = st.sidebar.checkbox(
            help="Tabular representation of the frequent itemsets.",
            key="CHOICE_FREQUENT_ITEMSETS_DETAILS",
            label="**Show Frequent Itemsets**",
            value=True,
        )
        if CHOICE_ALG_ECLAT:
            CHOICE_SHOW_FREQUENT_ITEMSETS_TREE_MAP_ECLAT = st.sidebar.checkbox(
                help="Tree map representation of the frequent itemsets.",
                key="CHOICE_ITEM_DISTRIBUTION_TREE_MAP_ECLAT",
                label="**Show Frequent Itemsets TreeMap**",
                value=False,
            )
        CHOICE_SHOW_ASSOCIATION_RULES = st.sidebar.checkbox(
            help="Tabular representation of the association rules.",
            key="CHOICE_ASSOCIATION_RULES_DETAILS",
            label="**Show Association Rules**",
            value=True,
        )
        if CHOICE_ALG_ECLAT:
            (
                CHOICE_ALG_COMBINATIONS_MIN,
                CHOICE_ALG_COMBINATIONS_MAX,
            ) = st.sidebar.slider(
                help="""The minimum and maximum amount of items in the transaction.""",
                label="**Combinations:**",
                min_value=2,
                max_value=10,
                value=(2, 2),
            )

    st.sidebar.markdown("""---""")

    _print_timestamp("_setup_task_controls()")


# ------------------------------------------------------------------
# Execute a query that returns the list of aircraft categories.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
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
# Execute a query that creates the list of category codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_category() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT category_code,
               description
          FROM io_md_codes_category;
        """
        )

        data = {}

        for row in cur:
            (category_code, description) = row
            data[category_code] = description

        _print_timestamp("_sql_query_codes_category()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of eventsoe codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_eventsoe() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT eventsoe_code,
               description
          FROM io_md_codes_eventsoe;
        """
        )

        data = {}

        for row in cur:
            (eventsoe_code, description) = row
            data[eventsoe_code] = description

        _print_timestamp("_sql_query_codes_eventsoe()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of modifier codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_modifier() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT modifier_code,
               description
          FROM io_md_codes_modifier;
        """
        )

        data = {}

        for row in cur:
            (modifier_code, description) = row
            data[modifier_code] = description

        _print_timestamp("_sql_query_codes_modifier()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of phase codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_phase() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT phase_code,
               description
          FROM io_md_codes_phase;
        """
        )

        data = {}

        for row in cur:
            (phase_code, description) = row
            data[phase_code] = description

        _print_timestamp("_sql_query_codes_phase()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of section codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_section() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT category_code,
               subcategory_code, 
               section_code,
               description
          FROM io_md_codes_section;
        """
        )

        data = {}

        for row in cur:
            (category_code, subcategory_code, section_code, description) = row
            data[category_code + subcategory_code + section_code] = description

        _print_timestamp("_sql_query_codes_section()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of subcategory codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_subcategory() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT category_code,
               subcategory_code,
               description
          FROM io_md_codes_subcategory;
        """
        )

        data = {}

        for row in cur:
            (category_code, subcategory_code, description) = row
            data[category_code + subcategory_code] = description

        _print_timestamp("_sql_query_codes_subcategory()")

        return data


# ------------------------------------------------------------------
# Execute a query that creates the list of subsection codes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_codes_subsection() -> dict[str, str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
        cur.execute(
            """
        SELECT category_code,
               subcategory_code, 
               section_code,
               subsection_code,
               description
          FROM io_md_codes_subsection;
        """
        )

        data = {}

        for row in cur:
            (
                category_code,
                subcategory_code,
                section_code,
                subsection_code,
                description,
            ) = row
            data[
                category_code + subcategory_code + section_code + subsection_code
            ] = description

        _print_timestamp("_sql_query_codes_subsection()")

        return data


# ------------------------------------------------------------------
# Execute a query that returns the list of injury levels
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_ev_highest_injury() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
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
@st.cache_data(persist=True)
def _sql_query_ev_type() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # flake8: noqa: E501
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
# Determine the maximum number of fatalities on ground.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_max_array_length() -> int:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT MAX(ARRAY_LENGTH(all_finding_codes, 1))
             + MAX(ARRAY_LENGTH(all_occurrence_codes, 1)) 
          FROM io_app_ae1982 iaa;
        """
        )

        return cur.fetchone()[0]  # type: ignore


# ------------------------------------------------------------------
# Determine the maximum number of fatalities on ground.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
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
@st.cache_data(persist=True)
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
# Execute a query that returns the list of categories.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_category() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', category_code), ',' ORDER BY 1)
          FROM io_md_codes_category;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of eventsoes.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_eventsoe() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', eventsoe_code), ',' ORDER BY 1)
          FROM io_md_codes_eventsoe;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of modifiers.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_modifier() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', modifier_code), ',' ORDER BY 1)
          FROM io_md_codes_modifier;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


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
# Execute a query that returns the list of sections.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_section() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', category_code, subcategory_code, section_code), ',' ORDER BY 1)
          FROM io_md_codes_section;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of subcategories.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_subcategory() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', category_code, subcategory_code), ',' ORDER BY 1)
          FROM io_md_codes_subcategory;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Execute a query that returns the list of subsections.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
def _sql_query_md_codes_subsection() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        cur.execute(
            """
        SELECT string_agg(CONCAT(description, ' - ', category_code, subcategory_code, section_code, subsection_code), ',' ORDER BY 1)
          FROM io_md_codes_subsection;
        """
        )

        return (cur.fetchone()[0]).split(",")  # type: ignore


# ------------------------------------------------------------------
# Determine the minimum number of involved aircraft.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
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
@st.cache_data(persist=True)
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
# Execute a query that returns the list of US states.
# ------------------------------------------------------------------
@st.cache_data(persist=True)
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
    global DF_RAW_DATA_FILTERED  # pylint: disable=global-statement
    global DF_RAW_DATA_FILTERED_ROWS  # pylint: disable=global-statement
    global DF_RAW_DATA_UNFILTERED  # pylint: disable=global-statement
    global DF_RAW_DATA_UNFILTERED_ROWS  # pylint: disable=global-statement
    global HOST_CLOUD  # pylint: disable=global-statement
    global MD_CODES_CATEGORY  # pylint: disable=global-statement
    global MD_CODES_EVENTSOE  # pylint: disable=global-statement
    global MD_CODES_MODIFIER  # pylint: disable=global-statement
    global MD_CODES_PHASE  # pylint: disable=global-statement
    global MD_CODES_SECTION  # pylint: disable=global-statement
    global MD_CODES_SUBCATEGORY  # pylint: disable=global-statement
    global MD_CODES_SUBSECTION  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement
    global START_TIME  # pylint: disable=global-statement

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
    else:
        (host, _mode) = utils.get_args()
        HOST_CLOUD = bool(host == "Cloud")
        st.session_state["HOST_CLOUD"] = HOST_CLOUD

    # flake8: noqa: E501
    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Favicon.ico?raw=true",
        page_title=f"{APP_ID} by IO-Aero",
    )

    col1, col2 = st.sidebar.columns(2)
    col1.markdown("##  [IO-Aero Website](https://www.io-aero.com)")
    url = "http://" + ("members.io-aero.com:8080" if HOST_CLOUD else "localhost:8598")
    col2.markdown(f"##  [Member Menu]({url})")

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    utils.has_access(HOST_CLOUD, APP_ID)

    # ------------------------------------------------------------------
    # Get data.
    # ------------------------------------------------------------------

    PG_CONN = _get_postgres_connection()
    _print_timestamp("_get_postgres_connection - got DB connection")

    _setup_sidebar()

    _setup_page()

    MD_CODES_CATEGORY = _sql_query_codes_category()
    MD_CODES_EVENTSOE = _sql_query_codes_eventsoe()
    MD_CODES_MODIFIER = _sql_query_codes_modifier()
    MD_CODES_PHASE = _sql_query_codes_phase()
    MD_CODES_SECTION = _sql_query_codes_section()
    MD_CODES_SUBCATEGORY = _sql_query_codes_subcategory()
    MD_CODES_SUBSECTION = _sql_query_codes_subsection()

    # ------------------------------------------------------------------
    # Filter data.
    # ------------------------------------------------------------------

    DF_RAW_DATA_UNFILTERED = _get_raw_data()
    _print_timestamp("_get_raw_data()")

    (DF_RAW_DATA_UNFILTERED_ROWS, _) = DF_RAW_DATA_UNFILTERED.shape
    if DF_RAW_DATA_UNFILTERED_ROWS == 0:
        st.error("##### Error: There are no data available.")
        st.stop()

    DF_RAW_DATA_FILTERED = DF_RAW_DATA_UNFILTERED

    if (
        CHOICE_FILTER_DATA_OTHER
        or CHOICE_FILTER_DATA_EVENTS_SEQUENCE
        or CHOICE_FILTER_DATA_FINDINGS
    ):
        DF_RAW_DATA_FILTERED = _apply_filter(
            DF_RAW_DATA_UNFILTERED,
        )

    (DF_RAW_DATA_FILTERED_ROWS, _) = DF_RAW_DATA_FILTERED.shape
    if DF_RAW_DATA_FILTERED_ROWS == 0:
        st.error("##### Error: No data has been selected.")
        st.stop()

    # ------------------------------------------------------------------
    # Present the results.
    # ------------------------------------------------------------------

    _present_results()

    # Stop time measurement.
    # flake8: noqa: E501
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
