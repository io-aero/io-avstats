# IO-AVSTATS - Installation

1. Clone or copy the **IO-AVSTATS** repository from [here](https://github.com/io-aero/io-avstats){:target="_blank"}.

2. Switch to the file directory **io-avstats**:

    **`cd io-avstats`**

3. Install the necessary Python packages by running the command  **`make pipenv-dev`**.

4. Optionally, adjustments can be made in the following configuration files:

    - **`logging_cfg.yaml`**: for the logging functionality
    - **`settings.io_avstats.toml`**: for the **IO-AVSTATS** application
 
5. Create the configuration file **`.settings.io_avstats.toml`** with the passwords for the PostgreSQL database users.
 
6. Use the **IO-AVSTATS** application by running the script **`run_io_avstats.bat`**.
