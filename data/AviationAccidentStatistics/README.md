# IO-AVSTATS - File Directory **`data/AviationAccidentStatistics`**

This file directory contains the necessary files for the processing step:

- `l_n_s` - Load NTSB MS Excel statistic data into PostgreSQL

The following parameter in the file **`settings.io_avstats.toml`** is used to locate the file: 

- `download_directory_aviation_event_statistics` = "data/AviationAccidentStatistics"

The data source can be found on the NTSB website here:

- [2002-2021 Accident Statistics](https://www.ntsb.gov/safety/data/Documents/AviationAccidentStatistics_2002-2021_20221208.xlsx)

The current version is dated 

- 2002-2021.
