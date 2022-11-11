# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""IO-AVSTATS-UI interface."""
import pandas as pd
import streamlit as st

from io_avstats_db import db_utils  # type: ignore  # pylint: disable=no-name-in-module

APP_TITLE = "Aviation fatalities in the U.S. since 1982"
APP_SUB_TITLE = "Data source: National Transportation Safety Board"


# ------------------------------------------------------------------
# Streamlit application.
# ------------------------------------------------------------------
def main():
    st.set_page_config(APP_TITLE)

    st.subheader("Aviation fatalities in the U.S. per year since 1982")
    st.caption(APP_SUB_TITLE)

    # ------------------------------------------------------------------
    # Load data.
    # ------------------------------------------------------------------
    data_df = get_data()

    st.write(data_df)

    # ------------------------------------------------------------------
    # Creating the diagram.
    # ------------------------------------------------------------------

    st.bar_chart(data_df, x="Year", y="Fatalities")

    st.line_chart(data_df, x="Year", y="Fatalities")

    st.area_chart(data_df, x="Year", y="Fatalities")


# ------------------------------------------------------------------
# Load data.
# ------------------------------------------------------------------
def get_data():
    with db_utils.get_postgres_connection() as conn_pg:
        data_df = pd.read_sql_query(
            """
        SELECT
            e.ev_year AS "Year",
               sum(i.inj_person_count) AS "Fatalities"
        FROM
            injury i
        INNER JOIN events e ON
            (i.ev_id = e.ev_id)
        WHERE
            e.ev_year >= 1982
            AND e.ev_year < EXTRACT( YEAR FROM CURRENT_DATE )::int
            AND e.ev_country = 'USA'
            AND i.inj_person_category <> 'ABRD'
            AND i.injury_level = 'FATL'
        GROUP BY
            e.ev_year
        ORDER BY
            e.ev_year;
            """,
            conn_pg,
        )

    return data_df


# ------------------------------------------------------------------
# Entry point.
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()