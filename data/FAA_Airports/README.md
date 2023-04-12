# IO-AVSTATS - File Directory **`data/FAA_Airports`**

This file directory contains the necessary files for the processing step:

- `l_a_p` - Load airport data into PostgreSQL

The following parameter in the file **`settings.io_avstats.toml`** is used to locate the file: 

- `download_file_faa_airports_xlsx` = "data/FAA_Airports/Airports.xlsx"

The data source can be found on the FAA website here:

- [FAA Airports](https://adds-faa.opendata.arcgis.com/datasets/faa::airports-1/explore?location=0.158824%2C-1.633886%2C2.00)

The FAA provides the data in a `csv` file which must then be converted to MS Excel format `xlsx` before processing.

The current version is dated 

- February 23, 2023.