import streamlit as st

st.set_page_config(
    layout="wide",
    # pylint: disable=line-too-long
    page_icon="https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Favicon.ico?raw=true",
    page_title="Aviation Events Statistics by IO-Aero",
)

st.write("# Welcome to IO-AVSTATS!")

st.sidebar.markdown("##  [IO-Aero Website](https://www.io-aero.com)")

# pylint: disable=line-too-long
st.sidebar.image(
    "https://github.com/io-aero/io-avstats/blob/main/resources/Images/IO-Aero_1_Logo.png?raw=true",
    width=200,
)

st.sidebar.success("Select an application above.")

st.markdown(
    """
    The IO-AVSTATS-DB database contains not only the NTSB's aviation accident data, but also a large number of supplementary data from a wide variety of data sources. 
    To enable the most comprehensive analysis of this data, IO-Aero provides the following applications as tools:
    - **`ae1982`** - **Association Rule Analysis**: to apply various association rule algorithms to selected aspects of event causes, such as phase of flight or cause of accident, and more,
    - **`pd1982`** - **Aviation Event Analysis**: allows detailed analysis of selectable event data using data profiling, maps, various chart types and more,
    - **`slara`** - **Database Profiling**: allows exploratory data analysis of all tables and views in the database IO-AVSTATS-DB.
"""
)