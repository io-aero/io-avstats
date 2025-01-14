# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Managing the database schema of the PostgreSQL database."""
import logging
import os
import shutil
import sys
import zipfile
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from iocommon import db_utils, io_settings, io_utils
from iocommon.io_utils import extract_column_value, setup_retry_session
from psycopg import connection, cursor, sql
from psycopg.errors import (
    ForeignKeyViolation,
    UniqueViolation,
)
from traittypes import DataFrame

from ioavstats import glob_local

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

COLUMN_ACCEPTABLE_CITIES = "acceptable_cities"
COLUMN_AIRANAL = "AIRANAL"
COLUMN_AIRPORT_ID = "AIRPORT_ID"
COLUMN_CENTLAT = "centlat"
COLUMN_CENTLON = "centlon"
COLUMN_CICTT_CODE_LOWER = "cictt_code"
COLUMN_CICTT_CODE_SPACE = "CICTT Code"
COLUMN_CICTT_CODE_UNDERSCORE = "CICTT_Code"
COLUMN_CITY = "city"
COLUMN_COMP_CODE = "COMP_CODE"
COLUMN_COUNTRY_LOWER = "country"
COLUMN_COUNTRY_NAME = "country_name"
COLUMN_COUNTRY_UPPER = "COUNTRY"
COLUMN_DEC_LATITUDE = "dec_latitude"
COLUMN_DEC_LONGITUDE = "dec_longitude"
COLUMN_DEFINITION = "Definition"
COLUMN_DIM_UOM = "DIM_UOM"
COLUMN_DODHIFLIP = "DODHIFLIP"
COLUMN_ELEVATION = "ELEVATION"
COLUMN_EVENTSOE_NO = "eventsoe_no"
COLUMN_FAR91 = "FAR91"
COLUMN_FAR93 = "FAR93"
COLUMN_GLOBAL_ID = "GLOBAL_ID"
COLUMN_IAPEXISTS = "IAPEXISTS"
COLUMN_IDENT = "IDENT"
COLUMN_IDENTIFIER = "Identifier"
COLUMN_LAT = "lat"
COLUMN_LATITUDE_LOWER = "latitude"
COLUMN_LATITUDE_UPPER = "LATITUDE"
COLUMN_LENGTH = "LENGTH"
COLUMN_LNG = "lng"
COLUMN_LOCID = "LocID"
COLUMN_LONGITUDE_LOWER = "longitude"
COLUMN_LONGITUDE_UPPER = "LONGITUDE"
COLUMN_MEANING = "meaning"
COLUMN_MIL_CODE = "MIL_CODE"
COLUMN_NAME = "NAME"
COLUMN_NAME_LOWER = "name"
COLUMN_OPERSTATUS = "OPERSTATUS"
COLUMN_PRIMARY_CITY = "primary_city"
COLUMN_PRIVATEUSE = "PRIVATEUSE"
COLUMN_SERVCITY = "SERVCITY"
COLUMN_SOE_NO = "soe_no"
COLUMN_STATE_CAMEL = "State"
COLUMN_STATE_ID = "state_id"
COLUMN_STATE_LOWER = "state"
COLUMN_STATE_UPPER = "STATE"
COLUMN_STUSAB = "stusab"
COLUMN_TYPE = "type"
COLUMN_TYPE_CODE = "TYPE_CODE"
COLUMN_X = "X"
COLUMN_Y = "Y"
COLUMN_ZIP = "zip"
COLUMN_ZIPS = "zips"

COUNTRIES_TIMEOUT = int(
    io_settings.settings.countries_timeout,
)
COUNTRIES_TRANSACTION_SIZE = int(
    io_settings.settings.countries_transaction_size,
)
COUNTRIES_URL = io_settings.settings.countries_url

DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES = (
    io_settings.settings.download_file_aviation_occurrence_categories
)
DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES_URL = (
    io_settings.settings.download_file_aviation_occurrence_categories_url
)
DOWNLOAD_FILE_FAA_AIRPORTS = io_settings.settings.download_file_faa_airports
DOWNLOAD_FILE_FAA_AIRPORTS_URL = io_settings.settings.download_file_faa_airports_url
DOWNLOAD_FILE_FAA_NPIAS = io_settings.settings.download_file_faa_npias
DOWNLOAD_FILE_FAA_NPIAS_URL = io_settings.settings.download_file_faa_npias_url
DOWNLOAD_FILE_FAA_RUNWAYS = io_settings.settings.download_file_faa_runways
DOWNLOAD_FILE_FAA_RUNWAYS_URL = io_settings.settings.download_file_faa_runways_url
DOWNLOAD_FILE_SEQUENCE_OF_EVENTS = io_settings.settings.download_file_sequence_of_events
DOWNLOAD_FILE_SEQUENCE_OF_EVENTS_REMARKS = (
    io_settings.settings.download_file_sequence_of_events_remarks
)
DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES = (
    io_settings.settings.download_file_simplemaps_us_cities
)
DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES_URL = (
    io_settings.settings.download_file_simplemaps_us_cities_url
)
DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS = io_settings.settings.download_file_simplemaps_us_zips
DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS_URL = (
    io_settings.settings.download_file_simplemaps_us_zips_url
)
DOWNLOAD_FILE_ZIP_CODES_ORG = io_settings.settings.download_file_zip_codes_org
DOWNLOAD_FILE_ZIP_CODES_ORG_URL = io_settings.settings.download_file_zip_codes_org_url

IO_LAST_SEEN = datetime.now(UTC)

OPENDATASOFT_US_STATE_BOUNDARIES_FILE = (
    io_settings.settings.opendatasoft_us_state_boundaries_file
)
OPENDATASOFT_US_STATE_BOUNDARIES_FILE_URL = (
    io_settings.settings.opendatasoft_us_state_boundaries_file_url
)
OPENDATASOFT_US_STATE_BOUNDARIES_URL = (
    io_settings.settings.opendatasoft_us_state_boundaries_url
)
OPENDATASOFT_TIMEOUT = int(
    io_settings.settings.opendatasoft_timeout,
)
OPENDATASOFT_TRANSACTION_SIZE = int(
    io_settings.settings.opendatasoft_transaction_size,
)
OPENDATASOFT_WORKDIR = io_settings.settings.opendatasoft_workdir


# ------------------------------------------------------------------
# Download a file from a specified URL.
# ------------------------------------------------------------------
def _download_file(
    url: str,
    file_path: Path,
    timeout: int,
) -> None:
    """Download a file from a specified URL.

    Downloads a file from a specified URL.

    Args:
    ----
        url (str): The URL.
        file_path (Path): The local file where the file from the URL will be downloaded.
        timeout (int): The timeout value for the request.

    """
    # Log the URL of the file to be downloaded
    logging.info("=" * 80)
    logging.info(glob_local.INFO_00_132.replace("{file_name}", url))

    # Step 1: Download the ZIP file with retries
    session = setup_retry_session(
        retries=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    }
    try:
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        logging.fatal(glob_local.FATAL_00_971.replace("{exception}", str(e)))
        sys.exit(1)

    with file_path.open("wb") as file:
        file.write(response.content)


