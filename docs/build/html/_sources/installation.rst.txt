Installation
============

Python
------

The project repository contains a ``scripts`` directory that includes operating system-specific installation scripts for Python, ensuring a smooth setup across various environments.

- **macOS**: The ``run_install_python.zsh`` script is available for macOS users. This script is adapted for the Zsh shell, which is the standard shell on recent versions of macOS, and it streamlines the Python installation.

- **Ubuntu**: For users on Ubuntu, the ``run_install_python.sh`` script is provided. This Bash script is created to operate within the default shell environment of Ubuntu, facilitating the Python installation process.

- **Windows**: The ``run_install_python.bat`` script is tailored for users on Windows systems. It is designed to be run in the Command Prompt and automates the Python installation process on Windows.

These scripts are named according to the convention ``run_install_python.<ext>``, where ``<ext>`` corresponds to the script extension appropriate for the target operating system and shell environment (e.g., `.bat` for Windows, `.sh` for Ubuntu Bash, `.zsh` for macOS Zsh). Users are recommended to execute the script matching their OS to ensure an efficient Python setup.

AWS Command Line Interface
--------------------------

Within the project's ``scripts`` directory, you will find a set of scripts specifically designed for the installation of the AWS Command Line Interface (AWS CLI). These scripts facilitate the installation process on different operating systems, ensuring a consistent and reliable setup.

- **macOS**: For macOS users, the ``run_install_aws_cli.zsh`` script is provided. Designed for the Zsh shell, this script streamlines the AWS CLI installation process on macOS by leveraging the Homebrew package manager.

- **Ubuntu**: Ubuntu users should utilize the ``run_install_aws_cli.sh`` script. This script is a Bash script that simplifies the AWS CLI installation on Ubuntu systems by setting up the necessary repositories and installing the CLI via apt-get.

- **Windows**: The ``run_install_aws_cli.bat`` script is intended for Windows users. It automates the process of downloading and installing the latest version of the AWS CLI in the Windows Command Prompt environment.

Each script is named following the pattern ``run_install_aws_cli.<ext>``, with ``<ext>`` being the respective script extension suitable for the target operating system and shell environment (e.g., `.bat` for Windows CMD, `.sh` for Ubuntu Bash, `.zsh` for macOS Zsh). Users are advised to execute the corresponding script for their operating system to achieve an optimal AWS CLI installation experience.

Miniconda
---------

The ``scripts`` directory includes a collection of operating system-specific scripts named ``run_install_miniconda`` to streamline the installation of Miniconda. These scripts are designed to cater to the needs of different environments, making the setup process efficient and user-friendly.

- **Windows CMD Shell**: The ``run_install_miniconda.bat`` script is tailored for the Windows CMD shell. It automates the Miniconda installation process on Windows, providing a hassle-free setup with a simple double-click or command line execution.

- **Ubuntu Bash Shell**: Ubuntu users can take advantage of the ``run_install_miniconda.sh`` script. This Bash script is intended for use within the Ubuntu terminal, encapsulating the necessary commands to install Miniconda seamlessly on Ubuntu systems.

- **macOS Zsh Shell**: For macOS, the ``run_install_miniconda.zsh`` script is available. It is optimized for the Zsh shell, which is the default on recent versions of macOS. This script simplifies the installation and configuration of Miniconda, ensuring a smooth integration with macOS.

Each script in the ``scripts`` directory is named to reflect its compatibility with the corresponding operating system and shell environment. Users are encouraged to execute the script that matches their OS for a smooth and error-free Miniconda installation experience.

Docker Desktop
--------------

The ``scripts`` directory contains scripts that assist with installing Docker Desktop on macOS and Ubuntu, facilitating an automated and streamlined setup.

- **macOS**: The ``run_install_docker.zsh`` script is designed for macOS users. By utilizing this Zsh script, the installation of Docker Desktop on macOS is executed through a series of automated steps, which are managed by the script to ensure a smooth installation process.

- **Ubuntu**: The ``run_install_docker.sh`` script is available for Ubuntu users. This Bash script sets up Docker Desktop on Ubuntu systems by configuring the necessary repositories and managing the installation steps through the system's package manager.

- **Windows**: For Windows users, it is recommended to download and install Docker Desktop using the traditional installer available at `Docker Desktop for Windows <https://www.docker.com/products/docker-desktop>`_. This approach guarantees the most stable version and is tailored to integrate seamlessly with Windows-specific features and configurations.

Please select and execute the appropriate script for your operating system from the ``scripts`` directory. Windows users should follow the provided link to obtain the official installer for a guided installation experience.

DBeaver - optional
------------------

DBeaver is an optional but highly recommended tool for this software as it offers a user-friendly interface to gain insights into the database internals. The project provides convenient scripts for installing DBeaver on macOS and Ubuntu.

- **macOS**: The ``run_install_dbeaver.zsh`` script is crafted for macOS systems. By running this Zsh script, users can easily install DBeaver and quickly connect to the database for management and querying tasks.

- **Ubuntu**: For Ubuntu users, the ``run_install_dbeaver.sh`` script facilitates the installation of DBeaver. This Bash script automates the setup process, adding necessary repositories and handling the installation seamlessly.

- **Windows**: Windows users are advised to download and install DBeaver using the official installer from the DBeaver website at `DBeaver Download <https://dbeaver.io/download/>`_. The installer ensures that DBeaver is properly configured and optimized for Windows environments.

To install DBeaver, locate the appropriate script in the ``scripts`` directory for macOS or Ubuntu. If you're a Windows user, please use the provided link to access the official installer for an intuitive installation experience.

Python Libraries
----------------

The project's Python dependencies are managed partly through Conda and partly through pip/pipenv. To facilitate a straightforward installation process, a Makefile is provided at the root of the project.

- **Development Environment**: Run the command ``make conda-dev`` from the terminal to set up a development environment. This will install the necessary Python libraries using Conda and pip/pipenv as specified for development purposes.

- **Production Environment**: Execute the command ``make conda-prod`` for preparing a production environment. It ensures that all the required dependencies are installed following the configurations optimized for production deployment.

The Makefile targets abstract away the complexity of managing multiple package managers and streamline the environment setup. It is crucial to have both Conda and the appropriate pip tools available in your system's PATH to utilize the Makefile commands successfully.




