# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Members Only Area."""
import datetime
import pathlib
import socket
import time

import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from streamlit_keycloak import login  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "members"

COLOR_HEADER: str = "#357f8f"

FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

HOST ="cloud" if socket.getfqdn()[-13:] == ".ec2.internal" else "local"

LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"

RESOURCES: dict[str,dict[str,list[str]]] = {}

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
def _setup_page():
    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        + 'font-weight: normal;border-radius:2%;">Members Only Area</p>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------
    # Application menu.
    # --------------------------------------------------------------
    url = "http://" + ("stats.io-aero.com" if HOST == "cloud" else "localhost:8599")
    applications = [("US Aviation Fatal Accidents", f"[stats]({url})")]

    for app_id in ["ae1982", "pd1982", "slara"]:
        if app_id in RESOURCES:
            if app_id == "ae1982":
                url = "http://" + (app_id+".io-aero.com" if HOST == "cloud" else "localhost:8501")
                applications.append(("Aviation Event Analysis", f"[{app_id}]({url})"))
            elif app_id == "pd1982":
                url = "http://" + (app_id+".io-aero.com" if HOST == "cloud" else "localhost:8502")
                applications.append(("Database Profiling", f"[{app_id}]({url})"))
            elif app_id == "slara":
                url = "http://" + (app_id+".io-aero.com" if HOST == "cloud" else "localhost:8503")
                applications.append(("Association Rule Analysis", f"[{app_id}]({url})"))
            else:
                applications.append((
                    "Unknown Application",
                    f"[{app_id}]",
                ))

    if len(applications) > 0:
        applications.sort()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## Applications")
        with col2:
            st.markdown("## Link")

        for app_desc, app_link in applications:
            with col1:
                st.markdown("#### " + app_desc)
            with col2:
                st.markdown("#### " + app_link)

    # --------------------------------------------------------------
    # Download menu.
    # --------------------------------------------------------------
    downloads = []

    for item_id in ["IO-AVSTATS-DB"]:
        if item_id in RESOURCES:
            if item_id == "IO-AVSTATS-DB":
                downloads.append(("IO-AVSTATS-DB Database", "IO-AVSTATS-DB.zip"))
                downloads.append(("IO-AVSTATS-DB Documentation", "IO-AVSTATS-DB.pdf"))
            else:
                downloads.append((
                    "Unknown Download",
                    f"[{item_id}]",
                ))

    if len(downloads) > 0:
        downloads.sort()

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## Downloadable Items")
        with col2:
            st.markdown("## Button")

        for item_desc, item_file in downloads:
            with col1:
                st.markdown("#### " + item_desc)
            with col2:
                with open("download/"+item_file,"rb") as download:
                    st.download_button("**Download "+pathlib.Path(item_file).suffix.upper()[1:]+"**",download,file_name=item_file)


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
def _streamlit_flow() -> None:
    global RESOURCES  # pylint: disable=global-statement

    # Start time measurement.
    start_time = time.time_ns()

    print(
        str(datetime.datetime.now())
        + "                         - Start application "
        + APP_ID,
        flush=True,
    )

    st.set_page_config(
        layout="wide",
        # flake8: noqa: E501
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png",
        page_title="members by IO-Aero",
    )

    st.sidebar.markdown("## [IO-Aero](https://www.io-aero.com)")

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    RESOURCES = utils.has_access(APP_ID)

    _setup_page()

    # Stop time measurement.
    print(
        str(datetime.datetime.now())
        + f" {f'{time.time_ns() - start_time:,}':>20} ns - "
        + "Total runtime for application "
        + APP_ID,
        flush=True,
    )


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

_streamlit_flow()