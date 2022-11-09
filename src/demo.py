# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""IO-AVSTATS-UI interface."""
import pandas as pd
import streamlit as st

from io_avstats_db import db_utils

# ------------------------------------------------------------------
# Database query.
# ------------------------------------------------------------------

with db_utils.get_postgres_connection() as conn_pg:
    data_df = pd.read_sql_query(
        """
    SELECT
        e.ev_year AS year,
           sum(i.inj_person_count) AS fatalities
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
        """, conn_pg
    )

# ------------------------------------------------------------------
# Creating the diagram.
# ------------------------------------------------------------------

st.subheader("Aviation fatalities in the U.S. per year since 1982")

st.bar_chart(data_df, x="year", y="fatalities")

st.line_chart(data_df, x="year", y="fatalities")

st.area_chart(data_df, x="year", y="fatalities")
