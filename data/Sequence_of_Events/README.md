# IO-AVSTATS - File Directory **`data/Sequence_of_Events`**

This file directory contains the necessary files for the processing step:

- `l_s_e` - Load sequence of events data into PostgreSQL

The following parameter in the file **`settings.io_aero.toml`** is used to locate the file: 

- `download_file_sequence_of_events` = "data/Sequence_of_Events/CICTT_SOE_MAP.csv"

The data come directly from the NTSB.

### Processing

Loads the data from the csv file according to the configuration parameter `download_file_sequence_of_events` into the database table `io_sequence_of_events`.

- Data not yet present will be added. 
- An update only takes place if the content of a database column has changed.
- The data in the database table that are no longer present in the MS Excel file are deleted from the database. 

