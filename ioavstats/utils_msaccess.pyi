import pyodbc

from ioavstats import glob_local as glob_local

def get_msaccess_cursor(filename: str) -> tuple[pyodbc.Connection, pyodbc.Cursor]: ...
