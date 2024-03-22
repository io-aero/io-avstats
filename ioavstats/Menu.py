# noqa: N999

# pylint: disable=invalid-name
# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""IO-Aero Menu."""
import streamlit as st

# flake8: noqa: E501
st.set_page_config(
    layout="wide",
    # pylint: disable=line-too-long
    page_icon="https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Favicon.ico?raw=true",
    page_title="Aviation Events Statistics by IO-Aero",
)

st.write("# Welcome to IO-AVSTATS!")

col1, col2 = st.sidebar.columns(2)
# pylint: disable=line-too-long
col1.image(
    "https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Logo.png?raw=true",
    width=150,
)
col2.markdown("##  [IO-Aero Website](https://www.io-aero.com)")

st.sidebar.success("Select an application above.")

st.markdown(
    """
    The IO-AVSTATS-DB database contains not only the NTSB's aviation accident data,
    but also a large number of supplementary data from a wide variety of data sources.
    To enable the most comprehensive analysis of this data, IO-Aero provides the
    following applications as tools:
    - **Association Rule Analysis**: to apply various association rule algorithms
      to selected aspects of event causes, such as phase of flight or cause of accident,
      and more,
    - **Aviation Event Analysis**: allows detailed analysis of selectable event data
      using data profiling, maps, various chart types and more,
    - **Database Profiling**: allows exploratory data analysis of all tables and
      views in the database IO-AVSTATS-DB.
""",
)
