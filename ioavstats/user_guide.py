# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Creation of the user guide."""
import streamlit as st

# pylint: disable=line-too-long
# pylint: disable=pointless-string-statement

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats/"


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _generic_footer_section() -> str:
    return ""


# ------------------------------------------------------------------
# Create the generic header section.
# ------------------------------------------------------------------
def _generic_header_section(header: str) -> str:
    return f"""
#### **{header}**

"""


# ------------------------------------------------------------------
# ae1982 - Creates the user guide for the whole application.
# ------------------------------------------------------------------
def get_ae1982_app() -> None:
    """ae1982 - Creates the user guide for the whole application."""
    # """
    # ...
    # """
    user_guide = (
        _generic_header_section("User Guide 'Application'")
        + """
#### Coming soon ...
"""
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# ae1982 - Creates the user guide for bar charts.
# ------------------------------------------------------------------
def get_ae1982_bar_chart(
    chart_id: str,
    chart_title: str,
) -> None:
    """ae1982 - Creates the user guide for bar charts."""
    # """
    # ...
    # """
    user_guide = (
        _generic_header_section(f"User Guide 'Bar chart {chart_id}'")
        + f"""
{chart_title}
#### Coming soon ...
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# pd1982 - Creates the user guide for the whole application.
# ------------------------------------------------------------------
def get_pd1982_app() -> None:
    """pd1982 - Creates the user guide for the whole application."""
    # """
    # On the one hand, this application provides the data of the tables and views of the **IO-AVSTATS-DB** database in a table format for display and download as **csv** file.
    #
    # On the other hand, it is also possible to perform an exploratory data analysis of individual tables or views using [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) and optionally download the result as a **HTML** file.
    #
    # The **IO-AVSTATS-DB** database is based primarily on air traffic accident data provided by the [NTSB]( https://www.ntsb.gov/Pages/home.aspx) in the form of Microsoft Access databases [here]( https://data.ntsb.gov/avdata).
    #
    # Detailed information on the **`pd1982`** application can be found [here](https://io-aero.github.io/io-avstats/).
    # """
    user_guide = (
        _generic_header_section("User Guide 'Application'")
        + f"""
On the one hand, this application provides the data of the tables and views of the **IO-AVSTATS-DB** database in a table format for display and upload as **csv** file. On the other hand, it is also possible to perform an exploratory data analysis of individual tables or views using [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) and optionally upload the result as a **HTML** file.

The **IO-AVSTATS-DB** database is based primarily on aviation accident data provided by the [NTSB]( https://www.ntsb.gov/Pages/home.aspx) in the form of Microsoft Access databases [here]( https://data.ntsb.gov/avdata).

Detailed information on the **`pd1982`** application can be found [here]({LINK_GITHUB_PAGES}).
"""
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# pd1982 - Creates the user guide for the 'Show data profile' task.
# ------------------------------------------------------------------
def get_pd1982_data_profile() -> None:
    """pd1982 - Creates the user guide for the 'Show data profile' task."""
    # """
    # This task performs a data analysis of the selected table or view.
    # This is carried out with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/).
    # One can select either the explorative or the minimal version.
    # Depending upon the size of the selected table and/or View it can come to delayed response times, whereby the explorative version requires again clearly more computation expenditure than the minimum version.
    # For further explanations please consult the documentation of **Pandas Profiling**.
    # The result of the data analysis can also be downloaded as **HTML** file if desired.
    # """
    user_guide = (
        _generic_header_section("User Guide 'Show data profile'")
        + """
This task performs a data analysis of the selected table or view. This is done with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/). You can select either the explorative or the minimal version. Depending on the size of the selected table or view, there may be delayed response times, with the exploratory version again requiring significantly more computational effort than the minimal version.
For further explanations please consult the documentation of **Pandas Profiling**. The result of the data analysis can also be downloaded as **HTML** file if desired.
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# pd1982 - Creates the user guide for the 'Show details' task.
# ------------------------------------------------------------------
def get_pd1982_details() -> None:
    """pd1982 - Creates the user guide for the 'Show details' task."""
    # This task provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and download as **csv** file.
    #
    # The series to be displayed can be limited to an interval of event years in the filter options.
    # The order of data display is based on the respective primary key of the database table.
    # The database columns of the selected series are always displayed in full.
    # """
    user_guide = (
        _generic_header_section("User Guide 'Show details'")
        + """
This task provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and upload as **csv** file. The rows to be displayed can be limited to an interval of event years in the filter options. The order of data display is based on the respective primary key of the database table. The database columns of the selected rows are always displayed in full.
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)
