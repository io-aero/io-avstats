# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Members Only Area."""
import datetime
import pathlib
import time

import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore
from PIL import Image  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "members"

COLOR_HEADER: str = "#357f8f"

FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

HOST_CLOUD: bool | None = None

LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"

RESOURCES: dict[str, dict[str, list[str]]] = {}

SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="IO_AVSTATS",
    settings_files=["settings.io_avstats.toml", ".settings.io_avstats.toml"],
)

USER_INFO: str = "n/a"


# ------------------------------------------------------------------
# Set up the page.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
def _setup_page():
    st.markdown(
        f'<p style="text-align:left;color:{COLOR_HEADER};font-size:{FONT_SIZE_HEADER}px;'
        + 'font-weight: normal;border-radius:2%;">Members Only Area</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------------
    # Application menu.
    # --------------------------------------------------------------
    applications = []
    downloads = []

    for app_id in ["ae1982", "pd1982", "slara"]:
        if app_id in RESOURCES:
            if app_id == "ae1982":
                url = "http://" + (
                    app_id + ".io-aero.com" if HOST_CLOUD else "localhost:8501"
                )
                applications.append(f"[Aviation Event Analysis]({url})")
            elif app_id == "pd1982":
                url = "http://" + (
                    app_id + ".io-aero.com" if HOST_CLOUD else "localhost:8502"
                )
                applications.append(f"[Database Profiling]({url})")
            elif app_id == "slara":
                url = "http://" + (
                    app_id + ".io-aero.com" if HOST_CLOUD else "localhost:8503"
                )
                applications.append(f"[Association Rule Analysis]({url})")
            else:
                applications.append(
                    (
                        "Unknown Application",
                        f"[{app_id}]",
                    )
                )

    if len(applications) > 0:
        downloads.append(("IO-AVSTATS Documentation", "IO-AVSTATS.pdf"))
        applications.sort()

        st.markdown("## Applications")

        for app_link in applications:
            st.markdown("##### " + app_link)

        st.divider()

    # --------------------------------------------------------------
    # Download menu.
    # --------------------------------------------------------------
    for item_id in ["IO-AVSTATS-DB"]:
        if item_id in RESOURCES:
            if item_id == "IO-AVSTATS-DB":
                downloads.append(("IO-AVSTATS-DB Database", "IO-AVSTATS-DB.zip"))
                downloads.append(("IO-AVSTATS-DB Documentation", "IO-AVSTATS-DB.pdf"))
            else:
                downloads.append(
                    (
                        "Unknown Download",
                        f"[{item_id}]",
                    )
                )

    if len(downloads) > 0:
        downloads.sort()

        st.markdown("## Downloads")

        for item_desc, item_file in downloads:
            with open("upload/" + item_file, "rb") as download:
                st.download_button(
                    "**Download "
                    + item_desc
                    + " ("
                    + pathlib.Path(item_file).suffix.upper()[1:]
                    + ")**",
                    download,
                    file_name=item_file,
                )

        st.divider()

    # --------------------------------------------------------------
    # Image.
    # --------------------------------------------------------------
    st.image(Image.open("docs/img/StockSnap_SLQQYN6CRR.jpg"))

    st.divider()


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
def _streamlit_flow() -> None:
    global HOST_CLOUD  # pylint: disable=global-statement
    global RESOURCES  # pylint: disable=global-statement
    global USER_INFO  # pylint: disable=global-statement

    # Start time measurement.
    start_time = time.time_ns()

    if "HOST_CLOUD" in st.session_state and "MODE_STANDARD" in st.session_state:
        HOST_CLOUD = st.session_state["HOST_CLOUD"]
    else:
        (host, _mode) = utils.get_args()
        HOST_CLOUD = bool(host == "Cloud")
        st.session_state["HOST_CLOUD"] = HOST_CLOUD

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

    USER_INFO, RESOURCES = utils.has_access(HOST_CLOUD, APP_ID)

    _setup_page()

    # Stop time measurement.
    print(
        str(datetime.datetime.now())
        + f" {f'{time.time_ns() - start_time:,}':>20} ns - Total runtime for application {APP_ID:<10} - {USER_INFO}",
        flush=True,
    )


# -----------------------------------------------------------------------------
# Program start.
# -----------------------------------------------------------------------------

_streamlit_flow()
