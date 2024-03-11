# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.

"""Managing the database schema of the PostgreSQL database."""
import json
import logging
import os
import zipfile
from datetime import datetime
from datetime import timezone

import pandas as pd
import requests
from iocommon import db_utils
from iocommon import io_config
from iocommon import io_glob
from iocommon import io_utils
from iocommon.io_utils import extract_column_value
from psycopg import connection
from psycopg import cursor
from psycopg.errors import ForeignKeyViolation  # pylint: disable=no-name-in-module
from psycopg.errors import UniqueViolation  # pylint: disable=no-name-in-module

from ioavstats import glob_local
from ioavstats import utils

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

COLUMN_ACCEPTABLE_CITIES = "acceptable_cities"
COLUMN_AIRANAL = "AIRANAL"
COLUMN_AIRPORT_ID = "AIRPORT_ID"
COLUMN_CICTT_CODE_SPACE = "CICTT Code"
COLUMN_CICTT_CODE_UNDERSCORE = "CICTT_Code"
COLUMN_CITY = "city"
COLUMN_COMP_CODE = "COMP_CODE"
COLUMN_COUNTRY_LOWER = "country"
COLUMN_COUNTRY_UPPER = "COUNTRY"
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
COLUMN_OPERSTATUS = "OPERSTATUS"
COLUMN_PRIMARY_CITY = "primary_city"
COLUMN_PRIVATEUSE = "PRIVATEUSE"
COLUMN_SERVCITY = "SERVCITY"
COLUMN_STATE_CAMEL = "State"
COLUMN_STATE_ID = "state_id"
COLUMN_STATE_LOWER = "state"
COLUMN_STATE_UPPER = "STATE"
COLUMN_TYPE = "type"
COLUMN_TYPE_CODE = "TYPE_CODE"
COLUMN_X = "X"
COLUMN_Y = "Y"
COLUMN_ZIP = "zip"
COLUMN_ZIPS = "zips"

FILE_AVIATION_OCCURRENCE_CATEGORIES = (
    io_config.settings.download_file_aviation_occurrence_categories
)
FILE_FAA_AIRPORTS = io_config.settings.download_file_faa_airports
FILE_FAA_NPIAS_DATA = io_config.settings.download_file_faa_npias
FILE_FAA_RUNWAYS = io_config.settings.download_file_faa_runways
FILE_SEQUENCE_OF_EVENTS = io_config.settings.download_file_sequence_of_events
FILE_SIMPLEMAPS_US_CITIES = io_config.settings.download_file_simplemaps_us_cities
FILE_SIMPLEMAPS_US_ZIPS = io_config.settings.download_file_simplemaps_us_zips
FILE_ZIP_CODES_ORG = io_config.settings.download_file_zip_codes_org