# ------------------------------------------------------------------
# Load airport data from an MS Excel file.
# ------------------------------------------------------------------
def _load_airport_data() -> None:
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Delete existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    DELETE FROM io_airports
    """,
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()
        io_utils.progress_msg("-" * 80)
        # INFO.00.087 Database table io_airports: Delete the existing data
        io_utils.progress_msg(glob_local.INFO_00_087)
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Start processing airport data.
    # ------------------------------------------------------------------

    us_state_names: list[str] = _sql_query_us_state_names(conn_pg)
    us_states: list[str] = _sql_query_us_states(conn_pg)

    locids: list[str] = _load_npias_data(us_state_names)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        columns = [
            COLUMN_X,
            COLUMN_Y,
            COLUMN_GLOBAL_ID,
            COLUMN_IDENT,
            COLUMN_NAME,
            COLUMN_LATITUDE_UPPER,
            COLUMN_LONGITUDE_UPPER,
            COLUMN_ELEVATION,
            COLUMN_TYPE_CODE,
            COLUMN_SERVCITY,
            COLUMN_STATE_UPPER,
            COLUMN_COUNTRY_UPPER,
            COLUMN_OPERSTATUS,
            COLUMN_PRIVATEUSE,
            COLUMN_IAPEXISTS,
            COLUMN_DODHIFLIP,
            COLUMN_FAR91,
            COLUMN_FAR93,
            COLUMN_MIL_CODE,
            COLUMN_AIRANAL,
        ]

        # Attempt to read the csv file
        dataframe = pd.read_csv(DOWNLOAD_FILE_FAA_AIRPORTS, sep=",", usecols=columns)

        # INFO.00.089 Database table io_airports: Load data from file '{filename}'
        io_utils.progress_msg("-" * 80)
        io_utils.progress_msg(
            glob_local.INFO_00_089.replace("{filename}", DOWNLOAD_FILE_FAA_AIRPORTS),
        )

        count_select = 0
        count_upsert = 0
        count_usable = 0

        # ------------------------------------------------------------------
        # Load the airport data.
        # ------------------------------------------------------------------

        for _index, row in dataframe.iterrows():
            count_select += 1

            ident = extract_column_value(row, COLUMN_IDENT)
            if ident is None or ident not in locids:
                continue

            country = extract_column_value(row, COLUMN_COUNTRY_UPPER)
            if country != "UNITED STATES":
                continue

            state = extract_column_value(row, COLUMN_STATE_UPPER)
            if state is None or state not in us_states:
                continue

            count_usable += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            airanal = extract_column_value(row, COLUMN_AIRANAL)
            country = "USA"
            dec_longitude = extract_column_value(row, COLUMN_X, float)
            dec_latitude = extract_column_value(row, COLUMN_Y, float)
            dodhiflib = extract_column_value(row, COLUMN_DODHIFLIP, int)
            elevation = extract_column_value(row, COLUMN_ELEVATION, float)
            far91 = extract_column_value(row, COLUMN_FAR91, int)
            far93 = extract_column_value(row, COLUMN_FAR93, int)
            global_id = extract_column_value(row, COLUMN_GLOBAL_ID)
            iapexists = extract_column_value(row, COLUMN_IAPEXISTS)
            latitude = extract_column_value(row, COLUMN_LATITUDE_UPPER)
            longitude = extract_column_value(row, COLUMN_LONGITUDE_UPPER)
            mil_code = extract_column_value(row, COLUMN_MIL_CODE)
            name = extract_column_value(row, COLUMN_NAME)
            operstatus = extract_column_value(row, COLUMN_OPERSTATUS)
            privateuse = extract_column_value(row, COLUMN_PRIVATEUSE, int)
            servcity = extract_column_value(row, COLUMN_SERVCITY)
            state = extract_column_value(row, COLUMN_STATE_UPPER)
            type_code = extract_column_value(row, COLUMN_TYPE_CODE)

            cur_pg.execute(
                """
            INSERT INTO io_airports AS ia (
                   global_id,
                   airanal,
                   country,
                   dec_latitude,
                   dec_longitude,
                   dodhiflib,
                   elevation,
                   far91,
                   far93,
                   iapexists,
                   ident,
                   latitude,
                   longitude,
                   mil_code,
                   name,
                   operstatus,
                   privateuse,
                   servcity,
                   state,
                   type_code,
                   first_processed
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,
                   %s
                   )
            ON CONFLICT ON CONSTRAINT io_airports_pkey
            DO UPDATE
               SET airanal = %s,
                   country = %s,
                   dec_latitude = %s,
                   dec_longitude = %s,
                   dodhiflib = %s,
                   elevation = %s,
                   far91 = %s,
                   far93 = %s,
                   iapexists = %s,
                   ident = %s,
                   latitude = %s,
                   longitude = %s,
                   mil_code = %s,
                   name = %s,
                   operstatus = %s,
                   privateuse = %s,
                   servcity = %s,
                   state = %s,
                   type_code = %s,
                   last_processed = %s
             WHERE ia.global_id = %s
            """,
                (
                    global_id,
                    airanal,
                    country,
                    dec_latitude,
                    dec_longitude,
                    dodhiflib,
                    elevation,
                    far91,
                    far93,
                    iapexists,
                    ident,
                    latitude,
                    longitude,
                    mil_code,
                    name,
                    operstatus,
                    privateuse,
                    servcity,
                    state,
                    type_code,
                    IO_LAST_SEEN,
                    airanal,
                    country,
                    dec_latitude,
                    dec_longitude,
                    dodhiflib,
                    elevation,
                    far91,
                    far93,
                    iapexists,
                    ident,
                    latitude,
                    longitude,
                    mil_code,
                    name,
                    operstatus,
                    privateuse,
                    servcity,
                    state,
                    type_code,
                    IO_LAST_SEEN,
                    global_id,
                ),
            )
            count_upsert += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

        # ------------------------------------------------------------------
        # Finalize processing.
        # ------------------------------------------------------------------

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_airports",
            data_source=DOWNLOAD_FILE_FAA_AIRPORTS,
            task_timestamp=IO_LAST_SEEN,
            remarks=DOWNLOAD_FILE_FAA_NPIAS_URL,
            url=DOWNLOAD_FILE_FAA_AIRPORTS_URL,
        )

        cur_pg.close()
        conn_pg.close()

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", DOWNLOAD_FILE_FAA_AIRPORTS),
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", DOWNLOAD_FILE_FAA_AIRPORTS),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_AIRPORTS,
            ).replace(
                "{error}",
                str(err),
            ),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_AIRPORTS,
            ).replace(
                "{error}",
                str(exc),
            ),
        )


# ------------------------------------------------------------------
# Load aviation occurrence categories from an MS Excel file.
# ------------------------------------------------------------------
def _load_aviation_occurrence_categories() -> None:
    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    filename_excel = Path.cwd() / DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES.replace(
        "/",
        os.sep,
    )

    if not Path(filename_excel).is_file():
        # ERROR.00.937 The aviation occurrence categories file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_937.replace("{filename}", filename_excel),
        )

    # INFO.00.074 Database table io_aviation_occurrence_categories: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_074.replace(
            "{filename}",
            DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
        ),
    )
    io_utils.progress_msg("-" * 80)

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            sheet_name="Sheet1",
        )

        # INFO.00.074 Database table io_aviation_occurrence_categories: ...
        io_utils.progress_msg(
            glob_local.INFO_00_074.replace(
                "{filename}",
                DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            ),
        )

        count_delete = 0
        count_upsert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the aviation occurrence categories.
        # ------------------------------------------------------------------

        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            cictt_code = extract_column_value(row, COLUMN_CICTT_CODE_SPACE)
            identifier = extract_column_value(row, COLUMN_IDENTIFIER)
            definition = extract_column_value(row, COLUMN_DEFINITION)

            cur_pg.execute(
                """
            INSERT INTO io_aviation_occurrence_categories AS aoc (
                   cictt_code,
                   identifier,
                   definition,
                   first_processed,
                   last_seen
                   ) VALUES (
                   %s,%s,%s,%s,%s
                   )
            ON CONFLICT ON CONSTRAINT io_aviation_occurrence_categories_pkey
            DO UPDATE
               SET identifier = %s,
                   definition = %s,
                   last_processed = %s,
                   last_seen = %s
             WHERE aoc.cictt_code = %s
            """,
                (
                    cictt_code,
                    identifier,
                    definition,
                    IO_LAST_SEEN,
                    IO_LAST_SEEN,
                    identifier,
                    definition,
                    IO_LAST_SEEN,
                    IO_LAST_SEEN,
                    cictt_code,
                ),
            )
            count_upsert += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

        # ------------------------------------------------------------------
        # Delete the obsolete data.
        # ------------------------------------------------------------------

        count_select = 0


        cur_pg.execute(
            """
        SELECT cictt_code
          FROM io_aviation_occurrence_categories
         WHERE last_seen <> %s
            """,
            (IO_LAST_SEEN,),
        )

        for row_pg in cur_pg.fetchall():
            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            cictt_code = row_pg[COLUMN_CICTT_CODE_LOWER]  # type: ignore

            try:
                cur_pg.execute(
                    """
                DELETE FROM io_aviation_occurrence_categories
                 WHERE cictt_code = %s;
                """,
                    (cictt_code,),
                )
                if cur_pg.rowcount > 0:
                    count_delete += cur_pg.rowcount
                    io_utils.progress_msg(f"Deleted cictt_code={cictt_code}")
            except ForeignKeyViolation:
                io_utils.progress_msg(f"Failed to delete cictt_code={cictt_code}")

        conn_pg.commit()

        if count_select > 0:
            io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")
        if count_delete > 0:
            io_utils.progress_msg(f"Number rows deleted  : {count_delete!s:>8}")

        # ------------------------------------------------------------------
        # Finalize processing.
        # ------------------------------------------------------------------

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_aviation_occurrence_categories",
            data_source=DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            task_timestamp=IO_LAST_SEEN,
            url=DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES_URL,
        )

        cur_pg.close()
        conn_pg.close()

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_AVIATION_OCCURRENCE_CATEGORIES,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Load country data.
# ------------------------------------------------------------------
def _load_country_data(dataframe: DataFrame) -> None:
    logging.info("=" * 80)
    logging.info(glob_local.INFO_00_132.replace("{file_name}", str(COUNTRIES_URL)))
    logging.info("-" * 80)

    insert_query = sql.SQL(
        """
        INSERT INTO io_countries AS ic (
               country,
               country_name,
               dec_latitude,
               dec_longitude,
               first_processed
               ) VALUES (
               %s,%s,%s,%s,%s
               );
    """,
    )

    update_query = sql.SQL(
        """
        UPDATE io_countries ic
           SET country_name = %s,
               dec_latitude = %s,
               dec_longitude = %s,
               last_processed = %s
         WHERE ic.country = %s
           AND (ic.country_name IS DISTINCT FROM %s
             OR ic.dec_latitude IS DISTINCT FROM %s
             OR ic.dec_longitude IS DISTINCT FROM %s);
    """,
    )

    # --------------------------------------------------------------
    # Create database connection.
    # --------------------------------------------------------------

    logging.info("")
    conn_pg, cur_pg = db_utils.get_postgres_cursor(autocommit=False)
    logging.info("")

    # --------------------------------------------------------------
    # Start processing airport base data.
    # --------------------------------------------------------------

    count_insert = 0
    count_relevant = 0
    count_update = 0

    primary_keys = _load_io_countries_primary_keys(cur_pg)

    count_select = len(primary_keys)

    if count_select > 0:
        info_msg = f"Number rows existing : {count_select!s:>8}"
        logging.info(info_msg)
        count_select = 0

    insert_data = []
    update_data = []

    # ------------------------------------------------------------------
    # Load the country data.
    # ------------------------------------------------------------------

    for _index, row in dataframe.iterrows():
        count_select += 1

        country = extract_column_value(row, "cca3", is_required=True)
        if country == "cca3":
            continue

        count_relevant += 1

        country_name = extract_column_value(row, "name.common", is_required=True)

        latlng = extract_column_value(row, "latlng", is_required=True)
        dec_latitude_str, dec_longitude_str = latlng.split(",")
        dec_latitude = float(dec_latitude_str.strip())
        dec_longitude = float(dec_longitude_str.strip())

        if country in primary_keys:
            update_data.append(
                (
                    country_name,
                    dec_latitude,
                    dec_longitude,
                    IO_LAST_SEEN,
                    country,
                    country_name,
                    dec_latitude,
                    dec_longitude,
                ),
            )
        else:
            insert_data.append(
                (
                    country,
                    country_name,
                    dec_latitude,
                    dec_longitude,
                    IO_LAST_SEEN,
                ),
            )

        if count_relevant % COUNTRIES_TRANSACTION_SIZE == 0:
            cur_pg.executemany(insert_query, insert_data)
            count_insert += cur_pg.rowcount
            cur_pg.executemany(update_query, update_data)
            count_update += cur_pg.rowcount
            conn_pg.commit()
            info_msg = (
                f"Processed rows       : {count_relevant!s:>8} - "
                f"inserted: {count_insert!s:>8} - updated: {count_update!s:>8}"
            )
            logging.info(info_msg)
            insert_data = []
            update_data = []

    cur_pg.executemany(insert_query, insert_data)
    count_insert += cur_pg.rowcount
    cur_pg.executemany(update_query, update_data)
    count_update += cur_pg.rowcount

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    logging.info("")
    info_msg = f"Number rows selected : {count_select!s:>8}"
    logging.info(info_msg)

    if count_relevant > 0:
        info_msg = f"Number rows relevant : {count_relevant!s:>8}"
        logging.info(info_msg)
    if count_insert > 0:
        info_msg = f"Number rows inserted : {count_insert!s:>8}"
        logging.info(info_msg)
    if count_update > 0:
        info_msg = f"Number rows updated  : {count_update!s:>8}"
        logging.info(info_msg)

    # ------------------------------------------------------------------
    # Finalize country processing.
    # ------------------------------------------------------------------

    db_utils.upd_io_processed_data(
        cur_pg=cur_pg,
        table_name="io_countries",
        data_source=COUNTRIES_URL,
        task_timestamp=IO_LAST_SEEN,
        url=COUNTRIES_URL,
    )

    cur_pg.close()
    conn_pg.commit()
    conn_pg.close()


# ------------------------------------------------------------------
# Get the primary keys for the io_countries table.
# ------------------------------------------------------------------
def _load_io_countries_primary_keys(cur_pg: cursor) -> set[tuple[str, str]]:
    """Get the primary keys for the io_countries table.

    Args:
    ----
        cur_pg (cursor): A database cursor.

    Returns:
    -------
        set: A set of tuples representing the primary key columns.

    """
    primary_keys = set()

    cur_pg.execute(
        """
        SELECT country
          FROM io_countries;
       """,
    )

    for row in cur_pg.fetchall():
        primary_keys.add(
            (row[COLUMN_COUNTRY_LOWER]),
        )

    return primary_keys


# ------------------------------------------------------------------
# Get the primary keys for the io_states table.
# ------------------------------------------------------------------
def _load_io_states_primary_keys(cur_pg: cursor) -> set[tuple[str, str]]:
    """Get the primary keys for the io_states table.

    Args:
    ----
        cur_pg (cursor): A database cursor.

    Returns:
    -------
        set: A set of tuples representing the primary key columns.

    """
    primary_keys = set()

    cur_pg.execute(
        """
        SELECT country,
               state
          FROM io_states;
       """,
    )

    for row in cur_pg.fetchall():
        primary_keys.add(
            (row[COLUMN_COUNTRY_LOWER], row[COLUMN_STATE_LOWER]),
        )

    return primary_keys


# ------------------------------------------------------------------
# Load NPIAS data from an MS Excel file.
# ------------------------------------------------------------------
def _load_npias_data(us_states: list[str]) -> list[str]:
    # ------------------------------------------------------------------
    # Start processing NPIAS data.
    # ------------------------------------------------------------------

    filename_excel = Path.cwd() / DOWNLOAD_FILE_FAA_NPIAS.replace("/", os.sep)

    if not Path(filename_excel).is_file():
        # ERROR.00.945 The NPIAS file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_945.replace("{filename}", filename_excel),
        )

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            DOWNLOAD_FILE_FAA_NPIAS,
            sheet_name="All NPIAS Airports",
        )

        count_select = 0
        count_usable = 0

        locids: list[str] = []

        # ------------------------------------------------------------------
        # Load the NPIAS data.
        # ------------------------------------------------------------------

        for _index, row in dataframe.iterrows():

            count_select += 1

            if extract_column_value(row, COLUMN_STATE_CAMEL) not in us_states:
                continue

            locids.append(extract_column_value(row, COLUMN_LOCID))

            count_usable += 1

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")
        io_utils.progress_msg(f"Number rows usable   : {count_usable!s:>8}")

        return locids  # noqa: TRY300

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_NPIAS,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_NPIAS,
            ).replace(
                "{error}",
                str(err),
            ),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_NPIAS,
            ).replace(
                "{error}",
                str(exc),
            ),
        )


# ------------------------------------------------------------------
# Load runway data from an MS Excel file.
# ------------------------------------------------------------------
def _load_runway_data() -> None:
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Load airport identifications.
    # ------------------------------------------------------------------
    # INFO.00.088 Database table io_airports: Load the global identifications
    io_utils.progress_msg("-" * 80)
    io_utils.progress_msg(glob_local.INFO_00_088)

    count_select = 0

    cur_pg.execute(
        """
    SELECT global_id
      FROM io_airports
     ORDER BY 1;
    """,
    )

    runway_data: dict[str, tuple[str | None, float | None]] = {}

    for row in cur_pg:
        count_select += 1
        runway_data[row["global_id"]] = (None, None)

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        columns = [
            COLUMN_AIRPORT_ID,
            COLUMN_COMP_CODE,
            COLUMN_DIM_UOM,
            COLUMN_LENGTH,
        ]

        # Attempt to read the csv file
        dataframe = pd.read_csv(DOWNLOAD_FILE_FAA_RUNWAYS, sep=",", usecols=columns)

        # INFO.00.092 Database table io_runways: Load data from file '{filename}'
        io_utils.progress_msg(
            glob_local.INFO_00_092.replace("{filename}", DOWNLOAD_FILE_FAA_RUNWAYS),
        )

        count_select = 0

        # ------------------------------------------------------------------
        # Load the runway data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            airport_id = extract_column_value(row, COLUMN_AIRPORT_ID)
            if airport_id not in runway_data:
                continue

            count_select += 1

            (
                comp_code,
                length,
            ) = runway_data[airport_id]

            new_length = extract_column_value(row, COLUMN_LENGTH, int)

            dim_vom = extract_column_value(row, COLUMN_DIM_UOM)
            if dim_vom == "M":
                new_length = new_length * 3.28084

            if length is None or new_length > length:
                runway_data[airport_id] = (
                    extract_column_value(row, COLUMN_COMP_CODE),
                    new_length,
                )

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")
        io_utils.progress_msg("-" * 80)

        # ------------------------------------------------------------------
        # Load the runway data.
        # ------------------------------------------------------------------

        # INFO.00.090 Database table io_airports: Update the runway data
        io_utils.progress_msg(glob_local.INFO_00_090)

        count_select = 0
        count_update = 0


        for airport_id, (comp_code, length) in runway_data.items():
            count_select += 1

            if comp_code is None:
                continue

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            cur_pg.execute(
                """
            UPDATE io_airports ia
               SET max_runway_comp_code = %s,
                   max_runway_length = %s,
                   last_processed = %s
             WHERE ia.global_id = %s
            """,
                (
                    comp_code,
                    length,
                    IO_LAST_SEEN,
                    airport_id,
                ),
            )
            count_update += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_update > 0:
            io_utils.progress_msg(f"Number rows updated  : {count_update!s:>8}")

        # ------------------------------------------------------------------
        # Finalize processing.
        # ------------------------------------------------------------------

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_airports",
            data_source=DOWNLOAD_FILE_FAA_RUNWAYS,
            task_timestamp=IO_LAST_SEEN,
            url=DOWNLOAD_FILE_FAA_RUNWAYS_URL,
        )

        cur_pg.close()
        conn_pg.close()

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", DOWNLOAD_FILE_FAA_RUNWAYS),
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", DOWNLOAD_FILE_FAA_RUNWAYS),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_RUNWAYS,
            ).replace(
                "{error}",
                str(err),
            ),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_FAA_RUNWAYS,
            ).replace(
                "{error}",
                str(exc),
            ),
        )


# ------------------------------------------------------------------
# Load sequence of events sequence data from an MS Excel file.
# ------------------------------------------------------------------
def _load_sequence_of_events() -> None:
    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    # INFO.00.076 Database table io_sequence_of_events: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_076.replace(
            "{filename}",
            io_settings.settings.download_file_sequence_of_events,
        ),
    )
    io_utils.progress_msg("-" * 80)

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        columns = [
            COLUMN_EVENTSOE_NO,
            COLUMN_MEANING,
            COLUMN_CICTT_CODE_UNDERSCORE,
        ]

        # Attempt to read the csv file
        dataframe = pd.read_csv(
            DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            sep=",",
            usecols=columns,
        )

        # INFO.00.076 Database table io_sequence_of_events: Load data from file '{filename}'
        io_utils.progress_msg(
            glob_local.INFO_00_076.replace(
                "{filename}",
                DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            ),
        )

        count_delete = 0
        count_upsert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the sequence of events data.
        # ------------------------------------------------------------------

        cictt_codes = _sql_query_cictt_codes(conn_pg)


        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            soe_no = extract_column_value(row, COLUMN_EVENTSOE_NO).rjust(3, "0")

            cictt_code = str(
                extract_column_value(row, COLUMN_CICTT_CODE_UNDERSCORE),
            ).rstrip()
            if cictt_code is None or cictt_code not in cictt_codes:
                continue

            meaning = str(extract_column_value(row, COLUMN_MEANING)).rstrip()

            cur_pg.execute(
                """
            INSERT INTO io_sequence_of_events AS isoe (
                   soe_no,
                   meaning,
                   cictt_code,
                   first_processed,
                   last_seen
                   ) VALUES (
                   %s,%s,%s,%s,%s
                   )
            ON CONFLICT ON CONSTRAINT io_sequence_of_events_pkey
            DO UPDATE
               SET meaning = %s,
                   cictt_code = %s,
                   last_processed = %s,
                   last_seen = %s
             WHERE isoe.soe_no = %s
            """,
                (
                    soe_no,
                    meaning,
                    cictt_code if cictt_code else None,
                    IO_LAST_SEEN,
                    IO_LAST_SEEN,
                    meaning,
                    cictt_code,
                    IO_LAST_SEEN,
                    IO_LAST_SEEN,
                    soe_no,
                ),
            )
            count_upsert += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

        # ------------------------------------------------------------------
        # Delete the obsolete data.
        # ------------------------------------------------------------------

        count_select = 0


        cur_pg.execute(
            """
        SELECT soe_no
          FROM io_sequence_of_events
         WHERE last_seen <> %s
            """,
            (IO_LAST_SEEN,),
        )

        for row_pg in cur_pg.fetchall():
            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            soe_no = row_pg[COLUMN_SOE_NO]  # type: ignore

            try:
                cur_pg.execute(
                    """
                DELETE FROM io_sequence_of_events
                 WHERE soe_no = %s;
                """,
                    (soe_no,),
                )
                if cur_pg.rowcount > 0:
                    count_delete += cur_pg.rowcount
                    io_utils.progress_msg(f"Deleted soe_no={soe_no}")
            except ForeignKeyViolation:
                io_utils.progress_msg(f"Failed to delete soe_no={soe_no}")

        conn_pg.commit()

        if count_select > 0:
            io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")
        if count_delete > 0:
            io_utils.progress_msg(f"Number rows deleted  : {count_delete!s:>8}")

        # ------------------------------------------------------------------
        # Finalize processing.
        # ------------------------------------------------------------------

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_sequence_of_events",
            data_source=DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            task_timestamp=IO_LAST_SEEN,
            remarks=DOWNLOAD_FILE_SEQUENCE_OF_EVENTS_REMARKS,
        )

        cur_pg.close()
        conn_pg.close()

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            ),
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace(
                "{file_name}",
                DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_SEQUENCE_OF_EVENTS,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Load city data from a US city file.
# ------------------------------------------------------------------
def _load_simplemaps_data_cities_from_us_cities(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    filename_excel = Path.cwd() / DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES.replace(
        "/",
        os.sep,
    )

    if not Path(filename_excel).is_file():
        # ERROR.00.914 The US city file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_914.replace("{filename}", filename_excel),
        )

    # INFO.00.027 Database table io_lat_lng: Load city data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_027.replace(
            "{filename}",
            DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
        ),
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            sheet_name="Sheet1",
        )

        count_upsert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the US city data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
            lat = extract_column_value(row, COLUMN_LAT, float)
            lng = extract_column_value(row, COLUMN_LNG, float)
            state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()


            cur_pg.execute(
                """
            INSERT INTO io_lat_lng AS ill (
                   type,
                   country,
                   state,
                   city,
                   dec_latitude,
                   dec_longitude,
                   source,
                   first_processed
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s,%s
                   )
            ON CONFLICT ON CONSTRAINT io_lat_lng_type_country_state_city_zipcode_key
            DO UPDATE
               SET dec_latitude = %s,
                   dec_longitude = %s,
                   source = %s,
                   last_processed = %s
             WHERE ill.type = %s
               AND ill.country = %s
               AND ill.state = %s
               AND ill.city = %s
               AND NOT (
                   ill.dec_latitude = %s
               AND ill.dec_longitude = %s
               );
            """,
                (
                    glob_local.IO_LAT_LNG_TYPE_CITY,
                    glob_local.COUNTRY_USA,
                    state_id,
                    city,
                    lat,
                    lng,
                    glob_local.SOURCE_SM_US_CITIES,
                    IO_LAST_SEEN,
                    lat,
                    lng,
                    glob_local.SOURCE_SM_US_CITIES,
                    IO_LAST_SEEN,
                    glob_local.IO_LAT_LNG_TYPE_CITY,
                    glob_local.COUNTRY_USA,
                    state_id,
                    city,
                    lat,
                    lng,
                ),
            )
            count_upsert += cur_pg.rowcount

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_lat_lng",
            data_source=DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            task_timestamp=IO_LAST_SEEN,
            url=DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES_URL,
        )

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Load zip data from a US city file.
# ------------------------------------------------------------------

def _load_simplemaps_data_zips_from_us_cities(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    filename_excel = Path.cwd() / DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES.replace(
        "/",
        os.sep,
    )

    if not Path(filename_excel).is_file():
        # ERROR.00.914 The US city file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_914.replace("{filename}", filename_excel),
        )

    # INFO.00.039 Database table io_lat_lng: Load zipcode data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_039.replace(
            "{filename}",
            DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
        ),
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            sheet_name="Sheet1",
        )

        count_insert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the US city data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
            lat = extract_column_value(row, COLUMN_LAT, float)
            lng = extract_column_value(row, COLUMN_LNG, float)
            state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()
            zips = list(f"{extract_column_value(row, COLUMN_ZIPS)}".split(" "))

            for zipcode in zips:
                count_select += 1
                if count_select % io_settings.settings.database_commit_size == 0:
                    conn_pg.commit()
                    io_utils.progress_msg(
                        f"Number of rows so far read : {count_select!s:>8}",
                    )


                cur_pg.execute(
                    """
                INSERT INTO io_lat_lng (
                       type,
                       country,
                       state,
                       city,
                       zipcode,
                       dec_latitude,
                       dec_longitude,
                       source,
                       first_processed
                       ) VALUES (
                       %s,%s,%s,%s,%s,
                       %s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT io_lat_lng_type_country_state_city_zipcode_key
                DO NOTHING;
                """,
                    (
                        glob_local.IO_LAT_LNG_TYPE_ZIPCODE,
                        glob_local.COUNTRY_USA,
                        state_id,
                        city,
                        zipcode.rstrip(),
                        lat,
                        lng,
                        glob_local.SOURCE_SM_US_CITIES,
                        IO_LAST_SEEN,
                    ),
                )
                count_insert += cur_pg.rowcount

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_lat_lng",
            data_source=DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            task_timestamp=IO_LAST_SEEN,
            url=DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES_URL,
        )

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_insert > 0:
            io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_CITIES,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Load zip data from a US zip code file.
# ------------------------------------------------------------------
def _load_simplemaps_data_zips_from_us_zips(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    filename_excel = Path.cwd() / DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS.replace("/", os.sep)

    if not Path(filename_excel).is_file():
        # ERROR.00.913 The US zip code file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_913.replace("{filename}", filename_excel),
        )

    # INFO.00.025 Database table io_lat_lng: Load zipcode data rom file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_025.replace(
            "{filename}",
            io_settings.settings.download_file_simplemaps_us_zips,
        ),
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS,
            sheet_name="Sheet1",
        )

        count_duplicates = 0
        count_upsert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the US zip data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            zip_code = f"{extract_column_value(row, COLUMN_ZIP):05}".rstrip()
            city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
            lat = extract_column_value(row, COLUMN_LAT, float)
            lng = extract_column_value(row, COLUMN_LNG, float)
            state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()


            cur_pg.execute(
                """
            INSERT INTO io_lat_lng AS ill (
                   type,
                   country,
                   state,
                   city,
                   zipcode,
                   dec_latitude,
                   dec_longitude,
                   source,
                   first_processed
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s
                   )
            ON CONFLICT ON CONSTRAINT io_lat_lng_type_country_state_city_zipcode_key
            DO UPDATE
               SET dec_latitude = %s,
                   dec_longitude = %s,
                   source = %s,
                   last_processed = %s
             WHERE ill.type = %s
               AND ill.country = %s
               AND ill.state = %s
               AND ill.city = %s
               AND ill.zipcode = %s
               AND NOT (
                   ill.dec_latitude = %s
               AND ill.dec_longitude = %s
               );
            """,
                (
                    glob_local.IO_LAT_LNG_TYPE_ZIPCODE,
                    glob_local.COUNTRY_USA,
                    state_id,
                    city,
                    zip_code,
                    lat,
                    lng,
                    glob_local.SOURCE_SM_US_ZIP_CODES,
                    IO_LAST_SEEN,
                    lat,
                    lng,
                    glob_local.SOURCE_SM_US_ZIP_CODES,
                    IO_LAST_SEEN,
                    glob_local.IO_LAT_LNG_TYPE_ZIPCODE,
                    glob_local.COUNTRY_USA,
                    state_id,
                    city,
                    zip_code,
                    lat,
                    lng,
                ),
            )
            count_upsert += cur_pg.rowcount

        db_utils.upd_io_processed_data(
            cur_pg=cur_pg,
            table_name="io_lat_lng",
            data_source=DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS,
            task_timestamp=IO_LAST_SEEN,
            url=DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS_URL,
        )

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

        if count_duplicates > 0:
            io_utils.progress_msg(f"Number rows duplicate: {count_duplicates!s:>8}")

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS,
            ),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                DOWNLOAD_FILE_SIMPLEMAPS_US_ZIPS,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Load state data.
# ------------------------------------------------------------------
def _load_state_data(file_path: Path) -> None:
    logging.info("=" * 80)
    logging.info(glob_local.INFO_00_132.replace("{file_name}", str(file_path)))
    logging.info("-" * 80)

    if not file_path.exists():
        logging.fatal(glob_local.FATAL_00_931.replace("{file_name}", str(file_path)))
        sys.exit(1)

    insert_query = sql.SQL(
        """
        INSERT INTO io_states AS ist (
               country,
               state,
               dec_latitude,
               dec_longitude,
               state_name,
               first_processed
               ) VALUES (
               %s,%s,%s,%s,%s,
               %s
               );
    """,
    )

    update_query = sql.SQL(
        """
        UPDATE io_states ist
           SET dec_latitude = %s,
               dec_longitude = %s,
               state_name = %s,
               last_processed = %s
         WHERE ist.country = %s
           AND ist.state = %s
           AND (ist.dec_latitude IS DISTINCT FROM %s
             OR ist.dec_longitude IS DISTINCT FROM %s
             OR ist.state_name IS DISTINCT FROM %s);
    """,
    )

    # --------------------------------------------------------------
    # Load the airport base data in a Pandas dataframe.
    # --------------------------------------------------------------

    dataframe: pd.DataFrame = pd.DataFrame()

    try:
        columns = [COLUMN_CENTLAT, COLUMN_CENTLON, COLUMN_NAME_LOWER, COLUMN_STUSAB]

        # Attempt to read the csv file
        dataframe = pd.read_csv(str(file_path), sep=";", usecols=columns)

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", str(file_path)),
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", str(file_path)),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", str(file_path)).replace(
                "{error}",
                str(err),
            ),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", str(file_path)).replace(
                "{error}",
                str(exc),
            ),
        )

    # --------------------------------------------------------------
    # Create database connection.
    # --------------------------------------------------------------

    logging.info("")
    conn_pg, cur_pg = db_utils.get_postgres_cursor(autocommit=False)
    logging.info("")

    # --------------------------------------------------------------
    # Start processing airport base data.
    # --------------------------------------------------------------

    count_insert = 0
    count_relevant = 0
    count_update = 0

    primary_keys = _load_io_states_primary_keys(cur_pg)

    count_select = len(primary_keys)

    if count_select > 0:
        info_msg = f"Number rows existing : {count_select!s:>8}"
        logging.info(info_msg)
        count_select = 0

    insert_data = []
    update_data = []

    # ------------------------------------------------------------------
    # Load the state data.
    # ------------------------------------------------------------------

    for _index, row in dataframe.iterrows():
        count_select += 1

        name = extract_column_value(row, COLUMN_NAME_LOWER, is_required=True)
        if name == COLUMN_NAME_LOWER:
            continue

        count_relevant += 1

        centlat = extract_column_value(row, COLUMN_CENTLAT, float, is_required=True)
        centlon = extract_column_value(row, COLUMN_CENTLON, float, is_required=True)
        stusab = extract_column_value(row, COLUMN_STUSAB, is_required=True)

        if ("USA", stusab) in primary_keys:
            update_data.append(
                (
                    centlat,
                    centlon,
                    name,
                    IO_LAST_SEEN,
                    "USA",
                    stusab,
                    centlat,
                    centlon,
                    name,
                ),
            )
        else:
            insert_data.append(
                (
                    "USA",
                    stusab,
                    centlat,
                    centlon,
                    name,
                    IO_LAST_SEEN,
                ),
            )

        if count_relevant % OPENDATASOFT_TRANSACTION_SIZE == 0:
            cur_pg.executemany(insert_query, insert_data)
            count_insert += cur_pg.rowcount
            cur_pg.executemany(update_query, update_data)
            count_update += cur_pg.rowcount
            conn_pg.commit()
            info_msg = (
                f"Processed rows       : {count_relevant!s:>8} - "
                f"inserted: {count_insert!s:>8} - updated: {count_update!s:>8}"
            )
            logging.info(info_msg)
            insert_data = []
            update_data = []

    cur_pg.executemany(insert_query, insert_data)
    count_insert += cur_pg.rowcount
    cur_pg.executemany(update_query, update_data)
    count_update += cur_pg.rowcount

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    logging.info("")
    info_msg = f"Number rows selected : {count_select!s:>8}"
    logging.info(info_msg)

    if count_relevant > 0:
        info_msg = f"Number rows relevant : {count_relevant!s:>8}"
        logging.info(info_msg)
    if count_insert > 0:
        info_msg = f"Number rows inserted : {count_insert!s:>8}"
        logging.info(info_msg)
    if count_update > 0:
        info_msg = f"Number rows updated  : {count_update!s:>8}"
        logging.info(info_msg)

    # ------------------------------------------------------------------
    # Finalize airport processing.
    # ------------------------------------------------------------------

    db_utils.upd_io_processed_data(
        cur_pg=cur_pg,
        table_name="io_states",
        data_source=OPENDATASOFT_US_STATE_BOUNDARIES_FILE,
        task_timestamp=IO_LAST_SEEN,
        url=OPENDATASOFT_US_STATE_BOUNDARIES_FILE_URL,
    )

    cur_pg.close()
    conn_pg.commit()
    conn_pg.close()


# ------------------------------------------------------------------
# Determine and load city averages.
# ------------------------------------------------------------------
def _load_table_io_lat_lng_average(conn_pg: connection, cur_pg: cursor) -> None:
    # ------------------------------------------------------------------
    # Delete averaged data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    DELETE FROM io_lat_lng
     WHERE
           source = %s;
    """,
        (glob_local.SOURCE_AVERAGE,),
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        # INFO.00.063 Processed data source '{data_source}'
        io_utils.progress_msg(
            glob_local.INFO_00_063.replace("{data_source}", glob_local.SOURCE_AVERAGE),
        )
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Insert averaged data.
    # ------------------------------------------------------------------
    # INFO.00.062 Database table io_lat_lng: Load the averaged city data
    io_utils.progress_msg(glob_local.INFO_00_062)
    io_utils.progress_msg("-" * 80)

    count_duplicates = 0
    count_insert = 0
    count_select = 0

    conn_pg_2, cur_pg_2 = db_utils.get_postgres_cursor()


    cur_pg_2.execute(
        sql.SQL(
            f"""
    SELECT country,
           state,
           city,
           sum(dec_latitude)/count(*) dec_latitude,
           sum(dec_longitude)/count(*) dec_longitude
      FROM io_lat_lng
     WHERE type = '{glob_local.IO_LAT_LNG_TYPE_ZIPCODE}'
     GROUP BY country, state, city;
        """,
        ),
    )

    for row_pg in cur_pg_2.fetchall():
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        try:
            cur_pg.execute(
                """
            INSERT INTO io_lat_lng (
                   type,
                   country,
                   state,
                   city,
                   dec_latitude,
                   dec_longitude,
                   source,
                   first_processed
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s,%s
                   )
            ON CONFLICT ON CONSTRAINT io_lat_lng_type_country_state_city_zipcode_key
            DO NOTHING;
            """,
                (
                    glob_local.IO_LAT_LNG_TYPE_CITY,
                    row_pg[COLUMN_COUNTRY_LOWER],  # type: ignore
                    row_pg[COLUMN_STATE_LOWER],  # type: ignore
                    row_pg[COLUMN_CITY],  # type: ignore
                    row_pg[COLUMN_DEC_LATITUDE],  # type: ignore
                    row_pg[COLUMN_DEC_LONGITUDE],  # type: ignore
                    glob_local.SOURCE_AVERAGE,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            count_duplicates += cur_pg.rowcount

    conn_pg.commit()

    cur_pg_2.close()
    conn_pg_2.close()

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    if count_duplicates > 0:
        io_utils.progress_msg(f"Number rows duplicate: {count_duplicates!s:>8}")


# ------------------------------------------------------------------
# Load ZIP Code Database data.
# ------------------------------------------------------------------
def _load_zip_codes_org_data() -> None:
    filename_excel = Path.cwd() / DOWNLOAD_FILE_ZIP_CODES_ORG.replace("/", os.sep)

    if not Path(filename_excel).is_file():
        # ERROR.00.935 The Zip Code Database file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_935.replace("{filename}", filename_excel),
        )

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Delete existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    DELETE FROM io_lat_lng
     WHERE SOURCE = %s;
    """,
        (glob_local.SOURCE_ZCO_ZIP_CODES,),
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        # INFO.00.063 Processed data source '{data_source}'
        io_utils.progress_msg(
            glob_local.INFO_00_063.replace(
                "{data_source}",
                glob_local.SOURCE_ZCO_ZIP_CODES,
            ),
        )
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Insert new data.
    # ------------------------------------------------------------------
    _load_zip_codes_org_data_zips(conn_pg, cur_pg, DOWNLOAD_FILE_ZIP_CODES_ORG)
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Delete and insert averaged data.
    # ------------------------------------------------------------------
    _load_table_io_lat_lng_average(conn_pg, cur_pg)

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    db_utils.upd_io_processed_data(
        cur_pg=cur_pg,
        table_name="io_lat_lng",
        data_source=DOWNLOAD_FILE_ZIP_CODES_ORG,
        task_timestamp=IO_LAST_SEEN,
        url=DOWNLOAD_FILE_ZIP_CODES_ORG_URL,
    )

    cur_pg.close()
    conn_pg.close()


# ------------------------------------------------------------------
# Load the estimated zip code data from the ZIP Code Database
# into the PostgreSQL database.
# ------------------------------------------------------------------
def _load_zip_codes_org_data_zips(
    conn_pg: connection,
    cur_pg: cursor,
    filename: str,
) -> None:
    # INFO.00.061 Database table io_lat_lng: Load the estimated zip code data
    io_utils.progress_msg(glob_local.INFO_00_061)
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            filename,
            sheet_name="zip_code_database",
        )

        count_upsert = 0
        count_select = 0

        # ------------------------------------------------------------------
        # Load the US city data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            if (
                extract_column_value(row, COLUMN_TYPE) != "STANDARD"
                or extract_column_value(row, COLUMN_COUNTRY_LOWER) != "US"
            ):
                continue

            zipcode = f"{extract_column_value(row, COLUMN_ZIP)!s:05}".rstrip()
            primary_city = [
                str(extract_column_value(row, COLUMN_PRIMARY_CITY)).upper().rstrip(),
            ]
            acceptable_cities = (
                str(extract_column_value(row, COLUMN_ACCEPTABLE_CITIES))
                .upper()
                .split(",")
                if extract_column_value(row, COLUMN_ACCEPTABLE_CITIES)
                else []
            )
            state = str(extract_column_value(row, COLUMN_STATE_LOWER)).upper().rstrip()
            lat = extract_column_value(row, COLUMN_LATITUDE_LOWER, float)
            lng = extract_column_value(row, COLUMN_LONGITUDE_LOWER, float)

            primary_city.extend([city.rstrip() for city in acceptable_cities])

            for city in primary_city:
                if city and city.rstrip():

                    cur_pg.execute(
                        """
                    INSERT INTO io_lat_lng AS ill (
                           type,
                           country,
                           state,
                           city,
                           zipcode,
                           dec_latitude,
                           dec_longitude,
                           source,
                           first_processed
                           ) VALUES (
                           %s,%s,%s,%s,%s,
                           %s,%s,%s,%s
                           )
                    ON CONFLICT ON CONSTRAINT io_lat_lng_type_country_state_city_zipcode_key
                    DO UPDATE
                       SET dec_latitude = %s,
                           dec_longitude = %s,
                           source = %s,
                           last_processed = %s
                     WHERE ill.type = %s
                       AND ill.country = %s
                       AND ill.state = %s
                       AND ill.city = %s
                       AND ill.zipcode = %s
                       AND ill.source = %s
                       AND NOT (
                           ill.dec_latitude = %s
                       AND ill.dec_longitude = %s
                       );
                    """,
                        (
                            glob_local.IO_LAT_LNG_TYPE_ZIPCODE,
                            glob_local.COUNTRY_USA,
                            state.rstrip(),
                            city.rstrip(),
                            zipcode.rstrip(),
                            lat,
                            lng,
                            glob_local.SOURCE_ZCO_ZIP_CODES,
                            IO_LAST_SEEN,
                            lat,
                            lng,
                            glob_local.SOURCE_ZCO_ZIP_CODES,
                            IO_LAST_SEEN,
                            glob_local.IO_LAT_LNG_TYPE_ZIPCODE,
                            glob_local.COUNTRY_USA,
                            state.rstrip(),
                            city.rstrip(),
                            zipcode.rstrip(),
                            glob_local.SOURCE_SM_US_CITIES,
                            lat,
                            lng,
                        ),
                    )
                    count_upsert += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_upsert > 0:
            io_utils.progress_msg(f"Number rows upserted : {count_upsert!s:>8}")

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", filename),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", filename).replace(
                "{error}",
                str(err),
            ),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", filename).replace(
                "{error}",
                str(exc),
            ),
        )


# ------------------------------------------------------------------
# Execute a query that returns the list of CICTT codes.
# ------------------------------------------------------------------
def _sql_query_cictt_codes(conn_pg: connection) -> list[str]:
    with conn_pg.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT cictt_code
          FROM io_aviation_occurrence_categories;
        """,
        )

        data = [row["cictt_code"] for row in cur]

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of US states.
# ------------------------------------------------------------------
def _sql_query_us_states(conn_pg: connection) -> list[str]:
    with conn_pg.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT state
          FROM io_states
         WHERE country = 'USA';
        """,
        )

        data = [row["state"] for row in cur]

        return sorted(data)


# ------------------------------------------------------------------
# Execute a query that returns the list of US state names.
# ------------------------------------------------------------------
def _sql_query_us_state_names(conn_pg: connection) -> list[str]:
    with conn_pg.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT state_name
          FROM io_states
         WHERE country = 'USA';
        """,
        )

        data = [row["state_name"] for row in cur]

        return sorted(data)


