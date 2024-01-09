First Steps
===========

To get started, you'll first need to clone the repository, which contains essential scripts for various operating systems.
After cloning, you will use these scripts to install the necessary foundational software.
Finally, you will complete the repository-specific installation to set up your environment correctly.
Detailed instructions for each of these steps are provided below.

Cloning the Repository
----------------------

Start by cloning the `io-avstats` repository. This repository contains essential scripts and configurations needed for the project.

.. code-block:: bash

    git clone https://github.com/io-aero/io-avstats

Install Foundational Software
-----------------------------

Once you have successfully cloned the repository, navigate to the cloned directory.
Within the `scripts` folder, you will find scripts tailored for various operating systems.
Proceed with the subsection that corresponds to your operating system for further instructions.

macOS
.....

To set up the project on a macOS system, the following steps should be performed in a terminal window within the repository directory:

a. Grant Execute Permission to Installation Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide execute permissions to the installation scripts:

.. code-block:: bash

    chmod +x scripts/*.zsh

b. Install Python, pip, and pipenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the script to install Python, pip, and pipenv:

.. code-block:: bash

    ./scripts/run_install_python.zsh

c. Install AWS Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute the script to install the AWS CLI:

.. code-block:: bash

    ./scripts/run_install_aws_cli.zsh

d. Install Miniconda and the Correct Python Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following script to install Miniconda and set the right Python version:

.. code-block:: bash

    ./scripts/run_install_miniconda.zsh

e. Install Docker Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~

To install Docker Desktop, run:

.. code-block:: bash

    ./scripts/run_install_docker.zsh

f. Optionally Install DBeaver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If needed, install DBeaver using the following script:

.. code-block:: bash

    ./scripts/run_install_dbeaver.zsh

g. Close the Terminal Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once all installations are complete, close the terminal window.

Ubuntu
.........

To set up the project on an Ubuntu system, the following steps should be performed in a terminal window within the repository directory:

a. Grant Execute Permission to Installation Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide execute permissions to the installation scripts:

.. code-block:: bash

    chmod +x scripts/*.sh

b. Install Python, pip, and pipenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the script to install Python, pip, and pipenv:

.. code-block:: bash

    ./scripts/run_install_python.sh

c. Install AWS Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute the script to install the AWS CLI:

.. code-block:: bash

    ./scripts/run_install_aws_cli.sh

d. Install Miniconda and the Correct Python Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following script to install Miniconda and set the right Python version:

.. code-block:: bash

    ./scripts/run_install_miniconda.sh

e. Install Docker Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~

To install Docker Desktop, run:

.. code-block:: bash

    ./scripts/run_install_docker.sh

f. Optionally Install DBeaver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If needed, install DBeaver using the following script:

.. code-block:: bash

    ./scripts/run_install_dbeaver.sh

g. Close the Terminal Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once all installations are complete, close the terminal window.

Windows 10/11
................

To set up the project on a Windows 10/11 system, the following steps should be performed in a command prompt (cmd) within the repository directory:

a. Install Python, pip, and pipenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the script to install Python, pip, and pipenv:

.. code-block:: bat

    scripts/run_install_python.bat

b. Install AWS Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute the script to install the AWS CLI:

.. code-block:: bat

    scripts/run_install_aws_cli.bat

c. Install Miniconda and the Correct Python Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following script to install Miniconda and set the right Python version:

.. code-block:: bat

    scripts/run_install_miniconda.bat

d. Close the Command Prompt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once all installations are complete, close the command prompt.

e. Install Docker Desktop
~~~~~~~~~~~~~~~~~~~~~~~~~

To install Docker Desktop, download the software from here:

    https://www.docker.com/products/docker-desktop/

and follow the installation instructions.

f. Optionally Install DBeaver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If needed, install DBeaver, download the software from here:

    https://dbeaver.io/

and follow the installation instructions.

Repository-Specific Installation
--------------------------------

After installing the basic software, you need to perform installation steps specific to the `io-avstats` repository.
This involves setting up project-specific dependencies and environment configurations.
To perform the repository-specific installation, the following steps should be performed in a command prompt or a terminal window (depending on the operating system) the repository directory.

Setting Up the Python Environment
.................................

To begin, you'll need to set up the Python environment using Miniconda and Pipenv, both of which are already pre-installed.
You can use the provided Makefile for managing the environment.

a. For **production** use, run the following command:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make conda-prod

b. For **software development**, use the following command:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   make conda-dev

These commands will create and configure a virtual environment for your Python project, ensuring a clean and reproducible development or production environment.
The virtual environment is automatically activated by the Makefile, so you don't need to activate it manually.

System Testing with Unit Tests
..............................

If you have previously executed `make conda-dev`, you can now perform a system test to verify the installation using `make test`.
Follow these steps:

a. Run the System Test:
~~~~~~~~~~~~~~~~~~~~~~~

   Execute the system test using the following command:

   .. code-block:: bash

      make tests

   This command will initiate the system tests using the previously installed components to verify the correctness of your installation.

b. Review the Test Results:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

   After the tests are completed, review the test results in the terminal. Ensure that all tests pass without errors.

   If any tests fail, review the error messages to identify and resolve any issues with your installation.

Running system tests using `make tests` is a valuable step to ensure that your installation is working correctly, and your environment is properly configured for your project.
It helps identify and address any potential problems early in the development process.

Downloading Database Files (Optional)
.....................................

Database files can be downloaded from the IO-Aero Google Drive directory
`io_aero_data/io-xpa/database/io_xpa_db` to your local repository directory `data`.
Before extracting, if a `postgres` directory exists within the `data` directory, it should be deleted.

Follow these steps to manage the database files:

a. Access the IO-Aero Google Drive Directory:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Navigate to the IO-Aero Google Drive and locate the directory `io_aero_data/io-xpa/database/io_xpa_db`.

b. Download Database Files:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the necessary database files from the specified directory to your local repository directory `data`.

c. Delete Existing `postgres` Directory (if present):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a directory named `postgres` already exists within the `data` directory, you should delete it to avoid conflicts.

d. Extract Database Files:
~~~~~~~~~~~~~~~~~~~~~~~~~~

The downloaded database files are in an archive format (ZIP) and should be extracted in the `data` directory.
After completing these steps, the database files should reside in the `data` directory of your local repository and will be ready for use.

Creating the Docker Container with PostgreSQL DB
.................................................

To create the Docker container with PostgreSQL database software, you can use the provided `run_io_avstats` script.
Depending on your operating system, follow the relevant instructions below:

a. macOS (zsh):
~~~~~~~~~~~~~~~

.. code-block:: bash

   ./scripts/run_io_avstats.zsh s_d_c

b. Ubuntu (sh):
~~~~~~~~~~~~~~~

.. code-block:: bash

   ./scripts/run_io_avstats.sh s_d_c

c. Windows 10/11 (cmd):
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: batch

   scripts\run_io_avstats.cmd s_d_c

These commands will initiate the process of creating the Docker container with PostgreSQL database software.

