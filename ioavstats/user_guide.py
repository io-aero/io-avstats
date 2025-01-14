# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Creation of the user guide."""
import streamlit as st

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats/"


# -----------------------------------------------------------------------------

def _generic_footer_section() -> str:
    """Create the generic footer section.

    Returns
    -------
    str
        The generic footer section.

    """
    return ""


# -----------------------------------------------------------------------------

def _generic_header_section(header: str) -> str:
    """Create the generic header section.

    Parameters
    ----------
    header : str
        The header text.

    Returns
    -------
    str
        The generic header section.

    """
    return f"""
#### **{header}**

"""


# -----------------------------------------------------------------------------

def get_ae1982_app() -> None:
    """Create the user guide for the whole application.

    This user guide is displayed when the user navigates to the 'Application' page.

    """
    # """
    # The user guide is a simple text that is displayed with a warning.
    # """
    user_guide = (
        _generic_header_section("User Guide 'Application'")
        + """
#### Coming soon ...
"""
        + _generic_footer_section()
    )

    # Display the user guide with a warning.
    st.warning(user_guide)


# -----------------------------------------------------------------------------

def get_ae1982_bar_chart(
    chart_id: str,
    chart_title: str,
) -> None:
    """ae1982 - Creates the user guide for bar charts.

    This function generates the user guide for bar charts.
    The user guide is divided into two parts:
    1. A detailed description of the bar chart.
    """
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


# -----------------------------------------------------------------------------

def get_pd1982_app() -> None:
    """Create the user guide for the whole application.

    This function generates the user guide for the whole application.
    The user guide is divided into two parts:
    1. A detailed description of the application.
    2. A link to the GitHub page where the user can find more information.

    """
    user_guide = (
        _generic_header_section("User Guide 'Application'")
        + """
This application provides the data of the tables and views of the **IO-AVSTATS-DB** database in a table format for display and upload as **csv** file. On the other hand, it is also possible to perform an exploratory data analysis of individual tables or views using [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) and optionally upload the result as a **HTML** file.
The **IO-AVSTATS-DB** database is based primarily on aviation accident data provided by the [NTSB]( https://www.ntsb.gov/Pages/home.aspx) in the form of Microsoft Access databases [here]( https://data.ntsb.gov/avdata).
"""
        + f"""
Detailed information on the **`pd1982`** application can be found [here]({LINK_GITHUB_PAGES}).
"""
        + _generic_footer_section()
    )

    st.warning(user_guide)


# -----------------------------------------------------------------------------

def get_pd1982_data_profile() -> None:
    """Create the user guide for the 'Show data profile' task.

    This task performs a data analysis of the selected table or view.
    This is carried out with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/).

    The task provides two versions of the data analysis:
    1. An explorative version that requires more computational effort than the minimal version.
    2. A minimal version that requires less computational effort than the explorative version.

    Depending upon the size of the selected table and/or View it can come to delayed response times.

    The result of the data analysis can also be downloaded as **HTML** file if desired.

    """
    user_guide = (
        _generic_header_section("User Guide 'Show data profile'")
        + """
This task performs a data analysis of the selected table or view.
This is done with the help of [**Pandas Profiling**](https://pandas-profiling.ydata.ai/docs/master/).
The task provides two versions of the data analysis:
1. An explorative version that requires more computational effort than the minimal version.
2. A minimal version that requires less computational effort than the explorative version.
Depending on the size of the selected table or view, there may be delayed response times.
The result of the data analysis can also be downloaded as **HTML** file if desired.
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)


# -----------------------------------------------------------------------------

def get_pd1982_details() -> None:
    """Create the user guide for the 'Show details' task.

    This function generates the user guide for the 'Show details' task.
    The user guide is divided into two parts:
    1. A detailed description of the task.
    2. A footer with links to the GitHub page and the IO-Aero website.

    The task provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and download as **csv** file.
    The series to be displayed can be limited to an interval of event years in the filter options.
    The order of data display is based on the respective primary key of the database table.
    The database columns of the selected series are always displayed in full.

    """
    user_guide = (
        _generic_header_section("User Guide 'Show details'")
        + """
This task provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and upload as **csv** file.
The rows to be displayed can be limited to an interval of event years in the filter options.
The order of data display is based on the respective primary key of the database table.
The database columns of the selected rows are always displayed in full.
"""
        + _generic_footer_section()
    )

    st.warning(user_guide)