# -----------------------------------------------------------------------------

def download_us_cities_file() -> None:
    """Download the US cities file from the simplemaps website.

    The function downloads the US cities file from the simplemaps website and stores it in the
    download work directory. The filename is specified in the settings.

    The function checks the status code of the response and checks if the file has been downloaded
    successfully. If not, it terminates with an error message.

    The function also checks if the file is a valid zip file and if it can be unpacked. If the file
    is not a valid zip file or if it cannot be unpacked, it terminates with an error message.

    """
    url = io_settings.settings.download_url_simplemaps_us_cities

    try:
        file_resp = requests.get(
            url=url,
            allow_redirects=True,
            stream=True,
            timeout=io_settings.settings.download_timeout,
        )

        if file_resp.status_code != 200:
            # ERROR.00.906 Unexpected response status code='{status_code}'
            io_utils.terminate_fatal(
                glob_local.ERROR_00_906.replace(
                    "{status_code}",
                    str(file_resp.status_code),
                ),
            )

        # INFO.00.030 The connection to the US city file '{filename}'
        # on the simplemaps download page was successfully established
        io_utils.progress_msg(
            glob_local.INFO_00_030.replace(
                "{filename}",
                io_settings.settings.download_file_simplemaps_us_cities_zip,
            ),
        )

        if not Path(io_settings.settings.download_work_dir).is_dir():
            Path(io_settings.settings.download_work_dir).mkdir(
                parents=True,
                exist_ok=True,
            )

        filename_zip = (
            io_settings.settings.download_work_dir.replace("/", os.sep)
            / io_settings.settings.download_file_simplemaps_us_cities_zip
        )

        no_chunks = 0

        with Path(filename_zip).open("wb") as file_zip:
            for chunk in file_resp.iter_content(
                chunk_size=io_settings.settings.download_chunk_size,
            ):
                file_zip.write(chunk)
                no_chunks += 1

        # INFO.00.023 From the file '{filename}' {no_chunks} chunks were downloaded
        io_utils.progress_msg(
            glob_local.INFO_00_023.replace(
                "{filename}",
                io_settings.settings.download_file_simplemaps_us_cities_zip,
            ).replace("{no_chunks}", str(no_chunks)),
        )

        try:
            zipped_files = zipfile.ZipFile(
                filename_zip,
            )

            for zipped_file in zipped_files.namelist():
                zipped_files.extract(
                    zipped_file,
                    io_settings.settings.download_work_dir,
                )

            zipped_files.close()
        except zipfile.BadZipFile:
            # ERROR.00.907 File '{filename}' is not a zip file
            io_utils.terminate_fatal(
                glob_local.ERROR_00_907.replace("{filename}", filename_zip),
            )

        Path(filename_zip).unlink()
        # INFO.00.024 The file '{filename}'  was successfully unpacked
        io_utils.progress_msg(
            glob_local.INFO_00_024.replace(
                "{filename}",
                io_settings.settings.download_file_simplemaps_us_cities_zip,
            ),
        )
    except ConnectionError:
        # ERROR.00.905 Connection problem with url={url}
        io_utils.terminate_fatal(glob_local.ERROR_00_905.replace("{url}", url))
    except TimeoutError:
        # ERROR.00.909 Timeout after '{timeout}' seconds with url='{url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_909.replace(
                "{timeout}",
                str(io_settings.settings.download_timeout),
            ).replace("{url}", url),
        )


