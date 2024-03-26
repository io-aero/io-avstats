# noqa: N999
# pylint: disable=invalid-name

# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Database Profiling."""
import datetime
import time

import pandas as pd
import streamlit as st
import utils  # type: ignore  # pylint: disable=import-error
from dynaconf import Dynaconf  # type: ignore
from pandas import DataFrame
from psycopg import Connection
from streamlit_pandas_profiling import st_profile_report  # type: ignore
from ydata_profiling import ProfileReport  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "pd1982"

# pylint: disable=R0801
CHOICE_ABOUT: bool | None = None
CHOICE_ACTIVE_FILTERS: bool | None = None
CHOICE_ACTIVE_FILTERS_TEXT: str = ""
CHOICE_DATA_PROFILE: bool | None = None
CHOICE_DDL_OBJECT_SELECTED: str = ""
CHOICE_DDL_OBJECT_SELECTION: str = ""
CHOICE_DETAILS: bool | None = None
CHOICE_FILTER_DATA: bool | None = None
CHOICE_UG_APP: bool | None = None
CHOICE_UG_DATA_PROFILE: bool | None = None
CHOICE_UG_DETAILS: bool | None = None

COLOR_HEADER: str = "#357f8f"

DF_FILTERED: DataFrame = DataFrame()
DF_FILTERED_ROWS = 0
DF_UNFILTERED: DataFrame = DataFrame()
DF_UNFILTERED_ROWS = 0

FILTER_EV_YEAR_FROM: int | None = None
FILTER_EV_YEAR_TO: int | None = None
FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

HOST_CLOUD: bool | None = None

LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats/"

PG_CONN: Connection | None = None

