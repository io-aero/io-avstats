# Copyright (c) 2022-2024 IO-Aero. All rights reserved. Use of this
# source code is governed by the IO-Aero License, that can
# be found in the LICENSE.md file.
"""IO-AVSTATS interface."""
from __future__ import annotations

from pathlib import Path

from iocommon import io_glob, io_settings


# -----------------------------------------------------------------------------
# Generate SQL statements: INSERT.
# -----------------------------------------------------------------------------
def _generate_sql_insert(ref_lines: list[str]) -> None:
    """Generate SQL statements: INSERT.

    Args:
        ref_lines (list[str]): DDL export of RazorSQL.

    """
    filename = io_settings.settings.download_work_dir / "generated_insert.sql"

    columns: list[str] = []
    table_name: str = ""
    value_placeholders: list[str] = []
    values: list[str] = []

    with Path(filename).open("w", encoding=io_glob.FILE_ENCODING_DEFAULT) as out:
        out.write("-- " + "=" * 80 + "\n")
        out.write("-- INSERT\n")
        out.write("-- " + "-" * 80 + "\n")

        for ref_line in ref_lines:
            ref_line_helper = ref_line.rstrip()

            if not ref_line_helper:
                continue

            if ref_line_helper == ");":
                out.write('cur_pg.execute("""\n')
                out.write("INSERT INTO " + table_name.lower() + " (\n")
                out.write("       " + ",".join(columns) + "\n")
                out.write("       ) VALUES (" + ",".join(value_placeholders) + ");\n")
                out.write('""",\n')
                out.write("(" + ",".join(values) + "))\n")
                out.write("-- " + "-" * 80 + "\n")
                continue

            ref_tokens = ref_line_helper.split()

            if ref_tokens[0] == "PRIMARY":
                continue

            if ref_tokens[0] == "CREATE":
                table_name = ref_tokens[2]
                out.write("-- INSERT for TABLE " + table_name + "\n")
                out.write("-- " + "-" * 80 + "\n")
                columns = []
                value_placeholders = []
                values = []
                continue

            columns.append(ref_tokens[0].lower())
            value_placeholders.append("%s")
            values.append("row_mdb." + ref_tokens[0])


# -----------------------------------------------------------------------------
# Generate SQL statements: UPDATE.
# -----------------------------------------------------------------------------
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def _generate_sql_update(ref_lines: list[str]) -> None:
    """Generate SQL statements: UPDATE.

    Args:
        ref_lines (list[str]): DDL export of RazorSQL.

    """
    table_name: str = ""

    # -----------------------------------------------------------------------------
    # Process the primary keys.
    # -----------------------------------------------------------------------------
    pks: dict[str, tuple[list[str], list[str], list[str]]] = {}

    is_pk = False

    for ref_line_helper in ref_lines:
        if not ref_line_helper.rstrip():
            continue

        ref_tokens = ref_line_helper.split()
        if ref_tokens[0] == "CREATE":
            if not is_pk and table_name:
                pks[table_name] = (["ev_id"], ["row_mdb.ev_id"], ["ev_id = %s"])

            table_name = ref_tokens[2]
            is_pk = False
            continue

        if ref_tokens[0] != "PRIMARY":
            continue

        pk_columns = []
        pk_values = []
        pk_where = []

        for ref_token in reversed(ref_tokens[2][1:-1].split(",")):
            pk_columns.append(ref_token)
            pk_values.append("row_mdb." + ref_token)
            pk_where.append(ref_token.lower() + " = %s")

        pks[table_name] = (pk_columns, pk_values, pk_where)

        is_pk = True

    if not is_pk and table_name:
        pks[table_name] = (["ev_id"], ["row_mdb.ev_id"], ["ev_id = %s"])

    # -----------------------------------------------------------------------------
    # Create the UPDATE statements.
    # -----------------------------------------------------------------------------
    filename = io_settings.settings.download_work_dir / "generated_update.sql"

    assignments: list[str] = []
    assignment_values: list[str] = []

    with Path(filename).open("w", encoding=io_glob.FILE_ENCODING_DEFAULT) as out:
        out.write("-- " + "=" * 80 + "\n")
        out.write("-- UPDATE\n")
        out.write("-- " + "-" * 80 + "\n")

        for ref_line in ref_lines:
            ref_line_helper = ref_line.rstrip()

            if not ref_line_helper:
                continue

            if ref_line_helper == ");":
                out.write('cur_pg.execute("""\n')
                out.write("UPDATE " + table_name.lower() + " SET\n")
                out.write("       " + ",".join(assignments) + "\n")
                out.write(" WHERE\n")
                out.write("       " + " AND ".join(pk_where) + "\n")
                out.write("   AND NOT (" + " AND ".join(assignments) + ");\n")
                out.write('""",\n')
                out.write(
                    "("
                    + ",".join(assignment_values + pk_values + assignment_values)
                    + "))\n",
                )
                out.write("-- " + "-" * 80 + "\n")
                continue

            ref_tokens = ref_line_helper.split()

            if ref_tokens[0] in ["FOREIGN", "PRIMARY"]:
                continue

            if ref_tokens[0] == "CREATE":
                table_name = ref_tokens[2]
                pk_columns, pk_values, pk_where = pks.get(table_name, ([], [], []))
                assignments = []
                assignment_values = []
                out.write("-- UPDATE for TABLE " + table_name + "\n")
                out.write("-- " + "-" * 80 + "\n")
                continue

            if ref_tokens[0] in pk_columns:
                continue

            assignments.append(ref_tokens[0].lower() + " = %s")
            assignment_values.append("row_mdb." + ref_tokens[0])


# -----------------------------------------------------------------------------
# Generate SQL statements: INSERT & UPDATE.
# -----------------------------------------------------------------------------
def generate_sql() -> None:
    """Generate SQL statements: INSERT & UPDATE.

    The underlying database structures originate from a DDL export of
    RazorSQL.
    """
    reference_filename = (
        io_settings.settings.razorsql_reference_dir
        / io_settings.settings.razorsql_reference_file
    )

    with Path(reference_filename).open(encoding=io_glob.FILE_ENCODING_DEFAULT) as ref:
        ref_lines = ref.readlines()

        _generate_sql_insert(ref_lines)

        _generate_sql_update(ref_lines)
