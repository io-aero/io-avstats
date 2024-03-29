# noqa: N999

# pylint: disable=invalid-name
# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""IO-Aero Menu."""
import os
import shutil

import streamlit as st
from streamlit.file_util import get_streamlit_file_path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

credential_path = get_streamlit_file_path("credentials.toml")
if not os.path.exists(credential_path):
    os.makedirs(os.path.dirname(credential_path), exist_ok=True)
    shutil.copyfile(
        os.path.join(PROJECT_ROOT, ".streamlit\\credentials.toml"),
        credential_path,
    )

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