# ------------------------------------------------------------------
# Query data for the US since 1982.
# ------------------------------------------------------------------
QUERIES = {
    "aircraft": """
        SELECT a.*,
               e.ev_year
          FROM aircraft a
          LEFT OUTER JOIN events e
            ON (a.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY a.ev_id,
                 a.aircraft_key;
    """,
    "dt_aircraft": """
        SELECT d.*,
               e.ev_year
          FROM dt_aircraft d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.col_name,
                 d.code;
    """,
    "dt_events": """
        SELECT d.*,
               e.ev_year
          FROM dt_events d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.col_name,
                 d.code;
    """,
    "dt_flight_crew": """
        SELECT d.*,
               e.ev_year
          FROM dt_flight_crew d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.crew_no,
                 d.col_name,
                 d.code;
    """,
    "engines": """
        SELECT d.*,
               e.ev_year
          FROM engines d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.eng_no;
    """,
    "events": """
        SELECT *
          FROM events
         WHERE ev_year >= 1982
         ORDER BY ev_id;
    """,
    "events_sequence": """
        SELECT d.*,
               e.ev_year
          FROM events_sequence d
          LEFT OUTER JOIN events e
            ON (d.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY d.ev_id,
                 d.aircraft_key,
                 d.occurrence_no;
    """,
    "findings": """
        SELECT f.*,
               e.ev_year
          FROM findings f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.finding_no;
    """,
    "flight_crew": """
        SELECT f.*,
               e.ev_year
          FROM flight_crew f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.crew_no;
    """,
    "flight_time": """
        SELECT f.*,
               e.ev_year
          FROM flight_time f
          LEFT OUTER JOIN events e
            ON (f.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY f.ev_id,
                 f.aircraft_key,
                 f.crew_no,
                 f.flight_type,
                 f.flight_craft;
    """,
    "injury": """
        SELECT i.*,
               e.ev_year
          FROM injury i
          LEFT OUTER JOIN events e
            ON (i.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY i.ev_id,
                 i.aircraft_key,
                 i.inj_person_category,
                 i.injury_level;
    """,
    "io_airports": """
        SELECT *
          FROM io_airports
        ORDER BY ident;
    """,
    "io_app_ae1982": """
        SELECT *
          FROM io_app_ae1982
        ORDER BY ev_id;
    """,
    "io_aviation_occurrence_categories": """
        SELECT *
          FROM io_aviation_occurrence_categories
         ORDER BY cictt_code;
    """,
    "io_countries": """
        SELECT *
          FROM io_countries
        ORDER BY country;
    """,
    "io_lat_lng": """
        SELECT *
          FROM io_lat_lng
        ORDER BY id;
    """,
    "io_lat_lng_issues": """
        SELECT l.*,
               e.ev_year
          FROM io_lat_lng_issues l
          LEFT OUTER JOIN events e
            ON (l.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY l.ev_id;
    """,
    "io_md_codes_category": """
        SELECT *
          FROM io_md_codes_category
        ORDER BY category_code;
    """,
    "io_md_codes_eventsoe": """
        SELECT *
          FROM io_md_codes_eventsoe
        ORDER BY eventsoe_code;
    """,
    "io_md_codes_modifier": """
        SELECT *
          FROM io_md_codes_modifier
        ORDER BY modifier_code;
    """,
    "io_md_codes_phase": """
        SELECT *
          FROM io_md_codes_phase
        ORDER BY phase_code;
    """,
    "io_md_codes_section": """
        SELECT *
          FROM io_md_codes_section
        ORDER BY category_code,
                 subcategory_code,
                 section_code;
    """,
    "io_md_codes_subcategory": """
        SELECT *
          FROM io_md_codes_subcategory
        ORDER BY category_code,
                 subcategory_code;
    """,
    "io_md_codes_subsection": """
        SELECT *
          FROM io_md_codes_subsection
        ORDER BY category_code,
                 subcategory_code,
                 section_code,
                 subsection_code;
    """,
    "io_processed_files": """
        SELECT *
          FROM io_processed_files
        ORDER BY COALESCE(last_processed, first_processed) DESC;
    """,
    "io_sequence_of_events": """
        SELECT *
          FROM io_sequence_of_events
        ORDER BY soe_no;
    """,
    "io_states": """
        SELECT *
          FROM io_states
        ORDER BY country,
                 state;
    """,
    "narratives": """
        SELECT n.*,
               e.ev_year
          FROM narratives n
          LEFT OUTER JOIN events e
            ON (n.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY n.ev_id,
                 n.aircraft_key;
    """,
    "ntsb_admin": """
        SELECT n.*,
               e.ev_year
          FROM ntsb_admin n
          LEFT OUTER JOIN events e
            ON (n.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY n.ev_id;
    """,
    "occurrences": """
        SELECT o.*,
               e.ev_year
          FROM occurrences o
          LEFT OUTER JOIN events e
            ON (o.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY o.ev_id,
                 o.aircraft_key,
                 o.occurrence_no;
    """,
    "seq_of_events": """
        SELECT s.*,
               e.ev_year
          FROM seq_of_events s
          LEFT OUTER JOIN events e
            ON (s.ev_id = e.ev_id)
        WHERE e.ev_year >= 1982
        ORDER BY s.ev_id,
                 s.aircraft_key,
                 s.occurrence_no,
                 s.seq_event_no,
                 s.group_code;
    """,
}

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AERO",
    settings_files=["settings.io_aero.toml"],
)


# ------------------------------------------------------------------
# Filter the data frame.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
def _apply_filter_controls(
    df_unfiltered: DataFrame,
) -> DataFrame:
    df_filtered = df_unfiltered

    # noinspection PyUnboundLocalVariable
    if FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO:
        df_filtered = df_filtered.loc[
            (df_filtered["ev_year"] >= FILTER_EV_YEAR_FROM)
            & (df_filtered["ev_year"] <= FILTER_EV_YEAR_TO)
        ]

    return df_filtered


