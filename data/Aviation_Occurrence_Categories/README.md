# IO-AVSTATS - File Directory **`data/Aviation_Occurrence_Categories`**

This file directory contains the necessary files for the processing step:

- `a_o_c` - Load aviation occurrence categories into PostgreSQL

The following parameter in the file **`settings.io_aero.toml`** is used to locate the file: 

- `download_file_aviation_occurrence_categories` = "data/Aviation_Occurrence_Categories/aviation_occurrence_categories.xlsx"

The data source can be found on the NTSB website here:

- [AVIATION OCCURRENCE CATEGORIES - DEFINITIONS AND USAGE NOTES](https://www.ntsb.gov/safety/data/Documents/datafiles/OccurrenceCategoryDefinitions.pdf)

The NTSB provides the data in a `pdf` file which must then be converted to MS Excel format `xlsx` before processing.

The current version is dated 

- October 2013 (4.6).

### Processing

- Data not yet present will be added. 
- An update only takes place if the content of a database column has changed.
- The data in the database table that are no longer present in the MS Excel file are deleted from the database. 
