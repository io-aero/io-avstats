# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Managing the database schema of the PostgreSQL database."""
import logging
import os.path
from pathlib import Path

import pandas as pd
from iocommon import db_utils, io_glob, io_settings, io_utils
from iocommon.io_utils import extract_column_value
from psycopg import DatabaseError, connection, cursor
from psycopg.errors import (
    DuplicateDatabase,
    DuplicateObject,
)

from ioavstats import glob_local

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

COLUMN_CATEGORY_NO = "category_no"
COLUMN_COUNT = "count"
COLUMN_DESCRIPTION = "description"
COLUMN_EVENTSOE_NO = "eventsoe_no"
COLUMN_FINDING_DESCRIPTION = "finding_description"
COLUMN_MAIN_PHASE = "main_phase"
COLUMN_MODIFIER_DESCRIPTION = "modifier_description"
COLUMN_MODIFIER_NO = "modifier_no"
COLUMN_OCCURRENCE_DESCRIPTION = "occurrence_description"
COLUMN_PHASE_CODE = "phase_code"
COLUMN_PHASE_NO = "phase_no"
COLUMN_SECTION_NO = "section_no"
COLUMN_SUBCATEGORY_CODE = "subcategory_code"
COLUMN_SUBCATEGORY_NO = "subcategory_no"
COLUMN_SUBSECTION_NO = "subsection_no"
COLUMN_TABLE_NAME = "table_name"

DLL_TABLE_STMNTS: dict[str, str] = {}
DLL_VIEW_STMNTS_CREATE: dict[str, str] = {}
DLL_VIEW_STMNTS_CREATE_MAT: dict[str, str] = {}
DLL_VIEW_STMNTS_DROP: list[str] = []
DLL_VIEW_STMNTS_REFRESH: list[str] = []

FILE_MAIN_PHASES_OF_FLIGHT = io_settings.settings.download_file_main_phases_of_flight


# -----------------------------------------------------------------------------

def _alter_db_tables(conn_pg: connection, cur_pg: cursor) -> None:
    """Alter existing database tables.

    This function checks if a database table exists and if it does, it alters the table according to
    the given SQL statement.

    :param conn_pg: The PostgreSQL database connection.
    :param cur_pg: The PostgreSQL database cursor.

    """
    # Iterate over the SQL statements for the tables to be created
    for table_name, stmnt in DLL_TABLE_STMNTS.items():
        # Check if the database table already exists
        if _check_exists_table(cur_pg, table_name):
            # Alter the database table
            cur_pg.execute(stmnt)
            # Commit the changes
            conn_pg.commit()
            # Log the action
            io_utils.progress_msg(
                glob_local.INFO_00_007.replace("{table}", table_name),
            )


# -----------------------------------------------------------------------------

def _check_exists_index(
    cur_pg: cursor,
    index_name: str,
) -> bool:
    """Check if a database index exists.

    :param cur_pg: The PostgreSQL database cursor.
    :param index_name: The name of the index to be checked.
    :return: True if the index exists, False otherwise.

    """
    # Execute the SQL statement
    cur_pg.execute(
        f"""
    SELECT count(*)
      FROM pg_indexes
     WHERE schemaname = '{io_settings.settings.postgres_database_schema}'
       AND indexname = '{index_name.lower()}'
        """,
    )

    # Fetch the result
    row_pg = cur_pg.fetchone()

    # Return True if the index exists, False otherwise
    return row_pg and row_pg[COLUMN_COUNT] > 0  # type: ignore


# -----------------------------------------------------------------------------

def _check_exists_table(
    cur_pg: cursor,
    table_name: str,
) -> bool:
    """Check if a database table exists.

    :param cur_pg: The PostgreSQL database cursor.
    :param table_name: The name of the table to be checked.
    :return: True if the table exists, False otherwise.

    """
    # Execute the SQL statement
    cur_pg.execute(
        f"""
    SELECT count(*)
      FROM information_schema.tables
     WHERE table_schema = '{io_settings.settings.postgres_database_schema}'
       AND table_name = '{table_name.lower()}'
        """,
    )

    # Fetch the result
    row_pg = cur_pg.fetchone()

    # Return True if the table exists, False otherwise
    return row_pg and row_pg[COLUMN_COUNT] > 0  # type: ignore


# -----------------------------------------------------------------------------

def _check_exists_table_column(
    cur_pg: cursor,
    table_name: str,
    column_name: str,
) -> bool:
    """Check if a database table column exists.

    Args:
        cur_pg (cursor): The PostgreSQL database cursor.
        table_name (str): The name of the table to be checked.
        column_name (str): The name of the column to be checked.

    Returns:
        bool: True if the column exists, False otherwise.

    """
    # Check if the column exists
    cur_pg.execute(
        f"""
    SELECT count(*)
      FROM information_schema.columns
     WHERE table_schema = '{io_settings.settings.postgres_database_schema}'
       AND table_name = '{table_name.lower()}'
       AND column_name = '{column_name.lower()}'
        """,
    )

    # Fetch the result
    row_pg = cur_pg.fetchone()

    # Return True if the column exists, False otherwise
    return row_pg and row_pg[COLUMN_COUNT] > 0  # type: ignore


# ------------------------------------------------------------------
# Check the existence of a database type.
# ------------------------------------------------------------------
def _check_exists_type(
    cur_pg: cursor,
    type_name: str,
) -> bool:
    cur_pg.execute(
        f"""
    SELECT count(*)
      FROM pg_type
     WHERE typname = '{type_name.lower()}'
        """,
    )

    row_pg = cur_pg.fetchone()

    return row_pg and row_pg[COLUMN_COUNT] > 0  # type: ignore


# ------------------------------------------------------------------
# Create database indexes.
# ------------------------------------------------------------------
def _create_db_indexes(conn_pg: connection, cur_pg: cursor) -> None:
    # ------------------------------------------------------------------
    # Table 'aircraft'.
    # ------------------------------------------------------------------
    indexes = [
        (
            "aircraft",
            "acft_category",
            "",
        ),
        (
            "events_sequence",
            "occurrence_code",
            "",
        ),
        (
            "findings",
            "finding_code",
            "",
        ),
        (
            "io_app_ae1982",
            "cictt_codes",
            "",
        ),
        (
            "io_app_ae1982",
            "ev_highest_injury",
            "",
        ),
        (
            "io_app_ae1982",
            "ev_type",
            "",
        ),
        (
            "io_app_ae1982",
            "far_parts",
            "",
        ),
        (
            "io_app_ae1982",
            "inj_f_grnd",
            "",
        ),
        (
            "io_app_ae1982",
            "inj_tot_f",
            "",
        ),
        (
            "io_app_ae1982",
            "latlong_acq",
            "",
        ),
        (
            "io_app_ae1982",
            "no_aircraft",
            "",
        ),
        (
            "io_app_ae1982",
            "preventable_events",
            "",
        ),
        (
            "io_app_ae1982",
            "tll_parameters",
            "",
        ),
    ]

    for table_name, column_names, index_name in indexes:
        index = (
            index_name
            if index_name
            else f"{table_name}_{column_names.replace(',','_')}"
        )
        if not _check_exists_index(cur_pg, index):
            cur_pg.execute(
                f"""
                CREATE INDEX {index}
                    ON {table_name}
                       ({column_names});
                """,
            )
            conn_pg.commit()
            # INFO.00.077 Database index is available: {index}
            io_utils.progress_msg(
                glob_local.INFO_00_077.replace("{index}", index),
            )


# ------------------------------------------------------------------
# Create database IO-Aero specific data.
# ------------------------------------------------------------------
def _create_db_io_aero_data(conn_pg: connection, cur_pg: cursor) -> None:
    _create_db_io_md_codes_eventsoe("io_md_codes_eventsoe", conn_pg, cur_pg)
    _create_db_io_md_codes_phase("io_md_codes_phase", conn_pg, cur_pg)

    _create_db_io_md_codes_category("io_md_codes_category", conn_pg, cur_pg)
    _create_db_io_md_codes_subcategory("io_md_codes_subcategory", conn_pg, cur_pg)
    _create_db_io_md_codes_section("io_md_codes_section", conn_pg, cur_pg)
    _create_db_io_md_codes_subsection("io_md_codes_subsection", conn_pg, cur_pg)
    _create_db_io_md_codes_modifier("io_md_codes_modifier", conn_pg, cur_pg)