IO_LAST_SEEN = datetime.now(timezone.utc)

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Load airport data from an MS Excel file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
def _load_airport_data() -> None:
    logger.debug(io_glob.LOGGER_START)

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
        io_utils.progress_msg(f"Number rows deleted  : {str(cur_pg.rowcount):>8}")

    # ------------------------------------------------------------------
    # Start processing airport data.
    # ------------------------------------------------------------------

    us_states: list[str] = _sql_query_us_states(conn_pg)

    locids: list[str] = _load_npias_data(us_states)

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
        dataframe = pd.read_csv(FILE_FAA_AIRPORTS, sep=",", usecols=columns)

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_FAA_AIRPORTS)
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", FILE_FAA_AIRPORTS)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", FILE_FAA_AIRPORTS).replace(
                "{error}", str(err)
            )
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", FILE_FAA_AIRPORTS).replace(
                "{error}", str(exc)
            )
        )

    # INFO.00.089 Database table io_airports: Load data from file '{filename}'
    io_utils.progress_msg("-" * 80)
    io_utils.progress_msg(
        glob_local.INFO_00_089.replace("{filename}", FILE_FAA_AIRPORTS)
    )

    count_select = 0
    count_upsert = 0
    count_usable = 0

    # ------------------------------------------------------------------
    # Load the airport data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
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

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
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
                datetime.now(),
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
                datetime.now(),
                global_id,
            ),
        )
        count_upsert += cur_pg.rowcount

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    utils.upd_io_processed_files(
        io_config.settings.download_file_sequence_of_events, cur_pg
    )

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load aviation occurrence categories from an MS Excel file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def _load_aviation_occurrence_categories() -> None:
    logger.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_AVIATION_OCCURRENCE_CATEGORIES.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.937 The aviation occurrence categories file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_937.replace("{filename}", filename_excel)
        )

    # INFO.00.074 Database table io_aviation_occurrence_categories: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_074.replace(
            "{filename}",
            FILE_AVIATION_OCCURRENCE_CATEGORIES,
        )
    )
    io_utils.progress_msg("-" * 80)

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_AVIATION_OCCURRENCE_CATEGORIES,
            sheet_name="Sheet1",
        )

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace(
                "{file_name}", FILE_AVIATION_OCCURRENCE_CATEGORIES
            )
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}", FILE_AVIATION_OCCURRENCE_CATEGORIES
            ).replace("{error}", str(err))
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}", FILE_AVIATION_OCCURRENCE_CATEGORIES
            ).replace("{error}", str(exc))
        )

    # INFO.00.074 Database table io_aviation_occurrence_categories: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_074.replace(
            "{filename}", FILE_AVIATION_OCCURRENCE_CATEGORIES
        )
    )

    count_delete = 0
    count_upsert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the aviation occurrence categories.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
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
                datetime.now(),
                IO_LAST_SEEN,
                identifier,
                definition,
                datetime.now(),
                IO_LAST_SEEN,
                cictt_code,
            ),
        )
        count_upsert += cur_pg.rowcount

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    # ------------------------------------------------------------------
    # Delete the obsolete data.
    # ------------------------------------------------------------------

    count_select = 0

    # pylint: disable=line-too-long
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

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        cictt_code = row_pg["cictt_code"]  # type: ignore

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
        io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")
    if count_delete > 0:
        io_utils.progress_msg(f"Number rows deleted  : {str(count_delete):>8}")

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    utils.upd_io_processed_files(FILE_AVIATION_OCCURRENCE_CATEGORIES, cur_pg)

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load country data from a JSON file.
# ------------------------------------------------------------------
def _load_country_data(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_json = os.path.join(
        os.getcwd(),
        io_config.settings.download_file_countries_states_json.replace("/", os.sep),
    )

    if not os.path.isfile(filename_json):
        # ERROR.00.934 The country and state data file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_934.replace("{filename}", filename_json)
        )

    count_insert = 0
    count_select = 0
    count_update = 0

    with open(filename_json, "r", encoding=io_glob.FILE_ENCODING_DEFAULT) as input_file:
        input_data = json.load(input_file)

        for record in input_data:
            count_select += 1

            if record["type"] == "country":
                try:
                    cur_pg.execute(
                        """
                    INSERT INTO io_countries (
                           country,country_name,dec_latitude,dec_longitude,first_processed
                           ) VALUES (
                           %s,%s,%s,%s,%s);
                    """,
                        (
                            record["country"],
                            record["country_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                            datetime.now(),
                        ),
                    )
                    count_insert += 1
                except UniqueViolation:
                    # pylint: disable=line-too-long
                    cur_pg.execute(
                        """
                    UPDATE io_countries SET
                           country_name = %s,
                           dec_latitude = %s,
                           dec_longitude = %s,
                           last_processed = %s
                     WHERE country = %s
                       AND NOT (country_name = %s
                            AND dec_latitude = %s
                            AND dec_longitude = %s);
                    """,
                        (
                            record["country_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                            datetime.now(),
                            record["country"],
                            record["country_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                        ),
                    )
                    count_update += cur_pg.rowcount

    utils.upd_io_processed_files(
        io_config.settings.download_file_countries_states_json, cur_pg
    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load NPIAS data from an MS Excel file.
# ------------------------------------------------------------------
def _load_npias_data(us_states) -> list[str]:
    # ------------------------------------------------------------------
    # Start processing NPIAS data.
    # ------------------------------------------------------------------

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_FAA_NPIAS_DATA.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.945 The NPIAS file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_945.replace("{filename}", filename_excel)
        )

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_FAA_NPIAS_DATA,
            sheet_name="All NPIAS Airports",
        )

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_FAA_NPIAS_DATA)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", FILE_FAA_NPIAS_DATA).replace(
                "{error}", str(err)
            )
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", FILE_FAA_NPIAS_DATA).replace(
                "{error}", str(exc)
            )
        )

    count_select = 0
    count_usable = 0

    locids: list[str] = []

    # ------------------------------------------------------------------
    # Load the NPIAS data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if not extract_column_value(row, COLUMN_STATE_CAMEL) in us_states:
            continue

        locids.append(extract_column_value(row, COLUMN_LOCID))

        count_usable += 1

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")
    io_utils.progress_msg(f"Number rows usable   : {str(count_usable):>8}")

    return locids


