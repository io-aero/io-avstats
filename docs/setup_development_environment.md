# 1. Create the repositories

* git clone https://github.com/io-aero/io-avstats
* git clone https://github.com/io-aero/io-avstats-db
* git clone https://github.com/io-aero/io-avstats-db-content

# 2. Setup PyCharm - Plugins

* .ignore
* Json Helper
* Makefile Language
* python-typing-adder
* Database Tools and SQL
* Docker
* IDE Settings Sync
* Settings Repository
* Ini
* Markdown
* Properties
* Shell Script
* YAML
* Windows 10 light Theme
* GitHub Color Scheme
* Git
* GitHub
* Copyright
* EditorConfig
* File Watchers
* Grazie
* HTTP Client
* Shared Project Indices
* Terminal
* Toml

<div style="page-break-after: always;"></div>

# 3. Install Software

# 3.1 Docker Desktop

[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

# 3.2 Make for Windows

[https://gnuwin32.sourceforge.net/packages/make.htm](https://gnuwin32.sourceforge.net/packages/make.htm)

# 3.3 Microsoft Access Database Engine 2016 Redistributable

Important: Microsoft Access, Microsoft Access Database Engine and Python should all be installed either in the 32 bit version or in the 64 bit version!

The installation file can be found in the **`io-avstats-db`** repository under **`resources/Microsoft Access Database Engine 2016 Redistributable`**

# 3.4 PostgreSQL

Important: Use version 15.0

[https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Install only "Command Line Tools" and add the **`bin`** directory of the installation location to the path variable of Windows.

# 3.5 Python

Important: Use version 3.10.8

[https://www.python.org/downloads/](https://www.python.org/downloads/)

# 3.6 RazorSQL

The installation file can be found in the **`io-avstats-db`** repository under **`resources/RazorSQL`**

<div style="page-break-after: always;"></div>

# 3.7 DBeaver (optional) - Universal Database Tool

[https://dbeaver.io](https://dbeaver.io)

# 3.8 AnyDesk (optional) - Remote Desktop Application

[https://anydesk.com/en](https://anydesk.com/en)

# 4. Set up **IO-AVSTATS-DB**

## 4.1 RazorSQL

Create the connection profile IO-AVSTATS in RazorSQL

    RazorSQL: Connections --> Add Connection Profile --> Microsoft Access --> Continuue --> ODBC (Direct)

        Connection Profile Name:   **IO-AVSTATS**
        Database file:             **...\io-avstats-db\data\NTSB\IO-AVSTATS.mdb**

## 4.2 Windows Terminal

Install the Python packages

    make pipenv-dev

Set up the database container

    run_io_avstats_db s_d_c

Create the database schema

    run_io_avstats_db c_d_s

Download Microsoft Access database file

    run_io_avstats_db d_m_a up22oct

Load Microsoft Access database data

    run_io_avstats_db l_m_a up22oct

## 4.3 Docker Desktop

Check that the PostgreSQL development container is running.

## 4.4 DBeaver

Import the io-avstats project settings:

    DBeaver: File --> import --> DBeaver --> Project

        File:  **...\io-avstats\data\DBeaver\io-avstats-....dbp**

Connect to the PostgreSQL development database.

# 5. Set up **IO-AVSTATS-DB-CONTENT**

## 5.1 Google Drive

Download the PostgreSQL database files.

    Shared with me

        22.11.05_postgre_avall.zip

            Dowbload to:   **...\io-avstats-db-content\data**

                Unzip the downloaded file.

## 5.2 Windows Terminal

Install the Python packages

    make pipenv-dev

Set up the database container

    run_io_avstats_db s_d_c

## 5.3 Docker Desktop

Check that the PostgreSQL production container is running.

## 5.4 DBeaver

Connect to the PostgreSQL production database.

# 6. Set up **IO-AVSTATS**

## 6.1 Create the credentials file **`.settings.io_avstats.toml`**

    [default]
    postgres_password="postgresql"
    postgres_password_admin = "postgresql"

## 6.2 Windows Terminal

Install the Python packages

    make pipenv-dev

Run the demo

    run_io_avstats demo
