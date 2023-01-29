# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Creation of the user guide."""
import streamlit as st

# flake8: noqa
# pylint: disable=line-too-long
# pylint: disable=pointless-string-statement

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"


# ------------------------------------------------------------------
# Create the generic footer section.
# ------------------------------------------------------------------
def _generic_footer_section() -> str:
    """Create the generic footer section.

    Returns:
        str: Generated footer section.
    """
    return ""


# ------------------------------------------------------------------
# Create the generic header section.
# ------------------------------------------------------------------
def _generic_header_section(header: str) -> str:
    """Create the generic header section.

    Args:
        header (str): Header.

    Returns:
        str: Generated header section.
    """
    return f"""
#### **{header}**

"""


# ------------------------------------------------------------------
# ae1982 - Create the application user guide. .
# ------------------------------------------------------------------
def get_ae1982_app() -> str:
    """ae1982 - Create the application user guide.

    Returns:
        str: User guide.
    """
    return """
---

#### **User Guide Application**

Der populistische Ex-Regierungschef

---
"""


# ------------------------------------------------------------------
# ae1982 - Create the application user guide. .
# ------------------------------------------------------------------
def get_ae1982_chart() -> str:
    """ae1982 - Create the chart user guide.

    Returns:
        str: User guide.
    """
    return """
---

#### **User Guide Chart**

Der populistische Ex-Regierungschef

---
"""


# ------------------------------------------------------------------
# pd1982 - Create the application user guide. .
# ------------------------------------------------------------------
def get_pd1982_app() -> None:
    """pd1982 - Create the application user guide."""
    """Diese Anwendung stellt zum einen die Daten der Tabellen und Views der
    Datenbank **IO-AVSTATS-DB** in einem Tabellenformat zur Anzeige und zum
    Herunterladen als **`csv`** Datei zur Verfügung.

    Zum anderen ist es auch möglich eine explorative Datenanalyse von einzelnen Tabellen oder Views mithilfe von [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) durchzuführen und das Ergebnis wahlweise als **`HTML`** Datei herunterzuladen.

    Die Datenbank **IO-AVSTATS-DB** beruht hauptsachlich auf den von der [NTSB]( https://www.ntsb.gov/Pages/home.aspx) in Form von Microsoft Access Datenbanken [hier]( https://data.ntsb.gov/avdata) zur Verfügung gestellten Flugverkehrsunfallzahlen.

    Detaillierte Informationen zur Anwendung **`pd1982`** finden sich [hier](https://io-aero.github.io/io-avstats-shared/).
    """
    user_guide = (
        _generic_header_section("User Guide Application `pd1982`")
        + f"""
On the one hand, this application provides the data of the tables and views of the **IO-AVSTATS-DB** database in a table format for display and download as **`csv`** file.

On the other hand, it is also possible to perform an exploratory data analysis of individual tables or views using [Pandas Profiling](https://pandas-profiling.ydata.ai/docs/master/) and optionally download the result as a **`HTML`** file.

The **IO-AVSTATS-DB** database is based primarily on aviation accident data provided by the [NTSB]( https://www.ntsb.gov/Pages/home.aspx) in the form of Microsoft Access databases [here]( https://data.ntsb.gov/avdata).

Detailed information on the **`pd1982`** application can be found [here]({LINK_GITHUB_PAGES}).
"""
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# pd1982 - Create the data profile user guide. .
# ------------------------------------------------------------------
def get_pd1982_data_profile() -> None:
    """pd1982 - Create the data profile user guide."""
    user_guide = (
        _generic_header_section("User Guide Profiling")
        + """
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)


# ------------------------------------------------------------------
# pd1982 - Create the details user guide. .
# ------------------------------------------------------------------
def get_pd1982_details() -> None:
    """pd1982 - Create the details user guide."""
    """Diese Anwendung stellt die Daten der Tabellen und Views der Datenbank.

    **IO-AVSTATS-DB** in einem Tabellenformat zur Anzeige und zum Herunterladen
    als **`csv`** Datei zur Verfügung.

    Die anzuzeigenden Reihen können bei den Filteroptionen auf ein
    Intervall von Ereignisjahren beschränkt werden. Die Reihenfolge der
    Datenanzeige richtet sich nach dem jeweiligen Primärschlüssel der
    Datenbanktabelle. Die Datenbankspalten der ausgewählten Reihen
    werden immer vollständig angezeigt.
    """
    user_guide = (
        _generic_header_section("User Guide Details")
        + """
This application provides the data of the tables and views of the database **IO-AVSTATS-DB** in a table format for display and download as **`csv`** file.
The rows to be displayed can be limited to an interval of event years in the filter options.
The order of data display is based on the respective primary key of the database table.
The database columns of the selected rows are always displayed in full.
    """
        + _generic_footer_section()
    )

    st.warning(user_guide)
