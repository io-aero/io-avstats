# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Association Rule Analysis."""
import datetime
import time

import pandas as pd
import psycopg2
import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from mlxtend.frequent_patterns import apriori  # type: ignore
from mlxtend.frequent_patterns import association_rules
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
APP_ID = "slara"

# pylint: disable=R0801
# pylint: disable=too-many-lines
CHOICE_ABOUT: bool | None = None
CHOICE_ACTIVE_FILTERS: bool | None = None
CHOICE_ACTIVE_FILTERS_TEXT: str = ""

CHOICE_ALG_APRIORI: bool | None = None
CHOICE_ALG_ECLAT: bool | None = None
CHOICE_ALG_FPGROWTH: bool | None = None
CHOICE_ALG_METRIC: str | None = None
CHOICE_ALG_MIN_SUPPORT: float | None = None
CHOICE_ALG_MIN_THRESHOLD: float | None = None

CHOICE_FILTER_DATA: bool | None = None
CHOICE_FREQUENT_ITEMSETS_DETAILS: bool | None = None

CHOICE_ONE_HOT_ENCODED_DETAILS: bool | None = None

CHOICE_RAW_DATA_DETAILS: bool | None = None
CHOICE_RAW_DATA_PROFILE: bool | None = None
CHOICE_RAW_DATA_PROFILE_TYPE: str | None = None
CHOICE_RULES_DETAILS: bool | None = None

CHOICE_TRANSACTION_DATA_DETAILS: bool | None = None

CHOICE_UG_APP: bool | None = None
CHOICE_UG_FREQUENT_ITEMSETS_DETAILS: bool | None = None
CHOICE_UG_ITEMS_EVENTS_SEQUENCE: bool | None = None
CHOICE_UG_ITEMS_FINDINGS: bool | None = None
CHOICE_UG_ONE_HOT_ENCODED_DETAILS: bool | None = None
CHOICE_UG_RAW_DATA_DETAILS: bool | None = None
CHOICE_UG_RAW_DATA_PROFILE: bool | None = None
CHOICE_UG_RULES_DETAILS: bool | None = None
CHOICE_UG_TRANSACTION_DATA_DETAILS: bool | None = None

COLOR_HEADER: str = "#357f8f"

COUNTRY_USA = "USA"

DF_FREQUENT_ITEMSETS_APRIORI: DataFrame = DataFrame()
DF_ONE_HOT_ENCODED_DATA: DataFrame = DataFrame()
DF_RAW_DATA_FILTERED: DataFrame = DataFrame()
DF_RAW_DATA_UNFILTERED: DataFrame = DataFrame()
DF_RULES_APRIORI: DataFrame = DataFrame()
DF_TRANSACTION_DATA: DataFrame = DataFrame()

FILTER_ACFT_CATEGORIES: list[str] = []
FILTER_EV_HIGHEST_INJURY: list[str] = []
FILTER_EV_HIGHEST_INJURY_DEFAULT: list[str] = ["fatal"]
FILTER_EV_TYPE: list[str] = []
FILTER_EV_TYPE_DEFAULT = ["Accident"]
FILTER_EV_YEAR_INCOMPATIBLE = 2008
FILTER_EV_YEAR_FROM: int | None = None
FILTER_EV_YEAR_TO: int | None = None
FILTER_INJ_F_GRND_FROM: int | None = None
FILTER_INJ_F_GRND_TO: int | None = None
FILTER_INJ_TOT_F_FROM: int | None = None
FILTER_INJ_TOT_F_TO: int | None = None
FILTER_NO_AIRCRAFT_FROM: int | None = None
FILTER_NO_AIRCRAFT_TO: int | None = None
FILTER_STATE: list[str] = []
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
FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

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
    if FILTER_STATE:
        # noinspection PyUnboundLocalVariable
        df_filtered = df_filtered.loc[(df_filtered["state"].isin(FILTER_STATE))]
        _print_timestamp(f"_apply_filter() - {len(df_filtered):>6} - FILTER_STATE")

    # noinspection PyUnboundLocalVariable
    if FILTER_US_AVIATION:
        df_filtered = _apply_filter_us_aviation(df_filtered, FILTER_US_AVIATION)
        _print_timestamp(
            f"_apply_filter() - {len(df_filtered):>6} - FILTER_US_AVIATION"
        )

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
# Present frequent itemset details.
# ------------------------------------------------------------------
def _create_df_frequent_itemsets_ext() -> DataFrame:
    df_ext = DF_FREQUENT_ITEMSETS_APRIORI.copy()

    df_ext["itemsets_description"] = ""

    for idx in df_ext.index:
        df_ext["itemsets_description"][idx] = _get_frozenset_description(
            df_ext["itemsets"][idx]
        )

    return df_ext