# -----------------------------------------------------------------------------

def download_zip_code_db_file() -> None:
    """Download the ZIP Code Database file.

    The function downloads the ZIP Code Database file from the Zip Codes.org website and stores it
    in the download work directory. The filename is specified in the settings.

    The function checks the status code of the response and checks if the file has been downloaded
    successfully. If not, it terminates with an error message.

    If the file has been downloaded successfully, it prints a message with the filename and the
    number of chunks that have been downloaded.

    """
    url = io_settings.settings.download_url_zip_codes_org

    try:
        file_resp = requests.get(
            url=url,
            allow_redirects=True,
            stream=True,
            timeout=io_settings.settings.download_timeout,
        )

        if file_resp.status_code != 200:
            # ERROR.00.906 Unexpected response status code='{status_code}'
            io_utils.terminate_fatal(
                glob_local.ERROR_00_906.replace(
                    "{status_code}",
                    str(file_resp.status_code),
                ),
            )

        # INFO.00.058 The connection to the Zip Code Database file '{filename}'
        # on the Zip Codes.org download page was successfully established
        io_utils.progress_msg(
            glob_local.INFO_00_058.replace(
                "{filename}",
                DOWNLOAD_FILE_ZIP_CODES_ORG,
            ),
        )

        if not Path(io_settings.settings.download_work_dir).is_dir():
            Path(io_settings.settings.download_work_dir).mkdir(
                parents=True,
                exist_ok=True,
            )

        filename_xls = (
            io_settings.settings.download_work_dir.replace("/", os.sep)
            / DOWNLOAD_FILE_ZIP_CODES_ORG
        )

        no_chunks = 0

        with Path(filename_xls).open("wb") as file_zip:
            for chunk in file_resp.iter_content(
                chunk_size=io_settings.settings.download_chunk_size,
            ):
                file_zip.write(chunk)
                no_chunks += 1

        # INFO.00.023 From the file '{filename}' {no_chunks} chunks were downloaded
        io_utils.progress_msg(
            glob_local.INFO_00_023.replace(
                "{filename}",
                DOWNLOAD_FILE_ZIP_CODES_ORG,
            ).replace(
                "{no_chunks}",
                str(no_chunks),
            ),
        )

    except ConnectionError:
        # ERROR.00.905 Connection problem with url={url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_905.replace("{url}", url),
        )
    except TimeoutError:
        # ERROR.00.909 Timeout after '{timeout}' seconds with url='{url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_909.replace(
                "{timeout}",
                str(io_settings.settings.download_timeout),
            ).replace("{url}", url),
        )


