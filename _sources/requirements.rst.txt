============
Requirements
============

The required software is listed below. Regarding the corresponding
software versions, you will find the detailed information in the
`Release Notes <https://github.com/io-aero/io-avstats/blob/main/docs/release_notes.md>`__\.

Operating System
------------------

Continuous delivery / integration (CD/CI) runs on Ubuntu and development is also done with macOS and Windows 10/11.

The installation of Homebrew is required for macOS. If necessary, Homebrew can be installed with the following command:

.. code-block::

   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

For the Windows operating systems, only additional the functionality of the ``make`` tool must be made available, e.g. via
`Make for Windows <http://gnuwin32.sourceforge.net/packages/make.htm>`__\

The command-line shells supported are:

.. list-table::
   :widths: 16 21
   :header-rows: 1

   * - Operating system
     - Command-line shell(s)
   * - macOS
     - zsh
   * - Ubuntu
     - bash
   * - Windows 10/11
     - cmd and PowerShell

For macOS and Ubuntu, the end-of-line character and the execution authorization may need to be adjusted for the shell scripts.
If the ``dos2Unix`` program is installed, the necessary adjustments can be made using the scripts ``./scripts/run_prep_zsh_scripts.zsh`` (macOS) or ``./scripts/run_prep_bash_scripts.sh`` (Ubuntu).

`Python <https://docs.python.org/3/whatsnew/3.11.html>`__\
----------------------------------------------------------

This project utilizes Python 3.10, which introduces significant enhancements in type hinting and type annotations.
These improvements provide a more robust and clear definition of function parameters, return types, and variable types, contributing to improved code readability and maintainability.
The use of Python 3.10 ensures compatibility with these advanced typing features, offering a more structured and error-resistant development environment.

`AWS Command Line Interface <https://aws.amazon.com/cli/>`__\
-------------------------------------------------------------

The AWS CLI is employed in this project to facilitate access to private Python libraries hosted on Amazon CodeArtifact, a fully managed artifact repository service.
This integration allows for seamless retrieval and management of project dependencies, ensuring a streamlined and secure development workflow.
Utilizing the AWS CLI ensures efficient and reliable access to the necessary Python libraries, enhancing the overall build and deployment process within the AWS ecosystem.

`Docker Desktop <https://www.docker.com/products/docker-desktop/>`__\
---------------------------------------------------------------------

The project employs PostgreSQL for data storage and leverages Docker images provided by PostgreSQL to simplify the installation process.
Docker Desktop is used for its ease of managing and running containerized applications, allowing for a consistent and isolated environment for PostgreSQL.
This approach streamlines the setup, ensuring that the database environment is quickly replicable and maintainable across different development setups.

`MS Access Database Engine <https://www.microsoft.com/en-us/download/details.aspx?id=54920>`__\
-----------------------------------------------------------------------------------------------

This Software consists of a set of components that facilitate the transfer of data between existing Microsoft Office files such as Microsoft Office Access (``*.mdb`` and ``*.accdb``) files and Microsoft Office Excel (``*.xls``, ``*.xlsx``, and ``*.xlsb``) files to other data sources.
Connectivity to existing text files is also supported.

`DBeaver Community <https://dbeaver.io>`__\  - optional
-------------------------------------------------------

DBeaver is recommended as the user interface for interacting with the PostgreSQL database due to its comprehensive and user-friendly features.
It provides a flexible and intuitive platform for database management, supporting a wide range of database functionalities including SQL scripting, data visualization, and import/export capabilities.
Additionally, the project includes predefined connection configurations for DBeaver, facilitating a hassle-free and streamlined setup process for users.
