# Installation

1. Addressing the requirements defined [here](setup_requirements.md){:target="_blank"}. 

2. Clone or copy the **IO-AVSTATS** repository from [here](https://github.com/io-aero/io-avstats){:target="_blank"}.

3. Switch to the file directory **io-avstats**:

    **`cd io-avstats`**

4. Install the necessary Python packages by running the command  **`make pipenv-dev`**.

5. Optionally, adjustments can be made in the following configuration files:

    - **`logging_cfg.yaml`**: for the logging functionality
    - **`settings.io_aero.toml`**: for the **IO-AVSTATS** application
 
6. Download the current database files from [here](https://drive.google.com/drive/folders/1E2X__35iujWQvXQfLrvwYbiMCwAaLE53?usp=drive_link){:target="_blank"} to the file directory `data`. 

7. Unpack the downloaded database file in the `data` file directory. The result should be a subdirectory `postgres` with the database files.

8. Use the script **`run_io_avstats`** with the task `s_d_c` to create a Docker container with the PostgreSQL database software.

9. Use the script **`run_io_avstats`** with the task `r_s_a` to run the application.
