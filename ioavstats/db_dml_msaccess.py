# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""Managing the database schema of the PostgreSQL database."""
import logging
import os
import platform
import shutil
import subprocess
import zipfile
from datetime import datetime
from datetime import timezone
from pathlib import Path

import pyodbc  # type: ignore
import requests
from iocommon import db_utils
from iocommon import io_config
from iocommon import io_glob
from iocommon import io_utils
from psycopg import connection
from psycopg import cursor
from psycopg.errors import ForeignKeyViolation  # pylint: disable=no-name-in-module
from psycopg.errors import UniqueViolation  # pylint: disable=no-name-in-module

from ioavstats import glob_local
from ioavstats import utils
from ioavstats import utils_msaccess

# -----------------------------------------------------------------------------
# Global variables.
# -----------------------------------------------------------------------------

COLUMN_CITY = "city"
COLUMN_COUNT = "count"
COLUMN_COUNTRY = "country"
COLUMN_DEC_LATITUDE = "dec_latitude"
COLUMN_DEC_LONGITUDE = "dec_longitude"
COLUMN_STATE = "state"

IO_LAST_SEEN = datetime.now(timezone.utc)

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Check for DDL changes.
# ------------------------------------------------------------------
# flake8: noqa
# pylint: disable=too-many-lines
def _check_ddl_changes(msaccess: str) -> None:
    """Check for DDL changes."""
    logger.debug(io_glob.LOGGER_START)

    download_work_dir = os.path.join(
        os.getcwd(), io_config.settings.download_work_dir.replace("/", os.sep)
    )

    shutil.copy(
        os.path.join(
            download_work_dir.replace("/", os.sep),
            msaccess + "." + glob_local.FILE_EXTENSION_MDB,
        ),
        os.path.join(
            download_work_dir.replace("/", os.sep),
            io_config.settings.razorsql_profile + "." + glob_local.FILE_EXTENSION_MDB,
        ),
    )

    msaccess_mdb = os.path.join(
        download_work_dir.replace("/", os.sep),
        "IO-AVSTATS.mdb",
    )

    # INFO.00.051 msaccess_file='{msaccess_file}'
    io_utils.progress_msg(
        glob_local.INFO_00_051.replace("{msaccess_file}", msaccess_mdb)
    )

    if not os.path.exists(msaccess_mdb):
        # ERROR.00.932 File '{filename}' is not existing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_932.replace("{filename}", msaccess_mdb)
        )

    msaccess_sql = os.path.join(
        download_work_dir.replace("/", os.sep),
        msaccess + "." + glob_local.FILE_EXTENSION_SQL,
    )

    # INFO.00.051 msaccess_file='{msaccess_file}'
    io_utils.progress_msg(
        glob_local.INFO_00_051.replace("{msaccess_file}", msaccess_sql)
    )

    razorsql_jar_file = ""
    razorsql_java_path = ""

    if platform.system() == "Windows":
        razorsql_jar_file = io_config.settings.razorsql_jar_file_windows
        razorsql_java_path = io_config.settings.razorsql_java_path_windows
    elif platform.system() == "Linux":
        razorsql_jar_file = io_config.settings.razorsql_jar_file_linux
        razorsql_java_path = io_config.settings.razorsql_java_path_linux
    else:
        # ERROR.00.908 The operating system '{os}' is not supported
        io_utils.terminate_fatal(
            glob_local.ERROR_00_908.replace("{os}", platform.system())
        )

    # INFO.00.052 razorsql_jar_file='{razorsql_jar_file}'
    io_utils.progress_msg(
        glob_local.INFO_00_052.replace("{razorsql_jar_file}", razorsql_jar_file)
    )

    if not Path(razorsql_jar_file).is_file():
        # ERROR.00.932 File '{filename}' is not existing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_932.replace("{filename}", razorsql_jar_file)
        )

    # INFO.00.053 razorsql_java_path='{razorsql_java_path}'"
    io_utils.progress_msg(
        glob_local.INFO_00_053.replace("{razorsql_java_path}", razorsql_java_path)
    )

    subprocess.run(
        [
            razorsql_java_path,
            "-jar",
            razorsql_jar_file,
            "-backup",
            io_config.settings.razorsql_profile,
            "null",
            "null",
            ";",
            "null",
            msaccess_sql,
            "NO",
            "tables",
            "YES",
            "null",
            "NO",
            "NO",
        ],
        check=True,
    )

    # INFO.00.011 The DDL script for the MS Access database '{msaccess}'
    # was created successfully
    io_utils.progress_msg(glob_local.INFO_00_011.replace("{msaccess}", msaccess))

    if msaccess == glob_local.MSACCESS_PRE2008:
        # INFO.00.020 The DDL script for the MS Access database '{msaccess}'
        # must be checked manually
        io_utils.progress_msg(glob_local.INFO_00_020.replace("{msaccess}", msaccess))
    else:
        _compare_ddl(msaccess)

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Compare the schema definitions with the reference file.
# ------------------------------------------------------------------
def _compare_ddl(msaccess: str) -> None:
    """Compare the schema definitions wirth the reference file."""
    logger.debug(io_glob.LOGGER_START)

    reference_filename = os.path.join(
        io_config.settings.razorsql_reference_dir.replace("/", os.sep),
        io_config.settings.razorsql_reference_file,
    )

    # pylint: disable=consider-using-with
    reference_file = open(
        reference_filename, "r", encoding=io_glob.FILE_ENCODING_DEFAULT
    )
    reference_file_lines = reference_file.readlines()
    reference_file.close()

    msaccess_filename = os.path.join(
        io_config.settings.download_work_dir.replace("/", os.sep),
        msaccess + "." + glob_local.FILE_EXTENSION_SQL,
    )

    # pylint: disable=consider-using-with
    msaccess_file = open(msaccess_filename, "r", encoding=io_glob.FILE_ENCODING_DEFAULT)
    msaccess_file_lines = msaccess_file.readlines()
    msaccess_file.close()

    if len(reference_file_lines) != len(msaccess_file_lines):
        # ERROR.00.911 Number of lines differs: file '{filename}' lines
        # {filename_lines} versus file'{reference}' lines {reference_lines}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_911.replace("{filename}", msaccess_filename)
            .replace("{filename_lines}", str(len(msaccess_file_lines)))
            .replace("{reference}", reference_filename)
            .replace("{reference_lines}", str(len(reference_file_lines)))
        )

    for line_no, line in enumerate(reference_file_lines):
        if line != msaccess_file_lines[line_no]:
            # INFO.00.009 line no.: {line_no}
            # INFO.00.010 {status} '{line}'
            io_utils.progress_msg_core(
                glob_local.INFO_00_009.replace("{line_no}", str(line_no))
            )
            io_utils.progress_msg_core(
                glob_local.INFO_00_010.replace("{status}", "expected").replace(
                    "{line}", line
                )
            )
            io_utils.progress_msg_core(
                glob_local.INFO_00_010.replace("{status}", "received").replace(
                    "{line}", msaccess_file_lines[line_no]
                )
            )
            # ERROR.00.910 The schema definition in file'{filename}'
            # does not match the reference definition in file'{reference}'
            io_utils.terminate_fatal(
                glob_local.ERROR_00_910.replace(
                    "{filename}", msaccess_filename
                ).replace("{reference}", reference_filename)
            )

    # INFO.00.012 The DDL script for the MS Access database '{msaccess}'
    # is identical to the reference script
    io_utils.progress_msg(glob_local.INFO_00_012.replace("{msaccess}", msaccess))

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Delete all the NTSB data.
# ------------------------------------------------------------------
def _delete_ntsb_data(
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Delete all the NTSB data."""
    logger.debug(io_glob.LOGGER_START)

    for table in [
        # Level 4 - FK: ev_id & Aircraft_Key & crew_no
        "dt_flight_crew",
        "flight_time",
        # Level 4 - FK: ev_id & Aircraft_Key & Occurrence_No
        "seq_of_events",
        # Level 3 - FK: ev_id & Aircraft_Key
        "dt_aircraft",
        "engines",
        "events_sequence",
        "findings",
        "flight_crew",
        "injury",
        "narratives",
        "occurrences",
        # Level 2 - FK: ev_id
        "aircraft",
        "dt_events",
        "ntsb_admin",
        # Level 1 - without FK
        "events",
    ]:
        cur_pg.execute(
            f"""
        SELECT count(*)
          FROM {table}
            """,
        )
        row_pg = cur_pg.fetchone()

        no_rows = row_pg[COLUMN_COUNT] if row_pg else 0  # type: ignore
        if no_rows > 0:
            cur_pg.execute(
                f"""
            TRUNCATE {table} CASCADE;
            """,
            )
            io_utils.progress_msg(
                f"Table {table:<15} - number rows deleted : {str(no_rows):>8}"
            )
            conn_pg.commit()

    logger.debug(io_glob.LOGGER_END)

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
# Load data from MS Access to the PostgreSQL database.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def load_ntsb_msaccess_data(msaccess: str) -> None:
    """Load data from MS Access to the PostgreSQL database.

    Args:
        msaccess (str):
            The MS Access database file without file extension.

    """
    logger.debug(io_glob.LOGGER_START)

    # ------------------------------------------------------------------
    # Start processing.
    # ------------------------------------------------------------------

    # pylint: disable=R0801
    filename = os.path.join(
        io_config.settings.download_work_dir.replace("/", os.sep),
        msaccess + "." + glob_local.FILE_EXTENSION_MDB,
    )

    if not os.path.isfile(filename):
        # ERROR.00.912 The MS Access database file '{filename}' is missing
        io_utils.terminate_fatal(
            glob_local.ERROR_00_912.replace("{filename}", filename)
        )

    conn_ma, cur_ma = utils_msaccess.get_msaccess_cursor(filename)
    conn_pg, cur_pg = db_utils.get_postgres_cursor()

    if msaccess in [glob_local.MSACCESS_AVALL, glob_local.MSACCESS_PRE2008]:
        conn_pg.autocommit = False

    if msaccess == glob_local.MSACCESS_PRE2008:
        _delete_ntsb_data(conn_pg, cur_pg)

    is_table_aircraft = False
    is_table_dt_aircraft = False
    is_table_dt_events = False
    is_table_dt_flight_crew = False
    is_table_engines = False
    is_table_events = False
    is_table_events_sequence = False
    is_table_findings = False
    is_table_flight_crew = False
    is_table_flight_time = False
    is_table_injury = False
    is_table_narratives = False
    is_table_ntsb_admin = False
    is_table_occurrences = False
    is_table_seq_of_events = False

    for table_info in cur_ma.tables():
        if table_info.table_name == glob_local.TABLE_NAME_AIRCRAFT:
            is_table_aircraft = True
        elif table_info.table_name == glob_local.TABLE_NAME_DT_AIRCRAFT:
            is_table_dt_aircraft = True
        elif table_info.table_name == glob_local.TABLE_NAME_DT_EVENTS:
            is_table_dt_events = True
        elif table_info.table_name == glob_local.TABLE_NAME_DT_FLIGHT_CREW:
            is_table_dt_flight_crew = True
        elif table_info.table_name == glob_local.TABLE_NAME_ENGINES:
            is_table_engines = True
        elif table_info.table_name == glob_local.TABLE_NAME_EVENTS:
            is_table_events = True
        elif table_info.table_name == glob_local.TABLE_NAME_EVENTS_SEQUENCE:
            is_table_events_sequence = True
        elif table_info.table_name == glob_local.TABLE_NAME_FINDINGS:
            is_table_findings = True
        elif table_info.table_name == glob_local.TABLE_NAME_FLIGHT_CREW:
            is_table_flight_crew = True
        elif table_info.table_name == glob_local.TABLE_NAME_FLIGHT_TIME:
            is_table_flight_time = True
        elif table_info.table_name == glob_local.TABLE_NAME_INJURY:
            is_table_injury = True
        elif table_info.table_name == glob_local.TABLE_NAME_NARRATIVES:
            is_table_narratives = True
        elif table_info.table_name == glob_local.TABLE_NAME_NTSB_ADMIN:
            is_table_ntsb_admin = True
        elif table_info.table_name == glob_local.TABLE_NAME_OCCURRENCES:
            is_table_occurrences = True
        elif table_info.table_name == glob_local.TABLE_NAME_SEQ_OF_EVENTS:
            is_table_seq_of_events = True
        else:
            # INFO.00.021 The following database table is not processed: '{msaccess}'
            io_utils.progress_msg(
                glob_local.INFO_00_021.replace("{msaccess}", table_info.table_name)
            )

    # ------------------------------------------------------------------
    # Load the NTSB data.
    # ------------------------------------------------------------------

    # Level 1 - without FK
    if is_table_events:
        _load_table_events(
            msaccess, glob_local.TABLE_NAME_EVENTS, cur_ma, conn_pg, cur_pg
        )

    # Level 2 - FK: ev_id
    if is_table_aircraft:
        _load_table_aircraft(
            msaccess, glob_local.TABLE_NAME_AIRCRAFT, cur_ma, conn_pg, cur_pg
        )
    if is_table_dt_events:
        _load_table_dt_events(
            msaccess, glob_local.TABLE_NAME_DT_EVENTS, cur_ma, conn_pg, cur_pg
        )
    if is_table_ntsb_admin:
        _load_table_ntsb_admin(
            msaccess, glob_local.TABLE_NAME_NTSB_ADMIN, cur_ma, conn_pg, cur_pg
        )

    # Level 3 - FK: ev_id & Aircraft_Key
    if is_table_dt_aircraft:
        _load_table_dt_aircraft(
            msaccess, glob_local.TABLE_NAME_DT_AIRCRAFT, cur_ma, conn_pg, cur_pg
        )
    if is_table_engines:
        _load_table_engines(
            msaccess, glob_local.TABLE_NAME_ENGINES, cur_ma, conn_pg, cur_pg
        )
    if is_table_events_sequence:
        _load_table_events_sequence(
            msaccess, glob_local.TABLE_NAME_EVENTS_SEQUENCE, cur_ma, conn_pg, cur_pg
        )
    if is_table_findings:
        _load_table_findings(
            msaccess, glob_local.TABLE_NAME_FINDINGS, cur_ma, conn_pg, cur_pg
        )
    if is_table_flight_crew:
        _load_table_flight_crew(
            msaccess, glob_local.TABLE_NAME_FLIGHT_CREW, cur_ma, conn_pg, cur_pg
        )
    if is_table_injury:
        _load_table_injury(
            msaccess, glob_local.TABLE_NAME_INJURY, cur_ma, conn_pg, cur_pg
        )
    if is_table_narratives:
        _load_table_narratives(
            msaccess, glob_local.TABLE_NAME_NARRATIVES, cur_ma, conn_pg, cur_pg
        )
    if is_table_occurrences:
        _load_table_occurrences(
            msaccess, glob_local.TABLE_NAME_OCCURRENCES, cur_ma, conn_pg, cur_pg
        )

    # Level 4 - FK: ev_id & Aircraft_Key & crew_no
    if is_table_dt_flight_crew:
        _load_table_dt_flight_crew(
            msaccess, glob_local.TABLE_NAME_DT_FLIGHT_CREW, cur_ma, conn_pg, cur_pg
        )
    if is_table_flight_time:
        _load_table_flight_time(
            msaccess, glob_local.TABLE_NAME_FLIGHT_TIME, cur_ma, conn_pg, cur_pg
        )

    # Level 4 - FK: ev_id & Aircraft_Key & Occurrence_No
    if is_table_seq_of_events:
        _load_table_seq_of_events(
            msaccess, glob_local.TABLE_NAME_SEQ_OF_EVENTS, cur_ma, conn_pg, cur_pg
        )

    # ------------------------------------------------------------------
    # Finalize processing.
    # ------------------------------------------------------------------

    conn_pg.autocommit = True

    # pylint: disable=R0801
    utils.upd_io_processed_files(msaccess, cur_pg)

    cur_pg.close()
    conn_pg.close()
    cur_ma.close()
    conn_ma.close()

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table aircraft.
# ------------------------------------------------------------------
def _load_table_aircraft(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table aircraft."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    # pylint: disable=R0801
    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO aircraft (
                   ev_id,aircraft_key,regis_no,ntsb_no,acft_missing,far_part,flt_plan_filed,flight_plan_activated,damage,acft_fire,acft_expl,acft_make,
                   acft_model,acft_series,acft_serial_no,cert_max_gr_wt,acft_category,acft_reg_cls,homebuilt,fc_seats,cc_seats,pax_seats,total_seats,
                   num_eng,fixed_retractable,type_last_insp,date_last_insp,afm_hrs_last_insp,afm_hrs,elt_install,elt_oper,elt_aided_loc_ev,elt_type,
                   owner_acft,owner_street,owner_city,owner_state,owner_country,owner_zip,oper_individual_name,oper_name,oper_same,oper_dba,oper_addr_same,
                   oper_street,oper_city,oper_state,oper_country,oper_zip,oper_code,certs_held,oprtng_cert,oper_cert,oper_cert_num,oper_sched,oper_dom_int,
                   oper_pax_cargo,type_fly,second_pilot,dprt_pt_same_ev,dprt_apt_id,dprt_city,dprt_state,dprt_country,dprt_time,dprt_timezn,dest_same_local,
                   dest_apt_id,dest_city,dest_state,dest_country,phase_flt_spec,report_to_icao,evacuation,lchg_date,lchg_userid,afm_hrs_since,rwy_num,
                   rwy_len,rwy_width,site_seeing,air_medical,med_type_flight,acft_year,fuel_on_board,commercial_space_flight,unmanned,ifr_equipped_cert,
                   elt_mounted_aircraft,elt_connected_antenna,elt_manufacturer,elt_model,elt_reason_other,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.regis_no,
                    row_mdb.ntsb_no,
                    row_mdb.acft_missing,
                    row_mdb.far_part,
                    row_mdb.flt_plan_filed,
                    row_mdb.flight_plan_activated,
                    row_mdb.damage,
                    row_mdb.acft_fire,
                    row_mdb.acft_expl,
                    row_mdb.acft_make,
                    row_mdb.acft_model,
                    row_mdb.acft_series,
                    row_mdb.acft_serial_no,
                    row_mdb.cert_max_gr_wt,
                    row_mdb.acft_category,
                    row_mdb.acft_reg_cls,
                    row_mdb.homebuilt,
                    row_mdb.fc_seats,
                    row_mdb.cc_seats,
                    row_mdb.pax_seats,
                    row_mdb.total_seats,
                    row_mdb.num_eng,
                    row_mdb.fixed_retractable,
                    row_mdb.type_last_insp,
                    row_mdb.date_last_insp,
                    row_mdb.afm_hrs_last_insp,
                    row_mdb.afm_hrs,
                    row_mdb.elt_install,
                    row_mdb.elt_oper,
                    row_mdb.elt_aided_loc_ev,
                    row_mdb.elt_type,
                    row_mdb.owner_acft,
                    row_mdb.owner_street,
                    row_mdb.owner_city,
                    row_mdb.owner_state,
                    row_mdb.owner_country,
                    row_mdb.owner_zip,
                    row_mdb.oper_individual_name,
                    row_mdb.oper_name,
                    row_mdb.oper_same,
                    row_mdb.oper_dba,
                    row_mdb.oper_addr_same,
                    row_mdb.oper_street,
                    row_mdb.oper_city,
                    row_mdb.oper_state,
                    row_mdb.oper_country,
                    row_mdb.oper_zip,
                    row_mdb.oper_code,
                    row_mdb.certs_held,
                    row_mdb.oprtng_cert,
                    row_mdb.oper_cert,
                    row_mdb.oper_cert_num,
                    row_mdb.oper_sched,
                    row_mdb.oper_dom_int,
                    row_mdb.oper_pax_cargo,
                    row_mdb.type_fly,
                    row_mdb.second_pilot,
                    row_mdb.dprt_pt_same_ev,
                    row_mdb.dprt_apt_id,
                    row_mdb.dprt_city,
                    row_mdb.dprt_state,
                    row_mdb.dprt_country,
                    row_mdb.dprt_time,
                    row_mdb.dprt_timezn,
                    row_mdb.dest_same_local,
                    row_mdb.dest_apt_id,
                    row_mdb.dest_city,
                    row_mdb.dest_state,
                    row_mdb.dest_country,
                    row_mdb.phase_flt_spec,
                    row_mdb.report_to_icao,
                    row_mdb.evacuation,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.afm_hrs_since,
                    row_mdb.rwy_num,
                    row_mdb.rwy_len,
                    row_mdb.rwy_width,
                    row_mdb.site_seeing,
                    row_mdb.air_medical,
                    row_mdb.med_type_flight,
                    row_mdb.acft_year,
                    row_mdb.fuel_on_board,
                    row_mdb.commercial_space_flight,
                    row_mdb.unmanned,
                    row_mdb.ifr_equipped_cert,
                    row_mdb.elt_mounted_aircraft,
                    row_mdb.elt_connected_antenna,
                    row_mdb.elt_manufacturer,
                    row_mdb.elt_model,
                    row_mdb.elt_reason_other,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE aircraft
               SET regis_no = %s,ntsb_no = %s,acft_missing = %s,far_part = %s,flt_plan_filed = %s,flight_plan_activated = %s,damage = %s,acft_fire = %s,
                   acft_expl = %s,acft_make = %s,acft_model = %s,acft_series = %s,acft_serial_no = %s,cert_max_gr_wt = %s,acft_category = %s,
                   acft_reg_cls = %s,homebuilt = %s,fc_seats = %s,cc_seats = %s,pax_seats = %s,total_seats = %s,num_eng = %s,fixed_retractable = %s,
                   type_last_insp = %s,date_last_insp = %s,afm_hrs_last_insp = %s,afm_hrs = %s,elt_install = %s,elt_oper = %s,elt_aided_loc_ev = %s,
                   elt_type = %s,owner_acft = %s,owner_street = %s,owner_city = %s,owner_state = %s,owner_country = %s,owner_zip = %s,
                   oper_individual_name = %s,oper_name = %s,oper_same = %s,oper_dba = %s,oper_addr_same = %s,oper_street = %s,oper_city = %s,
                   oper_state = %s,oper_country = %s,oper_zip = %s,oper_code = %s,certs_held = %s,oprtng_cert = %s,oper_cert = %s,oper_cert_num = %s,
                   oper_sched = %s,oper_dom_int = %s,oper_pax_cargo = %s,type_fly = %s,second_pilot = %s,dprt_pt_same_ev = %s,dprt_apt_id = %s,
                   dprt_city = %s,dprt_state = %s,dprt_country = %s,dprt_time = %s,dprt_timezn = %s,dest_same_local = %s,dest_apt_id = %s,dest_city = %s,
                   dest_state = %s,dest_country = %s,phase_flt_spec = %s,report_to_icao = %s,evacuation = %s,lchg_date = %s,lchg_userid = %s,
                   afm_hrs_since = %s,rwy_num = %s,rwy_len = %s,rwy_width = %s,site_seeing = %s,air_medical = %s,med_type_flight = %s,acft_year = %s,
                   fuel_on_board = %s,commercial_space_flight = %s,unmanned = %s,ifr_equipped_cert = %s,elt_mounted_aircraft = %s,elt_connected_antenna = %s,
                   elt_manufacturer = %s,elt_model = %s,elt_reason_other = %s,io_last_seen_ntsb = %s
             WHERE aircraft_key = %s AND ev_id = %s
               AND NOT (regis_no = %s AND ntsb_no = %s AND acft_missing = %s AND far_part = %s AND flt_plan_filed = %s AND flight_plan_activated = %s AND
                        damage = %s AND acft_fire = %s AND acft_expl = %s AND acft_make = %s AND acft_model = %s AND acft_series = %s AND
                        acft_serial_no = %s AND cert_max_gr_wt = %s AND acft_category = %s AND acft_reg_cls = %s AND homebuilt = %s AND fc_seats = %s AND
                        cc_seats = %s AND pax_seats = %s AND total_seats = %s AND num_eng = %s AND fixed_retractable = %s AND type_last_insp = %s AND
                        date_last_insp = %s AND afm_hrs_last_insp = %s AND afm_hrs = %s AND elt_install = %s AND elt_oper = %s AND elt_aided_loc_ev = %s AND
                        elt_type = %s AND owner_acft = %s AND owner_street = %s AND owner_city = %s AND owner_state = %s AND owner_country = %s AND
                        owner_zip = %s AND oper_individual_name = %s AND oper_name = %s AND oper_same = %s AND oper_dba = %s AND oper_addr_same = %s AND
                        oper_street = %s AND oper_city = %s AND oper_state = %s AND oper_country = %s AND oper_zip = %s AND oper_code = %s AND
                        certs_held = %s AND oprtng_cert = %s AND oper_cert = %s AND oper_cert_num = %s AND oper_sched = %s AND oper_dom_int = %s AND
                        oper_pax_cargo = %s AND type_fly = %s AND second_pilot = %s AND dprt_pt_same_ev = %s AND dprt_apt_id = %s AND dprt_city = %s AND
                        dprt_state = %s AND dprt_country = %s AND dprt_time = %s AND dprt_timezn = %s AND dest_same_local = %s AND dest_apt_id = %s AND
                        dest_city = %s AND dest_state = %s AND dest_country = %s AND phase_flt_spec = %s AND report_to_icao = %s AND evacuation = %s AND
                        lchg_date = %s AND lchg_userid = %s AND afm_hrs_since = %s AND rwy_num = %s AND rwy_len = %s AND rwy_width = %s AND site_seeing = %s AND
                        air_medical = %s AND med_type_flight = %s AND acft_year = %s AND fuel_on_board = %s AND commercial_space_flight = %s AND
                        unmanned = %s AND ifr_equipped_cert = %s AND elt_mounted_aircraft = %s AND elt_connected_antenna = %s AND elt_manufacturer = %s AND
                        elt_model = %s AND elt_reason_other = %s);
            """,
                (
                    row_mdb.regis_no,
                    row_mdb.ntsb_no,
                    row_mdb.acft_missing,
                    row_mdb.far_part,
                    row_mdb.flt_plan_filed,
                    row_mdb.flight_plan_activated,
                    row_mdb.damage,
                    row_mdb.acft_fire,
                    row_mdb.acft_expl,
                    row_mdb.acft_make,
                    row_mdb.acft_model,
                    row_mdb.acft_series,
                    row_mdb.acft_serial_no,
                    row_mdb.cert_max_gr_wt,
                    row_mdb.acft_category,
                    row_mdb.acft_reg_cls,
                    row_mdb.homebuilt,
                    row_mdb.fc_seats,
                    row_mdb.cc_seats,
                    row_mdb.pax_seats,
                    row_mdb.total_seats,
                    row_mdb.num_eng,
                    row_mdb.fixed_retractable,
                    row_mdb.type_last_insp,
                    row_mdb.date_last_insp,
                    row_mdb.afm_hrs_last_insp,
                    row_mdb.afm_hrs,
                    row_mdb.elt_install,
                    row_mdb.elt_oper,
                    row_mdb.elt_aided_loc_ev,
                    row_mdb.elt_type,
                    row_mdb.owner_acft,
                    row_mdb.owner_street,
                    row_mdb.owner_city,
                    row_mdb.owner_state,
                    row_mdb.owner_country,
                    row_mdb.owner_zip,
                    row_mdb.oper_individual_name,
                    row_mdb.oper_name,
                    row_mdb.oper_same,
                    row_mdb.oper_dba,
                    row_mdb.oper_addr_same,
                    row_mdb.oper_street,
                    row_mdb.oper_city,
                    row_mdb.oper_state,
                    row_mdb.oper_country,
                    row_mdb.oper_zip,
                    row_mdb.oper_code,
                    row_mdb.certs_held,
                    row_mdb.oprtng_cert,
                    row_mdb.oper_cert,
                    row_mdb.oper_cert_num,
                    row_mdb.oper_sched,
                    row_mdb.oper_dom_int,
                    row_mdb.oper_pax_cargo,
                    row_mdb.type_fly,
                    row_mdb.second_pilot,
                    row_mdb.dprt_pt_same_ev,
                    row_mdb.dprt_apt_id,
                    row_mdb.dprt_city,
                    row_mdb.dprt_state,
                    row_mdb.dprt_country,
                    row_mdb.dprt_time,
                    row_mdb.dprt_timezn,
                    row_mdb.dest_same_local,
                    row_mdb.dest_apt_id,
                    row_mdb.dest_city,
                    row_mdb.dest_state,
                    row_mdb.dest_country,
                    row_mdb.phase_flt_spec,
                    row_mdb.report_to_icao,
                    row_mdb.evacuation,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.afm_hrs_since,
                    row_mdb.rwy_num,
                    row_mdb.rwy_len,
                    row_mdb.rwy_width,
                    row_mdb.site_seeing,
                    row_mdb.air_medical,
                    row_mdb.med_type_flight,
                    row_mdb.acft_year,
                    row_mdb.fuel_on_board,
                    row_mdb.commercial_space_flight,
                    row_mdb.unmanned,
                    row_mdb.ifr_equipped_cert,
                    row_mdb.elt_mounted_aircraft,
                    row_mdb.elt_connected_antenna,
                    row_mdb.elt_manufacturer,
                    row_mdb.elt_model,
                    row_mdb.elt_reason_other,
                    IO_LAST_SEEN,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.regis_no,
                    row_mdb.ntsb_no,
                    row_mdb.acft_missing,
                    row_mdb.far_part,
                    row_mdb.flt_plan_filed,
                    row_mdb.flight_plan_activated,
                    row_mdb.damage,
                    row_mdb.acft_fire,
                    row_mdb.acft_expl,
                    row_mdb.acft_make,
                    row_mdb.acft_model,
                    row_mdb.acft_series,
                    row_mdb.acft_serial_no,
                    row_mdb.cert_max_gr_wt,
                    row_mdb.acft_category,
                    row_mdb.acft_reg_cls,
                    row_mdb.homebuilt,
                    row_mdb.fc_seats,
                    row_mdb.cc_seats,
                    row_mdb.pax_seats,
                    row_mdb.total_seats,
                    row_mdb.num_eng,
                    row_mdb.fixed_retractable,
                    row_mdb.type_last_insp,
                    row_mdb.date_last_insp,
                    row_mdb.afm_hrs_last_insp,
                    row_mdb.afm_hrs,
                    row_mdb.elt_install,
                    row_mdb.elt_oper,
                    row_mdb.elt_aided_loc_ev,
                    row_mdb.elt_type,
                    row_mdb.owner_acft,
                    row_mdb.owner_street,
                    row_mdb.owner_city,
                    row_mdb.owner_state,
                    row_mdb.owner_country,
                    row_mdb.owner_zip,
                    row_mdb.oper_individual_name,
                    row_mdb.oper_name,
                    row_mdb.oper_same,
                    row_mdb.oper_dba,
                    row_mdb.oper_addr_same,
                    row_mdb.oper_street,
                    row_mdb.oper_city,
                    row_mdb.oper_state,
                    row_mdb.oper_country,
                    row_mdb.oper_zip,
                    row_mdb.oper_code,
                    row_mdb.certs_held,
                    row_mdb.oprtng_cert,
                    row_mdb.oper_cert,
                    row_mdb.oper_cert_num,
                    row_mdb.oper_sched,
                    row_mdb.oper_dom_int,
                    row_mdb.oper_pax_cargo,
                    row_mdb.type_fly,
                    row_mdb.second_pilot,
                    row_mdb.dprt_pt_same_ev,
                    row_mdb.dprt_apt_id,
                    row_mdb.dprt_city,
                    row_mdb.dprt_state,
                    row_mdb.dprt_country,
                    row_mdb.dprt_time,
                    row_mdb.dprt_timezn,
                    row_mdb.dest_same_local,
                    row_mdb.dest_apt_id,
                    row_mdb.dest_city,
                    row_mdb.dest_state,
                    row_mdb.dest_country,
                    row_mdb.phase_flt_spec,
                    row_mdb.report_to_icao,
                    row_mdb.evacuation,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.afm_hrs_since,
                    row_mdb.rwy_num,
                    row_mdb.rwy_len,
                    row_mdb.rwy_width,
                    row_mdb.site_seeing,
                    row_mdb.air_medical,
                    row_mdb.med_type_flight,
                    row_mdb.acft_year,
                    row_mdb.fuel_on_board,
                    row_mdb.commercial_space_flight,
                    row_mdb.unmanned,
                    row_mdb.ifr_equipped_cert,
                    row_mdb.elt_mounted_aircraft,
                    row_mdb.elt_connected_antenna,
                    row_mdb.elt_manufacturer,
                    row_mdb.elt_model,
                    row_mdb.elt_reason_other,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table dt_aircraft.
# ------------------------------------------------------------------
def _load_table_dt_aircraft(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table dt_aircraft."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            cur_pg.execute(
                """
            INSERT INTO dt_aircraft (
                   ev_id,
                   aircraft_key,
                   col_name,
                   code,
                   lchg_date,
                   lchg_userid,
                   io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.col_name,
                    row_mdb.code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            UPDATE dt_aircraft
               SET lchg_date = %s,
                   lchg_userid = %s,
                   io_last_seen_ntsb = %s
             WHERE code = %s 
               AND col_name = %s 
               AND aircraft_key = %s 
               AND ev_id = %s
               AND NOT (lchg_date = %s 
                    AND lchg_userid = %s);
            """,
                (
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.code,
                    row_mdb.col_name,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"col_name={row_mdb.col_name} "
                        + f"code={row_mdb.code}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table dt_events.
# ------------------------------------------------------------------
def _load_table_dt_events(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table dt_events."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            cur_pg.execute(
                """
            INSERT INTO dt_events (
                   ev_id,
                   col_name,
                   code,
                   lchg_date,
                   lchg_userid,
                   io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.col_name,
                    row_mdb.code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE dt_events
               SET lchg_date = %s,
                   lchg_userid = %s,
                   io_last_seen_ntsb = %s
             WHERE code = %s 
               AND col_name = %s 
               AND ev_id = %s
               AND NOT (lchg_date = %s 
                    AND lchg_userid = %s);
            """,
                (
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.code,
                    row_mdb.col_name,
                    row_mdb.ev_id,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"col_name={row_mdb.col_name} "
                        + f"code={row_mdb.code}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table dt_flight_crew.
# ------------------------------------------------------------------
def _load_table_dt_flight_crew(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table dt_flight_crew."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            cur_pg.execute(
                """
            INSERT INTO dt_flight_crew (
                   ev_id,aircraft_key,crew_no,col_name,code,lchg_date,lchg_userid,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.crew_no,
                    row_mdb.col_name,
                    row_mdb.code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            UPDATE dt_flight_crew
               SET lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE code = %s AND col_name = %s AND crew_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.code,
                    row_mdb.col_name,
                    row_mdb.crew_no,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"Aircraft_Key={row_mdb.Aircraft_Key} "
                        + f"crew_no={row_mdb.crew_no} "
                        + f"col_name={row_mdb.col_name} "
                        + f"code={row_mdb.code}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table engines.
# ------------------------------------------------------------------
def _load_table_engines(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table engines."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO engines (
                   ev_id,aircraft_key,eng_no,eng_type,eng_mfgr,eng_model,power_units,hp_or_lbs,lchg_userid,lchg_date,carb_fuel_injection,propeller_type,
                   propeller_make,propeller_model,eng_time_total,eng_time_last_insp,eng_time_overhaul,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.eng_no,
                    row_mdb.eng_type,
                    row_mdb.eng_mfgr,
                    row_mdb.eng_model,
                    row_mdb.power_units,
                    row_mdb.hp_or_lbs,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                    row_mdb.carb_fuel_injection,
                    row_mdb.propeller_type,
                    row_mdb.propeller_make,
                    row_mdb.propeller_model,
                    row_mdb.eng_time_total,
                    row_mdb.eng_time_last_insp,
                    row_mdb.eng_time_overhaul,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE engines
               SET eng_type = %s,eng_mfgr = %s,eng_model = %s,power_units = %s,hp_or_lbs = %s,lchg_userid = %s,lchg_date = %s,carb_fuel_injection = %s,
                   propeller_type = %s,propeller_make = %s,propeller_model = %s,eng_time_total = %s,eng_time_last_insp = %s,eng_time_overhaul = %s,
                   io_last_seen_ntsb = %s
             WHERE eng_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (eng_type = %s AND eng_mfgr = %s AND eng_model = %s AND power_units = %s AND hp_or_lbs = %s AND lchg_userid = %s AND
                        lchg_date = %s AND carb_fuel_injection = %s AND propeller_type = %s AND propeller_make = %s AND propeller_model = %s AND
                        eng_time_total = %s AND eng_time_last_insp = %s AND eng_time_overhaul = %s);
            """,
                (
                    row_mdb.eng_type,
                    row_mdb.eng_mfgr,
                    row_mdb.eng_model,
                    row_mdb.power_units,
                    row_mdb.hp_or_lbs,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                    row_mdb.carb_fuel_injection,
                    row_mdb.propeller_type,
                    row_mdb.propeller_make,
                    row_mdb.propeller_model,
                    row_mdb.eng_time_total,
                    row_mdb.eng_time_last_insp,
                    row_mdb.eng_time_overhaul,
                    IO_LAST_SEEN,
                    row_mdb.eng_no,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.eng_type,
                    row_mdb.eng_mfgr,
                    row_mdb.eng_model,
                    row_mdb.power_units,
                    row_mdb.hp_or_lbs,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                    row_mdb.carb_fuel_injection,
                    row_mdb.propeller_type,
                    row_mdb.propeller_make,
                    row_mdb.propeller_model,
                    row_mdb.eng_time_total,
                    row_mdb.eng_time_last_insp,
                    row_mdb.eng_time_overhaul,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"eng_no={row_mdb.eng_no}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table events.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
def _load_table_events(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table events."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            if msaccess == glob_local.MSACCESS_PRE2008:
                # pylint: disable=line-too-long
                cur_pg.execute(
                    """
                INSERT INTO events (
                       ev_id,ntsb_no,ev_type,ev_date,ev_dow,ev_time,ev_tmzn,ev_city,ev_state,ev_country,ev_site_zipcode,ev_year,ev_month,mid_air,
                       on_ground_collision,latitude,longitude,latlong_acq,apt_name,ev_nr_apt_id,ev_nr_apt_loc,apt_dist,apt_dir,apt_elev,wx_brief_comp,
                       wx_src_iic,wx_obs_time,wx_obs_dir,wx_obs_fac_id,wx_obs_elev,wx_obs_dist,wx_obs_tmzn,light_cond,sky_cond_nonceil,sky_nonceil_ht,
                       sky_ceil_ht,sky_cond_ceil,vis_rvr,vis_rvv,vis_sm,wx_temp,wx_dew_pt,wind_dir_deg,wind_dir_ind,wind_vel_kts,wind_vel_ind,gust_ind,
                       gust_kts,altimeter,wx_dens_alt,wx_int_precip,metar,ev_highest_injury,inj_f_grnd,inj_m_grnd,inj_s_grnd,inj_tot_f,inj_tot_m,inj_tot_n,
                       inj_tot_s,inj_tot_t,invest_agy,ntsb_docket,ntsb_notf_from,ntsb_notf_date,ntsb_notf_tm,fiche_number,lchg_date,lchg_userid,wx_cond_basic,
                       faa_dist_office,io_last_seen_ntsb
                       ) VALUES (
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                    (
                        row_mdb.ev_id,
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                        IO_LAST_SEEN,
                    ),
                )
            else:
                # pylint: disable=line-too-long
                cur_pg.execute(
                    """
                INSERT INTO events (
                       ev_id,ntsb_no,ev_type,ev_date,ev_dow,ev_time,ev_tmzn,ev_city,ev_state,ev_country,ev_site_zipcode,ev_year,ev_month,mid_air,
                       on_ground_collision,latitude,longitude,latlong_acq,apt_name,ev_nr_apt_id,ev_nr_apt_loc,apt_dist,apt_dir,apt_elev,wx_brief_comp,
                       wx_src_iic,wx_obs_time,wx_obs_dir,wx_obs_fac_id,wx_obs_elev,wx_obs_dist,wx_obs_tmzn,light_cond,sky_cond_nonceil,sky_nonceil_ht,
                       sky_ceil_ht,sky_cond_ceil,vis_rvr,vis_rvv,vis_sm,wx_temp,wx_dew_pt,wind_dir_deg,wind_dir_ind,wind_vel_kts,wind_vel_ind,gust_ind,
                       gust_kts,altimeter,wx_dens_alt,wx_int_precip,metar,ev_highest_injury,inj_f_grnd,inj_m_grnd,inj_s_grnd,inj_tot_f,inj_tot_m,inj_tot_n,
                       inj_tot_s,inj_tot_t,invest_agy,ntsb_docket,ntsb_notf_from,ntsb_notf_date,ntsb_notf_tm,fiche_number,lchg_date,lchg_userid,wx_cond_basic,
                       faa_dist_office,dec_latitude,dec_longitude,io_last_seen_ntsb
                       ) VALUES (
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                    (
                        row_mdb.ev_id,
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                        row_mdb.dec_latitude,
                        row_mdb.dec_longitude,
                        IO_LAST_SEEN,
                    ),
                )
            count_insert += 1
            if msaccess not in [glob_local.MSACCESS_AVALL, glob_local.MSACCESS_PRE2008]:
                io_utils.progress_msg(
                    f"Inserted ev_id={row_mdb.ev_id} ev_year={row_mdb.ev_year}"
                )
        except UniqueViolation:
            if msaccess == glob_local.MSACCESS_PRE2008:
                # pylint: disable=line-too-long
                cur_pg.execute(
                    """
                UPDATE events
                   SET ntsb_no = %s,ev_type = %s,ev_date = %s,ev_dow = %s,ev_time = %s,ev_tmzn = %s,ev_city = %s,ev_state = %s,ev_country = %s,
                       ev_site_zipcode = %s,ev_year = %s,ev_month = %s,mid_air = %s,on_ground_collision = %s,latitude = %s,longitude = %s,latlong_acq = %s,
                       apt_name = %s,ev_nr_apt_id = %s,ev_nr_apt_loc = %s,apt_dist = %s,apt_dir = %s,apt_elev = %s,wx_brief_comp = %s,wx_src_iic = %s,
                       wx_obs_time = %s,wx_obs_dir = %s,wx_obs_fac_id = %s,wx_obs_elev = %s,wx_obs_dist = %s,wx_obs_tmzn = %s,light_cond = %s,
                       sky_cond_nonceil = %s,sky_nonceil_ht = %s,sky_ceil_ht = %s,sky_cond_ceil = %s,vis_rvr = %s,vis_rvv = %s,vis_sm = %s,wx_temp = %s,
                       wx_dew_pt = %s,wind_dir_deg = %s,wind_dir_ind = %s,wind_vel_kts = %s,wind_vel_ind = %s,gust_ind = %s,gust_kts = %s,altimeter = %s,
                       wx_dens_alt = %s,wx_int_precip = %s,metar = %s,ev_highest_injury = %s,inj_f_grnd = %s,inj_m_grnd = %s,inj_s_grnd = %s,inj_tot_f = %s,
                       inj_tot_m = %s,inj_tot_n = %s,inj_tot_s = %s,inj_tot_t = %s,invest_agy = %s,ntsb_docket = %s,ntsb_notf_from = %s,ntsb_notf_date = %s,
                       ntsb_notf_tm = %s,fiche_number = %s,lchg_date = %s,lchg_userid = %s,wx_cond_basic = %s,faa_dist_office = %s,io_last_seen_ntsb = %s
                 WHERE ev_id = %s
                   AND NOT (ntsb_no = %s AND ev_type = %s AND ev_date = %s AND ev_dow = %s AND ev_time = %s AND ev_tmzn = %s AND ev_city = %s AND
                            ev_state = %s AND ev_country = %s AND ev_site_zipcode = %s AND ev_year = %s AND ev_month = %s AND mid_air = %s AND
                            on_ground_collision = %s AND latitude = %s AND longitude = %s AND latlong_acq = %s AND apt_name = %s AND ev_nr_apt_id = %s AND
                            ev_nr_apt_loc = %s AND apt_dist = %s AND apt_dir = %s AND apt_elev = %s AND wx_brief_comp = %s AND wx_src_iic = %s AND
                            wx_obs_time = %s AND wx_obs_dir = %s AND wx_obs_fac_id = %s AND wx_obs_elev = %s AND wx_obs_dist = %s AND wx_obs_tmzn = %s AND
                            light_cond = %s AND sky_cond_nonceil = %s AND sky_nonceil_ht = %s AND sky_ceil_ht = %s AND sky_cond_ceil = %s AND vis_rvr = %s AND
                            vis_rvv = %s AND vis_sm = %s AND wx_temp = %s AND wx_dew_pt = %s AND wind_dir_deg = %s AND wind_dir_ind = %s AND
                            wind_vel_kts = %s AND wind_vel_ind = %s AND gust_ind = %s AND gust_kts = %s AND altimeter = %s AND wx_dens_alt = %s AND
                            wx_int_precip = %s AND metar = %s AND ev_highest_injury = %s AND inj_f_grnd = %s AND inj_m_grnd = %s AND inj_s_grnd = %s AND
                            inj_tot_f = %s AND inj_tot_m = %s AND inj_tot_n = %s AND inj_tot_s = %s AND inj_tot_t = %s AND invest_agy = %s AND
                            ntsb_docket = %s AND ntsb_notf_from = %s AND ntsb_notf_date = %s AND ntsb_notf_tm = %s AND fiche_number = %s AND
                            lchg_date = %s AND lchg_userid = %s AND wx_cond_basic = %s AND faa_dist_office = %s);
                """,
                    (
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                        IO_LAST_SEEN,
                        row_mdb.ev_id,
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                    ),
                )
            else:
                # pylint: disable=line-too-long
                cur_pg.execute(
                    """
                UPDATE events
                   SET ntsb_no = %s,ev_type = %s,ev_date = %s,ev_dow = %s,ev_time = %s,ev_tmzn = %s,ev_city = %s,ev_state = %s,ev_country = %s,
                   ev_site_zipcode = %s,ev_year = %s,ev_month = %s,mid_air = %s,on_ground_collision = %s,latitude = %s,longitude = %s,latlong_acq = %s,
                   apt_name = %s,ev_nr_apt_id = %s,ev_nr_apt_loc = %s,apt_dist = %s,apt_dir = %s,apt_elev = %s,wx_brief_comp = %s,wx_src_iic = %s,
                   wx_obs_time = %s,wx_obs_dir = %s,wx_obs_fac_id = %s,wx_obs_elev = %s,wx_obs_dist = %s,wx_obs_tmzn = %s,light_cond = %s,
                   sky_cond_nonceil = %s,sky_nonceil_ht = %s,sky_ceil_ht = %s,sky_cond_ceil = %s,vis_rvr = %s,vis_rvv = %s,vis_sm = %s,
                   wx_temp = %s,wx_dew_pt = %s,wind_dir_deg = %s,wind_dir_ind = %s,wind_vel_kts = %s,wind_vel_ind = %s,gust_ind = %s,gust_kts = %s,
                   altimeter = %s,wx_dens_alt = %s,wx_int_precip = %s,metar = %s,ev_highest_injury = %s,inj_f_grnd = %s,inj_m_grnd = %s,inj_s_grnd = %s,
                   inj_tot_f = %s,inj_tot_m = %s,inj_tot_n = %s,inj_tot_s = %s,inj_tot_t = %s,invest_agy = %s,ntsb_docket = %s,ntsb_notf_from = %s,
                   ntsb_notf_date = %s,ntsb_notf_tm = %s,fiche_number = %s,lchg_date = %s,lchg_userid = %s,wx_cond_basic = %s,faa_dist_office = %s,
                   dec_latitude = %s,dec_longitude = %s,io_last_seen_ntsb = %s
                 WHERE ev_id = %s
                   AND NOT (ntsb_no = %s AND ev_type = %s AND ev_date = %s AND ev_dow = %s AND ev_time = %s AND ev_tmzn = %s AND ev_city = %s AND
                            ev_state = %s AND ev_country = %s AND ev_site_zipcode = %s AND ev_year = %s AND ev_month = %s AND mid_air = %s AND
                            on_ground_collision = %s AND latitude = %s AND longitude = %s AND latlong_acq = %s AND apt_name = %s AND ev_nr_apt_id = %s AND
                            ev_nr_apt_loc = %s AND apt_dist = %s AND apt_dir = %s AND apt_elev = %s AND wx_brief_comp = %s AND wx_src_iic = %s AND
                            wx_obs_time = %s AND wx_obs_dir = %s AND wx_obs_fac_id = %s AND wx_obs_elev = %s AND wx_obs_dist = %s AND wx_obs_tmzn = %s AND
                            light_cond = %s AND sky_cond_nonceil = %s AND sky_nonceil_ht = %s AND sky_ceil_ht = %s AND sky_cond_ceil = %s AND
                            vis_rvr = %s AND vis_rvv = %s AND vis_sm = %s AND wx_temp = %s AND wx_dew_pt = %s AND wind_dir_deg = %s AND
                            wind_dir_ind = %s AND wind_vel_kts = %s AND wind_vel_ind = %s AND gust_ind = %s AND gust_kts = %s AND altimeter = %s AND
                            wx_dens_alt = %s AND wx_int_precip = %s AND metar = %s AND ev_highest_injury = %s AND inj_f_grnd = %s AND inj_m_grnd = %s AND
                            inj_s_grnd = %s AND inj_tot_f = %s AND inj_tot_m = %s AND inj_tot_n = %s AND inj_tot_s = %s AND inj_tot_t = %s AND
                            invest_agy = %s AND ntsb_docket = %s AND ntsb_notf_from = %s AND ntsb_notf_date = %s AND ntsb_notf_tm = %s AND
                            fiche_number = %s AND lchg_date = %s AND lchg_userid = %s AND wx_cond_basic = %s AND faa_dist_office = %s
                            AND dec_latitude = %s AND dec_longitude = %s);
                """,
                    (
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                        row_mdb.dec_latitude,
                        row_mdb.dec_longitude,
                        IO_LAST_SEEN,
                        row_mdb.ev_id,
                        row_mdb.ntsb_no,
                        row_mdb.ev_type,
                        row_mdb.ev_date,
                        row_mdb.ev_dow,
                        row_mdb.ev_time,
                        row_mdb.ev_tmzn,
                        (
                            None
                            if row_mdb.ev_city is None
                            else (
                                row_mdb.ev_city.rstrip()
                                if len(row_mdb.ev_city.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_state,
                        row_mdb.ev_country,
                        (
                            None
                            if row_mdb.ev_site_zipcode is None
                            else (
                                row_mdb.ev_site_zipcode.rstrip()
                                if len(row_mdb.ev_site_zipcode.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.ev_year,
                        row_mdb.ev_month,
                        row_mdb.mid_air,
                        row_mdb.on_ground_collision,
                        (
                            None
                            if row_mdb.latitude is None
                            else (
                                row_mdb.latitude.rstrip()
                                if len(row_mdb.latitude.rstrip()) > 0
                                else None
                            )
                        ),
                        (
                            None
                            if row_mdb.longitude is None
                            else (
                                row_mdb.longitude.rstrip()
                                if len(row_mdb.longitude.rstrip()) > 0
                                else None
                            )
                        ),
                        row_mdb.latlong_acq,
                        row_mdb.apt_name,
                        row_mdb.ev_nr_apt_id,
                        row_mdb.ev_nr_apt_loc,
                        row_mdb.apt_dist,
                        row_mdb.apt_dir,
                        row_mdb.apt_elev,
                        row_mdb.wx_brief_comp,
                        row_mdb.wx_src_iic,
                        row_mdb.wx_obs_time,
                        row_mdb.wx_obs_dir,
                        row_mdb.wx_obs_fac_id,
                        row_mdb.wx_obs_elev,
                        row_mdb.wx_obs_dist,
                        row_mdb.wx_obs_tmzn,
                        row_mdb.light_cond,
                        row_mdb.sky_cond_nonceil,
                        row_mdb.sky_nonceil_ht,
                        row_mdb.sky_ceil_ht,
                        row_mdb.sky_cond_ceil,
                        row_mdb.vis_rvr,
                        row_mdb.vis_rvv,
                        row_mdb.vis_sm,
                        row_mdb.wx_temp,
                        row_mdb.wx_dew_pt,
                        row_mdb.wind_dir_deg,
                        row_mdb.wind_dir_ind,
                        row_mdb.wind_vel_kts,
                        row_mdb.wind_vel_ind,
                        row_mdb.gust_ind,
                        row_mdb.gust_kts,
                        row_mdb.altimeter,
                        row_mdb.wx_dens_alt,
                        row_mdb.wx_int_precip,
                        row_mdb.metar,
                        row_mdb.ev_highest_injury,
                        row_mdb.inj_f_grnd,
                        row_mdb.inj_m_grnd,
                        row_mdb.inj_s_grnd,
                        row_mdb.inj_tot_f,
                        row_mdb.inj_tot_m,
                        row_mdb.inj_tot_n,
                        row_mdb.inj_tot_s,
                        row_mdb.inj_tot_t,
                        row_mdb.invest_agy,
                        row_mdb.ntsb_docket,
                        row_mdb.ntsb_notf_from,
                        row_mdb.ntsb_notf_date,
                        row_mdb.ntsb_notf_tm,
                        row_mdb.fiche_number,
                        row_mdb.lchg_date,
                        row_mdb.lchg_userid,
                        row_mdb.wx_cond_basic,
                        row_mdb.faa_dist_office,
                        row_mdb.dec_latitude,
                        row_mdb.dec_longitude,
                    ),
                )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"ev_year={row_mdb.ev_year}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table events_sequence.
# ------------------------------------------------------------------
def _load_table_events_sequence(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table events_sequence."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO events_sequence (
                   ev_id,aircraft_key,occurrence_no,occurrence_code,occurrence_description,phase_no,eventsoe_no,defining_ev,lchg_date,lchg_userid,
                   io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.Occurrence_No,
                    row_mdb.Occurrence_Code,
                    row_mdb.Occurrence_Description,
                    row_mdb.phase_no,
                    row_mdb.eventsoe_no,
                    row_mdb.Defining_ev,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE events_sequence
               SET occurrence_code = %s,occurrence_description = %s,phase_no = %s,eventsoe_no = %s,defining_ev = %s,lchg_date = %s,lchg_userid = %s,
                   io_last_seen_ntsb = %s
             WHERE occurrence_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (occurrence_code = %s AND occurrence_description = %s AND phase_no = %s AND eventsoe_no = %s AND defining_ev = %s AND
                        lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.Occurrence_Code,
                    row_mdb.Occurrence_Description,
                    row_mdb.phase_no,
                    row_mdb.eventsoe_no,
                    row_mdb.Defining_ev,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.Occurrence_No,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.Occurrence_Code,
                    row_mdb.Occurrence_Description,
                    row_mdb.phase_no,
                    row_mdb.eventsoe_no,
                    row_mdb.Defining_ev,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"Aircraft_Key={row_mdb.Aircraft_Key} "
                        + f"Occurrence_No={row_mdb.Occurrence_No}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table findings.
# ------------------------------------------------------------------
def _load_table_findings(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table findings."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO findings (
                   ev_id,
                   aircraft_key,
                   finding_no,
                   finding_code,
                   finding_description,
                   category_no,
                   subcategory_no,
                   section_no,
                   subsection_no,
                   modifier_no,
                   cause_factor,
                   cm_inPc,
                   lchg_date,
                   lchg_userid,
                   io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s,
                   %s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.finding_no,
                    row_mdb.finding_code,
                    row_mdb.finding_description,
                    row_mdb.category_no,
                    row_mdb.subcategory_no,
                    row_mdb.section_no,
                    row_mdb.subsection_no,
                    row_mdb.modifier_no,
                    row_mdb.Cause_Factor,
                    row_mdb.cm_inPc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE findings
               SET finding_code = %s,
                   finding_description = %s,
                   category_no = %s,
                   subcategory_no = %s,
                   section_no = %s,
                   subsection_no = %s,
                   modifier_no = %s,
                   cause_factor = %s,
                   cm_inpc = %s,
                   lchg_date = %s,
                   lchg_userid = %s,
                   io_last_seen_ntsb = %s
             WHERE finding_no = %s 
               AND aircraft_key = %s 
               AND ev_id = %s
               AND NOT (finding_code = %s 
                    AND finding_description = %s 
                    AND category_no = %s 
                    AND subcategory_no = %s 
                    AND section_no = %s 
                    AND subsection_no = %s 
                    AND modifier_no = %s 
                    AND cause_factor = %s 
                    AND cm_inpc = %s 
                    AND lchg_date = %s 
                    AND lchg_userid = %s);
            """,
                (
                    row_mdb.finding_code,
                    row_mdb.finding_description,
                    row_mdb.category_no,
                    row_mdb.subcategory_no,
                    row_mdb.section_no,
                    row_mdb.subsection_no,
                    row_mdb.modifier_no,
                    row_mdb.Cause_Factor,
                    row_mdb.cm_inPc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.finding_no,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.finding_code,
                    row_mdb.finding_description,
                    row_mdb.category_no,
                    row_mdb.subcategory_no,
                    row_mdb.section_no,
                    row_mdb.subsection_no,
                    row_mdb.modifier_no,
                    row_mdb.Cause_Factor,
                    row_mdb.cm_inPc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"finding_no={row_mdb.finding_no}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table flight_crew.
# ------------------------------------------------------------------
def _load_table_flight_crew(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table flight_crew."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO flight_crew (
                   ev_id,aircraft_key,crew_no,crew_category,crew_age,crew_sex,crew_city,crew_res_state,crew_res_country,med_certf,med_crtf_vldty,
                   date_lst_med,crew_rat_endorse,crew_inj_level,seatbelts_used,shldr_harn_used,crew_tox_perf,seat_occ_pic,pc_profession,bfr,bfr_date,
                   ft_as_of,lchg_date,lchg_userid,seat_occ_row,infl_rest_inst,infl_rest_depl,child_restraint,med_crtf_limit,mr_faa_med_certf,pilot_flying,
                   available_restraint,restraint_used,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.crew_no,
                    row_mdb.crew_category,
                    row_mdb.crew_age,
                    row_mdb.crew_sex,
                    row_mdb.crew_city,
                    row_mdb.crew_res_state,
                    row_mdb.crew_res_country,
                    row_mdb.med_certf,
                    row_mdb.med_crtf_vldty,
                    row_mdb.date_lst_med,
                    row_mdb.crew_rat_endorse,
                    row_mdb.crew_inj_level,
                    row_mdb.seatbelts_used,
                    row_mdb.shldr_harn_used,
                    row_mdb.crew_tox_perf,
                    row_mdb.seat_occ_pic,
                    row_mdb.pc_profession,
                    row_mdb.bfr,
                    row_mdb.bfr_date,
                    row_mdb.ft_as_of,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.seat_occ_row,
                    row_mdb.infl_rest_inst,
                    row_mdb.infl_rest_depl,
                    row_mdb.child_restraint,
                    row_mdb.med_crtf_limit,
                    row_mdb.mr_faa_med_certf,
                    row_mdb.pilot_flying,
                    row_mdb.available_restraint,
                    row_mdb.restraint_used,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE flight_crew
               SET crew_category = %s,crew_age = %s,crew_sex = %s,crew_city = %s,crew_res_state = %s,crew_res_country = %s,med_certf = %s,
                   med_crtf_vldty = %s,date_lst_med = %s,crew_rat_endorse = %s,crew_inj_level = %s,seatbelts_used = %s,shldr_harn_used = %s,
                   crew_tox_perf = %s,seat_occ_pic = %s,pc_profession = %s,bfr = %s,bfr_date = %s,ft_as_of = %s,lchg_date = %s,lchg_userid = %s,
                   seat_occ_row = %s,infl_rest_inst = %s,infl_rest_depl = %s,child_restraint = %s,med_crtf_limit = %s,mr_faa_med_certf = %s,
                   pilot_flying = %s,available_restraint = %s,restraint_used = %s,io_last_seen_ntsb = %s
             WHERE crew_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (crew_category = %s AND crew_age = %s AND crew_sex = %s AND crew_city = %s AND crew_res_state = %s AND crew_res_country = %s AND
                        med_certf = %s AND med_crtf_vldty = %s AND date_lst_med = %s AND crew_rat_endorse = %s AND crew_inj_level = %s AND
                        seatbelts_used = %s AND shldr_harn_used = %s AND crew_tox_perf = %s AND seat_occ_pic = %s AND pc_profession = %s AND bfr = %s AND
                        bfr_date = %s AND ft_as_of = %s AND lchg_date = %s AND lchg_userid = %s AND seat_occ_row = %s AND infl_rest_inst = %s AND
                        infl_rest_depl = %s AND child_restraint = %s AND med_crtf_limit = %s AND mr_faa_med_certf = %s AND pilot_flying = %s AND
                        available_restraint = %s AND restraint_used = %s);
            """,
                (
                    row_mdb.crew_category,
                    row_mdb.crew_age,
                    row_mdb.crew_sex,
                    row_mdb.crew_city,
                    row_mdb.crew_res_state,
                    row_mdb.crew_res_country,
                    row_mdb.med_certf,
                    row_mdb.med_crtf_vldty,
                    row_mdb.date_lst_med,
                    row_mdb.crew_rat_endorse,
                    row_mdb.crew_inj_level,
                    row_mdb.seatbelts_used,
                    row_mdb.shldr_harn_used,
                    row_mdb.crew_tox_perf,
                    row_mdb.seat_occ_pic,
                    row_mdb.pc_profession,
                    row_mdb.bfr,
                    row_mdb.bfr_date,
                    row_mdb.ft_as_of,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.seat_occ_row,
                    row_mdb.infl_rest_inst,
                    row_mdb.infl_rest_depl,
                    row_mdb.child_restraint,
                    row_mdb.med_crtf_limit,
                    row_mdb.mr_faa_med_certf,
                    row_mdb.pilot_flying,
                    row_mdb.available_restraint,
                    row_mdb.restraint_used,
                    IO_LAST_SEEN,
                    row_mdb.crew_no,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.crew_category,
                    row_mdb.crew_age,
                    row_mdb.crew_sex,
                    row_mdb.crew_city,
                    row_mdb.crew_res_state,
                    row_mdb.crew_res_country,
                    row_mdb.med_certf,
                    row_mdb.med_crtf_vldty,
                    row_mdb.date_lst_med,
                    row_mdb.crew_rat_endorse,
                    row_mdb.crew_inj_level,
                    row_mdb.seatbelts_used,
                    row_mdb.shldr_harn_used,
                    row_mdb.crew_tox_perf,
                    row_mdb.seat_occ_pic,
                    row_mdb.pc_profession,
                    row_mdb.bfr,
                    row_mdb.bfr_date,
                    row_mdb.ft_as_of,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    row_mdb.seat_occ_row,
                    row_mdb.infl_rest_inst,
                    row_mdb.infl_rest_depl,
                    row_mdb.child_restraint,
                    row_mdb.med_crtf_limit,
                    row_mdb.mr_faa_med_certf,
                    row_mdb.pilot_flying,
                    row_mdb.available_restraint,
                    row_mdb.restraint_used,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"crew_no={row_mdb.crew_no}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table flight_time.
# ------------------------------------------------------------------
def _load_table_flight_time(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table flight_time."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO flight_time (
                   ev_id,aircraft_key,crew_no,flight_type,flight_craft,flight_hours,lchg_date,lchg_userid,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.crew_no,
                    row_mdb.flight_type,
                    row_mdb.flight_craft,
                    row_mdb.flight_hours,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE flight_time
               SET flight_hours = %s,lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE flight_craft = %s AND flight_type = %s AND crew_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (flight_hours = %s AND lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.flight_hours,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.flight_craft,
                    row_mdb.flight_type,
                    row_mdb.crew_no,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.flight_hours,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"crew_no={row_mdb.crew_no} "
                        + f"flight_type={row_mdb.flight_type} "
                        + f"flight_craft={row_mdb.flight_craft}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table injury.
# ------------------------------------------------------------------
def _load_table_injury(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table injury."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO injury (
                   ev_id,aircraft_key,inj_person_category,injury_level,inj_person_count,lchg_date,lchg_userid,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.inj_person_category,
                    row_mdb.injury_level,
                    row_mdb.inj_person_count,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE injury
               SET inj_person_count = %s,lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE injury_level = %s AND inj_person_category = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (inj_person_count = %s AND lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.inj_person_count,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.injury_level,
                    row_mdb.inj_person_category,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.inj_person_count,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"inj_person_category={row_mdb.inj_person_category} "
                        + f"injury_level={row_mdb.injury_level}"
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
    """Determine and load city averages."""
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

    conn_pg_2.autocommit = False

    # pylint: disable=line-too-long
    cur_pg_2.execute(
        f"""
    SELECT country, state, city, sum(dec_latitude)/count(*) dec_latitude, sum(dec_longitude)/count(*) dec_longitude
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
                    row_pg[COLUMN_COUNTRY],  # type: ignore
                    row_pg[COLUMN_STATE],  # type: ignore
                    row_pg[COLUMN_CITY],  # type: ignore
                    row_pg[COLUMN_DEC_LATITUDE],  # type: ignore
                    row_pg[COLUMN_DEC_LONGITUDE],  # type: ignore
                    glob_local.SOURCE_AVERAGE,
                    datetime.now(tz=timezone.utc),
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
# Load the data from database table narratives.
# ------------------------------------------------------------------
def _load_table_narratives(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table narratives."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        try:
            cur_pg.execute(
                # pylint: disable=line-too-long
                """
            INSERT INTO narratives (
                   ev_id,aircraft_key,narr_accp,narr_accf,narr_cause,narr_inc,lchg_date,lchg_userid,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.narr_accp,
                    row_mdb.narr_accf,
                    row_mdb.narr_cause,
                    row_mdb.narr_inc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            UPDATE narratives
               SET narr_accp = %s,narr_accf = %s,narr_cause = %s,narr_inc = %s,lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE aircraft_key = %s AND ev_id = %s
               AND NOT (narr_accp = %s AND narr_accf = %s AND narr_cause = %s AND narr_inc = %s AND lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.narr_accp,
                    row_mdb.narr_accf,
                    row_mdb.narr_cause,
                    row_mdb.narr_inc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.narr_accp,
                    row_mdb.narr_accf,
                    row_mdb.narr_cause,
                    row_mdb.narr_inc,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key}"
                    )

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table ntsb_admin.
# ------------------------------------------------------------------
def _load_table_ntsb_admin(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table ntsb_admin."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        if row_mdb.ev_id in ["20210527103155", "20220328104839"]:
            # ERROR_00_946 = "ERROR.00.946 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_946.replace("{ev_id}", row_mdb.ev_id)
            )
            continue

        try:
            cur_pg.execute(
                """
            INSERT INTO ntsb_admin (
                   ev_id,rec_stat,approval_date,lchg_userid,lchg_date,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.rec_stat,
                    row_mdb.approval_date,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            UPDATE ntsb_admin
               SET rec_stat = %s,approval_date = %s,lchg_userid = %s,lchg_date = %s,io_last_seen_ntsb = %s
             WHERE ev_id = %s
               AND NOT (rec_stat = %s AND approval_date = %s AND lchg_userid = %s AND lchg_date = %s);
            """,
                (
                    row_mdb.rec_stat,
                    row_mdb.approval_date,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                    IO_LAST_SEEN,
                    row_mdb.ev_id,
                    row_mdb.rec_stat,
                    row_mdb.approval_date,
                    row_mdb.lchg_userid,
                    row_mdb.lchg_date,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(f"Updated  ev_id={row_mdb.ev_id}")
        except ForeignKeyViolation:
            # ERROR_00_947 = "ERROR.00.947 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_947.replace("{ev_id}", row_mdb.ev_id)
            )
            conn_pg.rollback()

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table occurrences.
# ------------------------------------------------------------------
def _load_table_occurrences(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table occurrences."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        if row_mdb.ev_id in [
            "20001213X25705",
            "20001213X29793",
            "20001213X30454",
            "20001213X31758",
            "20001213X32752",
            "20001218X45444",
            "20001218X45446",
        ]:
            # ERROR_00_946 = "ERROR.00.946 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_946.replace("{ev_id}", row_mdb.ev_id)
            )
            continue

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO occurrences (
                   ev_id,aircraft_key,occurrence_no,occurrence_code,phase_of_flight,altitude,lchg_date,lchg_userid,io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.Occurrence_No,
                    row_mdb.Occurrence_Code,
                    row_mdb.Phase_of_Flight,
                    row_mdb.Altitude,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE occurrences
               SET occurrence_code = %s,phase_of_flight = %s,altitude = %s,lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE occurrence_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (occurrence_code = %s AND phase_of_flight = %s AND altitude = %s AND lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.Occurrence_Code,
                    row_mdb.Phase_of_Flight,
                    row_mdb.Altitude,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.Occurrence_No,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.Occurrence_Code,
                    row_mdb.Phase_of_Flight,
                    row_mdb.Altitude,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"Occurrence_No={row_mdb.Occurrence_No}"
                    )
        except ForeignKeyViolation:
            # ERROR_00_947 = "ERROR.00.947 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_947.replace("{ev_id}", row_mdb.ev_id)
            )
            conn_pg.rollback()

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

    logger.debug(io_glob.LOGGER_END)


# ------------------------------------------------------------------
# Load the data from database table seq_of_events.
# ------------------------------------------------------------------
def _load_table_seq_of_events(
    msaccess: str,
    table_name: str,
    cur_mdb: pyodbc.Cursor,
    conn_pg: connection,
    cur_pg: cursor,
) -> None:
    """Load the data from database table seq_of_events."""
    logger.debug(io_glob.LOGGER_START)

    count_insert = 0
    count_select = 0
    count_update = 0

    io_utils.progress_msg("")
    io_utils.progress_msg(
        f"Database table       : {table_name.lower():30}" + "<" + "-" * 35
    )

    cur_mdb.execute(f"SELECT * FROM {table_name};")

    rows_mdb = cur_mdb.fetchall()

    for row_mdb in rows_mdb:
        count_select += 1

        if count_select % io_config.settings.database_commit_size == 0:
            conn_pg.commit()
            io_utils.progress_msg(
                f"Number of rows so far read : {str(count_select):>8}"
            )

        if row_mdb.ev_id in [
            "20020917X03487",
        ]:
            # ERROR_00_946 = "ERROR.00.946 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_946.replace("{ev_id}", row_mdb.ev_id)
            )
            continue

        try:
            # pylint: disable=line-too-long
            cur_pg.execute(
                """
            INSERT INTO seq_of_events (
                   ev_id,aircraft_key,occurrence_no,seq_event_no,group_code,subj_code,cause_factor,modifier_code,person_code,lchg_date,lchg_userid,
                   io_last_seen_ntsb
                   ) VALUES (
                   %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """,
                (
                    row_mdb.ev_id,
                    row_mdb.Aircraft_Key,
                    row_mdb.Occurrence_No,
                    row_mdb.seq_event_no,
                    row_mdb.group_code,
                    row_mdb.Subj_Code,
                    row_mdb.Cause_Factor,
                    row_mdb.Modifier_Code,
                    row_mdb.Person_Code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                ),
            )
            count_insert += 1
        except UniqueViolation:
            cur_pg.execute(
                """
            UPDATE seq_of_events
               SET aircraft_key = %s,occurrence_no = %s,seq_event_no = %s,group_code = %s,subj_code = %s,cause_factor = %s,modifier_code = %s,
                   person_code = %s,lchg_date = %s,lchg_userid = %s,io_last_seen_ntsb = %s
             WHERE group_code = %s AND seq_event_no = %s AND occurrence_no = %s AND aircraft_key = %s AND ev_id = %s
               AND NOT (subj_code = %s AND cause_factor = %s AND modifier_code = %s AND person_code = %s AND lchg_date = %s AND lchg_userid = %s);
            """,
                (
                    row_mdb.Aircraft_Key,
                    row_mdb.Occurrence_No,
                    row_mdb.seq_event_no,
                    row_mdb.group_code,
                    row_mdb.Subj_Code,
                    row_mdb.Cause_Factor,
                    row_mdb.Modifier_Code,
                    row_mdb.Person_Code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                    IO_LAST_SEEN,
                    row_mdb.group_code,
                    row_mdb.seq_event_no,
                    row_mdb.Occurrence_No,
                    row_mdb.Aircraft_Key,
                    row_mdb.ev_id,
                    row_mdb.Subj_Code,
                    row_mdb.Cause_Factor,
                    row_mdb.Modifier_Code,
                    row_mdb.Person_Code,
                    row_mdb.lchg_date,
                    row_mdb.lchg_userid,
                ),
            )
            if cur_pg.rowcount > 0:
                count_update += cur_pg.rowcount
                if msaccess not in [
                    glob_local.MSACCESS_AVALL,
                    glob_local.MSACCESS_PRE2008,
                ]:
                    io_utils.progress_msg(
                        f"Updated  ev_id={row_mdb.ev_id} "
                        + f"aircraft_key={row_mdb.Aircraft_Key} "
                        + f"Occurrence_No={row_mdb.Occurrence_No} "
                        + f"seq_event_no={row_mdb.seq_event_no} "
                        + f"group_code={row_mdb.group_code}"
                    )
        except ForeignKeyViolation:
            # ERROR_00_947 = "ERROR.00.947 The ev_id '{ev_id}' is missing in database table events"
            io_utils.progress_msg(
                glob_local.ERROR_00_947.replace("{ev_id}", row_mdb.ev_id)
            )
            conn_pg.rollback()

    conn_pg.commit()

    io_utils.progress_msg(f"Number rows selected : {str(count_select):>8}")

    if count_insert > 0:
        io_utils.progress_msg(f"Number rows inserted : {str(count_insert):>8}")
    if count_update > 0:
        io_utils.progress_msg(f"Number rows updated  : {str(count_update):>8}")

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
# Download an MS Access database file.
# ------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def download_ntsb_msaccess_file(msaccess: str) -> None:
    """Download an MS Access database file.

    Args:
        msaccess (str):
            The MS Access database file without file extension.

    """
    logger.debug(io_glob.LOGGER_START)

    filename_zip = msaccess + "." + glob_local.FILE_EXTENSION_ZIP
    url = io_config.settings.download_url_ntsb_prefix + filename_zip

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

        # INFO.00.013 The connection to the MS Access database file '{msaccess}.zip'
        # on the NTSB download page was successfully established
        io_utils.progress_msg(glob_local.INFO_00_013.replace("{msaccess}", msaccess))

        if not os.path.isdir(io_config.settings.download_work_dir):
            os.makedirs(io_config.settings.download_work_dir)

        filename_zip = os.path.join(
            io_config.settings.download_work_dir.replace("/", os.sep), filename_zip
        )

        no_chunks = 0

        with open(filename_zip, "wb") as file_zip:
            for chunk in file_resp.iter_content(
                chunk_size=io_config.settings.download_chunk_size
            ):
                file_zip.write(chunk)
                no_chunks += 1

        # INFO.00.014 From the file '{msaccess}' {no_chunks} chunks were downloaded
        io_utils.progress_msg(
            glob_local.INFO_00_014.replace("{msaccess}", msaccess).replace(
                "{no_chunks}", str(no_chunks)
            )
        )

        try:
            zipped_files = zipfile.ZipFile(  # pylint: disable=consider-using-with
                filename_zip
            )

            for zipped_file in zipped_files.namelist():
                zipped_files.extract(zipped_file, io_config.settings.download_work_dir)

            zipped_files.close()
        except zipfile.BadZipFile:
            # ERROR.00.907 File'{filename}' is not a zip file
            io_utils.terminate_fatal(
                glob_local.ERROR_00_907.replace("{filename}", filename_zip)
            )

        os.remove(filename_zip)
        # INFO.00.015 The file '{msaccess}.zip'  was successfully unpacked
        io_utils.progress_msg(glob_local.INFO_00_015.replace("{msaccess}", msaccess))

        _check_ddl_changes(msaccess)
    except ConnectionError:
        # ERROR.00.905 Connection problem with url='{url}'
        io_utils.terminate_fatal(glob_local.ERROR_00_905.replace("{url}", url))
    except TimeoutError:
        # ERROR.00.909 Timeout after'{timeout}' seconds with url='{url}
        io_utils.terminate_fatal(
            glob_local.ERROR_00_909.replace(
                "{timeout}", str(io_config.settings.download_timeout)
            ).replace("{url}", url)
        )

    logger.debug(io_glob.LOGGER_END)
