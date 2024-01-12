=========================
PostgreSQL Administration
=========================

**IO-AVSTATS** uses the `PostgreSQL DBMS <https://www.postgresql.org>`_ for data management.
PostgreSQL is a very powerful relational database system where the SQL language can be extended by procedural add-ons like `PL/pgSQL <https://www.postgresql.org/docs/current/plpgsql.html>`_ or `PL/Python <https://www.postgresql.org/docs/current/plpython.html>`_.

**IO-AVSTATS** provides all the tools to import the data from the MS Access databases available on the `**NTSB** <https://data.ntsb.gov/avdata>`_ website and the data from the basic flat files available on **simplemaps** `United States Cities Database <https://simplemaps.com/data/us-cities>`_ and `US Zip Codes Database <https://simplemaps.com/data/us-zips>`_ websites.

Docker
======

The PostgreSQL Docker community provides PostgreSQL images suitable for **IO-AVSTATS** on `DockerHub <https://hub.docker.com>`_.
The official image can be found `here <https://hub.docker.com/_/postgres>`_.
The `c_d_l` task available in the `run_io_avstats_db` script downloads a selected PostgreSQL DBMS image from DockerHub and creates, configures and starts a Docker container.

Parameterization
================

The parameters can be defined either via environment variables or in the `settings.io_aero.toml` file.
Details can be found under `Configuration` and `IO-AVSTATS`.

The following parameters are used when downloading the Docker image and creating the Docker container:

- ``postgres_connection_port`` - the database IP address
- ``postgres_container_name`` - the container name
- ``postgres_dbname_admin`` - the administration database name
- ``postgres_password_admin`` - the administration database password
- ``postgres_pgdata`` - the file directory on the host for the database files
- ``postgres_user_admin`` - the administration database username
- ``postgres_version`` - the requested PostgreSQL version from DockerHub

When using environment variables, they must contain the prefix ``IO_AERO_``, e.g., ``IO_AERO_POSTGRES_USER``.

Backup & Restore
================

Since the **IO-AVSTATS** database contains only statistical data, it is subject to a relatively low frequency of change.
The following three events can lead to a change in the **IO-AVSTATS** database:

1. a new change file on the **NTSB** download site, or
2. an evolution of the database software or schema, or
3. a new PostgreSQL version that requires database migration.

This does not require sophisticated methods for backing up and restoring the **IO-AVSTATS** database, especially since the database contents reside in a dedicated local file directory.
For data backup it is therefore sufficient to create a copy of the file directory with the **IO-AVSTATS** database before a change event.
This copy can then replace the corrupted **IO-AVSTATS** database in the event of an error.

**Very important**: before any backup or restore, the PostgreSQL Docker container must be stopped first!
