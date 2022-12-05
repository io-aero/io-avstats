# Copyright (c) 2022 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

import pandas as pd
import psycopg2
import streamlit as st
from psycopg2.extensions import connection
import datetime
from psycopg2.extensions import cursor
import pandas.io.sql as sqlio

# ------------------------------------------------------------------
# Query regarding the aircraft fatalities in the US since 2008.
# ------------------------------------------------------------------
QUERY = """
    SELECT ev_year "year",
           inj_tot_f fatalities,
           COALESCE(io_state, ev_state) state,
           COALESCE(io_city, ev_city) city,
           COALESCE(io_site_zipcode, ev_site_zipcode) zip,
           COALESCE(io_latitude, latitude) latitude,
           COALESCE(io_dec_latitude, dec_latitude) dec_latitude,
           io_dec_latitude_deviating latitude_deviating,
           COALESCE(io_longitude, longitude) longitude,
           COALESCE(io_dec_longitude, dec_longitude) dec_longitude,
           io_dec_longitude_deviating longitude_deviating,
           io_invalid_latitude invalid_latitude,
           io_invalid_longitude invalid_longitude,
           io_invalid_us_city invalid_us_city,
           io_invalid_us_city_zipcode invalid_us_city_zipcode,
           io_invalid_us_state invalid_us_state,
           io_invalid_us_zipcode invalid_us_zipcode,
           ev_id event_id,
           ntsb_no,
           io_dec_lat_lng_actions actions
     FROM io_fatalities_us_2008
    ORDER BY ev_id;
"""


# ------------------------------------------------------------------
# Create a PostgreSQL connection.
# ------------------------------------------------------------------
# @st.cache(allow_output_mutation=True,
#           hash_funcs={"_thread.RLock": lambda _: None},
#           show_spinner=True)
def _get_postgres_connection() -> connection:
    return psycopg2.connect(**st.secrets["db_postgres"])


# ------------------------------------------------------------------
# Run a SQL query.
# ------------------------------------------------------------------
def _sql_query(conn:connection, query:str)->list[tuple]:
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


st.set_page_config(layout="wide")
st.header("Fatal Aviation Accidents in the US since 2008")

pg_conn = _get_postgres_connection()

df = sqlio.read_sql_query(QUERY, pg_conn)

filter_states = st.sidebar.text_input(label="Select one or more states",help="xxx")
filter_year_from,filter_year_to = st.sidebar.slider(label="Select a time frame",help="xxx",min_value=2008,max_value=datetime.date.today().year,value=(2008,datetime.date.today().year))
choice_details = st.sidebar.checkbox(label="Show details",help="xxx")

if filter_states:
    df_filtered_states = df.loc[(df["state"].isin(filter_states.upper().split(",")))]
else:
    df_filtered_states = df

if filter_year_from or filter_year_to:
    df_filtered = df_filtered_states.loc[(df["year"] >= filter_year_from )&(df["year"]<=filter_year_to)]
else:
    df_filtered = df_filtered_states

if choice_details:
    st.dataframe(df_filtered)

