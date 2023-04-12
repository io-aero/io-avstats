# IO-AVSTATS - File Directory **`data/United States Zip Codes.org`**

This file directory contains the necessary files for the processing step:

- `l_z_d` - Load ZIP Code Database data into PostgreSQL

The following parameter in the file **`settings.io_avstats.toml`** is used to locate the file: 

- `download_file_zip_codes_org_xlsx` = "data/United States Zip Codes.org/zip_code_database.xlsx"

The data source can be found on the FAA website here:

- [ZIP Code Database](https://www.unitedstateszipcodes.org/zip-code-database/)

The United States Zip Codes.org provides the data in a `csv` and `xlsx` format.

The current version is dated 

- no information available.

### Processing

Data from the **Zip Codes.org** flat file **`zip_code_database.xls`** is loaded into a PostgreSQL database using the following processing logic:

1. the existing data with column **`source`** equal to **`Zip Codes.org ZIP Code Database`** are deleted,

2. the Excel rows of **`type`** equals **`STANDARD`** and **`country`** equals **`US`** are inserted or updated in the database table **`io_lat_lng`** with column **`source`** equal to **`Zip Codes.org ZIP Code Database`**,

3. the existing rows of the database table **`io_lat_lng`** with column **`source`** equal to **`average`** are deleted,

4. from the lines of the database table **`io_lat_lng`** of **`type`** **`ZIPCODE`** the average of latitude and longitude per city is determined and this value is stored as latitude and longitude of this city in the database table **`io_lat_lng`** with **`source`** equal to **`average`**.   

```
      type   |source                                  |count|
      -------+----------------------------------------+-----+
      CITY   |average                                 |14392|
      CITY   |simplemaps United States Cities Database|30351|
      ZIPCODE|simplemaps United States Cities Database|14235|
      ZIPCODE|simplemaps US Zip Codes Database        |33784|
      ZIPCODE|Zip Codes.org ZIP Code Database         |13367|
```
