# IO-AVSTATS - File Directory **`data/FAA_Airports`**

This file directory contains the necessary files for the processing step:

- `l_a_p` - Load airport data into PostgreSQL

The following parameters in the file **`settings.io_avstats.toml`** are used to locate the files: 

- `download_file_faa_airports_xlsx` = "data/FAA_Airports/Airports.xlsx"
- `download_file_faa_npias_xlsx` = "data/FAA_Airports/NPIAS-2023-2027-Appendix-A.xlsx"
- `download_file_faa_runways_xlsx` = "data/FAA_Airports/Runways.xlsx"

The data sources can be found on the FAA website here:

- [FAA Airports](https://adds-faa.opendata.arcgis.com/datasets/faa::airports-1/explore?location=0.158824%2C-1.633886%2C2.00)
- [FAA Runways](https://adds-faa.opendata.arcgis.com/datasets/faa::runways/explore?location=0.059024%2C-1.628764%2C2.00)
- [NPIAS 2023-2027](https://www.faa.gov/airports/planning_capacity/npias/current/2023_NPIAS_Appendix_A)

The FAA provides the data in a `csv` file which must then be converted to MS Excel format `xlsx` before processing.

The current version is dated 

- April 20, 2023.