# ------------------------------------------------------------------
# Convert a dataframe to csv data.
# ------------------------------------------------------------------
def _convert_df_2_csv(dataframe: DataFrame) -> bytes:
    return dataframe.to_csv().encode("utf-8")


# ------------------------------------------------------------------
# Read the data.
# ------------------------------------------------------------------
def _get_data(ddl_object_name: str) -> DataFrame:
    return pd.read_sql(QUERIES[ddl_object_name], con=utils.get_engine(SETTINGS))  # type: ignore


# ------------------------------------------------------------------
# Creates the user guide for the whole application.
# ------------------------------------------------------------------
def _get_user_guide_app() -> None:
    text = f"""
#### User guide: pd1982 Application

On the one hand, this application provides the data of the tables and views of the **IO-AVSTATS-DB** database in a
table format for display and upload as **csv** file.
On the other hand, it is also possible to perform an exploratory data analysis of individual tables or views using
[Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) and optionally upload the result as a **HTML** file.

The **IO-AVSTATS-DB** database is based primarily on aviation accident data provided by the
[NTSB]( https://www.ntsb.gov/Pages/home.aspx) in the form of Microsoft Access databases [here]( https://data.ntsb.gov/avdata).

Further information on the **`pd1982`** application can be found [here]({LINK_GITHUB_PAGES}).
"""

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show data profile' task.
# ------------------------------------------------------------------
def _get_user_guide_data_profile() -> None:
    text = """
#### User guide: Show data profile

This task performs a data analysis of the selected table or view. This is done with the help of
[**ydata-profiling**](https://pandas-profiling.ydata.ai/docs/master/).
Depending on the size of the selected table or view, there may be delayed response times, with the exploratory version
again requiring significantly more computational effort than the minimal version.
For further explanations please consult the documentation of **Pandas Profiling**.
The result of the data analysis can also be downloaded as **HTML** file if desired.


If you encounter any problem in the application, documentation or data, we would appreciate it if you would notify us
[here](https://github.com/io-aero/io-avstats/issues) so that we can make any necessary correction.
Also suggestions for improvement or enhancements are welcome.
    """

    st.warning(text)


# ------------------------------------------------------------------
# Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def _get_user_guide_details() -> None:
    text = """
#### User guide: Show details

This task provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and
upload as **csv** file.
The rows to be displayed can be limited to an interval of event years in the filter options.
The order of data display is based on the respective primary key of the database table.
The database columns of the selected rows are always displayed in full.
    """

    st.warning(text)


# ------------------------------------------------------------------
# Present the filtered data.
# ------------------------------------------------------------------
def _present_data() -> None:
    global CHOICE_UG_DETAILS  # pylint: disable=global-statement
    global CHOICE_UG_DATA_PROFILE  # pylint: disable=global-statement
    global DF_FILTERED_ROWS  # pylint: disable=global-statement
    global DF_UNFILTERED_ROWS  # pylint: disable=global-statement

    if CHOICE_ACTIVE_FILTERS:
        st.warning(CHOICE_ACTIVE_FILTERS_TEXT)

    if CHOICE_ABOUT:
        _col1, col2 = st.columns(
            [
                1,
                2,
            ],
        )
        with col2:
            utils.present_about(PG_CONN, APP_ID)

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

    if CHOICE_DATA_PROFILE:
        col1, col2 = st.columns(
            [
                2,
                1,
            ],
        )

        with col1:
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                'font-weight: normal;border-radius:2%;">Profiling Database '
                f"{CHOICE_DDL_OBJECT_SELECTED} {CHOICE_DDL_OBJECT_SELECTION}</p>",
                unsafe_allow_html=True,
            )

        with col2:
            CHOICE_UG_DATA_PROFILE = st.checkbox(
                help="Explanations and operating instructions related to profiling "
                "of the database tables or views.",
                label="**User Guide: Show data profile**",
                value=False,
            )

        if CHOICE_UG_DATA_PROFILE:
            _get_user_guide_data_profile()

        _present_data_data_profile()

    if CHOICE_DETAILS:
        col1, col2 = st.columns(
            [
                2,
                1,
            ],
        )

        with col1:
            st.markdown(
                f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_SUBHEADER}px;'
                'font-weight: normal;border-radius:2%;">Detailed Database '
                f"{CHOICE_DDL_OBJECT_SELECTED} {CHOICE_DDL_OBJECT_SELECTION}</p>",
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

        st.write(
            f"No rows unfiltered: {DF_UNFILTERED_ROWS} - filtered: {DF_FILTERED_ROWS}",
        )

        st.dataframe(DF_FILTERED)

        st.download_button(
            data=_convert_df_2_csv(DF_FILTERED),
            file_name=APP_ID + "_" + CHOICE_DDL_OBJECT_SELECTION + ".csv",
            help="The upload includes all data of the selected "
            f"{CHOICE_DDL_OBJECT_SELECTED.lower()} after applying the filter options.",
            label="Download all data as CSV file",
            mime="text/csv",
        )