# ------------------------------------------------------------------
# Present rules details.
# ------------------------------------------------------------------
def _create_df_rules_ext() -> DataFrame:
    df_ext = DF_RULES_APRIORI.copy()

    df_ext.insert(1, "antecedents_description", "")
    df_ext.insert(3, "consequents_description", "")

    for idx in df_ext.index:
        df_ext["antecedents_description"][idx] = _get_frozenset_description(
            df_ext["antecedents"][idx]
        )
        df_ext["consequents_description"][idx] = _get_frozenset_description(
            df_ext["consequents"][idx]
        )

    return df_ext


# ------------------------------------------------------------------
# Create frequent itemsets with the Apriori Algorithm.
# ------------------------------------------------------------------
def _create_frequent_itemsets_apriori() -> None:
    global DF_FREQUENT_ITEMSETS_APRIORI  # pylint: disable=global-statement

    _print_timestamp("_create_frequent_itemsets_apriori() - Start")

    DF_FREQUENT_ITEMSETS_APRIORI = apriori(
        DF_ONE_HOT_ENCODED_DATA, min_support=CHOICE_ALG_MIN_SUPPORT, use_colnames=True
    )

    if DF_FREQUENT_ITEMSETS_APRIORI.empty:
        # pylint: disable=line-too-long
        st.error(
            "**Error**: The selected algorithm did not find any data with the given items and parameters."
        )
        st.stop()

    _print_timestamp("_create_frequent_itemsets_apriori() - End")


# ------------------------------------------------------------------
# Apply one-hot encoding.
# ------------------------------------------------------------------
def _create_one_hot_encoded_data() -> None:
    global DF_ONE_HOT_ENCODED_DATA  # pylint: disable=global-statement

    _print_timestamp("_create_one_hot_encoded_data() - Start")

    DF_ONE_HOT_ENCODED_DATA = (
        DF_TRANSACTION_DATA["items"].str.join("|").str.get_dummies()
    )

    _print_timestamp("_create_one_hot_encoded_data() - End")


# ------------------------------------------------------------------
# Create association rules with the Apriori Algorithm.
# ------------------------------------------------------------------
def _create_rules_apriori() -> None:
    global DF_RULES_APRIORI  # pylint: disable=global-statement

    _print_timestamp("_create_rules_apriori() - Start")

    DF_RULES_APRIORI = association_rules(
        DF_FREQUENT_ITEMSETS_APRIORI,
        metric=CHOICE_ALG_METRIC,
        min_threshold=CHOICE_ALG_MIN_THRESHOLD,
    )

    _print_timestamp("_create_rules_apriori() - End")


# ------------------------------------------------------------------
# Create the transaction dataframe.
# ------------------------------------------------------------------
def _create_transaction_data() -> None:
    _print_timestamp("_get_transaction_data() - Start")

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
        st.error("**Error**: No items selected.")
        st.stop()

    DF_TRANSACTION_DATA["items"] = eval(transaction_cmd)  # pylint: disable=eval-used

    _print_timestamp("_get_transaction_data() - End")


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
# Determine the itemset description.
# ------------------------------------------------------------------
def _get_frozenset_description(itemset) -> list[tuple[str, list[str], str]]:
    descriptions = []

    for item in itemset:
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

        descriptions.append((attribute, description, variant))

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
# Read the raw data.
# ------------------------------------------------------------------
# @st.cache_data
def _get_raw_data() -> DataFrame:
    _print_timestamp("_get_raw_data() - Start")

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
            WHERE ev_year >= 2008
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
# one-hot encoded data.
# ------------------------------------------------------------------
def _get_user_guide_details_one_hot_encoded_data() -> None:
    text = """
#### User guide: One-hot encoded data details

This task provides the detailed one-hot encoded data in a table format for display and download as **csv** file. 
To avoid memory problems in the web browser, the display is limited to the first 100 rows and columns.
The **csv** download is not limited, but may not be processable with MS Excel.
    """

    st.warning(text + _get_user_guide_details_standard())


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