# ------------------------------------------------------------------
# Create database IO-Aero codes of categories data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_category(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT category_no,
                        finding_description
          FROM findings
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[str, list[str]] = {}

    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        category_no = row_tbd[COLUMN_CATEGORY_NO]
        finding_description = row_tbd[COLUMN_FINDING_DESCRIPTION]

        if category_no not in unstructured_desc:
            unstructured_desc[category_no] = []

        tokens = _create_tokens_4_finding_description(finding_description)

        if len(tokens) == 5 or (len(tokens) == 6 and tokens[5].strip() in ["C", "F"]):
            curr_desc = unstructured_desc[category_no]
            curr_desc.append(_prep_token_4_finding_description(tokens[0]))
            unstructured_desc[category_no] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for category_no, finding_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(finding_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               category_code,
               description
               ) VALUES (
               %s,
               %s);
        """,
            (
                category_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of occurrences data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_eventsoe(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT eventsoe_no,
                        occurrence_description
          FROM events_sequence
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[str, list[str]] = {}

    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        eventsoe_no = row_tbd[COLUMN_EVENTSOE_NO]
        occurrence_description = row_tbd[COLUMN_OCCURRENCE_DESCRIPTION]

        if eventsoe_no not in unstructured_desc:
            unstructured_desc[eventsoe_no] = []

        if occurrence_description:
            curr_desc = unstructured_desc[eventsoe_no]
            curr_desc.append(occurrence_description.strip()[::-1])
            unstructured_desc[eventsoe_no] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for eventsoe_no, occurrence_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(occurrence_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               eventsoe_code,
               description
               ) VALUES (
               %s,
               %s);
        """,
            (
                eventsoe_no,
                description[::-1],
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of modifiers data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_modifier(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT modifier_no,
                        finding_description
          FROM findings
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[str, list[str]] = {}

    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        modifier_no = row_tbd[COLUMN_MODIFIER_NO]
        finding_description = row_tbd[COLUMN_FINDING_DESCRIPTION]

        if modifier_no not in unstructured_desc:
            unstructured_desc[modifier_no] = []

        tokens = _create_tokens_4_finding_description(finding_description)

        if len(tokens) == 5 or (len(tokens) == 6 and tokens[5].strip() in ["C", "F"]):
            curr_desc = unstructured_desc[modifier_no]
            curr_desc.append(_prep_token_4_finding_description(tokens[4]))
            unstructured_desc[modifier_no] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for modifier_no, finding_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(finding_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               modifier_code,
               description
               ) VALUES (
               %s,
               %s);
        """,
            (
                modifier_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of phases of operation data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_phase(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT phase_no,
                        occurrence_description
          FROM events_sequence
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[str, list[str]] = {}


    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        phase_no = row_tbd[COLUMN_PHASE_NO]
        occurrence_description = row_tbd[COLUMN_OCCURRENCE_DESCRIPTION]

        if phase_no not in unstructured_desc:
            unstructured_desc[phase_no] = []

        if occurrence_description:
            curr_desc = unstructured_desc[phase_no]
            curr_desc.append(occurrence_description.strip())
            unstructured_desc[phase_no] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for phase_no, occurrence_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(occurrence_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               phase_code,
               description
               ) VALUES (
               %s,
               %s);
        """,
            (
                phase_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    # ------------------------------------------------------------------
    # Add the main phase descriptions.
    # ------------------------------------------------------------------

    _load_description_main_phase(conn_pg, cur_pg)

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of sections data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_section(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------

    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT category_no,
                        subcategory_no,
                        section_no,
                        finding_description
          FROM findings
          order by 1,2,3
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[tuple[str, str, str], list[str]] = {}


    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        category_no = row_tbd[COLUMN_CATEGORY_NO]
        subcategory_no = row_tbd[COLUMN_SUBCATEGORY_NO]
        section_no = row_tbd[COLUMN_SECTION_NO]
        finding_description = row_tbd[COLUMN_FINDING_DESCRIPTION]

        if (category_no, subcategory_no, section_no) not in unstructured_desc:
            unstructured_desc[(category_no, subcategory_no, section_no)] = []

        tokens = _create_tokens_4_finding_description(finding_description)

        if len(tokens) == 5 or (len(tokens) == 6 and tokens[5].strip() in ["C", "F"]):
            curr_desc = unstructured_desc[(category_no, subcategory_no, section_no)]
            curr_desc.append(_prep_token_4_finding_description(tokens[2]))
            unstructured_desc[(category_no, subcategory_no, section_no)] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for (
        category_no,
        subcategory_no,
        section_no,
    ), finding_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(finding_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               category_code,
               subcategory_code,
               section_code,
               description
               ) VALUES (
               %s,
               %s,
               %s,
               %s);
        """,
            (
                category_no,
                subcategory_no,
                section_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of subcategories data.
# ------------------------------------------------------------------
def _create_db_io_md_codes_subcategory(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------

    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT category_no,
                        subcategory_no,
                        finding_description
          FROM findings
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[tuple[str, str], list[str]] = {}


    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        category_no = row_tbd[COLUMN_CATEGORY_NO]
        subcategory_no = row_tbd[COLUMN_SUBCATEGORY_NO]
        finding_description = row_tbd[COLUMN_FINDING_DESCRIPTION]

        if (category_no, subcategory_no) not in unstructured_desc:
            unstructured_desc[(category_no, subcategory_no)] = []

        tokens = _create_tokens_4_finding_description(finding_description)

        if len(tokens) == 5 or (len(tokens) == 6 and tokens[5].strip() in ["C", "F"]):
            curr_desc = unstructured_desc[(category_no, subcategory_no)]
            curr_desc.append(_prep_token_4_finding_description(tokens[1]))
            unstructured_desc[(category_no, subcategory_no)] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for (
        category_no,
        subcategory_no,
    ), finding_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(finding_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               category_code,
               subcategory_code,
               description
               ) VALUES (
               %s,
               %s,
               %s);
        """,
            (
                category_no,
                subcategory_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database IO-Aero codes of subsections data.
# ------------------------------------------------------------------

def _create_db_io_md_codes_subsection(
    table_name: str,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    logging.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35,
    )

    # ------------------------------------------------------------------
    # Delete the existing data.
    # ------------------------------------------------------------------

    cur_pg.execute(
        f"""
    DELETE FROM {table_name}
    """,
    )

    if cur_pg.rowcount > 0:
        io_utils.progress_msg(f"Number rows deleted  : {cur_pg.rowcount!s:>8}")

    # ------------------------------------------------------------------
    # Load the raw data.
    # ------------------------------------------------------------------
    cur_pg.execute(
        """
        SELECT DISTINCT category_no,
                        subcategory_no,
                        section_no,
                        subsection_no,
                        finding_description
          FROM findings
         """,
    )

    rows_tbd = cur_pg.fetchall()

    unstructured_desc: dict[tuple[str, str, str, str], list[str]] = {}


    for row_tbd in rows_tbd:
        count_select += 1

        if count_select % io_settings.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {count_select!s:>8}",
            )

        category_no = row_tbd[COLUMN_CATEGORY_NO]
        subcategory_no = row_tbd[COLUMN_SUBCATEGORY_NO]
        section_no = row_tbd[COLUMN_SECTION_NO]
        subsection_no = row_tbd[COLUMN_SUBSECTION_NO]
        finding_description = row_tbd[COLUMN_FINDING_DESCRIPTION]

        if (
            category_no,
            subcategory_no,
            section_no,
            subsection_no,
        ) not in unstructured_desc:
            unstructured_desc[
                (category_no, subcategory_no, section_no, subsection_no)
            ] = []

        tokens = _create_tokens_4_finding_description(finding_description)

        if len(tokens) == 5 or (len(tokens) == 6 and tokens[5].strip() in ["C", "F"]):
            curr_desc = unstructured_desc[
                (category_no, subcategory_no, section_no, subsection_no)
            ]
            curr_desc.append(_prep_token_4_finding_description(tokens[3]))
            unstructured_desc[
                (category_no, subcategory_no, section_no, subsection_no)
            ] = curr_desc

    io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

    # ------------------------------------------------------------------
    # Create the master data.
    # ------------------------------------------------------------------

    for (
        category_no,
        subcategory_no,
        section_no,
        subsection_no,
    ), finding_descriptions in unstructured_desc.items():
        description = os.path.commonprefix(finding_descriptions).strip()

        cur_pg.execute(
            f"""
        INSERT INTO {table_name} (
               category_code,
               subcategory_code,
               section_code,
               subsection_code,
               description
               ) VALUES (
               %s,
               %s,
               %s,
               %s,
               %s);
        """,
            (
                category_no,
                subcategory_no,
                section_no,
                subsection_no,
                description,
            ),
        )
        count_insert += 1

    io_utils.progress_msg(f"Number rows inserted : {count_insert!s:>8}")

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Create database role 'guest'.
# ------------------------------------------------------------------
def _create_db_role_guest(conn_pg: connection, cur_pg: cursor) -> None:
    try:
        cur_pg.execute(
            f"""
        SELECT count(*)
          FROM pg_roles
         WHERE rolname = '{io_settings.settings.postgres_user_guest}'
            """,
        )

        row_pg = cur_pg.fetchone()

        if row_pg and row_pg[COLUMN_COUNT] > 0:  # type: ignore
            cur_pg.execute(
                f"DROP OWNED BY {io_settings.settings.postgres_user_guest} CASCADE",
            )

            conn_pg.commit()

        cur_pg.execute(
            f"DROP ROLE IF EXISTS {io_settings.settings.postgres_user_guest}",
        )

        conn_pg.commit()

        # INFO.00.018 Database role is dropped: {role}
        io_utils.progress_msg(
            glob_local.INFO_00_018.replace(
                "{role}",
                io_settings.settings.postgres_user_guest,
            ),
        )
    except DatabaseError:
        # INFO.00.082 Database role is not existing: {role}
        io_utils.progress_msg(
            glob_local.INFO_00_082.replace(
                "{role}",
                io_settings.settings.postgres_user_guest,
            ),
        )

    cur_pg.execute(
        f"CREATE ROLE {io_settings.settings.postgres_user_guest} WITH LOGIN "
        f"PASSWORD '{io_settings.settings.postgres_password_guest}'",
    )

    conn_pg.commit()

    # INFO.00.016 Database role is available: {role}
    io_utils.progress_msg(
        glob_local.INFO_00_016.replace(
            "{role}",
            io_settings.settings.postgres_user_guest,
        ),
    )

    cur_pg.execute(
        f"GRANT CONNECT ON DATABASE {io_settings.settings.postgres_dbname} "
        f"TO {io_settings.settings.postgres_user_guest}",
    )

    cur_pg.execute(
        f"GRANT USAGE ON SCHEMA public TO {io_settings.settings.postgres_user_guest}",
    )

    cur_pg.execute(
        f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {io_settings.settings.postgres_user_guest}",
    )

    conn_pg.commit()


# ------------------------------------------------------------------
# Create database tables.
# ------------------------------------------------------------------
def _create_db_tables(conn_pg: connection, cur_pg: cursor) -> None:
    for table_name, stmnt in DLL_TABLE_STMNTS.items():
        if not _check_exists_table(cur_pg, table_name):
            cur_pg.execute(stmnt)
            conn_pg.commit()
            # INFO.00.007 Database table created: {table}
            io_utils.progress_msg(
                glob_local.INFO_00_007.replace("{table}", table_name),
            )


# ------------------------------------------------------------------
# Create database table columns.
# ------------------------------------------------------------------
def _create_db_table_columns(conn_pg: connection, cur_pg: cursor) -> None:
    table_columns = [
        ("events", "io_city", "ALTER TABLE events ADD COLUMN io_city VARCHAR(50);"),
        (
            "events",
            "io_country",
            "ALTER TABLE events ADD COLUMN io_country VARCHAR(4);",
        ),
        (
            "events",
            "io_dec_lat_lng_actions",
            "ALTER TABLE events ADD COLUMN io_dec_lat_lng_actions TEXT;",
        ),
        (
            "events",
            "io_dec_latitude",
            "ALTER TABLE events ADD COLUMN io_dec_latitude FLOAT;",
        ),
        (
            "events",
            "io_dec_latitude_deviating",
            "ALTER TABLE events ADD COLUMN io_dec_latitude_deviating FLOAT;",
        ),
        (
            "events",
            "io_dec_longitude",
            "ALTER TABLE events ADD COLUMN io_dec_longitude FLOAT;",
        ),
        (
            "events",
            "io_dec_longitude_deviating",
            "ALTER TABLE events ADD COLUMN io_dec_longitude_deviating FLOAT;",
        ),
        (
            "events",
            "io_invalid_latitude",
            "ALTER TABLE events ADD COLUMN io_invalid_latitude BOOLEAN;",
        ),
        (
            "events",
            "io_invalid_longitude",
            "ALTER TABLE events ADD COLUMN io_invalid_longitude BOOLEAN;",
        ),
        (
            "events",
            "io_invalid_us_city",
            "ALTER TABLE events ADD COLUMN io_invalid_us_city BOOLEAN;",
        ),
        (
            "events",
            "io_invalid_us_city_zipcode",
            "ALTER TABLE events ADD COLUMN io_invalid_us_city_zipcode BOOLEAN;",
        ),
        (
            "events",
            "io_invalid_us_state",
            "ALTER TABLE events ADD COLUMN io_invalid_us_state BOOLEAN;",
        ),
        (
            "events",
            "io_invalid_us_zipcode",
            "ALTER TABLE events ADD COLUMN io_invalid_us_zipcode BOOLEAN;",
        ),
        (
            "events",
            "io_latitude",
            "ALTER TABLE events ADD COLUMN io_latitude VARCHAR(7);",
        ),
        (
            "events",
            "io_latlong_acq",
            "ALTER TABLE events ADD COLUMN io_latlong_acq VARCHAR(4);",
        ),
        (
            "events",
            "io_longitude",
            "ALTER TABLE events ADD COLUMN io_longitude VARCHAR(8);",
        ),
        (
            "events",
            "io_nearest_airport_distance",
            "ALTER TABLE events ADD COLUMN io_nearest_airport_distance FLOAT;",
        ),
        (
            "events",
            "io_nearest_airport_global_id",
            "ALTER TABLE events ADD COLUMN io_nearest_airport_global_id VARCHAR(254);",
        ),
        (
            "events",
            "io_site_zipcode",
            "ALTER TABLE events ADD COLUMN io_site_zipcode VARCHAR(10);",
        ),
        ("events", "io_state", "ALTER TABLE events ADD COLUMN io_state VARCHAR(2);"),
        (
            "events",
            "io_terminal_areas",
            "ALTER TABLE events ADD COLUMN io_terminal_areas io_terminal_area[];",
        ),
        (
            "io_md_codes_phase",
            "description_main_phase",
            "ALTER TABLE io_md_codes_phase ADD COLUMN description_main_phase VARCHAR(100);",
        ),
    ]

    for table_name, column_name, stmnt in table_columns:
        if not _check_exists_table_column(cur_pg, table_name, column_name):
            cur_pg.execute(stmnt)
            conn_pg.commit()
            # INFO.00.031 Database column added: table_schema '{schema}'
            # table_name '{table}' column_name '{column}'
            io_utils.progress_msg(
                glob_local.INFO_00_031.replace(
                    "{schema}",
                    io_settings.settings.postgres_database_schema,
                )
                .replace("{table}", table_name)
                .replace("{column}", column_name),
            )

    # ------------------------------------------------------------------
    # Column 'io_last_seen_ntsb'.
    # ------------------------------------------------------------------
    tables = [
        "aircraft",
        "dt_aircraft",
        "dt_events",
        "dt_flight_crew",
        "engines",
        "events",
        "events_sequence",
        "findings",
        "flight_crew",
        "flight_time",
        "injury",
        "narratives",
        "ntsb_admin",
        "occurrences",
        "seq_of_events",
    ]

    column_name = "io_last_seen_ntsb"
    ddl_stmnt = """
    ALTER TABLE table_name
    ADD COLUMN IF NOT EXISTS io_last_seen_ntsb TIMESTAMP;
    """

    for table_name in tables:
        if not _check_exists_table_column(cur_pg, table_name, column_name):
            cur_pg.execute(ddl_stmnt.replace("table_name", table_name))
            conn_pg.commit()
            # INFO.00.031 Database column added: table_schema '{schema}'
            # table_name '{table}' column_name '{column}'
            io_utils.progress_msg(
                glob_local.INFO_00_031.replace(
                    "{schema}",
                    io_settings.settings.postgres_database_schema,
                )
                .replace("{table}", table_name)
                .replace("{column}", column_name),
            )


# ------------------------------------------------------------------
# Create database composite types.
# ------------------------------------------------------------------
def _create_db_types_composite(conn_pg: connection, cur_pg: cursor) -> None:
    types = [
        (
            "io_terminal_area",
            "airport_distance float8, airport_global_id varchar(254)",
        ),
    ]

    for type_name, attributes in types:
        if not _check_exists_type(cur_pg, type_name):
            cur_pg.execute(
                f"""
                CREATE TYPE {type_name} AS (
                    {attributes});
                """,
            )
            conn_pg.commit()
            # INFO.00.091 Database type  is available: {type}
            io_utils.progress_msg(
                glob_local.INFO_00_091.replace("{type}", type_name),
            )


# ------------------------------------------------------------------
# Create database views.
# ------------------------------------------------------------------
def _create_db_views(conn_pg: connection, cur_pg: cursor) -> None:
    _create_dll_view_io_lat_lng_issues()

    _create_dll_view_io_app_ae1982()

    for view_name in reversed(DLL_VIEW_STMNTS_REFRESH):
        cur_pg.execute("DROP MATERIALIZED VIEW IF EXISTS " + view_name + ";")
        conn_pg.commit()
        # INFO.00.070 Materialized database view is dropped: {view}
        io_utils.progress_msg(
            glob_local.INFO_00_070.replace("{view}", view_name),
        )

    for view_name in reversed(DLL_VIEW_STMNTS_DROP):
        cur_pg.execute("DROP VIEW IF EXISTS " + view_name + ";")
        conn_pg.commit()
        # INFO.00.067 Database view dropped: {view}
        io_utils.progress_msg(
            glob_local.INFO_00_067.replace("{view}", view_name),
        )

    for view_name, stmnt in DLL_VIEW_STMNTS_CREATE.items():
        cur_pg.execute(stmnt)
        conn_pg.commit()
        # INFO.00.032 Database view created: {view}
        io_utils.progress_msg(
            glob_local.INFO_00_032.replace("{view}", view_name),
        )

    for view_name, stmnt in DLL_VIEW_STMNTS_CREATE_MAT.items():
        cur_pg.execute(stmnt)
        conn_pg.commit()
        # INFO.00.068 Materialized database view is created: {view}
        io_utils.progress_msg(
            glob_local.INFO_00_068.replace("{view}", view_name),
        )


# ------------------------------------------------------------------
# Collect the IO-Aero specific alter database table definitions.
# ------------------------------------------------------------------
def _create_dll_alter_tables_io() -> None:
    _create_dll_table_io_msaccess_file_alter()


# ------------------------------------------------------------------
# Collect the IO-Aero specific create database table definitions.
# ------------------------------------------------------------------
def _create_dll_create_tables_io() -> None:
    # ------------------------------------------------------------------
    # Level 1 - without FK
    # ------------------------------------------------------------------
    _create_dll_table_io_aviation_occurrence_categories()
    _create_dll_table_io_countries()
    _create_dll_table_io_md_codes_category()
    _create_dll_table_io_md_codes_subcategory()
    _create_dll_table_io_md_codes_section()
    _create_dll_table_io_md_codes_subsection()
    _create_dll_table_io_md_codes_modifier()
    _create_dll_table_io_md_codes_eventsoe()
    _create_dll_table_io_md_codes_phase()
    _create_dll_table_io_processed_data()

    # ------------------------------------------------------------------
    # Level 2 - FK io_countries.country
    # ------------------------------------------------------------------
    _create_dll_table_io_lat_lng()
    _create_dll_table_io_sequence_of_events()
    _create_dll_table_io_states()

    # ------------------------------------------------------------------
    # Level 3 - FK  io_states.country & state
    # ------------------------------------------------------------------
    _create_dll_table_io_airports()


# ------------------------------------------------------------------
# Adds the DDL instructions for setting up the database schema.
# ------------------------------------------------------------------
def _create_dll_tables_base() -> None:
    logging.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Level 1 - without FK
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MS Access: events
    DLL_TABLE_STMNTS[
        "events"
    ] = """
        CREATE TABLE IF NOT EXISTS events
        (
            ev_id               VARCHAR(14),
            ntsb_no             VARCHAR(10),
            ev_type             VARCHAR(3),
            ev_date             TIMESTAMP,
            ev_dow              VARCHAR(2),
            ev_time             SMALLINT,
            ev_tmzn             VARCHAR(3),
            ev_city             VARCHAR(50),
            ev_state            VARCHAR(2),
            ev_country          VARCHAR(4),
            ev_site_zipcode     VARCHAR(10),
            ev_year             SMALLINT,
            ev_month            SMALLINT,
            mid_air             VARCHAR(1),
            on_ground_collision VARCHAR(1),
            latitude            VARCHAR(7),
            longitude           VARCHAR(8),
            latlong_acq         VARCHAR(4),
            apt_name            VARCHAR(30),
            ev_nr_apt_id        VARCHAR(4),
            ev_nr_apt_loc       VARCHAR(4),
            apt_dist            REAL,
            apt_dir             SMALLINT,
            apt_elev            SMALLINT,
            wx_brief_comp       VARCHAR(4),
            wx_src_iic          VARCHAR(4),
            wx_obs_time         SMALLINT,
            wx_obs_dir          SMALLINT,
            wx_obs_fac_id       VARCHAR(4),
            wx_obs_elev         INT,
            wx_obs_dist         SMALLINT,
            wx_obs_tmzn         VARCHAR(3),
            light_cond          VARCHAR(4),
            sky_cond_nonceil    VARCHAR(4),
            sky_nonceil_ht      INT,
            sky_ceil_ht         INT,
            sky_cond_ceil       VARCHAR(4),
            vis_rvr             REAL,
            vis_rvv             SMALLINT,
            vis_sm              REAL,
            wx_temp             SMALLINT,
            wx_dew_pt           SMALLINT,
            wind_dir_deg        SMALLINT,
            wind_dir_ind        VARCHAR(1),
            wind_vel_kts        SMALLINT,
            wind_vel_ind        VARCHAR(4),
            gust_ind            VARCHAR(1),
            gust_kts            SMALLINT,
            altimeter           REAL,
            wx_dens_alt         INT,
            wx_int_precip       VARCHAR(3),
            metar               TEXT,
            ev_highest_injury   VARCHAR(4),
            inj_f_grnd          SMALLINT,
            inj_m_grnd          SMALLINT,
            inj_s_grnd          SMALLINT,
            inj_tot_f           SMALLINT,
            inj_tot_m           SMALLINT,
            inj_tot_n           SMALLINT,
            inj_tot_s           SMALLINT,
            inj_tot_t           SMALLINT,
            invest_agy          VARCHAR(1),
            ntsb_docket         INT,
            ntsb_notf_from      VARCHAR(30),
            ntsb_notf_date      TIMESTAMP,
            ntsb_notf_tm        SMALLINT,
            fiche_number        VARCHAR(5),
            lchg_date           TIMESTAMP,
            lchg_userid         VARCHAR(18),
            wx_cond_basic       VARCHAR(3),
            faa_dist_office     VARCHAR(50),
            dec_latitude        FLOAT,
            dec_longitude       FLOAT,
            PRIMARY KEY (ev_id)
        );
    """

    # ------------------------------------------------------------------
    # Level 2 - FK ev_id
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MS Access: aircraft
    DLL_TABLE_STMNTS[
        "aircraft"
    ] = """
        CREATE TABLE IF NOT EXISTS aircraft
        (
            ev_id                   VARCHAR(14),
            aircraft_key            INT,
            regis_no                VARCHAR(11),
            ntsb_no                 VARCHAR(11),
            acft_missing            VARCHAR(1),
            far_part                VARCHAR(4),
            flt_plan_filed          VARCHAR(4),
            flight_plan_activated   VARCHAR(1),
            damage                  VARCHAR(4),
            acft_fire               VARCHAR(4),
            acft_expl               VARCHAR(4),
            acft_make               VARCHAR(30),
            acft_model              VARCHAR(20),
            acft_series             VARCHAR(10),
            acft_serial_no          VARCHAR(20),
            cert_max_gr_wt          INT,
            acft_category           VARCHAR(4),
            acft_reg_cls            VARCHAR(4),
            homebuilt               VARCHAR(3),
            fc_seats                INT,
            cc_seats                INT,
            pax_seats               INT,
            total_seats             SMALLINT,
            num_eng                 SMALLINT,
            fixed_retractable       VARCHAR(4),
            type_last_insp          VARCHAR(4),
            date_last_insp          TIMESTAMP,
            afm_hrs_last_insp       REAL,
            afm_hrs                 REAL,
            elt_install             VARCHAR(1),
            elt_oper                VARCHAR(1),
            elt_aided_loc_ev        VARCHAR(1),
            elt_type                VARCHAR(4),
            owner_acft              VARCHAR(50),
            owner_street            VARCHAR(50),
            owner_city              VARCHAR(50),
            owner_state             VARCHAR(2),
            owner_country           VARCHAR(4),
            owner_zip               VARCHAR(10),
            oper_individual_name    VARCHAR(1),
            oper_name               VARCHAR(50),
            oper_same               VARCHAR(1),
            oper_dba                VARCHAR(50),
            oper_addr_same          VARCHAR(1),
            oper_street             VARCHAR(50),
            oper_city               VARCHAR(50),
            oper_state              VARCHAR(2),
            oper_country            VARCHAR(4),
            oper_zip                VARCHAR(10),
            oper_code               VARCHAR(4),
            certs_held              VARCHAR(1),
            oprtng_cert             VARCHAR(3),
            oper_cert               VARCHAR(4),
            oper_cert_num           VARCHAR(11),
            oper_sched              VARCHAR(4),
            oper_dom_int            VARCHAR(3),
            oper_pax_cargo          VARCHAR(4),
            type_fly                VARCHAR(4),
            second_pilot            VARCHAR(1),
            dprt_pt_same_ev         VARCHAR(1),
            dprt_apt_id             VARCHAR(4),
            dprt_city               VARCHAR(50),
            dprt_state              VARCHAR(2),
            dprt_country            VARCHAR(3),
            dprt_time               SMALLINT,
            dprt_timezn             VARCHAR(3),
            dest_same_local         VARCHAR(4),
            dest_apt_id             VARCHAR(4),
            dest_city               VARCHAR(50),
            dest_state              VARCHAR(2),
            dest_country            VARCHAR(3),
            phase_flt_spec          INT,
            report_to_icao          VARCHAR(1),
            evacuation              VARCHAR(1),
            lchg_date               TIMESTAMP,
            lchg_userid             VARCHAR(18),
            afm_hrs_since           VARCHAR(4),
            rwy_num                 VARCHAR(4),
            rwy_len                 INT,
            rwy_width               INT,
            site_seeing             VARCHAR(1),
            air_medical             VARCHAR(1),
            med_type_flight         VARCHAR(15),
            acft_year               INT,
            fuel_on_board           VARCHAR(20),
            commercial_space_flight BOOLEAN NOT NULL,
            unmanned                BOOLEAN NOT NULL,
            ifr_equipped_cert       BOOLEAN NOT NULL,
            elt_mounted_aircraft    BOOLEAN NOT NULL,
            elt_connected_antenna   BOOLEAN NOT NULL,
            elt_manufacturer        VARCHAR(50),
            elt_model               VARCHAR(50),
            elt_reason_other        TEXT,
            PRIMARY KEY (ev_id, aircraft_key),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: dt_events
    DLL_TABLE_STMNTS[
        "dt_events"
    ] = """
        CREATE TABLE IF NOT EXISTS dt_events
        (
            ev_id       VARCHAR(14),
            col_name    VARCHAR(20),
            code        VARCHAR(4),
            lchg_date   TIMESTAMP,
            lchg_userid VARCHAR(18),
            PRIMARY KEY (ev_id, col_name, code),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: NTSB_Admin
    DLL_TABLE_STMNTS[
        "ntsb_admin"
    ] = """
        CREATE TABLE IF NOT EXISTS ntsb_admin
        (
            ev_id         VARCHAR(14),
            rec_stat      VARCHAR(1),
            approval_date TIMESTAMP,
            lchg_userid   VARCHAR(18),
            lchg_date     TIMESTAMP,
            PRIMARY KEY (ev_id),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # Level 3 - FKs ev_id & aircraft_key
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MS Access: dt_aircraft
    DLL_TABLE_STMNTS[
        "dt_aircraft"
    ] = """
        CREATE TABLE IF NOT EXISTS dt_aircraft
        (
            ev_id        VARCHAR(14),
            aircraft_key INT,
            col_name     VARCHAR(20),
            code         VARCHAR(4),
            lchg_date    TIMESTAMP,
            lchg_userid  VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, col_name, code),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: engines
    DLL_TABLE_STMNTS[
        "engines"
    ] = """
        CREATE TABLE IF NOT EXISTS engines
        (
            ev_id               VARCHAR(14),
            aircraft_key        INT,
            eng_no              SMALLINT,
            eng_type            VARCHAR(4),
            eng_mfgr            VARCHAR(30),
            eng_model           VARCHAR(13),
            power_units         INT,
            hp_or_lbs           VARCHAR(4),
            lchg_userid         VARCHAR(18),
            lchg_date           TIMESTAMP,
            carb_fuel_injection VARCHAR(4),
            propeller_type      VARCHAR(4),
            propeller_make      VARCHAR(50),
            propeller_model     VARCHAR(50),
            eng_time_total      REAL,
            eng_time_last_insp  REAL,
            eng_time_overhaul   REAL,
            PRIMARY KEY (ev_id, aircraft_key, eng_no),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: Events_Sequence                                   EMPTY
    DLL_TABLE_STMNTS[
        "events_sequence"
    ] = """
        CREATE TABLE IF NOT EXISTS events_sequence
        (
            ev_id                  VARCHAR(14),
            aircraft_key           INT,
            occurrence_no          INT,
            occurrence_code        VARCHAR(7),
            occurrence_description VARCHAR(100),
            phase_no               VARCHAR(3),
            eventsoe_no            VARCHAR(3),
            defining_ev            BOOLEAN NOT NULL,
            lchg_date              TIMESTAMP,
            lchg_userid            VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, occurrence_no),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: Findings
    DLL_TABLE_STMNTS[
        "findings"
    ] = """
        CREATE TABLE IF NOT EXISTS findings
        (
            ev_id               VARCHAR(14),
            aircraft_key        INT,
            finding_no          INT,
            finding_code        VARCHAR(10),
            finding_description VARCHAR(255),
            category_no         VARCHAR(2),
            subcategory_no      VARCHAR(2),
            section_no          VARCHAR(2),
            subsection_no       VARCHAR(2),
            modifier_no         VARCHAR(2),
            cause_factor        VARCHAR(1),
            cm_inPc             VARCHAR(1),
            lchg_date           TIMESTAMP,
            lchg_userid         VARCHAR(50),
            PRIMARY KEY (ev_id, aircraft_key, finding_no),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: Flight_Crew
    DLL_TABLE_STMNTS[
        "flight_crew"
    ] = """
        CREATE TABLE IF NOT EXISTS flight_crew
        (
            ev_id               VARCHAR(14),
            aircraft_key        INT,
            crew_no             SMALLINT,
            crew_category       VARCHAR(5),
            crew_age            SMALLINT,
            crew_sex            VARCHAR(1),
            crew_city           VARCHAR(15),
            crew_res_state      VARCHAR(2),
            crew_res_country    VARCHAR(4),
            med_certf           VARCHAR(4),
            med_crtf_vldty      VARCHAR(4),
            date_lst_med        TIMESTAMP,
            crew_rat_endorse    VARCHAR(1),
            crew_inj_level      VARCHAR(4),
            seatbelts_used      VARCHAR(1),
            shldr_harn_used     VARCHAR(1),
            crew_tox_perf       VARCHAR(1),
            seat_occ_pic        VARCHAR(4),
            pc_profession       VARCHAR(4),
            bfr                 VARCHAR(1),
            bfr_date            TIMESTAMP,
            ft_as_of            TIMESTAMP,
            lchg_date           TIMESTAMP,
            lchg_userid         VARCHAR(18),
            seat_occ_row        INT,
            infl_rest_inst      VARCHAR(1),
            infl_rest_depl      VARCHAR(1),
            child_restraint     VARCHAR(3),
            med_crtf_limit      TEXT,
            mr_faa_med_certf    VARCHAR(4),
            pilot_flying        BOOLEAN NOT NULL,
            available_restraint VARCHAR(1),
            restraint_used      VARCHAR(1),
            PRIMARY KEY (ev_id, aircraft_key, crew_no),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: injury
    DLL_TABLE_STMNTS[
        "injury"
    ] = """
        CREATE TABLE IF NOT EXISTS injury
        (
            ev_id               VARCHAR(14),
            aircraft_key        INT,
            inj_person_category VARCHAR(4),
            injury_level        VARCHAR(4),
            inj_person_count    SMALLINT,
            lchg_date           TIMESTAMP,
            lchg_userid         VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, inj_person_category, injury_level),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: narratives
    DLL_TABLE_STMNTS[
        "narratives"
    ] = """
        CREATE TABLE IF NOT EXISTS narratives
        (
            ev_id        VARCHAR(14),
            aircraft_key INT,
            narr_accp    TEXT,
            narr_accf    TEXT,
            narr_cause   TEXT,
            narr_inc     TEXT,
            lchg_date    TIMESTAMP,
            lchg_userid  VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: Occurrences
    DLL_TABLE_STMNTS[
        "occurrences"
    ] = """
        CREATE TABLE IF NOT EXISTS occurrences
        (
            ev_id           VARCHAR(14),
            aircraft_key    INT,
            occurrence_no   INT,
            occurrence_code INT,
            phase_of_flight INT,
            altitude        INT,
            lchg_date       TIMESTAMP,
            lchg_userid     VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, occurrence_no),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # Level 4 - FKs ev_id & aircraft_key & crew_no
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MS Access: dt_Flight_Crew
    DLL_TABLE_STMNTS[
        "dt_flight_crew"
    ] = """
        CREATE TABLE IF NOT EXISTS dt_flight_crew
        (
            ev_id        VARCHAR(14),
            aircraft_key INT,
            crew_no      SMALLINT,
            col_name     VARCHAR(20),
            code         VARCHAR(4),
            lchg_date    TIMESTAMP,
            lchg_userid  VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, crew_no, col_name, code),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key, crew_no) REFERENCES flight_crew (ev_id, aircraft_key, crew_no) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # MS Access: flight_time
    DLL_TABLE_STMNTS[
        "flight_time"
    ] = """
        CREATE TABLE IF NOT EXISTS flight_time
        (
            ev_id        VARCHAR(14),
            aircraft_key INT,
            crew_no      SMALLINT,
            flight_type  VARCHAR(4),
            flight_craft VARCHAR(4),
            flight_hours REAL,
            lchg_date    TIMESTAMP,
            lchg_userid  VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, crew_no, flight_type, flight_craft),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key, crew_no) REFERENCES flight_crew (ev_id, aircraft_key, crew_no) ON DELETE CASCADE
        );
    """

    # ------------------------------------------------------------------
    # Level 4 - FKs ev_id & aircraft_key & occurrence_no
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MS Access: seq_of_events                                     EMPTY
    DLL_TABLE_STMNTS[
        "seq_of_events"
    ] = """
        CREATE TABLE IF NOT EXISTS seq_of_events
        (
            ev_id         VARCHAR(14),
            aircraft_key  INT,
            occurrence_no INT,
            seq_event_no  INT,
            group_code    SMALLINT,
            subj_code     INT,
            cause_factor  VARCHAR(1),
            modifier_code INT,
            person_code   INT,
            lchg_date     TIMESTAMP,
            lchg_userid   VARCHAR(18),
            PRIMARY KEY (ev_id, aircraft_key, occurrence_no, seq_event_no, group_code),
            FOREIGN KEY (ev_id) REFERENCES events (ev_id) ON DELETE CASCADE,
            FOREIGN KEY (ev_id, aircraft_key) REFERENCES aircraft (ev_id, aircraft_key) ON DELETE CASCADE
        );
    """

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_airports.
# ------------------------------------------------------------------
def _create_dll_table_io_airports() -> None:
    DLL_TABLE_STMNTS[
        "io_airports"
    ] = """
        CREATE TABLE IF NOT EXISTS io_airports
        (
            global_id            VARCHAR(254) NOT NULL,
            airanal              VARCHAR(254),
            country              VARCHAR(254),
            dec_latitude         FLOAT,
            dec_longitude        FLOAT,
            dodhiflib            SMALLINT,
            elevation            FLOAT,
            far91                SMALLINT,
            far93                SMALLINT,
            iapexists            SMALLINT,
            ident                VARCHAR(254),
            latitude             VARCHAR(254),
            longitude            VARCHAR(254),
            max_runway_comp_code VARCHAR(254),
            max_runway_length    FLOAT,
            mil_code             VARCHAR(50),
            name                 VARCHAR(254),
            operstatus           VARCHAR(254),
            privateuse           SMALLINT,
            servcity             VARCHAR(254),
            state                VARCHAR(254),
            type_code            VARCHAR(254),
            first_processed      TIMESTAMP    NOT NULL,
            last_processed       TIMESTAMP,
            PRIMARY KEY (global_id),
            FOREIGN KEY (country) REFERENCES io_countries (country) ON DELETE CASCADE,
            FOREIGN KEY (country, state) REFERENCES io_states (country, state) ON DELETE CASCADE,
            UNIQUE (ident)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_aviation_occurrence_categories.
# ------------------------------------------------------------------
def _create_dll_table_io_aviation_occurrence_categories() -> None:
    DLL_TABLE_STMNTS[
        "io_aviation_occurrence_categories"
    ] = """
        CREATE TABLE IF NOT EXISTS io_aviation_occurrence_categories
        (
            cictt_code      VARCHAR(10) NOT NULL,
            identifier      VARCHAR(100) NOT NULL,
            definition      TEXT NOT NULL,
            first_processed TIMESTAMP NOT NULL,
            last_processed  TIMESTAMP,
            last_seen       TIMESTAMP,
            PRIMARY KEY (cictt_code)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_countries.
# ------------------------------------------------------------------
def _create_dll_table_io_countries() -> None:
    DLL_TABLE_STMNTS[
        "io_countries"
    ] = """
        CREATE TABLE IF NOT EXISTS io_countries
        (
            country         VARCHAR(4),
            country_name    VARCHAR(100),
            dec_latitude    FLOAT NOT NULL,
            dec_longitude   FLOAT NOT NULL,
            first_processed TIMESTAMP NOT NULL,
            last_processed  TIMESTAMP,
            PRIMARY KEY (country)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_lat_lng.
# ------------------------------------------------------------------
def _create_dll_table_io_lat_lng() -> None:
    DLL_TABLE_STMNTS[
        "io_lat_lng"
    ] = """
        CREATE TABLE IF NOT EXISTS io_lat_lng
        (
            id              SERIAL PRIMARY KEY,
            type            VARCHAR(7) NOT NULL,
            country         VARCHAR(4),
            state           VARCHAR(2),
            city            VARCHAR(50),
            zipcode         VARCHAR(10),
            dec_latitude    FLOAT NOT NULL,
            dec_longitude   FLOAT NOT NULL,
            source          VARCHAR(50) NOT NULL,
            first_processed TIMESTAMP NOT NULL,
            last_processed  TIMESTAMP,
            FOREIGN KEY (country) REFERENCES io_countries (country) ON DELETE CASCADE,
            UNIQUE NULLS NOT DISTINCT (type, country, state, city, zipcode)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_category.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_category() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_category"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_category
        (
            category_code   VARCHAR(2)   NOT NULL,
            description     VARCHAR(255) NOT NULL,
            PRIMARY KEY (category_code)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_eventsoe.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_eventsoe() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_eventsoe"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_eventsoe
        (
            eventsoe_code VARCHAR(3)   NOT NULL,
            description   VARCHAR(100) NOT NULL,
            PRIMARY KEY (eventsoe_code)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_modifier.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_modifier() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_modifier"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_modifier
        (
            modifier_code   VARCHAR(3)   NOT NULL,
            description     VARCHAR(100) NOT NULL,
            PRIMARY KEY (modifier_code)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_phase.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_phase() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_phase"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_phase
        (
            phase_code             VARCHAR(3)   NOT NULL,
            description            VARCHAR(100) NOT NULL,
            description_main_phase VARCHAR(100),
            PRIMARY KEY (phase_code)
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_section.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_section() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_section"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_section
        (
            category_code    VARCHAR(2)   NOT NULL,
            subcategory_code VARCHAR(2)   NOT NULL,
            section_code     VARCHAR(2)   NOT NULL,
            description      VARCHAR(255) NOT NULL,
            PRIMARY KEY (category_code, subcategory_code, section_code),
            FOREIGN KEY (category_code, subcategory_code) REFERENCES io_md_codes_subcategory (category_code, subcategory_code) ON DELETE CASCADE
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_subcategory.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_subcategory() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_subcategory"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_subcategory
        (
            category_code    VARCHAR(2)   NOT NULL,
            subcategory_code VARCHAR(2)   NOT NULL,
            description      VARCHAR(255) NOT NULL,
            PRIMARY KEY (category_code, subcategory_code),
            FOREIGN KEY (category_code) REFERENCES io_md_codes_category (category_code) ON DELETE CASCADE
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_md_codes_subsection.
# ------------------------------------------------------------------
def _create_dll_table_io_md_codes_subsection() -> None:
    DLL_TABLE_STMNTS[
        "io_md_codes_subsection"
    ] = """
        CREATE TABLE IF NOT EXISTS io_md_codes_subsection
        (
            category_code    VARCHAR(2)   NOT NULL,
            subcategory_code VARCHAR(2)   NOT NULL,
            section_code     VARCHAR(2)   NOT NULL,
            subsection_code  VARCHAR(2)   NOT NULL,
            description      VARCHAR(255) NOT NULL,
            PRIMARY KEY (category_code, subcategory_code, section_code, subsection_code),
            FOREIGN KEY (category_code, subcategory_code, section_code) REFERENCES io_md_codes_section (category_code, subcategory_code, section_code) ON DELETE CASCADE
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for altering io_msaccess_file.
# ------------------------------------------------------------------
def _create_dll_table_io_msaccess_file_alter() -> None:
    logging.debug(io_glob.LOGGER_START)

    DLL_TABLE_STMNTS[
        "io_msaccess_file"
    ] = """
        ALTER TABLE IF EXISTS io_msaccess_file
              RENAME TO io_processed_data;
    """

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Adds the DDL statement for setting up io_processed_data.
# ------------------------------------------------------------------
def _create_dll_table_io_processed_data() -> None:
    logging.debug(io_glob.LOGGER_START)

    DLL_TABLE_STMNTS[
        "io_processed_data"
    ] = """
        CREATE TABLE IF NOT EXISTS io_processed_data
        (
            table_name        VARCHAR(63) NOT NULL,
            data_source       TEXT        NOT NULL,
            counter_processed INT         NOT NULL DEFAULT 0,
            first_processed   TIMESTAMP   NOT NULL,
            last_processed    TIMESTAMP,
            remarks           TEXT,
            rows_deleted      INT         NOT NULL DEFAULT 0,
            rows_modified     INT         NOT NULL DEFAULT 0,
            rows_new          INT         NOT NULL DEFAULT 0,
            rows_total        INT         NOT NULL DEFAULT 0,
            url               TEXT,
            PRIMARY KEY (table_name, data_source)
        );
    """

    logging.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_sequence_of_events.
# ------------------------------------------------------------------
def _create_dll_table_io_sequence_of_events() -> None:
    DLL_TABLE_STMNTS[
        "io_sequence_of_events"
    ] = """
        CREATE TABLE IF NOT EXISTS io_sequence_of_events
        (
            soe_no          VARCHAR(3)   NOT NULL,
            cictt_code      VARCHAR(10),
            meaning         VARCHAR(100) NOT NULL,
            first_processed TIMESTAMP    NOT NULL,
            last_processed  TIMESTAMP,
            last_seen       TIMESTAMP,
            PRIMARY KEY (soe_no),
            FOREIGN KEY (cictt_code) REFERENCES io_aviation_occurrence_categories (cictt_code) ON DELETE CASCADE
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database table
# io_states.
# ------------------------------------------------------------------
def _create_dll_table_io_states() -> None:
    DLL_TABLE_STMNTS[
        "io_states"
    ] = """
        CREATE TABLE IF NOT EXISTS io_states
        (
            country         VARCHAR(4),
            state           VARCHAR(2),
            state_name      VARCHAR(100),
            dec_latitude    FLOAT NOT NULL,
            dec_longitude   FLOAT NOT NULL,
            first_processed TIMESTAMP NOT NULL,
            last_processed  TIMESTAMP,
            PRIMARY KEY (country, state),
            FOREIGN KEY (country) REFERENCES io_countries (country) ON DELETE CASCADE
        );
    """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database view
# io_app_ae1982.
# ------------------------------------------------------------------
def _create_dll_view_io_app_ae1982() -> None:

    DLL_VIEW_STMNTS_REFRESH.append("io_app_ae1982")

    DLL_VIEW_STMNTS_CREATE_MAT[
        "io_app_ae1982"
    ] = """
        CREATE MATERIALIZED
            VIEW io_app_ae1982
                AS
                    -- -------------------------------------------------------------------------------------------------------------------------------
                    -- Level 4
                    -- -------------------------------------------------------------------------------------------------------------------------------
                    SELECT level_4.ev_id,
                           level_4.ntsb_no,
                           level_4.ev_type,
                           level_4.ev_year,
                           level_4.ev_month,
                           level_4.ev_dow,
                           level_4.country,
                           level_4.state,
                           level_4.city,
                           level_4.zip,
                           level_4.acft_categories,
                           level_4.all_category_codes,
                           level_4.all_category_cause_codes,
                           level_4.all_category_factor_codes,
                           level_4.all_category_none_codes,
                           level_4.all_eventsoe_codes,
                           level_4.all_eventsoe_false_codes,
                           level_4.all_eventsoe_true_codes,
                           level_4.all_finding_codes,
                           level_4.all_finding_cause_codes,
                           level_4.all_finding_factor_codes,
                           level_4.all_finding_none_codes,
                           level_4.all_modifier_codes,
                           level_4.all_modifier_cause_codes,
                           level_4.all_modifier_factor_codes,
                           level_4.all_modifier_none_codes,
                           level_4.all_occurrence_codes,
                           level_4.all_occurrence_false_codes,
                           level_4.all_occurrence_true_codes,
                           level_4.all_phase_codes,
                           level_4.all_phase_false_codes,
                           level_4.all_phase_true_codes,
                           level_4.all_section_codes,
                           level_4.all_section_cause_codes,
                           level_4.all_section_factor_codes,
                           level_4.all_section_none_codes,
                           level_4.all_subcategory_codes,
                           level_4.all_subcategory_cause_codes,
                           level_4.all_subcategory_factor_codes,
                           level_4.all_subcategory_none_codes,
                           level_4.all_subsection_codes,
                           level_4.all_subsection_cause_codes,
                           level_4.all_subsection_factor_codes,
                           level_4.all_subsection_none_codes,
                           REPLACE(COALESCE(NULLIF(level_4.cictt_codes, ''), 'n/a'), 'n/a', 'no data') cictt_codes,
                           level_4.dec_lat_lng_actions,
                           level_4.dec_latitude,
                           level_4.dec_latitude_deviating,
                           level_4.dec_longitude,
                           level_4.dec_longitude_deviating,
                           level_4.description_main_phase_defining,
                           level_4.dest_countries,
                           level_4.dprt_countries,
                           level_4.ev_highest_injury,
                           REPLACE(level_4.far_parts, 'n/a', 'no data') far_parts,
                           level_4.finding_codes,
                           level_4.inj_f_grnd,
                           level_4.inj_tot_f,
                           -- ------------------------------------------------------------------------------------------------------------------------
                           -- BOOLEAN VARIABLES - START ----------------------------------------------------------------------------------------------
                           --
                           level_4.is_altitude_controllable,
                           level_4.is_altitude_low,
                           level_4.is_attitude_controllable,
                           level_4.is_dest_country_usa,
                           level_4.is_dprt_country_usa,
                           level_4.is_emergency_landing,
                           level_4.is_far_part_091x,
                           level_4.is_far_part_121,
                           level_4.is_far_part_135,
                           level_4.is_invalid_latitude,
                           level_4.is_invalid_longitude,
                           level_4.is_invalid_us_city,
                           level_4.is_invalid_us_city_zipcode,
                           level_4.is_invalid_us_state,
                           level_4.is_invalid_us_zipcode,
                           --
                           CASE WHEN level_4.is_altitude_low                           IS TRUE OR
                                     level_4.is_attitude_controllable                  IS TRUE OR
                                     level_4.is_emergency_landing                      IS TRUE OR
                                     level_4.is_midair_collision                       IS TRUE OR
                                     level_4.is_pilot_issue                            IS TRUE OR
                                     level_4.is_rss_forced_landing                     IS TRUE OR
                                     level_4.is_rss_spin_stall_prevention_and_recovery IS TRUE OR
                                     level_4.is_rss_terrain_collision_avoidance        IS TRUE OR
                                     level_4.is_spin_stall                             IS TRUE THEN FALSE
                                                                                               ELSE TRUE
                            END is_lp_n_a,
                           --
                           level_4.is_midair_collision,
                           level_4.is_narrative_stall,
                           level_4.is_oper_country_usa,
                           level_4.is_owner_country_usa,
                           level_4.is_pilot_issue,
                           level_4.is_regis_country_usa,
                           level_4.is_rss_forced_landing,
                           --
                           CASE WHEN level_4.is_midair_collision                       IS TRUE OR
                                     level_4.is_rss_forced_landing                     IS TRUE OR
                                     level_4.is_rss_spin_stall_prevention_and_recovery IS TRUE OR
                                     level_4.is_rss_terrain_collision_avoidance        IS TRUE THEN FALSE
                                                                                              ELSE TRUE
                            END is_rss_n_a,
                           --
                           level_4.is_rss_spin_stall_prevention_and_recovery,
                           level_4.is_rss_terrain_collision_avoidance,
                           level_4.is_spin_stall,
                           --
                           -- BOOLEAN VARIABLES - END ------------------------------------------------------------------------------------------------
                           -- ------------------------------------------------------------------------------------------------------------------------
                           level_4.latlong_acq,
                           level_4.nearest_airport_distance,
                           level_4.nearest_airport_global_id,
                           level_4.nearest_airport_ident,
                           level_4.nearest_airport_servcity,
                           level_4.no_aircraft,
                           level_4.occurrence_codes,
                           level_4.oper_countries,
                           level_4.owner_countries,
                           COALESCE(NULLIF(level_4.phase_codes_defining, ''), 'no data') phase_codes_defining,
                           (SELECT ARRAY_TO_STRING(ARRAY(SELECT CASE WHEN level_4.is_midair_collision                       IS TRUE
                                                                     THEN 'Airborne collision'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_rss_forced_landing                     IS TRUE
                                                                     THEN 'Forced landing'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_rss_spin_stall_prevention_and_recovery IS TRUE
                                                                     THEN 'Spin / stall'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_rss_terrain_collision_avoidance        IS TRUE
                                                                     THEN 'Terrain collision'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_midair_collision                       IS FALSE AND
                                                                          level_4.is_rss_forced_landing                     IS FALSE AND
                                                                          level_4.is_rss_spin_stall_prevention_and_recovery IS FALSE AND
                                                                          level_4.is_rss_terrain_collision_avoidance        IS FALSE
                                                                     THEN 'Not preventable'
                                                                END
                                                          ORDER BY 1),', ')) preventable_events,
                           level_4.regis_countries,
                           level_4.regis_nos,
                           (SELECT ARRAY_TO_STRING(ARRAY(SELECT CASE WHEN level_4.is_spin_stall                             IS TRUE
                                                                     THEN 'Aerodynamic spin / stall'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_altitude_controllable                  IS TRUE
                                                                     THEN 'Aircraft can climb'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_emergency_landing                      IS TRUE
                                                                     THEN 'Aircraft has degraded control failure'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_altitude_low                           IS TRUE
                                                                     THEN 'Altitude too low'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_attitude_controllable                  IS TRUE
                                                                     THEN 'Attitude is controllable'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_pilot_issue                            IS TRUE
                                                                     THEN 'Pilot is able to perform maneuver'
                                                                END
                                                          UNION
                                                         SELECT CASE WHEN level_4.is_spin_stall                             IS FALSE AND
                                                                          level_4.is_altitude_controllable                  IS FALSE AND
                                                                          level_4.is_emergency_landing                      IS FALSE AND
                                                                          level_4.is_altitude_low                           IS FALSE AND
                                                                          level_4.is_attitude_controllable                  IS FALSE AND
                                                                          level_4.is_pilot_issue                            IS FALSE
                                                                     THEN 'n/a'
                                                                END
                                                          ORDER BY 1),', ')) tll_parameters
                  FROM (-- -----------------------------------------------------------------------------------------------------------------------
                        -- Level 3
                        -- -------------------------------------------------------------------------------------------------------------------------------
                        SELECT level_3.ev_id,
                               level_3.ntsb_no,
                               level_3.ev_type,
                               level_3.ev_year,
                               level_3.ev_month,
                               level_3.ev_dow,
                               level_3.country,
                               level_3.state,
                               level_3.city,
                               level_3.zip,
                               level_3.acft_categories,
                               level_3.all_category_codes,
                               level_3.all_category_cause_codes,
                               level_3.all_category_factor_codes,
                               level_3.all_category_none_codes,
                               level_3.all_eventsoe_codes,
                               level_3.all_eventsoe_false_codes,
                               level_3.all_eventsoe_true_codes,
                               level_3.all_finding_codes,
                               level_3.all_finding_cause_codes,
                               level_3.all_finding_factor_codes,
                               level_3.all_finding_none_codes,
                               level_3.all_modifier_codes,
                               level_3.all_modifier_cause_codes,
                               level_3.all_modifier_factor_codes,
                               level_3.all_modifier_none_codes,
                               level_3.all_occurrence_codes,
                               level_3.all_occurrence_false_codes,
                               level_3.all_occurrence_true_codes,
                               level_3.all_phase_codes,
                               level_3.all_phase_false_codes,
                               level_3.all_phase_true_codes,
                               level_3.all_section_codes,
                               level_3.all_section_cause_codes,
                               level_3.all_section_factor_codes,
                               level_3.all_section_none_codes,
                               level_3.all_subcategory_codes,
                               level_3.all_subcategory_cause_codes,
                               level_3.all_subcategory_factor_codes,
                               level_3.all_subcategory_none_codes,
                               level_3.all_subsection_codes,
                               level_3.all_subsection_cause_codes,
                               level_3.all_subsection_factor_codes,
                               level_3.all_subsection_none_codes,
                               level_3.cictt_codes,
                               level_3.dec_lat_lng_actions,
                               level_3.dec_latitude,
                               level_3.dec_latitude_deviating,
                               level_3.dec_longitude,
                               level_3.dec_longitude_deviating,
                               level_3.description_main_phase_defining,
                               level_3.dest_countries,
                               level_3.dprt_countries,
                               level_3.ev_highest_injury,
                               level_3.far_parts,
                               level_3.finding_codes,
                               level_3.inj_f_grnd,
                               level_3.inj_tot_f,
                               -- ------------------------------------------------------------------------------------------------------------------------
                               -- BOOLEAN VARIABLES - START ----------------------------------------------------------------------------------------------
                               --
                               level_3.is_altitude_controllable,
                               level_3.is_altitude_low,
                               level_3.is_attitude_controllable,
                               level_3.is_dest_country_usa,
                               level_3.is_dprt_country_usa,
                               level_3.is_emergency_landing,
                               level_3.is_far_part_091x,
                               level_3.is_far_part_121,
                               level_3.is_far_part_135,
                               level_3.is_invalid_latitude,
                               level_3.is_invalid_longitude,
                               level_3.is_invalid_us_city,
                               level_3.is_invalid_us_city_zipcode,
                               level_3.is_invalid_us_state,
                               level_3.is_invalid_us_zipcode,
                               level_3.is_midair_collision,
                               level_3.is_narrative_stall,
                               level_3.is_oper_country_usa,
                               level_3.is_owner_country_usa,
                               level_3.is_pilot_issue,
                               level_3.is_regis_country_usa,
                               --
                               CASE WHEN level_3.is_attitude_controllable IS TRUE AND
                                         level_3.is_emergency_landing     IS TRUE THEN TRUE
                                                                                  ELSE FALSE
                                END is_rss_forced_landing,
                               --
                               CASE WHEN level_3.is_attitude_controllable IS TRUE AND
                                         level_3.is_spin_stall            IS TRUE THEN TRUE
                                                                                  ELSE FALSE
                                END is_rss_spin_stall_prevention_and_recovery,
                               --
                               CASE WHEN level_3.is_attitude_controllable IS TRUE AND
                                         level_3.is_altitude_low          IS TRUE AND
                                         level_3.is_altitude_controllable IS TRUE THEN TRUE
                                                                                  ELSE FALSE
                                END is_rss_terrain_collision_avoidance,
                               --
                               level_3.is_spin_stall,
                               --
                               -- BOOLEAN VARIABLES - END ------------------------------------------------------------------------------------------------
                               -- ------------------------------------------------------------------------------------------------------------------------
                               level_3.latlong_acq,
                               level_3.nearest_airport_distance,
                               level_3.nearest_airport_global_id,
                               level_3.nearest_airport_ident,
                               level_3.nearest_airport_servcity,
                               level_3.no_aircraft,
                               level_3.occurrence_codes,
                               level_3.oper_countries,
                               level_3.owner_countries,
                               level_3.phase_codes_defining,
                               level_3.regis_countries,
                               level_3.regis_nos
                          FROM (-- -----------------------------------------------------------------------------------------------------------------------
                                -- Level 2
                                -- -----------------------------------------------------------------------------------------------------------------------
                                SELECT level_2.ev_id,
                                       level_2.ntsb_no,
                                       level_2.ev_type,
                                       level_2.ev_year,
                                       level_2.ev_month,
                                       level_2.ev_dow,
                                       level_2.country,
                                       level_2.state,
                                       level_2.city,
                                       level_2.zip,
                                       level_2.acft_categories,
                                       level_2.all_category_codes,
                                       level_2.all_category_cause_codes,
                                       level_2.all_category_factor_codes,
                                       level_2.all_category_none_codes,
                                       level_2.all_eventsoe_codes,
                                       level_2.all_eventsoe_false_codes,
                                       level_2.all_eventsoe_true_codes,
                                       level_2.all_finding_codes,
                                       level_2.all_finding_cause_codes,
                                       level_2.all_finding_factor_codes,
                                       level_2.all_finding_none_codes,
                                       level_2.all_modifier_codes,
                                       level_2.all_modifier_cause_codes,
                                       level_2.all_modifier_factor_codes,
                                       level_2.all_modifier_none_codes,
                                       level_2.all_occurrence_codes,
                                       level_2.all_occurrence_false_codes,
                                       level_2.all_occurrence_true_codes,
                                       level_2.all_phase_codes,
                                       level_2.all_phase_false_codes,
                                       level_2.all_phase_true_codes,
                                       level_2.all_section_codes,
                                       level_2.all_section_cause_codes,
                                       level_2.all_section_factor_codes,
                                       level_2.all_section_none_codes,
                                       level_2.all_subcategory_codes,
                                       level_2.all_subcategory_cause_codes,
                                       level_2.all_subcategory_factor_codes,
                                       level_2.all_subcategory_none_codes,
                                       level_2.all_subsection_codes,
                                       level_2.all_subsection_cause_codes,
                                       level_2.all_subsection_factor_codes,
                                       level_2.all_subsection_none_codes,
                                       level_2.cictt_codes,
                                       level_2.dec_lat_lng_actions,
                                       level_2.dec_latitude,
                                       level_2.dec_latitude_deviating,
                                       level_2.dec_longitude,
                                       level_2.dec_longitude_deviating,
                                       level_2.description_main_phase_defining,
                                       level_2.dest_countries,
                                       level_2.dprt_countries,
                                       level_2.ev_highest_injury,
                                       ARRAY_TO_STRING(level_2.far_parts,', ') far_parts,
                                       level_2.finding_codes,
                                       level_2.inj_f_grnd,
                                       level_2.inj_tot_f,
                                       -- ------------------------------------------------------------------------------------------------------------------------
                                       -- BOOLEAN VARIABLES - START ----------------------------------------------------------------------------------------------
                                       --
                                       CASE WHEN level_2.is_attitude_controllable AND NOT
                                                 level_2.is_emergency_landing     AND NOT
                                                 level_2.is_spin_stall THEN TRUE
                                                                       ELSE FALSE
                                        END is_altitude_controllable,
                                       CASE WHEN ('CAA'              = ANY (level_2.occurrence_codes)                                                   OR
                                                  'CFIT'             = ANY (level_2.occurrence_codes)                                                   OR
                                                 ('ENV_OAS'          = ANY (level_2.finding_codes)   AND NOT ('BIRD' = ANY (level_2.occurrence_codes))) OR
                                                  'ENV_TER'          = ANY (level_2.finding_codes)                                                      OR
                                                  'FINAL_APP'        = ANY (level_2.occurrence_codes)                                                   OR
                                                  'INIT_CLIMB'       = ANY (level_2.occurrence_codes)                                                   OR
                                                  'LALT'             = ANY (level_2.occurrence_codes)                                                   OR
                                                  'MAN_LALT'         = ANY (level_2.occurrence_codes)                                                   OR
                                                  'PARAMS_ALT'       = ANY (level_2.finding_codes)                                                      OR
                                                  'PARAMS_DEC_APP'   = ANY (level_2.finding_codes)                                                      OR
                                                  'PARAMS_DEC_RATE'  = ANY (level_2.finding_codes))                                                     AND
                                             NOT ('MIDAIR'           = ANY (level_2.occurrence_codes))                                                  AND
                                                  level_2.is_spin_stall IS FALSE THEN TRUE
                                                                                 ELSE FALSE
                                        END is_altitude_low,
                                       --
                                       level_2.is_attitude_controllable,
                                       --
                                       level_2.is_dest_country_usa,
                                       level_2.is_dprt_country_usa,
                                       level_2.is_emergency_landing,
                                       level_2.is_far_part_091x,
                                       level_2.is_far_part_121,
                                       level_2.is_far_part_135,
                                       level_2.is_invalid_latitude,
                                       level_2.is_invalid_longitude,
                                       level_2.is_invalid_us_city,
                                       level_2.is_invalid_us_city_zipcode,
                                       level_2.is_invalid_us_state,
                                       level_2.is_invalid_us_zipcode,
                                       level_2.is_midair_collision,
                                       level_2.is_narrative_stall,
                                       level_2.is_oper_country_usa,
                                       level_2.is_owner_country_usa,
                                       level_2.is_pilot_issue,
                                       level_2.is_regis_country_usa,
                                       level_2.is_spin_stall,
                                       --
                                       -- BOOLEAN VARIABLES - END ------------------------------------------------------------------------------------------------
                                       -- ------------------------------------------------------------------------------------------------------------------------
                                       level_2.latlong_acq,
                                       level_2.nearest_airport_distance,
                                       level_2.nearest_airport_global_id,
                                       level_2.nearest_airport_ident,
                                       level_2.nearest_airport_servcity,
                                       level_2.no_aircraft,
                                       level_2.occurrence_codes,
                                       level_2.oper_countries,
                                       level_2.owner_countries,
                                       level_2.phase_codes_defining,
                                       level_2.regis_countries,
                                       level_2.regis_nos
                                  FROM (-- -----------------------------------------------------------------------------------------------------------------------
                                        -- Level 1
                                        -- -----------------------------------------------------------------------------------------------------------------------
                                        SELECT level_1.ev_id,
                                               level_1.ntsb_no,
                                               level_1.ev_type,
                                               level_1.ev_year,
                                               level_1.ev_month,
                                               level_1.ev_dow,
                                               level_1.country,
                                               level_1.state,
                                               level_1.city,
                                               level_1.zip,
                                               level_1.acft_categories,
                                               level_1.all_category_codes,
                                               level_1.all_category_cause_codes,
                                               level_1.all_category_factor_codes,
                                               level_1.all_category_none_codes,
                                               level_1.all_eventsoe_codes,
                                               level_1.all_eventsoe_false_codes,
                                               level_1.all_eventsoe_true_codes,
                                               level_1.all_finding_codes,
                                               level_1.all_finding_cause_codes,
                                               level_1.all_finding_factor_codes,
                                               level_1.all_finding_none_codes,
                                               level_1.all_modifier_codes,
                                               level_1.all_modifier_cause_codes,
                                               level_1.all_modifier_factor_codes,
                                               level_1.all_modifier_none_codes,
                                               level_1.all_occurrence_codes,
                                               level_1.all_occurrence_false_codes,
                                               level_1.all_occurrence_true_codes,
                                               level_1.all_phase_codes,
                                               level_1.all_phase_false_codes,
                                               level_1.all_phase_true_codes,
                                               level_1.all_section_codes,
                                               level_1.all_section_cause_codes,
                                               level_1.all_section_factor_codes,
                                               level_1.all_section_none_codes,
                                               level_1.all_subcategory_codes,
                                               level_1.all_subcategory_cause_codes,
                                               level_1.all_subcategory_factor_codes,
                                               level_1.all_subcategory_none_codes,
                                               level_1.all_subsection_codes,
                                               level_1.all_subsection_cause_codes,
                                               level_1.all_subsection_factor_codes,
                                               level_1.all_subsection_none_codes,
                                               level_1.cictt_codes,
                                               level_1.dec_lat_lng_actions,
                                               level_1.dec_latitude,
                                               level_1.dec_latitude_deviating,
                                               level_1.dec_longitude,
                                               level_1.dec_longitude_deviating,
                                               level_1.description_main_phase_defining,
                                               level_1.dest_countries,
                                               level_1.dprt_countries,
                                               level_1.ev_highest_injury,
                                               level_1.far_parts,
                                               level_1.finding_codes,
                                               level_1.inj_f_grnd,
                                               level_1.inj_tot_f,
                                               -- ----------------------------------------------------------------------------------------------------------------
                                               -- BOOLEAN VARIABLES - START --------------------------------------------------------------------------------------
                                               --
                                               level_1.is_attitude_controllable,
                                               --
                                               CASE WHEN 'USA' = ANY (level_1.dest_countries) THEN TRUE
                                                    ELSE FALSE
                                                END is_dest_country_usa,
                                               --
                                               CASE WHEN 'USA' = ANY (level_1.dprt_countries) THEN TRUE
                                                    ELSE FALSE
                                                END is_dprt_country_usa,
                                               --
                                               CASE WHEN level_1.is_attitude_controllable AND
                                                         ((SELECT COUNT(*)
                                                             FROM findings f
                                                            WHERE f.ev_id = level_1.ev_id
                                                              AND (f.modifier_no                 = '01'        -- Failure
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010224'    -- Aircraft-Aircraft systems-Electrical power system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010228'    -- Aircraft-Aircraft systems-Fuel system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010230'    -- Aircraft-Aircraft systems-Ice/rain protection system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010461'    -- Aircraft-Aircraft propeller/rotor-Propeller system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010462'    -- Aircraft-Aircraft propeller/rotor-Main rotor system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010465'    -- Aircraft-Aircraft propeller/rotor-Tail rotor drive system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010467'    -- Aircraft-Aircraft propeller/rotor-Rotorcraft flight control
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01050000'  -- Aircraft-Aircraft power plant-(general)
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010571'    -- Aircraft-Aircraft power plant-Power plant
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010572'    -- Aircraft-Aircraft power plant-Engine (turbine/turboprop)
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010573'    -- Aircraft-Aircraft power plant-Engine fuel and control
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010574'    -- Aircraft-Aircraft power plant-Ignition system
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010578'    -- Aircraft-Aircraft power plant-Engine exhaust
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010579'    -- Aircraft-Aircraft power plant-Eng oil sys (airframe furnish)
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010581'    -- Aircraft-Aircraft power plant-Turbocharging (recip only)
                                                               OR  SUBSTRING(f.finding_code,1,6) = '010585'    -- Aircraft-Aircraft power plant-Engine (reciprocating)
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01061010'  -- Aircraft-Aircraft oper/perf/capability-Aircraft capability-Climb capability
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01061020'  -- Aircraft-Aircraft oper/perf/capability-Aircraft capability-Engine out capability
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01062025'  -- Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Engine out control
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01071000'  -- Aircraft-Fluids/misc hardware-Fluids
                                                               OR  SUBSTRING(f.finding_code,1,8) = '01071010'  -- Aircraft-Fluids/misc hardware-Fluids-Fuel
                                                               OR  f.modifier_no                 = '02'        -- Malfunction
                                                               OR  f.modifier_no                 = '03'        -- Simulated malf/failure
                                                               OR  f.modifier_no                 = '06'        -- Fatigue/wear/corrosion
                                                               OR  f.modifier_no                 = '22'        -- Fluid type
                                                               OR  f.modifier_no                 = '23'        -- Fluid condition
                                                               OR  f.modifier_no                 = '24'        -- Fluid level
                                                               OR  f.modifier_no                 = '25'        -- Fluid management
                                                               OR  f.modifier_no                 = '26')       -- Inoperative
                                                            LIMIT 1)
                                                        + (SELECT COUNT(*)
                                                             FROM events_sequence es
                                                             WHERE es.ev_id = level_1.ev_id
                                                               AND (es.phase_no    = '600'   -- Emergency descent
                                                                OR  es.eventsoe_no = '130'   -- Emergency descent initiated
                                                                OR  es.eventsoe_no = '140'   -- Engine shutdown
                                                                OR  es.eventsoe_no = '190'   -- Fuel related
                                                                OR  es.eventsoe_no = '191'   -- Fuel starvation
                                                                OR  es.eventsoe_no = '192'   -- Fuel exhaustion
                                                                OR  es.eventsoe_no = '193'   -- Fuel contamination
                                                                OR  es.eventsoe_no = '194'   -- Wrong fuel
                                                                OR  es.eventsoe_no = '337'   -- Aircraft structural failure
                                                               AND  es.defining_ev IS TRUE
                                                                OR  es.eventsoe_no = '338'   -- Part(s) separation from AC
                                                               AND  es.defining_ev IS TRUE
                                                                OR  es.eventsoe_no = '340'   -- Powerplant sys/comp malf/fail
                                                                OR  es.eventsoe_no = '341'   -- Loss of engine power (total)
                                                                OR  es.eventsoe_no = '342'   -- Loss of engine power (partial)
                                                                OR  es.eventsoe_no = '343'   -- Uncontained engine failure
                                                                OR  es.eventsoe_no = '440'   -- Off-field or emergency landing
                                                                OR  es.eventsoe_no = '441'   -- Ditching
                                                                OR  es.eventsoe_no = '500'   -- Loss of lift
                                                                OR  es.eventsoe_no = '901')  -- Birdstrike
                                                             LIMIT 1)) > 0 THEN TRUE
                                                                           ELSE FALSE
                                                END is_emergency_landing,
                                               --
                                               CASE WHEN ARRAY ['091', '091F', '091K'] && level_1.far_parts::TEXT[] THEN TRUE
                                                                                                                    ELSE FALSE
                                                END is_far_part_091x,
                                               --
                                               CASE WHEN ARRAY ['121'] <@ level_1.far_parts::TEXT[] THEN TRUE
                                                                                                    ELSE FALSE
                                                END is_far_part_121,
                                               --
                                               CASE WHEN ARRAY ['135'] <@ level_1.far_parts::TEXT[] THEN TRUE
                                                                                                    ELSE FALSE
                                                END is_far_part_135,
                                               --
                                               level_1.is_invalid_latitude,
                                               level_1.is_invalid_longitude,
                                               level_1.is_invalid_us_city,
                                               level_1.is_invalid_us_city_zipcode,
                                               level_1.is_invalid_us_state,
                                               level_1.is_invalid_us_zipcode,
                                               level_1.is_midair_collision,
                                               level_1.is_narrative_stall,
                                               --
                                               CASE WHEN 'USA' = ANY (level_1.oper_countries) THEN TRUE
                                                                                              ELSE FALSE
                                                END is_oper_country_usa,
                                               --
                                               CASE WHEN 'USA' = ANY (level_1.owner_countries) THEN TRUE
                                                                                               ELSE FALSE
                                                END is_owner_country_usa,
                                               --
                                               level_1.is_pilot_issue,
                                               --
                                               CASE WHEN 'USA' = ANY (level_1.regis_countries) THEN TRUE
                                                                                               ELSE FALSE
                                                END is_regis_country_usa,
                                               --
                                               CASE WHEN (('PARAMS_AoA' = ANY (level_1.finding_codes)    OR
                                                           'STALL'      = ANY (level_1.occurrence_codes) OR
                                                          ('LOC-I'      = ANY (level_1.occurrence_codes) AND
                                                           level_1.is_narrative_stall))                  AND NOT
                                                         ('CAA'         = ANY (level_1.occurrence_codes) OR
                                                          'CFIT'        = ANY (level_1.occurrence_codes))) THEN TRUE
                                                                                                           ELSE FALSE
                                                END is_spin_stall,
                                               --
                                               -- BOOLEAN VARIABLES - END ----------------------------------------------------------------------------------------
                                               -- ----------------------------------------------------------------------------------------------------------------
                                               level_1.latlong_acq,
                                               level_1.nearest_airport_distance,
                                               level_1.nearest_airport_global_id,
                                               level_1.nearest_airport_ident,
                                               level_1.nearest_airport_servcity,
                                               level_1.no_aircraft,
                                               level_1.occurrence_codes,
                                               level_1.oper_countries,
                                               level_1.owner_countries,
                                               level_1.phase_codes_defining,
                                               level_1.regis_countries,
                                               level_1.regis_nos
                                          FROM (-- ---------------------------------------------------------------------------------------------------------------
                                                -- Base
                                                -- ---------------------------------------------------------------------------------------------------------------
                                                SELECT ifu.ev_id,
                                                       ifu.ntsb_no,
                                                       ifu.ev_type,
                                                       ifu.ev_year,
                                                       ifu.ev_month,
                                                       UPPER(ifu.ev_dow) ev_dow,
                                                       COALESCE(ifu.io_country, ifu.ev_country) country,
                                                       COALESCE(ifu.io_state, ifu.ev_state) state,
                                                       COALESCE(ifu.io_city, ifu.ev_city) city,
                                                       COALESCE(ifu.io_site_zipcode, ifu.ev_site_zipcode) zip,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.acft_category, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) acft_categories,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fc_', f.category_no, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_category_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fc_', f.category_no, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_category_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fc_', f.category_no, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_category_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fc_', f.category_no, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_category_none_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ee_', es.eventsoe_no, '_a')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_eventsoe_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ee_', es.eventsoe_no, '_f')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS NOT TRUE
                                                                      ORDER BY 1)) all_eventsoe_false_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ee_', es.eventsoe_no, '_t')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS TRUE
                                                                      ORDER BY 1)) all_eventsoe_true_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ff_', f.finding_code, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_finding_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ff_', f.finding_code, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_finding_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ff_', f.finding_code, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_finding_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ff_', f.finding_code, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_finding_none_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fm_', f.modifier_no, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_modifier_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fm_', f.modifier_no, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_modifier_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fm_', f.modifier_no, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_modifier_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fm_', f.modifier_no, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_modifier_none_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('eo_', es.occurrence_code, '_a')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_occurrence_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('eo_', es.occurrence_code, '_f')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS NOT TRUE
                                                                      ORDER BY 1)) all_occurrence_false_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('eo_', es.occurrence_code, '_t')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS TRUE
                                                                      ORDER BY 1)) all_occurrence_true_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ep_', es.phase_no, '_a')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_phase_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ep_', es.phase_no, '_f')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS NOT TRUE
                                                                      ORDER BY 1)) all_phase_false_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('ep_', es.phase_no, '_t')
                                                                       FROM events_sequence es
                                                                      WHERE es.ev_id = ifu.ev_id
                                                                        AND es.defining_ev IS TRUE
                                                                      ORDER BY 1)) all_phase_true_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fs_', f.category_no, f.subcategory_no, f.section_no, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_section_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fs_', f.category_no, f.subcategory_no, f.section_no, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_section_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fs_', f.category_no, f.subcategory_no, f.section_no, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_section_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fs_', f.category_no, f.subcategory_no, f.section_no, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_section_none_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fsc_', f.category_no, f.subcategory_no, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subcategory_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fsc_', f.category_no, f.subcategory_no, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subcategory_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fsc_', f.category_no, f.subcategory_no, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subcategory_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fsc_', f.category_no, f.subcategory_no, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subcategory_none_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fss_', f.category_no, f.subcategory_no, f.section_no, f.subsection_no, '_a')
                                                                       FROM findings f
                                                                      WHERE f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subsection_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fss_', f.category_no, f.subcategory_no, f.section_no, f.subsection_no, '_c')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'C'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subsection_cause_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fss_', f.category_no, f.subcategory_no, f.section_no, f.subsection_no, '_f')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor = 'F'
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subsection_factor_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT CONCAT('fss_', f.category_no, f.subcategory_no, f.section_no, f.subsection_no, '_n')
                                                                       FROM findings f
                                                                      WHERE f.cause_factor NOT IN  ('C', 'F')
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) all_subsection_none_codes,
                                                       --
                                                       (SELECT ARRAY_TO_STRING(ARRAY (SELECT DISTINCT COALESCE(isoe.cictt_code, 'n/a')
                                                                                        FROM events_sequence es LEFT OUTER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
                                                                                       WHERE es.ev_id = ifu.ev_id
                                                                                         AND es.defining_ev  IS TRUE
                                                                                       ORDER BY 1),', ')) cictt_codes,
                                                       --
                                                       ifu.io_dec_lat_lng_actions dec_lat_lng_actions,
                                                       COALESCE(ifu.io_dec_latitude, ifu.dec_latitude) dec_latitude,
                                                       COALESCE(ifu.io_dec_latitude_deviating, 0) dec_latitude_deviating,
                                                       COALESCE(ifu.io_dec_longitude, ifu.dec_longitude) dec_longitude,
                                                       COALESCE(ifu.io_dec_longitude_deviating, 0) dec_longitude_deviating,
                                                       --
                                                       (SELECT ARRAY_TO_STRING(ARRAY (SELECT DISTINCT imcp.description_main_phase
                                                                                        FROM events_sequence es INNER JOIN io_md_codes_phase imcp ON es.phase_no = imcp.phase_code
                                                                                       WHERE es.ev_id = ifu.ev_id
                                                                                         AND es.defining_ev  IS TRUE
                                                                                       ORDER BY 1),', ')) description_main_phase_defining,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.dest_country, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) dest_countries,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.dprt_country, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) dprt_countries,
                                                       --
                                                       CASE WHEN ifu.ev_highest_injury IN ('FATL', 'MINR', 'NONE', 'SERS') THEN ifu.ev_highest_injury
                                                                                                                           ELSE 'n/a'
                                                            END ev_highest_injury,
                                                       --
                                                       (SELECT ARRAY(SELECT DISTINCT COALESCE(a.far_part, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) far_parts,
                                                       --
                                                       (SELECT ARRAY(SELECT CASE WHEN SUBSTRING(f.finding_code,1,8) = '01062012' THEN 'PARAMS_ALT'       -- Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Altitude
                                                                                 WHEN SUBSTRING(f.finding_code,1,8) = '01062037' THEN 'PARAMS_DEC_RATE'  -- Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Descent rate
                                                                                 WHEN SUBSTRING(f.finding_code,1,8) = '01062040' THEN 'PARAMS_DEC_APP'   -- Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Descent/approach/glide path
                                                                                 WHEN SUBSTRING(f.finding_code,1,8) = '01062042' THEN 'PARAMS_AoA'       -- Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Angle of attack
                                                                                 WHEN SUBSTRING(f.finding_code,1,6) = '030210'   THEN 'ENV_TER'          -- Environmental issues-Physical environment-Terrain
                                                                                 WHEN SUBSTRING(f.finding_code,1,6) = '030220'   THEN 'ENV_OAS'          -- Environmental issues-Physical environment-Object/animal/substance
                                                                                                                                 ELSE f.finding_code
                                                                            END
                                                                       FROM findings f
                                                                      WHERE (SUBSTRING(f.finding_code,1,8) IN ('01062012', '01062037', '01062040', '01062042')
                                                                         OR  SUBSTRING(f.finding_code,1,6) IN ('030210', '030220'))
                                                                        AND f.finding_code IS NOT NULL
                                                                        AND f.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) finding_codes,
                                                       --
                                                       COALESCE(ifu.inj_f_grnd, 0) inj_f_grnd,
                                                       COALESCE(ifu.inj_tot_f, 0) inj_tot_f,
                                                       -- --------------------------------------------------------------------------------------------------------
                                                       -- BOOLEAN VARIABLES - START ------------------------------------------------------------------------------
                                                       --
                                                       CASE WHEN ((SELECT COUNT(*)
                                                                     FROM findings f
                                                                    WHERE f.ev_id = ifu.ev_id
                                                                      AND (SUBSTRING(f.finding_code,1,6) = '010355'     -- Aircraft-Aircraft structures-Empennage structure
                                                                       OR  SUBSTRING(f.finding_code,1,6) = '010357'     -- Aircraft-Aircraft structures-Wing structure
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '01061040'   -- Aircraft-Aircraft oper/perf/capability-Aircraft capability-CG/weight distribution
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '03031025'   -- Environmental issues-Conditions/weather/phenomena-Temp/humidity/pressure-Conducive to structural icing
                                                                       OR  SUBSTRING(f.finding_code,1,6) = '030320'     -- Environmental issues-Conditions/weather/phenomena-Turbulence-(general)
                                                                       OR  SUBSTRING(f.finding_code,1,6) = '030330'     -- Environmental issues-Conditions/weather/phenomena-Convective weather-(general)
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '03034020'   -- Environmental issues-Conditions/weather/phenomena-Wind-Windshear
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '03034030'   -- Environmental issues-Conditions/weather/phenomena-Wind-Updraft
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '03034050'   -- Environmental issues-Conditions/weather/phenomena-Wind-Microburst
                                                                       OR  SUBSTRING(f.finding_code,1,8) = '03034060')  -- Environmental issues-Conditions/weather/phenomena-Wind-Dust devil/whirlwind
                                                                    LIMIT 1)
                                                                + (SELECT COUNT(*)
                                                                     FROM events_sequence es
                                                                     WHERE es.ev_id = ifu.ev_id
                                                                       AND (es.eventsoe_no = '210'   -- Structural Icing
                                                                        OR  es.eventsoe_no = '245'   -- Mast bumping
                                                                        OR  es.eventsoe_no = '333'   -- Flight control sys malf/fail
                                                                        OR  es.eventsoe_no = '337'   -- Aircraft structural failure
                                                                       AND  es.defining_ev IS TRUE
                                                                        OR  es.eventsoe_no = '338'   -- Part(s) separation from AC
                                                                       AND  es.defining_ev IS TRUE
                                                                        OR  es.eventsoe_no = '361')  -- Aircraft wake turb encounter
                                                                     LIMIT 1)) = 0 THEN TRUE
                                                                                   ELSE FALSE
                                                        END is_attitude_controllable,
                                                       --
                                                       ifu.io_invalid_latitude is_invalid_latitude,
                                                       ifu.io_invalid_longitude is_invalid_longitude,
                                                       ifu.io_invalid_us_city is_invalid_us_city,
                                                       ifu.io_invalid_us_city_zipcode is_invalid_us_city_zipcode,
                                                       ifu.io_invalid_us_state is_invalid_us_state,
                                                       ifu.io_invalid_us_zipcode is_invalid_us_zipcode,
                                                       --
                                                       CASE WHEN ((SELECT COUNT(*)
                                                                     FROM events_sequence es
                                                                     WHERE es.ev_id = ifu.ev_id
                                                                       AND es.eventsoe_no = '250'   -- Midair collision
                                                                       AND es.defining_ev IS TRUE
                                                                     LIMIT 1)) = 0 THEN FALSE
                                                                                   ELSE TRUE
                                                        END is_midair_collision,
                                                       --
                                                       COALESCE((SELECT TRUE
                                                                   FROM narratives n
                                                                  WHERE upper(narr_accp) LIKE '%STALL%'
                                                                    AND n.narr_accp  IS NOT NULL
                                                                    AND n.ev_id = ifu.ev_id
                                                                   LIMIT 1), FALSE) is_narrative_stall,
                                                       --
                                                       CASE WHEN (SELECT COUNT(*)
                                                                    FROM findings f
                                                                   WHERE f.ev_id = ifu.ev_id
                                                                     AND (f.modifier_no = '44'   -- Pilot
                                                                      OR  f.modifier_no = '45'   -- Pilot of other aircraft
                                                                      OR  f.modifier_no = '46')  -- Student/instructed pilot
                                                                    LIMIT 1) = 0 THEN FALSE
                                                                                  ELSE TRUE
                                                        END is_pilot_issue,
                                                       --
                                                       -- BOOLEAN VARIABLES - END --------------------------------------------------------------------------------
                                                       -- --------------------------------------------------------------------------------------------------------
                                                       CASE WHEN ifu.io_latlong_acq                                 IS     NULL
                                                             AND ifu.latlong_acq                                    IS     NULL
                                                             AND (COALESCE(ifu.io_dec_latitude, ifu.dec_latitude)   IS NOT NULL
                                                              OR  COALESCE(ifu.io_dec_longitude, ifu.dec_longitude) IS NOT NULL) THEN 'NONE'
                                                                                                                                 ELSE COALESCE(ifu.io_latlong_acq, ifu.latlong_acq, 'NREC')
                                                        END latlong_acq,
                                                       ifu.io_nearest_airport_distance  nearest_airport_distance,
                                                       ifu.io_nearest_airport_global_id nearest_airport_global_id,
                                                       a.ident                          nearest_airport_ident,
                                                       a.servcity                       nearest_airport_servcity,
                                                       --
                                                       (SELECT COUNT(*)
                                                          FROM aircraft a
                                                         WHERE a.ev_id = ifu.ev_id) no_aircraft,
                                                       --
                                                       (SELECT ARRAY(SELECT CASE WHEN es.phase_no    = '350' THEN 'INIT_CLIMB'  -- Initial climb
                                                                                 WHEN es.phase_no    = '452' THEN 'MAN_LALT'    -- Maneuvering-low-alt flying
                                                                                 WHEN es.phase_no    = '502' THEN 'FINAL_APP'   -- Approach-IFR final approach
                                                                                 WHEN es.eventsoe_no = '120' THEN 'CFIT'        -- Controlled flight into terr/obj
                                                                                 WHEN es.eventsoe_no = '220' THEN 'LALT'        -- Low altitude operation/event
                                                                                 WHEN es.eventsoe_no = '240' THEN 'LOC-I'       -- Loss of control in flight
                                                                                 WHEN es.eventsoe_no = '241' THEN 'STALL'       -- Aerodynamic stall/spin
                                                                                 WHEN es.eventsoe_no = '250' THEN 'MIDAIR'      -- Midair collision
                                                                                 WHEN es.eventsoe_no = '401' THEN 'UIMC'        -- VFR encounter with IMC
                                                                                 WHEN es.eventsoe_no = '420' THEN 'CAA'         -- Collision avoidance alert
                                                                                 WHEN es.eventsoe_no = '901' THEN 'BIRD'        -- Birdstrike
                                                                                                                                ELSE es.occurrence_code
                                                                             END
                                                                       FROM events_sequence es
                                                                      WHERE (es.phase_no    IN ('350', '452', '502')
                                                                         OR  es.eventsoe_no IN ('120', '220', '240', '241', '250', '401', '420', '901'))
                                                                        AND es.occurrence_code  IS NOT NULL
                                                                        AND es.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) occurrence_codes,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.oper_country, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) oper_countries,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.owner_country, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) owner_countries,
                                                       --
                                                       (SELECT ARRAY_TO_STRING(ARRAY (SELECT DISTINCT es.phase_no
                                                                                        FROM events_sequence es
                                                                                       WHERE es.ev_id = ifu.ev_id
                                                                                         AND es.defining_ev  IS TRUE
                                                                                       ORDER BY 1),', ')) phase_codes_defining,
                                                       --
                                                       (SELECT ARRAY(SELECT CASE WHEN upper(a.regis_no) ~ '^N[1-9][0-9][0-9][0-9][0-9]$' THEN 'USA'
                                                                                 WHEN upper(a.regis_no) ~ '^N[1-9][0-9][0-9][0-9][A-Z]$' THEN 'USA'
                                                                                 WHEN upper(a.regis_no) ~ '^N[1-9][0-9][0-9][A-Z][A-Z]$' THEN 'USA'
                                                                                                                                         ELSE 'NON-US'
                                                                             END
                                                                       FROM aircraft a
                                                                      WHERE a.regis_no IS NOT NULL
                                                                        AND a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) regis_countries,
                                                       --
                                                       (SELECT ARRAY(SELECT COALESCE(a.regis_no, 'n/a')
                                                                       FROM aircraft a
                                                                      WHERE a.ev_id = ifu.ev_id
                                                                      ORDER BY 1)) regis_nos
                                                 FROM events ifu LEFT OUTER JOIN io_airports a
                                                                 ON ifu.io_nearest_airport_global_id = a.global_id
                                                WHERE ifu.ev_year >= 1982) level_1) level_2) level_3) level_4
        """


# ------------------------------------------------------------------
# Adds the DDL statement for setting up database view
# io_lat_lng_issues.
# ------------------------------------------------------------------
def _create_dll_view_io_lat_lng_issues() -> None:

    DLL_VIEW_STMNTS_DROP.append("io_lat_lng_issues")

    DLL_VIEW_STMNTS_CREATE[
        "io_lat_lng_issues"
    ] = """
        CREATE OR REPLACE
            VIEW io_lat_lng_issues
                AS
                    SELECT e.ev_id ev_id,
                           e.ev_country ev_country,
                           e.ev_state ev_state,
                           e.ev_city ev_city,
                           e.ev_site_zipcode ev_site_zipcode,
                           e.dec_latitude ev_dec_latitude,
                           e.dec_longitude ev_dec_longitude,
                           e.latitude ev_latitude ,
                           e.longitude ev_longitude,
                           e.io_country io_country,
                           e.io_state  io_state,
                           e.io_city io_city,
                           e.io_site_zipcode io_site_zipcode,
                           e.io_dec_latitude io_dec_latitude,
                           e.io_dec_longitude io_dec_longitude,
                           e.io_latitude io_latitude,
                           e.io_longitude io_longitude,
                           e.io_dec_lat_lng_actions io_dec_lat_lng_actions,
                           e.io_dec_latitude_deviating io_dec_latitude_deviating,
                           e.io_dec_longitude_deviating io_dec_longitude_deviating,
                           e.io_invalid_latitude io_invalid_latitude,
                           e.io_invalid_longitude io_invalid_longitude,
                           e.io_invalid_us_city io_invalid_us_city,
                           e.io_invalid_us_city_zipcode io_invalid_us_city_zipcode,
                           e.io_invalid_us_state io_invalid_us_state,
                           e.io_invalid_us_zipcode io_invalid_us_zipcode,
                           COALESCE (e.io_country, e.ev_country) country,
                           COALESCE (e.io_state, e.ev_state) state,
                           COALESCE (e.io_city, e.ev_city) city,
                           COALESCE (e.io_site_zipcode, e.ev_site_zipcode) site_zipcode,
                           COALESCE (e.io_latitude, e.latitude) latitude,
                           COALESCE (e.io_longitude, e.longitude) longitude,
                           n.state_name state_name,
                           z.dec_latitude zipcode_dec_latitude,
                           z.dec_longitude zipcode_dec_longitude,
                           c.dec_latitude city_dec_latitude,
                           c.dec_longitude city_dec_longitude,
                           s.dec_latitude state_dec_latitude,
                           s.dec_longitude state_dec_longitude,
                           u.dec_latitude country_dec_latitude,
                           u.dec_longitude country_dec_longitude
                      FROM events e
                      LEFT OUTER JOIN io_states n on n.state = e.ev_state
                      LEFT OUTER JOIN io_lat_lng z on z.type = 'ZIPCODE' AND z.zipcode = e.ev_site_zipcode
                      LEFT OUTER JOIN io_lat_lng c on c.type = 'CITY' AND c.state = e.ev_state AND c.city = upper(e.ev_city)
                      LEFT OUTER JOIN io_states s on s.country = e.ev_country and s.state = e.ev_state
                      LEFT OUTER JOIN io_countries u on u.country = 'USA'
                     WHERE (e.dec_latitude IS NULL
                        OR e.dec_latitude  = 0
                        OR e.dec_longitude IS NULL
                        OR e.dec_longitude = 0)
                       AND e.ev_country = 'USA';
    """


# ------------------------------------------------------------------
# Decompose xxx into suitable tokens.
# ------------------------------------------------------------------
def _create_tokens_4_finding_description(finding_description: str) -> list[str]:
    return (
        finding_description.replace("Alternator-generator", "Alternator generator")
        .replace("Anti-skid", "Anti skid")
        .replace("Color-vision", "Color vision")
        .replace("Record-keeping", "Record keeping")
        .replace("Starter-generator", "Starter generator")
        .replace("Tie-down", "Tie down")
        .replace("Windows-windshield", "Windows windshield")
        .replace("anti-ic", "anti ic")
        .replace("change-over", "change over")
        .replace("filter-strainer", "filter strainer")
        .replace("gear-boxes", "gear boxes")
        .replace("generator-alternator", "generator alternator")
        .replace("limitation-Color-vision", "limitation Color vision")
        .replace("rectifier-converter", "rectifier converter")
        .split("-")
    )


# ------------------------------------------------------------------
# Load the description_main_phase from an MS Excel file.
# ------------------------------------------------------------------

def _load_description_main_phase(conn_pg: connection, cur_pg: cursor) -> None:
    logging.debug(io_glob.LOGGER_START)

    if not Path(FILE_MAIN_PHASES_OF_FLIGHT).is_file():
        # ERROR.00.941 The Main Phases of Flight file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_941.replace("{filename}", FILE_MAIN_PHASES_OF_FLIGHT),
        )

    io_utils.progress_msg("")
    io_utils.progress_msg("-" * 80)
    # INFO.00.084 Database table io_md_codes_phase: Load description_main_phase
    # from file '{filename}'
    io_utils.progress_msg(
        glob_local.INFO_00_084.replace("{filename}", FILE_MAIN_PHASES_OF_FLIGHT),
    )
    io_utils.progress_msg("-" * 80)

    # ------------------------------------------------------------------
    # Load the data into a Pandas dataframe.
    # ------------------------------------------------------------------

    try:
        # Attempt to read the Excel file
        dataframe = pd.read_excel(
            FILE_MAIN_PHASES_OF_FLIGHT,
            sheet_name="io_md_codes_phase",
        )

        count_select = 0
        count_update = 0

        # ------------------------------------------------------------------
        # Load the NPIAS data.
        # ------------------------------------------------------------------


        for _index, row in dataframe.iterrows():

            count_select += 1

            if count_select % io_settings.settings.database_commit_size == 0:
                conn_pg.commit()
                io_utils.progress_msg(
                    f"Number of rows so far read : {count_select!s:>8}",
                )

            phase_code = str(extract_column_value(row, COLUMN_PHASE_CODE))
            main_phase = extract_column_value(row, COLUMN_MAIN_PHASE)


            cur_pg.execute(
                """
            UPDATE io_md_codes_phase imcp
               SET description_main_phase = %s
             WHERE imcp.phase_code = %s;
            """,
                (
                    main_phase,
                    phase_code,
                ),
            )
            count_update += cur_pg.rowcount

        conn_pg.commit()

        io_utils.progress_msg(f"Number rows selected : {count_select!s:>8}")

        if count_update > 0:
            io_utils.progress_msg(f"Number rows updated  : {count_update!s:>8}")

        logging.debug(io_glob.LOGGER_END)

    except FileNotFoundError:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_931.replace("{file_name}", FILE_MAIN_PHASES_OF_FLIGHT),
        )

    except ValueError as err:
        io_utils.terminate_fatal(
            glob_local.FATAL_00_933.replace(
                "{file_name}",
                FILE_MAIN_PHASES_OF_FLIGHT,
            ).replace("{error}", str(err)),
        )

    except Exception as exc:  # noqa: BLE001
        io_utils.terminate_fatal(
            glob_local.FATAL_00_934.replace(
                "{file_name}",
                FILE_MAIN_PHASES_OF_FLIGHT,
            ).replace("{error}", str(exc)),
        )


# ------------------------------------------------------------------
# Prepare the selected token.
# ------------------------------------------------------------------
def _prep_token_4_finding_description(token: str) -> str:
    return (
        token.replace("Alternator generator", "Alternator-generator")
        .replace("Anti skid", "Anti-skid")
        .replace("Color vision", "Color-vision")
        .replace("Record keeping", "Record-keeping")
        .replace("Starter generator", "Starter-generator")
        .replace("Terrain Mountainous", "Terrain-Mountainous")
        .replace("Tie down", "Tie-down")
        .replace("Windows windshield", "Windows-windshield")
        .replace("anti ic", "anti-ic")
        .replace("change over", "change-over")
        .replace("filter strainer", "filter-strainer")
        .replace("gear boxes", "gear-boxes")
        .replace("generator alternator", "generator-alternator")
        .replace("limitation Color vision", "limitation-Color-vision")
        .replace("rectifier converter", "rectifier-converter")
        .strip()
    )


# -----------------------------------------------------------------------------

def _refresh_db_views(conn_pg: connection, cur_pg: cursor) -> None:
    """Refresh the materialized database views.

    This function refreshes the materialized database views by calling the REFRESH MATERIALIZED VIEW
    statement for each view in the list of views to be refreshed.

    :param conn_pg: The PostgreSQL database connection.
    :param cur_pg: The PostgreSQL database cursor.

    """
    # Add the io_app_ae1982 view to the list of views to be refreshed
    DLL_VIEW_STMNTS_REFRESH.append("io_app_ae1982")

    # Iterate over the list of views to be refreshed
    for view_name in DLL_VIEW_STMNTS_REFRESH:
        # Refresh the materialized view
        cur_pg.execute("REFRESH MATERIALIZED VIEW " + view_name + ";")
        conn_pg.commit()
        # Log the action
        io_utils.progress_msg(
            # INFO.00.069 Materialized database view is refreshed: {view}
            glob_local.INFO_00_069.replace("{view}", view_name),
        )


# -----------------------------------------------------------------------------

def create_db_schema() -> None:
    """Create the database schema.

    This function is a part of the setup of the database. It is called after the database has been
    created and the tables have been created. It creates the database schema by calling the
    functions that create the tables and the views.

    """
    global DLL_TABLE_STMNTS

    logging.debug(io_glob.LOGGER_START)

    # Create the PostgreSQL database role.
    conn_pg, cur_pg = db_utils.get_postgres_cursor_admin()

    try:
        cur_pg.execute(
            f"CREATE ROLE {io_settings.settings.postgres_user} WITH CREATEDB LOGIN "
            f"PASSWORD '{io_settings.settings.postgres_password}'",
        )

        # INFO.00.016 Database role is available: {user}
        io_utils.progress_msg(
            glob_local.INFO_00_016.replace(
                "{role}",
                io_settings.settings.postgres_user,
            ),
        )
    except DuplicateObject:
        # INFO.00.082 Database role already existing: {role}
        io_utils.progress_msg(
            glob_local.INFO_00_082.replace(
                "{role}",
                io_settings.settings.postgres_user,
            ),
        )

    # Create the PostgreSQL database.
    try:
        cur_pg.execute(
            f"CREATE DATABASE {io_settings.settings.postgres_dbname} "
            f"WITH OWNER {io_settings.settings.postgres_user}",
        )

        # INFO.00.017 Database is available: {dbname}
        io_utils.progress_msg(
            glob_local.INFO_00_017.replace(
                "{dbname}",
                io_settings.settings.postgres_dbname,
            ),
        )
    except DuplicateDatabase:
        # INFO.00.083 Database already existing: {dbname}
        io_utils.progress_msg(
            glob_local.INFO_00_083.replace(
                "{dbname}",
                io_settings.settings.postgres_dbname,
            ),
        )

    cur_pg.close()
    conn_pg.close()

    DLL_TABLE_STMNTS = {}

    # Create the tables.
    _create_dll_tables_base()
    _create_dll_create_tables_io()

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # Create the composite database types.
    _create_db_types_composite(conn_pg, cur_pg)

    # Create the tables.
    _create_db_tables(conn_pg, cur_pg)

    cur_pg.close()
    conn_pg.close()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def refresh_db_schema() -> None:
    """Refresh the database schema.

    This function is a part of the setup of the database. It is called after the database has been
    created and the tables have been created. It updates the database schema by refreshing the
    materialized views.

    """
    global DLL_VIEW_STMNTS_REFRESH

    logging.debug(io_glob.LOGGER_START)

    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # Refresh the database IO-Aero specific data.
    _create_db_io_aero_data(conn_pg, cur_pg)

    # Initialize the list of database views that need to be refreshed.
    DLL_VIEW_STMNTS_REFRESH = []

    # Refresh the database views.
    _refresh_db_views(conn_pg, cur_pg)

    cur_pg.close()
    conn_pg.close()

    logging.debug(io_glob.LOGGER_END)


# -----------------------------------------------------------------------------

def update_db_schema() -> None:
    """Update the database schema.

    This function is a part of the setup of the database. It is called after the database has been
    created and the tables have been created. It drops all existing views and creates new ones and
    also creates the indexes for the tables.

    """
    global DLL_TABLE_STMNTS
    global DLL_VIEW_STMNTS_CREATE
    global DLL_VIEW_STMNTS_DROP
    global DLL_VIEW_STMNTS_REFRESH

    logging.debug(io_glob.LOGGER_START)

    # Connect to the database.
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    # Drop the existing tables.
    DLL_TABLE_STMNTS = {}
    _create_dll_alter_tables_io()
    _alter_db_tables(conn_pg, cur_pg)

    # Create the new tables.
    DLL_TABLE_STMNTS = {}
    _create_dll_create_tables_io()
    _create_db_tables(conn_pg, cur_pg)

    # Create the columns for the tables.
    _create_db_table_columns(conn_pg, cur_pg)

    # Create the IO-Aero specific data.
    _create_db_io_aero_data(conn_pg, cur_pg)

    # Create the database views.
    DLL_VIEW_STMNTS_CREATE = {}
    DLL_VIEW_STMNTS_DROP = []
    DLL_VIEW_STMNTS_REFRESH = []
    _create_db_views(conn_pg, cur_pg)

    # Create the indexes for the tables.
    _create_db_indexes(conn_pg, cur_pg)

    # Close the database connection.
    cur_pg.close()
    conn_pg.close()

    # Connect to the database as the admin user.
    conn_pg, cur_pg = db_utils.get_postgres_cursor_admin(
        dbname=io_settings.settings.postgres_dbname,
    )

    # Create the guest user.
    _create_db_role_guest(conn_pg, cur_pg)

    # Close the database connection.
    cur_pg.close()
    conn_pg.close()

    logging.debug(io_glob.LOGGER_END)