# -----------------------------------------------------------------------------

def load_airport_data() -> None:
    """l_a_p: Load airport data into PostgreSQL.

    This function loads the airport data into the PostgreSQL database.
    The airport data is read from a CSV file and stored into the tables
    'io_airports' and 'io_runways'.
    """
    _load_airport_data()

    _load_runway_data()


# -----------------------------------------------------------------------------

def load_aviation_occurrence_categories() -> None:
    """Load aviation occurrence categories from an Excel file.

    The categories are part of the ICAO common taxonomy, which is used to categorize events. The
    categories are used to link events to their corresponding CICTT codes.

    The function loads the categories from an Excel file into the PostgreSQL database. The Excel
    file is expected to be in the same directory as this module.

    """
    _load_aviation_occurrence_categories()


# -----------------------------------------------------------------------------

def load_country_state_data() -> None:
    """Load country and state data from various sources and save it into the PostgreSQL database.

    The function first loads the country data from a CSV file into a pandas DataFrame. Then, it
    loads the state data from an Excel file into another pandas DataFrame. The data is then saved
    into the 'io_countries' and 'io_states' tables in the PostgreSQL database.

    :return: None

    """
    # Load the country data.
    dataframe: DataFrame

    try:
        # Send HTTP GET request to download the CSV data
        response = requests.get(COUNTRIES_URL, timeout=COUNTRIES_TIMEOUT)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Decode the content to a string (assuming UTF-8 encoding)
        csv_data = response.content.decode("utf-8")

        # Use StringIO to convert the string data into a file-like object
        csv_buffer = StringIO(csv_data)

        # Define the desired columns without trailing comma
        desired_columns = ["cca3", "name.common", "latlng"]

        # Read the CSV data into a pandas DataFrame, selecting only desired columns
        dataframe = pd.read_csv(csv_buffer, usecols=desired_columns)

    except requests.RequestException as e:
        logging.fatal(glob_local.FATAL_00_972.replace("{error}", str(e)))
        sys.exit(1)

    _load_country_data(dataframe)

    # ------------------------------------------------------------------
    # Load the state data.
    # ------------------------------------------------------------------

    # Reference to the working directory as a Path object
    workdir_path = Path(OPENDATASOFT_WORKDIR)

    # Delete and recreate the working directory
    if workdir_path.exists() and workdir_path.is_dir():
        shutil.rmtree(workdir_path)

    workdir_path.mkdir(parents=True, exist_ok=True)

    file_path = Path(OPENDATASOFT_WORKDIR) / OPENDATASOFT_US_STATE_BOUNDARIES_FILE

    # Download and extract data
    _download_file(
        url=OPENDATASOFT_US_STATE_BOUNDARIES_URL,
        file_path=file_path,
        timeout=OPENDATASOFT_TIMEOUT,
    )

    _load_state_data(file_path)