- **Eventsoe no** - event sequence
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
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data() -> None:
    global CHOICE_UG_ITEMS_EVENTS_SEQUENCE  # pylint: disable=global-statement
    global CHOICE_UG_ITEMS_FINDINGS  # pylint: disable=global-statement
    global ITEMS_FROM_ES_EVENTSOE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_EVENTSOE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_EVENTSOE_CODES_TRUE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_OCCURRENCE_CODES_TRUE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_ALL  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_FALSE  # pylint: disable=global-statement
    global ITEMS_FROM_ES_PHASE_CODES_TRUE  # pylint: disable=global-statement
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

    _print_timestamp("_present_data() - Start")

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

    # ------------------------------------------------------------------
    # Items from database table events_sequence.
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
            + 'font-weight: normal;border-radius:2%;">Items from database table events_sequence</p>',
            unsafe_allow_html=True,
        )

    with col2:
        # pylint: disable=line-too-long
        CHOICE_UG_ITEMS_EVENTS_SEQUENCE = st.checkbox(
            help="Explanations for the item selection of database table events_sequence.",
            key="CHOICE_UG_ITEMS_EVENTS_SEQUENCE",
            label="**User Guide: Items from events_sequence**",
            value=False,
        )

    if CHOICE_UG_ITEMS_EVENTS_SEQUENCE:
        _get_user_guide_items_events_sequence()

    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

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
                "**Error**: The selection **All** of **Occurrence code** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_OCCURRENCE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Occurrence code** already contains the items of the selection **Not defining event**."
            )
            st.stop()

        if (
            ITEMS_FROM_ES_EVENTSOE_CODES_ALL
            or ITEMS_FROM_ES_EVENTSOE_CODES_FALSE
            or ITEMS_FROM_ES_EVENTSOE_CODES_TRUE
        ):
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **Occurrence code** already contains the items of the selection **Eventsoe no**."
            )
            st.stop()

        if (
            ITEMS_FROM_ES_PHASE_CODES_ALL
            or ITEMS_FROM_ES_PHASE_CODES_FALSE
            or ITEMS_FROM_ES_PHASE_CODES_TRUE
        ):
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **Occurrence code** already contains the items of the selection **Phase no**."
            )
            st.stop()

    if ITEMS_FROM_ES_EVENTSOE_CODES_ALL:
        if ITEMS_FROM_ES_EVENTSOE_CODES_TRUE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Eventsoe no** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_EVENTSOE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Eventsoe no** already contains the items of the selection **Not defining event**."
            )
            st.stop()

    if ITEMS_FROM_ES_PHASE_CODES_ALL:
        if ITEMS_FROM_ES_PHASE_CODES_TRUE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Phase no** already contains the items of the selection **Defining event**."
            )
            st.stop()

        if ITEMS_FROM_ES_PHASE_CODES_FALSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Phase no** already contains the items of the selection **Not defining event**."
            )
            st.stop()

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
        CHOICE_UG_ITEMS_FINDINGS = st.checkbox(
            help="Explanations for the item selection of database table findings.",
            key="CHOICE_UG_ITEMS_FINDINGS",
            label="**User Guide: Items from findings**",
            value=False,
        )

    if CHOICE_UG_ITEMS_FINDINGS:
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
                "**Error**: The selection **All** of **Finding code** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_FINDING_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Finding code** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_FINDING_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Finding code** already contains the items of the selection **None**."
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
                "**Error**: The selection **Finding code** already contains the items of the selection **Category no**."
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
                "**Error**: The selection **Finding code** already contains the items of the selection **Subcategory no**."
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
                "**Error**: The selection **Finding code** already contains the items of the selection **Section no**."
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
                "**Error**: The selection **Finding code** already contains the items of the selection **Subsection no**."
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
                "**Error**: The selection **Finding code** already contains the items of the selection **Modifier no**."
            )
            st.stop()

    if ITEMS_FROM_F_CATEGORY_CODES_ALL:
        if ITEMS_FROM_F_CATEGORY_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Category no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_CATEGORY_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Category no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_CATEGORY_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Category no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SUBCATEGORY_CODES_ALL:
        if ITEMS_FROM_F_SUBCATEGORY_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subcategory no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBCATEGORY_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subcategory no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBCATEGORY_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subcategory no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SECTION_CODES_ALL:
        if ITEMS_FROM_F_SECTION_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Section no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SECTION_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Section no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SECTION_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Section no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_SUBSECTION_CODES_ALL:
        if ITEMS_FROM_F_SUBSECTION_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subsection no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBSECTION_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subsection no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_SUBSECTION_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Subsection no** already contains the items of the selection **None**."
            )
            st.stop()

    if ITEMS_FROM_F_MODIFIER_CODES_ALL:
        if ITEMS_FROM_F_MODIFIER_CODES_CAUSE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Modifier no** already contains the items of the selection **Cause**."
            )
            st.stop()

        if ITEMS_FROM_F_MODIFIER_CODES_FACTOR:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Modifier no** already contains the items of the selection **Factor**."
            )
            st.stop()

        if ITEMS_FROM_F_MODIFIER_CODES_NONE:
            # pylint: disable=line-too-long
            st.error(
                "**Error**: The selection **All** of **Modifier no** already contains the items of the selection **None**."
            )
            st.stop()

    # ------------------------------------------------------------------
    # Raw data.
    # ------------------------------------------------------------------

    if CHOICE_RAW_DATA_DETAILS:
        _present_details_raw_data()
        _print_timestamp("_present_raw_data_details() - CHOICE_RAW_DATA_DETAILS")

        if CHOICE_RAW_DATA_PROFILE:
            _present_profile_raw_data()
            _print_timestamp("_present_raw_data_profile() - CHOICE_RAW_DATA_PROFILE")

    # ------------------------------------------------------------------
    # Transaction data.
    # ------------------------------------------------------------------

    _create_transaction_data()

    if CHOICE_TRANSACTION_DATA_DETAILS:
        _present_details_transaction_data()
        _print_timestamp(
            "_present_transaction_data_details() - CHOICE_TRANSACTION_DATA_DETAILS"
        )

    # ------------------------------------------------------------------
    # One-hot encoded data.
    # ------------------------------------------------------------------

    if CHOICE_ALG_APRIORI:
        _create_one_hot_encoded_data()
        if CHOICE_ONE_HOT_ENCODED_DETAILS:
            _present_details_one_hot_encoded_data()
            _print_timestamp(
                "_present_one_hot_encoded_details() - CHOICE_ONE_HOT_ENCODED_DETAILS"
            )

    # ------------------------------------------------------------------
    # Frequent itemsets.
    # ------------------------------------------------------------------

    if CHOICE_ALG_APRIORI:
        _create_frequent_itemsets_apriori()
        if CHOICE_FREQUENT_ITEMSETS_DETAILS:
            _present_details_frequent_itemsets()
            _print_timestamp(
                "_present_frequent_itemsets_details() - CHOICE_FREQUENT_ITEMSETS_DETAILS"
            )

    # ------------------------------------------------------------------
    # Association rules.
    # ------------------------------------------------------------------

    if CHOICE_ALG_APRIORI:
        _create_rules_apriori()
        if CHOICE_RULES_DETAILS:
            _present_details_rules()
            _print_timestamp("_present_rules_details() - CHOICE_RULES_DETAILS")

    _print_timestamp("_present_data() - End")