# ------------------------------------------------------------------
# Present the data profile.
# ------------------------------------------------------------------
def _present_data_data_profile() -> None:
    # noinspection PyUnboundLocalVariable
    profile_report = ProfileReport(
        DF_FILTERED,
        minimal=True,
    )

    st_profile_report(profile_report)

    st.download_button(
        data=profile_report.to_html(),
        file_name=APP_ID + ".html",
        help="The upload includes a profile report from the dataframe "
        "after applying the filter options.",
        label="Download the profile report",
        mime="text/html",
    )


# ------------------------------------------------------------------
# Set up the filter controls.
# ------------------------------------------------------------------
def _setup_filter_controls() -> None:
    global CHOICE_ACTIVE_FILTERS_TEXT  # pylint: disable=global-statement
    global CHOICE_FILTER_DATA  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement

    CHOICE_FILTER_DATA = st.sidebar.checkbox(
        help="""
        The following filter options can be used to limit the data to be processed.
        """,
        label="**Filter data ?**",
        value=True,
    )

    if not CHOICE_FILTER_DATA:
        return

    CHOICE_ACTIVE_FILTERS_TEXT = ""

    FILTER_EV_YEAR_FROM, FILTER_EV_YEAR_TO = st.sidebar.slider(
        help="""
            - **`1982`** is the first year with complete statistics.
            - **`2008`** changes were made to the data collection mode.
            """,
        label="**Event year(s):**",
        min_value=1982,
        max_value=datetime.datetime.now(datetime.timezone.utc).year,
        value=(2008, datetime.datetime.now(datetime.timezone.utc).year - 1),
    )

    if FILTER_EV_YEAR_FROM or FILTER_EV_YEAR_TO:
        # pylint: disable=line-too-long
        CHOICE_ACTIVE_FILTERS_TEXT = (
            CHOICE_ACTIVE_FILTERS_TEXT
            + f"\n- **Event year(s)**: between **`{FILTER_EV_YEAR_FROM}`** and **`{FILTER_EV_YEAR_TO}`**"
        )

    st.sidebar.divider()


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page() -> None:
    global CHOICE_ABOUT  # pylint: disable=global-statement
    global CHOICE_ACTIVE_FILTERS  # pylint: disable=global-statement
    global CHOICE_UG_APP  # pylint: disable=global-statement
    global FILTER_EV_YEAR_FROM  # pylint: disable=global-statement
    global FILTER_EV_YEAR_TO  # pylint: disable=global-statement

    FILTER_EV_YEAR_FROM = FILTER_EV_YEAR_FROM if FILTER_EV_YEAR_FROM else 1982
    FILTER_EV_YEAR_TO = (
        FILTER_EV_YEAR_TO
        if FILTER_EV_YEAR_TO
        else datetime.datetime.now(datetime.timezone.utc).year - 1
    )

    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        'font-weight: normal;border-radius:2%;">Database Profiling - Year '
        f"{FILTER_EV_YEAR_FROM} until {FILTER_EV_YEAR_TO}</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(
        [
            1,
            1,
            1,
        ],
    )

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
    _setup_task_controls()
    _setup_filter_controls()