# -----------------------------------------------------------------------------

def load_sequence_of_events() -> None:
    """Load sequence of events sequence data.

    This function loads sequence of events sequence data from a CSV file into the PostgreSQL
    database. The data is loaded into the 'seq_of_events' table.

    The function starts by deleting any existing data from the table and then loads the data from
    the CSV file.

    The function then finalizes the processing by closing the database connection.

    """
    _load_sequence_of_events()


# -----------------------------------------------------------------------------

def load_simplemaps_data() -> None:
    """Load simplemaps data.

    This function loads data from simplemaps into the PostgreSQL database. The
    data is loaded into the 'io_lat_lng' table.

    The data loaded is from two sources:

    1. A US city file
    2. A US zip code file

    The data from the two sources is loaded into two separate tables and then
    averaged into a third table.

    The function starts by deleting any existing data from the two sources
    and then loads the data from the two sources. The data is then averaged
    and inserted into the third table.

    The function then finalizes the processing by closing the database
    connection.

    """
    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Delete existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
    DELETE FROM io_lat_lng
    WHERE SOURCE IN (%s, %s);
    """,
        (
            glob_local.SOURCE_SM_US_CITIES,
            glob_local.SOURCE_SM_US_ZIP_CODES,
        ),
    )

    if cur_pg.rowcount > 0:
        conn_pg.commit()

        # INFO.00.063 Processed data source '{data_source}'
        io_utils.progress_msg(
            glob_local.INFO_00_063.replace(
                "{data_source}",
                glob_local.SOURCE_SM_US_CITIES,
            ),
        )
        io_utils.progress_msg(
            glob_local.INFO_00_063.replace(
                "{data_source}",
                glob_local.SOURCE_SM_US_ZIP_CODES,
            ),
        )
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load zip data from a US city file.
    # ------------------------------------------------------------------
    _load_simplemaps_data_zips_from_us_cities(conn_pg, cur_pg)

    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load zip data from a US zip code file.
    # ------------------------------------------------------------------
    _load_simplemaps_data_zips_from_us_zips(conn_pg, cur_pg)

    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load city data from a US city file.
    # ------------------------------------------------------------------
    _load_simplemaps_data_cities_from_us_cities(conn_pg, cur_pg)

    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Delete and insert averaged data.
    # ------------------------------------------------------------------
    _load_table_io_lat_lng_average(conn_pg, cur_pg)

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    cur_pg.close()
    conn_pg.close()


# -----------------------------------------------------------------------------

def load_zip_codes_org_data() -> None:
    """Load ZIP Code Database data.

    This function loads data from the ZIP Code Database file into the PostgreSQL database. The data
    is loaded into the 'io_lat_lng' table.

    """
    _load_zip_codes_org_data()