# ------------------------------------------------------------------
# Load runway data from an MS Excel file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def _load_runway_data() -> None:
    logger.debug(io_glob.LOGGER_START)

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

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")
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
        dataframe = pd.read_csv(FILE_FAA_RUNWAYS, sep=",", usecols=columns)

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_FAA_RUNWAYS)
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", FILE_FAA_RUNWAYS)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", FILE_FAA_RUNWAYS).replace(
                "{error}", str(err)
            )
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", FILE_FAA_RUNWAYS).replace(
                "{error}", str(exc)
            )
        )

    # INFO.00.092 Database table io_runways: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_092.replace("{filename}", FILE_FAA_RUNWAYS)
    )

    count_select = 0

    # ------------------------------------------------------------------
    # Load the runway data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
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

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the runway data.
    # ------------------------------------------------------------------

    # INFO.00.090 Database table io_airports: Update the runway data
    io_utils.progress_msg(glob_local.INFO_00_090)

    count_select = 0
    count_update = 0

    # pylint: disable=R0801
    for airport_id, (comp_code, length) in runway_data.items():
        count_select += 1

        if comp_code is None:
            continue

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
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
                datetime.now(),
                airport_id,
            ),
        )
        count_update += cur_pg.rowcount

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    utils.upd_io_processed_files(
        io_config.settings.download_file_sequence_of_events, cur_pg
    )

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load sequence of events sequence data from an MS Excel file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def _load_sequence_of_events() -> None:
    logger.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    # INFO.00.076 Database table io_sequence_of_events: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_076.replace(
            "{filename}", io_config.settings.download_file_sequence_of_events
        )
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
        dataframe = pd.read_csv(FILE_SEQUENCE_OF_EVENTS, sep=",", usecols=columns)

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_SEQUENCE_OF_EVENTS)
        )

    except pd.errors.EmptyDataError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_932.replace("{file_name}", FILE_SEQUENCE_OF_EVENTS)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}", FILE_SEQUENCE_OF_EVENTS
            ).replace("{error}", str(err))
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}", FILE_SEQUENCE_OF_EVENTS
            ).replace("{error}", str(exc))
        )

    # INFO.00.076 Database table io_sequence_of_events: Load data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_076.replace("{filename}", FILE_SEQUENCE_OF_EVENTS)
    )

    count_delete = 0
    count_upsert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the sequence of events data.
    # ------------------------------------------------------------------

    cictt_codes = _sql_query_cictt_codes(conn_pg)

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        soe_no = extract_column_value(row, COLUMN_EVENTSOE_NO).rjust(3, "0")

        cictt_code = str(
            extract_column_value(row, COLUMN_CICTT_CODE_UNDERSCORE)
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
                datetime.now(),
                IO_LAST_SEEN,
                meaning,
                cictt_code,
                datetime.now(),
                IO_LAST_SEEN,
                soe_no,
            ),
        )
        count_upsert += cur_pg.rowcount

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    # ------------------------------------------------------------------
    # Delete the obsolete data.
    # ------------------------------------------------------------------

    count_select = 0

    # pylint: disable=line-too-long
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

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        soe_no = row_pg["soe_no"]  # type: ignore

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
        io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")
    if count_delete > 0:
        io_utils.progress_msg(f"Number rows deleted  : {str(count_delete):>8}")

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    utils.upd_io_processed_files(
        io_config.settings.download_file_sequence_of_events, cur_pg
    )

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load city data from a US city file.
# ------------------------------------------------------------------
# pylint: disable=too-many-locals
def _load_simplemaps_data_cities_from_us_cities(
    conn_pg: connection, cur_pg: cursor
) -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_SIMPLEMAPS_US_CITIES.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.914 The US city file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_914.replace("{filename}", filename_excel)
        )

    # INFO.00.027 Database table io_lat_lng: Load city data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_027.replace("{filename}", FILE_SIMPLEMAPS_US_CITIES)
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_SIMPLEMAPS_US_CITIES,
            sheet_name="Sheet1",
        )

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_SIMPLEMAPS_US_CITIES)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_CITIES
            ).replace("{error}", str(err))
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_CITIES
            ).replace("{error}", str(exc))
        )

    count_upsert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the US city data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
        lat = extract_column_value(row, COLUMN_LAT, float)
        lng = extract_column_value(row, COLUMN_LNG, float)
        state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()

        # pylint: disable=line-too-long
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
                datetime.now(),
                lat,
                lng,
                glob_local.SOURCE_SM_US_CITIES,
                datetime.now(),
                glob_local.IO_LAT_LNG_TYPE_CITY,
                glob_local.COUNTRY_USA,
                state_id,
                city,
                lat,
                lng,
            ),
        )
        count_upsert += cur_pg.rowcount

    utils.upd_io_processed_files(FILE_SIMPLEMAPS_US_CITIES, cur_pg)

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load zip data from a US city file.
# ------------------------------------------------------------------
# pylint: disable=R0801
# pylint: disable=too-many-locals
def _load_simplemaps_data_zips_from_us_cities(
    conn_pg: connection, cur_pg: cursor
) -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_SIMPLEMAPS_US_CITIES.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.914 The US city file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_914.replace("{filename}", filename_excel)
        )

    # INFO.00.039 Database table io_lat_lng: Load zipcode data from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_039.replace("{filename}", FILE_SIMPLEMAPS_US_CITIES)
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_SIMPLEMAPS_US_CITIES,
            sheet_name="Sheet1",
        )

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_SIMPLEMAPS_US_CITIES)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_CITIES
            ).replace("{error}", str(err))
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_CITIES
            ).replace("{error}", str(exc))
        )

    count_insert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the US city data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
        lat = extract_column_value(row, COLUMN_LAT, float)
        lng = extract_column_value(row, COLUMN_LNG, float)
        state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()
        zips = list(f"{extract_column_value(row, COLUMN_ZIPS)}".split(" "))

        for zipcode in zips:
            count_select += 1
            if count_select % io_config.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {str(count_select):>8}"
                )

            # pylint: disable=line-too-long
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
                    datetime.now(),
                ),
            )
            count_insert += cur_pg.rowcount

    utils.upd_io_processed_files(FILE_SIMPLEMAPS_US_CITIES, cur_pg)

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load zip data from a US zip code file.
# ------------------------------------------------------------------
# pylint: disable=too-many-locals
def _load_simplemaps_data_zips_from_us_zips(
    conn_pg: connection, cur_pg: cursor
) -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_SIMPLEMAPS_US_ZIPS.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.913 The US zip code file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_913.replace("{filename}", filename_excel)
        )

    # INFO.00.025 Database table io_lat_lng: Load zipcode data rom file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_025.replace(
            "{filename}", io_config.settings.download_file_simplemaps_us_zips
        )
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_SIMPLEMAPS_US_ZIPS,
            sheet_name="Sheet1",
        )

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_SIMPLEMAPS_US_ZIPS)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_ZIPS
            ).replace("{error}", str(err))
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}", FILE_SIMPLEMAPS_US_ZIPS
            ).replace("{error}", str(exc))
        )

    count_duplicates = 0
    count_upsert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the US zip data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        zip_code = f"{extract_column_value(row, COLUMN_ZIP):05}".rstrip()
        city = str(extract_column_value(row, COLUMN_CITY)).upper().rstrip()
        lat = extract_column_value(row, COLUMN_LAT, float)
        lng = extract_column_value(row, COLUMN_LNG, float)
        state_id = str(extract_column_value(row, COLUMN_STATE_ID)).upper().rstrip()

        # pylint: disable=line-too-long
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
                datetime.now(),
                lat,
                lng,
                glob_local.SOURCE_SM_US_ZIP_CODES,
                datetime.now(),
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

    utils.upd_io_processed_files(
        io_config.settings.download_file_simplemaps_us_zips, cur_pg
    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    if count_duplicates > 0:
        io_utils.progress_msg(f"Number rows duplicate: {str(count_duplicates):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load state data from a JSON file.
# ------------------------------------------------------------------
def _load_state_data(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_json = os.path.join(
        os.getcwd(),
        io_config.settings.download_file_countries_states_json.replace("/", os.sep),
    )

    if not os.path.isfile(filename_json):
        # ERROR.00.934 The country and state data file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_934.replace("{filename}", filename_json)
        )

    count_insert = 0
    count_select = 0
    count_update = 0

    with open(filename_json, "r", encoding=io_glob.FILE_ENCODING_DEFAULT) as input_file:
        input_data = json.load(input_file)

        for record in input_data:
            count_select += 1

            if record["type"] == "state":
                try:
                    cur_pg.execute(
                        """
                    INSERT INTO io_states (
                           country,state, state_name,dec_latitude,dec_longitude,first_processed
                           ) VALUES (%s,%s,%s,%s,%s,%s);
                    """,
                        (
                            record["country"],
                            record["state"],
                            record["state_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                            datetime.now(),
                        ),
                    )
                    count_insert += 1
                except UniqueViolation:
                    cur_pg.execute(
                        """
                    UPDATE io_states SET
                           state_name = %s,dec_latitude = %s,dec_longitude = %s,last_processed = %s
                     WHERE
                           country = %s AND state = %s
                       AND NOT (state_name = %s AND dec_latitude = %s AND dec_longitude = %s);
                    """,
                        (
                            record["state_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                            datetime.now(),
                            record["country"],
                            record["state"],
                            record["state_name"],
                            record["dec_latitude"],
                            record["dec_longitude"],
                        ),
                    )
                    count_update += cur_pg.rowcount

    utils.upd_io_processed_files(
        io_config.settings.download_file_countries_states_json, cur_pg
    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")

    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Determine and load city averages.
# ------------------------------------------------------------------
def _load_table_io_lat_lng_average(conn_pg, cur_pg) -> None:
    logger.debug(io_glob.LOGGER_START)

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
            glob_local.INFO_00_063.replace("{data_source}", glob_local.SOURCE_AVERAGE)
        )
        io_utils.progress_msg(f"Number rows deleted  : {str(cur_pg.rowcount):>8}")
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

    # pylint: disable=line-too-long
    cur_pg_2.execute(
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
    )

    for row_pg in cur_pg_2.fetchall():
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
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
                    row_pg["country"],  # type: ignore
                    row_pg["state"],  # type: ignore
                    row_pg["city"],  # type: ignore
                    row_pg["dec_latitude"],  # type: ignore
                    row_pg["dec_longitude"],  # type: ignore
                    glob_local.SOURCE_AVERAGE,
                    datetime.now(),
                ),
            )
            count_insert += 1
        except UniqueViolation:
            count_duplicates += cur_pg.rowcount

    conn_pg.commit()

    cur_pg_2.close()
    conn_pg_2.close()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")

    if count_duplicates > 0:
        io_utils.progress_msg(f"Number rows duplicate: {str(count_duplicates):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load ZIP Code Database data.
# ------------------------------------------------------------------
def _load_zip_codes_org_data() -> None:
    logger.debug(io_glob.LOGGER_START)

    filename_excel = os.path.join(
        os.getcwd(),
        FILE_ZIP_CODES_ORG.replace("/", os.sep),
    )

    if not os.path.isfile(filename_excel):
        # ERROR.00.935 The Zip Code Database file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_935.replace("{filename}", filename_excel)
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
                "{data_source}", glob_local.SOURCE_ZCO_ZIP_CODES
            )
        )
        io_utils.progress_msg(f"Number rows deleted  : {str(cur_pg.rowcount):>8}")
        io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Insert new data.
    # ------------------------------------------------------------------
    _load_zip_codes_org_data_zips(conn_pg, cur_pg, FILE_ZIP_CODES_ORG)
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Delete and insert averaged data.
    # ------------------------------------------------------------------
    _load_table_io_lat_lng_average(conn_pg, cur_pg)

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------
    utils.upd_io_processed_files(FILE_ZIP_CODES_ORG, cur_pg)

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the estimated zip code data from the ZIP Code Database
# into the PostgreSQL database.
# ------------------------------------------------------------------
def _load_zip_codes_org_data_zips(conn_pg, cur_pg, filename) -> None:
    logger.debug(io_glob.LOGGER_START)

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

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", filename)
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace("{file_name}", filename).replace(
                "{error}", str(err)
            )
        )

    except Exception as exc:  # pylint: disable=broad-exception-caught
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace("{file_name}", filename).replace(
                "{error}", str(exc)
            )
        )

    count_upsert = 0
    count_select = 0

    # ------------------------------------------------------------------
    # Load the US city data.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    for _index, row in dataframe.iterrows():

        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        if (
            extract_column_value(row, COLUMN_TYPE) != "STANDARD"
            or extract_column_value(row, COLUMN_COUNTRY_LOWER) != "US"
        ):
            continue

        zipcode = f"{str(extract_column_value(row, COLUMN_ZIP)):05}".rstrip()
        primary_city = [
            str(extract_column_value(row, COLUMN_PRIMARY_CITY)).upper().rstrip()
        ]
        acceptable_cities = (
            str(extract_column_value(row, COLUMN_ACCEPTABLE_CITIES)).upper().split(",")
            if extract_column_value(row, COLUMN_ACCEPTABLE_CITIES)
            else []
        )
        state = str(extract_column_value(row, COLUMN_STATE_LOWER)).upper().rstrip()
        lat = extract_column_value(row, COLUMN_LATITUDE_LOWER, float)
        lng = extract_column_value(row, COLUMN_LONGITUDE_LOWER, float)

        for city in acceptable_cities:
            primary_city.append(city.rstrip())

        for city in primary_city:
            if city and city.rstrip():
                # pylint: disable=line-too-long
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
                        datetime.now(),
                        lat,
                        lng,
                        glob_local.SOURCE_ZCO_ZIP_CODES,
                        datetime.now(),
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

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_upsert > 0:
        io_utils.progress_msg(f"Number rows upserted : {str(count_upsert):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Execute a query that returns the list of CICTT codes.
# ------------------------------------------------------------------
def _sql_query_cictt_codes(conn_pg: connection) -> list[str]:
    with conn_pg.cursor() as cur:  # type: ignore
        cur.execute(
            """
        SELECT cictt_code
          FROM io_aviation_occurrence_categories;
        """
        )

        data = []

        for row in cur:
            data.append(row["cictt_code"])

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
        """
        )

        data = []

        for row in cur:
            data.append(row["state"])

        return sorted(data)


# ------------------------------------------------------------------
# Download a US zip code file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def download_us_cities_file() -> None:
    """Download a US zip code file."""
    logger.debug(io_glob.LOGGER_START)

    url = io_config.settings.download_url_simplemaps_us_cities

    try:
        file_resp = requests.get(
            url=url,
            allow_redirects=True,
            stream=True,
            timeout=io_config.settings.download_timeout,
        )

        if file_resp.status_code != 200:
            # ERROR.00.906 Unexpected response status code='{status_code}'
            io_utils.terminate_fatal(
                glob_local.ERROR_00_906.replace(
                    "{status_code}", str(file_resp.status_code)
                )
            )

        # INFO.00.030 The connection to the US city file '{filename}'
        # on the simplemaps download page was successfully established
        io_utils.progress_msg(
            glob_local.INFO_00_030.replace(
                "{filename}", io_config.settings.download_file_simplemaps_us_cities_zip
            )
        )

        if not os.path.isdir(io_config.settings.download_work_dir):
            os.makedirs(io_config.settings.download_work_dir)

        filename_zip = os.path.join(
            io_config.settings.download_work_dir.replace("/", os.sep),
            io_config.settings.download_file_simplemaps_us_cities_zip,
        )

        no_chunks = 0

        with open(filename_zip, "wb") as file_zip:
            for chunk in file_resp.iter_content(
                chunk_size=io_config.settings.download_chunk_size
            ):
                file_zip.write(chunk)
                no_chunks += 1

        # INFO.00.023 From the file '{filename}' {no_chunks} chunks were downloaded
        io_utils.progress_msg(
            glob_local.INFO_00_023.replace(
                "{filename}", io_config.settings.download_file_simplemaps_us_cities_zip
            ).replace("{no_chunks}", str(no_chunks))
        )

        try:
            zipped_files = zipfile.ZipFile(  # pylint: disable=consider-using-with
                filename_zip
            )

            for zipped_file in zipped_files.namelist():
                zipped_files.extract(zipped_file, io_config.settings.download_work_dir)

            zipped_files.close()
        except zipfile.BadZipFile:
            # ERROR.00.907 File '{filename}' is not a zip file
            io_utils.terminate_fatal(
                glob_local.ERROR_00_907.replace("{filename}", filename_zip)
            )

        os.remove(filename_zip)
        # INFO.00.024 The file '{filename}'  was successfully unpacked
        io_utils.progress_msg(
            glob_local.INFO_00_024.replace(
                "{filename}", io_config.settings.download_file_simplemaps_us_cities_zip
            )
        )
    except ConnectionError:
        # ERROR.00.905 Connection problem with url='{url}'
        io_utils.terminate_fatal(glob_local.ERROR_00_905.replace("{url}", url))
    except TimeoutError:
        # ERROR.00.909 Timeout after '{timeout}' seconds with url='{url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_909.replace(
                "{timeout}", str(io_config.settings.download_timeout)
            ).replace("{url}", url)
        )

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Download the ZIP Code Database file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def download_zip_code_db_file() -> None:
    """Download the ZIP Code Database file."""
    logger.debug(io_glob.LOGGER_START)

    url = io_config.settings.download_url_zip_codes_org

    try:
        file_resp = requests.get(
            url=url,
            allow_redirects=True,
            stream=True,
            timeout=io_config.settings.download_timeout,
        )

        if file_resp.status_code != 200:
            # ERROR.00.906 Unexpected response status code='{status_code}'
            io_utils.terminate_fatal(
                glob_local.ERROR_00_906.replace(
                    "{status_code}", str(file_resp.status_code)
                )
            )

        # INFO.00.058 The connection to the Zip Code Database file '{filename}'
        # on the Zip Codes.org download page was successfully established
        io_utils.progress_msg(
            glob_local.INFO_00_058.replace("{filename}", FILE_ZIP_CODES_ORG)
        )

        if not os.path.isdir(io_config.settings.download_work_dir):
            os.makedirs(io_config.settings.download_work_dir)

        filename_xls = os.path.join(
            io_config.settings.download_work_dir.replace("/", os.sep),
            FILE_ZIP_CODES_ORG,
        )

        no_chunks = 0

        with open(filename_xls, "wb") as file_zip:
            for chunk in file_resp.iter_content(
                chunk_size=io_config.settings.download_chunk_size
            ):
                file_zip.write(chunk)
                no_chunks += 1

        # INFO.00.023 From the file '{filename}' {no_chunks} chunks were downloaded
        io_utils.progress_msg(
            glob_local.INFO_00_023.replace("{filename}", FILE_ZIP_CODES_ORG).replace(
                "{no_chunks}", str(no_chunks)
            )
        )

    except ConnectionError:
        # ERROR.00.905 Connection problem with url='{url}'
        io_utils.terminate_fatal(glob_local.ERROR_00_905.replace("{url}", url))
    except TimeoutError:
        # ERROR.00.909 Timeout after '{timeout}' seconds with url='{url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_909.replace(
                "{timeout}", str(io_config.settings.download_timeout)
            ).replace("{url}", url)
        )

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load airports.
# ------------------------------------------------------------------
def load_airport_data() -> None:
    """Load airports."""
    logger.debug(io_glob.LOGGER_START)

    _load_airport_data()

    _load_runway_data()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load aviation occurrence categories.
# ------------------------------------------------------------------
def load_aviation_occurrence_categories() -> None:
    """Load aviation occurrence categories."""
    logger.debug(io_glob.LOGGER_START)

    _load_aviation_occurrence_categories()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load country and state data.
# ------------------------------------------------------------------
def load_country_state_data() -> None:
    """Load country and state data."""
    logger.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # ------------------------------------------------------------------
    # Load the country data.
    # ------------------------------------------------------------------

    # INFO.00.059 Load country data
    io_utils.progress_msg(glob_local.INFO_00_059)
    io_utils.progress_msg("-" * 80)
    _load_country_data(
        conn_pg,
        cur_pg,
    )

    # ------------------------------------------------------------------
    # Load the state data.
    # ------------------------------------------------------------------

    io_utils.progress_msg("-" * 80)

    # INFO.00.060 Load state data
    io_utils.progress_msg(glob_local.INFO_00_060)
    io_utils.progress_msg("-" * 80)
    _load_state_data(
        conn_pg,
        cur_pg,
    )

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    utils.upd_io_processed_files(
        io_config.settings.download_file_countries_states_json, cur_pg
    )

    cur_pg.close()
    conn_pg.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load sequence of events sequence data.
# ------------------------------------------------------------------
def load_sequence_of_events() -> None:
    """Load sequence of events sequence data."""
    logger.debug(io_glob.LOGGER_START)

    _load_sequence_of_events()

    # pylint: disable=R0801
    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load simplemaps data.
# ------------------------------------------------------------------
def load_simplemaps_data() -> None:
    """Load simplemaps data."""
    logger.debug(io_glob.LOGGER_START)

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
                "{data_source}", glob_local.SOURCE_SM_US_CITIES
            )
        )
        io_utils.progress_msg(
            glob_local.INFO_00_063.replace(
                "{data_source}", glob_local.SOURCE_SM_US_ZIP_CODES
            )
        )
        io_utils.progress_msg(f"Number rows deleted  : {str(cur_pg.rowcount):>8}")
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

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load ZIP Code Database data.
# ------------------------------------------------------------------
def load_zip_codes_org_data() -> None:
    """Load ZIP Code Database data."""
    logger.debug(io_glob.LOGGER_START)

    _load_zip_codes_org_data()

    logger.debug(io_glob.LOGGER_END)
