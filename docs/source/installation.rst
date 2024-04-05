============
Installation
============

Python
------

The project repository contains a ``scripts`` directory that includes operating system-specific installation scripts for Python, ensuring a smooth setup across various environments.

- **macOS**: For users on macOS, the ``run_install_python.zsh`` script is provided. This zsh script is created to operate within the default shell environment of macOS, facilitating the Python installation process.

- **Ubuntu**: For users on Ubuntu, the ``run_install_python.sh`` script is provided. This Bash script is created to operate within the default shell environment of Ubuntu, facilitating the Python installation process.

- **Windows**: The ``run_install_python.bat`` script is tailored for users on Windows systems. It is designed to be run in the Command Prompt and automates the Python installation process on Windows.

These scripts are named according to the convention ``run_install_python.<ext>``, where ``<ext>`` corresponds to the script extension appropriate for the target operating system and shell environment (e.g. `.zsh` for macOS zsh, `.sh` for Ubuntu Bash or `.bat` for Windows). Users are recommended to execute the script matching their OS to ensure an efficient Python setup.


Docker Desktop
--------------

The ``scripts`` directory contains scripts that assist with installing Docker Desktop on Ubuntu, facilitating an automated and streamlined setup.

- **macOS**: The ``run_install_docker.zsh`` script is available for macOS users. This zsh script sets up Docker Desktop on Ubuntu systems by configuring the necessary repositories and managing the installation steps through the system's package manager.

- **Ubuntu**: The ``run_install_docker.sh`` script is available for Ubuntu users. This Bash script sets up Docker Desktop on Ubuntu systems by configuring the necessary repositories and managing the installation steps through the system's package manager.

- **Windows**: For Windows users, it is recommended to download and install Docker Desktop using the traditional installer available at `Docker Desktop for Windows <https://www.docker.com/products/docker-desktop>`_. This approach guarantees the most stable version and is tailored to integrate seamlessly with Windows-specific features and configurations.

Please select and execute the appropriate script for your operating system from the ``scripts`` directory. Windows users should follow the provided link to obtain the official installer for a guided installation experience.

MS Access Database Engine
-------------------------

- **Windows**: The software can be downloaded from `here <https://www.microsoft.com/en-us/download/details.aspx?id=54920>`__\  and then installed according to the instructions provided.

DBeaver - optional
------------------

DBeaver is an optional but highly recommended tool for this software as it offers a user-friendly interface to gain insights into the database internals. The project provides convenient scripts for installing DBeaver on Ubuntu.

- **Ubuntu**: For Ubuntu users, the ``run_install_dbeaver.sh`` script facilitates the installation of DBeaver. This Bash script automates the setup process, adding necessary repositories and handling the installation seamlessly.

- **Windows**: Windows users are advised to download and install DBeaver using the official installer from the DBeaver website at `DBeaver Download <https://dbeaver.io/download/>`_. The installer ensures that DBeaver is properly configured and optimized for Windows environments.

To install DBeaver, locate the appropriate script in the ``scripts`` directory for Ubuntu. If you're a Windows user, please use the provided link to access the official installer for an intuitive installation experience.

Python Libraries
----------------

The project's Python dependencies are managed partly through Conda and partly through pip/pipenv. To facilitate a straightforward installation process, a Makefile is provided at the root of the project.

- **Development Environment**: Run the command ``make conda-dev`` from the terminal to set up a development environment. This will install the necessary Python libraries using Conda and pip/pipenv as specified for development purposes.

- **Production Environment**: Execute the command ``make conda-prod`` for preparing a production environment. It ensures that all the required dependencies are installed following the configurations optimized for production deployment.

The Makefile targets abstract away the complexity of managing multiple package managers and streamline the environment setup. It is crucial to have both Conda and the appropriate pip tools available in your system's PATH to utilize the Makefile commands successfully.




