# Copyright (c) 2022-2023 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Members Only Area."""
import datetime
import time

import streamlit as st
import utils  # type: ignore
from dynaconf import Dynaconf  # type: ignore

# ------------------------------------------------------------------
# Global constants and variables.
# ------------------------------------------------------------------
APP_ID = "members"

COLOR_HEADER: str = "#357f8f"

FONT_SIZE_HEADER = 48
FONT_SIZE_SUBHEADER = 36

LINK_GITHUB_PAGES = "https://io-aero.github.io/io-avstats-shared/"

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


# ------------------------------------------------------------------
# Streamlit flow.
# ------------------------------------------------------------------
def _streamlit_flow() -> None:
    # Start time measurement.
    start_time = time.time_ns()

    st.set_page_config(
        layout="wide",
        # flake8: noqa: E501
        # pylint: disable=line-too-long
        page_icon="https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png",
        page_title="members by IO-Aero",
    )

    st.sidebar.markdown("## [IO-Aero Website](https://www.io-aero.com)")

    # pylint: disable=line-too-long
    st.sidebar.image(
        "https://github.com/io-aero/io-avstats-shared/blob/main/resources/Images/IO-Aero_Logo.png?raw=true",
        width=200,
    )

    utils.has_access(APP_ID)

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