# ------------------------------------------------------------------
# Present frequent itemset details.
# ------------------------------------------------------------------
def _present_details_frequent_itemsets() -> None:
    global CHOICE_UG_FREQUENT_ITEMSETS_DETAILS  # pylint: disable=global-statement

    if CHOICE_FREQUENT_ITEMSETS_DETAILS:
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
                + 'font-weight: normal;border-radius:2%;">Detailed frequent itemsets</p>',
                unsafe_allow_html=True,
            )

        with col2:
            # pylint: disable=line-too-long
            CHOICE_UG_FREQUENT_ITEMSETS_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed frequent itemsets view.",
                label="**User Guide: Frequent itemset details**",
                value=False,
            )

        if CHOICE_UG_FREQUENT_ITEMSETS_DETAILS:
            _get_user_guide_details_frequent_itemsets()

        df_frequent_itemsets_ext = _create_df_frequent_itemsets_ext()

        st.dataframe(df_frequent_itemsets_ext)

        st.download_button(
            data=_convert_df_2_csv(df_frequent_itemsets_ext),
            file_name=APP_ID + "_frequent_itemsets_detail.csv",
            help="The download includes all frequent itemsets.",
            label="Download the frequent itemsets",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present one-hot encoded data details.
# ------------------------------------------------------------------
def _present_details_one_hot_encoded_data() -> None:
    global CHOICE_UG_ONE_HOT_ENCODED_DETAILS  # pylint: disable=global-statement

    if CHOICE_ONE_HOT_ENCODED_DETAILS:
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
                + 'font-weight: normal;border-radius:2%;">Detailed one-hot encoded data</p>',
                unsafe_allow_html=True,
            )

        with col2:
            # pylint: disable=line-too-long
            CHOICE_UG_ONE_HOT_ENCODED_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed one-hot encoded data view.",
                label="**User Guide: One-hot encoded data details**",
                value=False,
            )

        if CHOICE_UG_ONE_HOT_ENCODED_DETAILS:
            _get_user_guide_details_one_hot_encoded_data()

        st.dataframe(DF_ONE_HOT_ENCODED_DATA.iloc[:100, :100])

        st.download_button(
            data=_convert_df_2_csv(DF_ONE_HOT_ENCODED_DATA),
            file_name=APP_ID + "_one_hot_encoded_data_detail.csv",
            help="The download includes all one-hot encoded data.",
            label="Download the detailed one-hot encoded data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present raw data details.
# ------------------------------------------------------------------
def _present_details_raw_data() -> None:
    global CHOICE_UG_RAW_DATA_DETAILS  # pylint: disable=global-statement

    if CHOICE_RAW_DATA_DETAILS:
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
                + 'font-weight: normal;border-radius:2%;">Detailed raw data</p>',
                unsafe_allow_html=True,
            )

        with col2:
            # pylint: disable=line-too-long
            CHOICE_UG_RAW_DATA_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed raw data view.",
                label="**User Guide: Raw data details**",
                value=False,
            )

        if CHOICE_UG_RAW_DATA_DETAILS:
            _get_user_guide_details_raw_data()

        st.dataframe(DF_RAW_DATA_FILTERED)

        st.download_button(
            data=_convert_df_2_csv(DF_RAW_DATA_FILTERED),
            file_name=APP_ID + "_raw_data_detail.csv",
            help="The download includes all raw data "
            + "after applying the filter options.",
            label="Download the detailed raw data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present association rule details.
# ------------------------------------------------------------------
def _present_details_rules() -> None:
    global CHOICE_UG_RULES_DETAILS  # pylint: disable=global-statement

    if CHOICE_RULES_DETAILS:
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
                + 'font-weight: normal;border-radius:2%;">Detailed association rules</p>',
                unsafe_allow_html=True,
            )

        # pylint: disable=line-too-long
        with col2:
            CHOICE_UG_RULES_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed association rules view.",
                label="**User Guide: Association rule details**",
                value=False,
            )

        if CHOICE_UG_RULES_DETAILS:
            _get_user_guide_details_association_rules()

        df_rules_ext = _create_df_rules_ext()

        st.dataframe(df_rules_ext)

        st.download_button(
            data=_convert_df_2_csv(df_rules_ext),
            file_name=APP_ID + "_rules_detail.csv",
            help="The download includes all association rules.",
            label="Download the association rules",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present transaction data details.
# ------------------------------------------------------------------
def _present_details_transaction_data() -> None:
    global CHOICE_UG_TRANSACTION_DATA_DETAILS  # pylint: disable=global-statement

    if CHOICE_TRANSACTION_DATA_DETAILS:
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
                + 'font-weight: normal;border-radius:2%;">Detailed transaction data</p>',
                unsafe_allow_html=True,
            )

        with col2:
            # pylint: disable=line-too-long
            CHOICE_UG_TRANSACTION_DATA_DETAILS = st.checkbox(
                help="Explanations and operating instructions related to the detailed transaction data view.",
                label="**User Guide: Transaction data details**",
                value=False,
            )

        if CHOICE_UG_TRANSACTION_DATA_DETAILS:
            _get_user_guide_details_transaction_data()

        st.dataframe(DF_TRANSACTION_DATA)

        st.download_button(
            data=_convert_df_2_csv(DF_TRANSACTION_DATA),
            file_name=APP_ID + "_transaction_data_detail.csv",
            help="The download includes all transaction data.",
            label="Download the detailed transaction data",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present raw data profile.
# ------------------------------------------------------------------
def _present_profile_raw_data() -> None:
    global CHOICE_UG_RAW_DATA_PROFILE  # pylint: disable=global-statement

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
        CHOICE_UG_RAW_DATA_PROFILE = st.checkbox(
            help="Explanations and operating instructions related to profiling "
            + "of the database view **io_app_ae1982",
            label="**User Guide: Raw data profile**",
            value=False,
        )

    if CHOICE_UG_RAW_DATA_PROFILE:
        _get_user_guide_data_profile("Raw data")

    # noinspection PyUnboundLocalVariable
    if CHOICE_RAW_DATA_PROFILE_TYPE == "explorative":
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
        file_name=APP_ID + "_raw_data_profile_" + CHOICE_RAW_DATA_PROFILE_TYPE + ".html",  # type: ignore
        help="The download includes a profile report from the dataframe "
        + "after applying the filter options.",
        label="Download the raw data profile report",
        mime="text/html",
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
    global FILTER_EV_HIGHEST_INJURY  # pylint: disable=global-statement
    global FILTER_EV_TYPE  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_FROM  # pylint: disable=global-statement
    global FILTER_INJ_F_GRND_TO  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_FROM  # pylint: disable=global-statement
    global FILTER_INJ_TOT_F_TO  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_FROM  # pylint: disable=global-statement
    global FILTER_NO_AIRCRAFT_TO  # pylint: disable=global-statement
    global FILTER_STATE  # pylint: disable=global-statement
    global FILTER_US_AVIATION  # pylint: disable=global-statement

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

    st.sidebar.markdown("""---""")

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
        _print_timestamp("_setup_filter - FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO")

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
        + 'font-weight: normal;border-radius:2%;">Association Rule Analysis between '
        + f"{FILTER_EV_YEAR_FROM} and {FILTER_EV_YEAR_TO}</p>",
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
    global CHOICE_ALG_APRIORI  # pylint: disable=global-statement
    global CHOICE_ALG_ECLAT  # pylint: disable=global-statement
    global CHOICE_ALG_FPGROWTH  # pylint: disable=global-statement
    global CHOICE_ALG_METRIC  # pylint: disable=global-statement
    global CHOICE_ALG_MIN_SUPPORT  # pylint: disable=global-statement
    global CHOICE_ALG_MIN_THRESHOLD  # pylint: disable=global-statement
    global CHOICE_FREQUENT_ITEMSETS_DETAILS  # pylint: disable=global-statement
    global CHOICE_ONE_HOT_ENCODED_DETAILS  # pylint: disable=global-statement
    global CHOICE_RAW_DATA_DETAILS  # pylint: disable=global-statement
    global CHOICE_RAW_DATA_PROFILE  # pylint: disable=global-statement
    global CHOICE_RAW_DATA_PROFILE_TYPE  # pylint: disable=global-statement
    global CHOICE_RULES_DETAILS  # pylint: disable=global-statement
    global CHOICE_TRANSACTION_DATA_DETAILS  # pylint: disable=global-statement

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    CHOICE_ALG_APRIORI = st.sidebar.checkbox(
        help="""
Apriori is a popular algorithm [1] for extracting frequent itemsets with applications in association rule learning. 
The apriori algorithm has been designed to operate on databases containing transactions. 
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
        disabled=True,
        help="Use the Eclat Algorithm.",
        key="CHOICE_ALG_ECLAT",
        label="**Eclat Algorithm**",
        value=False,
    )

    CHOICE_ALG_FPGROWTH = st.sidebar.checkbox(
        disabled=True,
        help="Use the FP-Growth Algorithm.",
        key="CHOICE_ALG_FPGROWTH",
        label="**FP-Growth Algorithm**",
        value=False,
    )

    if CHOICE_ALG_APRIORI:
        CHOICE_ALG_MIN_SUPPORT = st.sidebar.number_input(
            help="""
A decimal value 0 and 1 for minimum support of the itemsets returned.
The support is computed as the fraction
`transactions_where_item(s)_occur / total_transactions`.
            """,
            key="CHOICE_ALG_MIN_SUPPORT",
            label="Minimum support",
            max_value=1.00,
            min_value=0.01,
            value=0.50,
        )
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
            label="Metric",
            options=[
                "confidence",
                "conviction",
                "leverage",
                "lift",
                "support",
                "zhangs_metric",
            ],
        )
        CHOICE_ALG_MIN_THRESHOLD = st.sidebar.number_input(
            help="""
Minimal threshold for the evaluation metric,
via the `metric` parameter,
to decide whether a candidate rule is of interest.
            """,
            key="CHOICE_ALG_MIN_THRESHOLD",
            label="Minimum threshold",
            max_value=1.00,
            min_value=0.01,
            value=0.80,
        )

    st.sidebar.markdown("""---""")

    CHOICE_RAW_DATA_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed raw data.",
        key="CHOICE_RAW_DATA_DETAILS",
        label="**Show Detailed Raw Data**",
        value=False,
    )

    if CHOICE_RAW_DATA_DETAILS:
        CHOICE_RAW_DATA_PROFILE = st.sidebar.checkbox(
            help="Profiling of the filtered raw dataset.",
            key="CHOICE_RAW_DATA_PROFILE",
            label="**Show Raw Data Profile**",
            value=False,
        )

        if CHOICE_RAW_DATA_PROFILE:
            CHOICE_RAW_DATA_PROFILE_TYPE = st.sidebar.radio(
                help="explorative: thorough but also slow - minimal: minimal but faster.",
                index=1,
                key="CHOICE_RAW_DATA_PROFILE_TYPE",
                label="Data profile type",
                options=(
                    [
                        "explorative",
                        "minimal",
                    ]
                ),
            )

    CHOICE_TRANSACTION_DATA_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the filtered detailed transaction data.",
        key="CHOICE_TRANSACTION_DATA_DETAILS",
        label="**Show Detailed Transaction Data**",
        value=False,
    )

    if CHOICE_ALG_APRIORI:
        CHOICE_ONE_HOT_ENCODED_DETAILS = st.sidebar.checkbox(
            help="Tabular representation of the one-hot encoded data.",
            key="CHOICE_ONE_HOT_ENCODED_DETAILS",
            label="**Show Detailed One-Hot Encoded Data**",
            value=False,
        )

        CHOICE_FREQUENT_ITEMSETS_DETAILS = st.sidebar.checkbox(
            help="Tabular representation of the frequent itemsets.",
            key="CHOICE_FREQUENT_ITEMSETS_DETAILS",
            label="**Show Frequent Itemsets**",
            value=True,
        )

        CHOICE_RULES_DETAILS = st.sidebar.checkbox(
            help="Tabular representation of the association rules.",
            key="CHOICE_RULES_DETAILS",
            label="**Show Association Rules**",
            value=True,
        )

        st.sidebar.markdown("""---""")


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
# Execute a query that creates the list of category codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_category():
    global MD_CODES_CATEGORY  # pylint: disable=global-statement

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

        MD_CODES_CATEGORY = {}

        for row in cur:
            (category_code, description) = row
            MD_CODES_CATEGORY[category_code] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of eventsoe codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_eventsoe():
    global MD_CODES_EVENTSOE  # pylint: disable=global-statement

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

        MD_CODES_EVENTSOE = {}

        for row in cur:
            (eventsoe_code, description) = row
            MD_CODES_EVENTSOE[eventsoe_code] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of modifier codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_modifier():
    global MD_CODES_MODIFIER  # pylint: disable=global-statement

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

        MD_CODES_MODIFIER = {}

        for row in cur:
            (modifier_code, description) = row
            MD_CODES_MODIFIER[modifier_code] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of phase codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_phase():
    global MD_CODES_PHASE  # pylint: disable=global-statement

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

        MD_CODES_PHASE = {}

        for row in cur:
            (phase_code, description) = row
            MD_CODES_PHASE[phase_code] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of section codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_section():
    global MD_CODES_SECTION  # pylint: disable=global-statement

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

        MD_CODES_SECTION = {}

        for row in cur:
            (category_code, subcategory_code, section_code, description) = row
            MD_CODES_SECTION[
                category_code + subcategory_code + section_code
            ] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of subcategory codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_subcategory():
    global MD_CODES_SUBCATEGORY  # pylint: disable=global-statement

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

        MD_CODES_SUBCATEGORY = {}

        for row in cur:
            (category_code, subcategory_code, description) = row
            MD_CODES_SUBCATEGORY[category_code + subcategory_code] = description


# ------------------------------------------------------------------
# Execute a query that creates the list of subsection codes.
# ------------------------------------------------------------------
# @st.cache_data
def _sql_query_codes_subsection():
    global MD_CODES_SUBSECTION  # pylint: disable=global-statement

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

        MD_CODES_SUBSECTION = {}

        for row in cur:
            (
                category_code,
                subcategory_code,
                section_code,
                subsection_code,
                description,
            ) = row
            MD_CODES_SUBSECTION[
                category_code + subcategory_code + section_code + subsection_code
            ] = description


# ------------------------------------------------------------------
# Execute a query that returns the list of injury levels
# ------------------------------------------------------------------
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
def _sql_query_ev_type() -> list[str]:
    with PG_CONN.cursor() as cur:  # type: ignore
        # pylint: disable=line-too-long
        # flake8: noqa: E501
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
# Execute a query that returns the list of US states.
# ------------------------------------------------------------------
def _sql_query_us_states() -> list[str]:
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
    global DF_RAW_DATA_FILTERED  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement
    global START_TIME  # pylint: disable=global-statement
    global DF_RAW_DATA_UNFILTERED  # pylint: disable=global-statement

    # Start time measurement.
    START_TIME = time.time_ns()

    # flake8: noqa: E501
    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Favicon.ico?raw=true",
        page_title="slara by IO-Aero",
    )
    # st.sidebar.markdown("[IO-Aero Website](%s)" % "https://www.io-aero.com")

    PG_CONN = _get_postgres_connection()
    _print_timestamp("_setup_filter - got DB connection")

    _setup_sidebar()
    _print_timestamp("_setup_sidebar()")

    _setup_page()
    _print_timestamp("_setup_page()")

    _sql_query_codes_category()
    _sql_query_codes_eventsoe()
    _sql_query_codes_modifier()
    _sql_query_codes_phase()
    _sql_query_codes_section()
    _sql_query_codes_subcategory()
    _sql_query_codes_subsection()

    DF_RAW_DATA_UNFILTERED = _get_raw_data()
    DF_RAW_DATA_FILTERED = DF_RAW_DATA_UNFILTERED
    _print_timestamp("_get_data()")

    if CHOICE_FILTER_DATA:
        DF_RAW_DATA_FILTERED = _apply_filter(
            DF_RAW_DATA_UNFILTERED,
        )
        _print_timestamp("_apply_filter()")

    _present_data()
    _print_timestamp("_present_data()")

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
