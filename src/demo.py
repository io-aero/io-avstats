# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""IO-AVSTATS-UI interface."""
import pandas as pd
import streamlit as st

from io_avstats_ui import db_utils

# ------------------------------------------------------------------
# Database query.
# ------------------------------------------------------------------

conn_pg, cur_pg = db_utils.get_postgres_cursor()

cur_pg.execute(
    """
SELECT
    e.ev_year AS YEAR,
       sum(i.inj_person_count) AS fatalities
FROM
    injury i
INNER JOIN events e ON
    (i.ev_id = e.ev_id)
WHERE
    e.ev_year >= 1982
    AND e.ev_year < EXTRACT( YEAR FROM CURRENT_DATE )::int
    AND e.ev_country = 'USA'
    AND i.injury_level = 'FATL'
GROUP BY
    e.ev_year
ORDER BY
    e.ev_year;
    """
)

years = []
fatalities = []

for row in cur_pg.fetchall():
    years.append(row[0])
    fatalities.append(row[1])

cur_pg.close()
conn_pg.close()

# ------------------------------------------------------------------
# Preparing the database results.
# ------------------------------------------------------------------

data = {"Year": years, "Fatalities": fatalities}

data_df = pd.DataFrame(data)

# ------------------------------------------------------------------
# Creating the diagram.
# ------------------------------------------------------------------

st.subheader("Aviation fatalities in the U.S. per year since 1982")

st.bar_chart(data_df, x="Year", y="Fatalities")
