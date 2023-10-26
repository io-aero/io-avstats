# Installation

1. Install the software components specified in the requirements.


    In an Ubuntu environment, the following scripts from the `scripts` 
    directory can be used for this purpose:

    - run_install_4_vm_wsl2_1.sh
    - run_install_4_vm_wsl2_2.sh


2. Configure the AWS CLI:

    - `AWS Access Key ID:     ...`
    - `AWS Secret Access Key: ...`
    - `Default region name:   ...`
    - `Default output form:`


3. Clone or copy the **IO-AVSTATS** repository from [here](https://github.com/io-aero/io-avstats){:target="_blank"}.


4. Switch to the file directory **io-avstats**:

    - **`cd io-avstats`**


5. Install the necessary Python packages by running the command  **`make pipenv-dev`**.


6. Optionally, adjustments can be made in the following configuration files:

    - **`logging_cfg.yaml`**: for the logging functionality
    - **`settings.io_aero.toml`**: for the **IO-AVSTATS** application
 

7. Download the current database files from [here](https://drive.google.com/drive/folders/1E2X__35iujWQvXQfLrvwYbiMCwAaLE53?usp=drive_link){:target="_blank"} to the file directory `data`. 


8. Unpack the downloaded database file in the `data` file directory. The result should be a subdirectory `postgres` with the database files.


9. Use the script **`run_io_avstats`** with the task `s_d_c` to create a Docker container with the PostgreSQL database software.


10. Use the script **`run_io_avstats`** with the task `r_s_a` to run the application.


11. Optional: Import the project file in the directory `data/DBeaver` as a project in DBeaver.