# ------------------------------------------------------------------
# Set up the task controls.
# ------------------------------------------------------------------
def _setup_task_controls() -> None:
    global CHOICE_DDL_OBJECT_SELECTED  # pylint: disable=global-statement
    global CHOICE_DDL_OBJECT_SELECTION  # pylint: disable=global-statement
    global CHOICE_DETAILS  # pylint: disable=global-statement
    global CHOICE_DATA_PROFILE  # pylint: disable=global-statement

    CHOICE_DATA_PROFILE = st.sidebar.checkbox(
        help="Pandas profiling of the dataset.",
        label="**Show data profile**",
        value=False,
    )

    st.sidebar.divider()

    CHOICE_DETAILS = st.sidebar.checkbox(
        help="Tabular representation of the selected detailed data.",
        label="**Show details**",
        value=False,
    )

    st.sidebar.divider()

    CHOICE_DDL_OBJECT_SELECTION = st.sidebar.radio(  # type: ignore
        help="Available database tables and views for profiling.",
        label="**Database tables and views**",
        options=(QUERIES.keys()),
    )

    CHOICE_DDL_OBJECT_SELECTED = (
        "View"
        if CHOICE_DDL_OBJECT_SELECTION
        in [
            "io_app_ae1982",
            "io_lat_long_issues",
        ]
        else "Table"
    )

    st.sidebar.divider()


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
def _streamlit_flow() -> None:
    global DF_FILTERED  # pylint: disable=global-statement
    global DF_UNFILTERED  # pylint: disable=global-statement
    global HOST_CLOUD  # pylint: disable=global-statement
    global PG_CONN  # pylint: disable=global-statement

    # Start time measurement.
    start_time = time.time_ns()

    if "HOST_CLOUD" in st.session_state:
        HOST_CLOUD = st.session_state["HOST_CLOUD"]
    else:
        host = utils.get_args()
        HOST_CLOUD = bool(host == "Cloud")
        st.session_state["HOST_CLOUD"] = HOST_CLOUD

    st.set_page_config(
        layout="wide",
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Favicon.ico?raw=true",
        page_title="pd1982 by IO-Aero",
    )

    col1, col2 = st.sidebar.columns(2)
    # pylint: disable=line-too-long
    col1.image(
        "https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Logo.png?raw=true",
        width=150,
    )
    col2.markdown("##  [IO-Aero Website](https://www.io-aero.com)")

    PG_CONN = utils.get_postgres_connection()  # type: ignore

    _setup_sidebar()

    _setup_page()

    DF_UNFILTERED = _get_data(CHOICE_DDL_OBJECT_SELECTION)

    DF_FILTERED = DF_UNFILTERED

    if CHOICE_DDL_OBJECT_SELECTION not in [
        "io_airports",
        "io_aviation_occurrence_categories",
        "io_countries",
        "io_lat_lng",
        "io_md_codes_category",
        "io_md_codes_eventsoe",
        "io_md_codes_modifier",
        "io_md_codes_phase",
        "io_md_codes_section",
        "io_md_codes_subcategory",
        "io_md_codes_subsection",
        "io_processed_files",
        "io_sequence_of_events",
        "io_states",
    ]:
        if CHOICE_FILTER_DATA:
            DF_FILTERED = _apply_filter_controls(
                DF_UNFILTERED,
            )

    _present_data()

    # Stop time measurement.
    print(  # noqa: T201
        str(datetime.datetime.now(datetime.timezone.utc))
        + f" {f'{time.time_ns() - start_time:,}':>20} ns - Total runtime for application {APP_ID:<10}",
        flush=True,
    )


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

_streamlit_flow()
