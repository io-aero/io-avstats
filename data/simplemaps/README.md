# IO-AVSTATS - File Directory **`data/simplemaps`**

This file directory contains the necessary files for the processing step:

- `l_s_d` - Load simplemaps data into PostgreSQL

The following parameters in the file **`settings.io_avstats.toml`** is used to locate the files: 

- `download_file_simplemaps_us_cities_xlsx` = "data/simplemaps/uscities.xlsx"
- `download_file_simplemaps_us_zips_xlsx` = "data/simplemaps/uszips.xlsx"

The data sources can be found on the simplemaps website here:

- [United States Cities Database](https://simplemaps.com/data/us-cities)
- [US Zip Codes Database](https://simplemaps.com/data/us-zips)

The FAA provides the data in a `csv` file which must then be converted to MS Excel format `xlsx` before processing.

The current versions are dated 

- January 31, 2023 (United States Cities Database),
- February 13, 2023 (US Zip Codes Database).

### Processing:

Data from the **simplemaps** flat files **`uscities.xlsx`** and **`uszips.xlsx`** is loaded into a PostgreSQL database using the following processing logic:

1. the existing data with column **`source`** equal to **`simplemaps United States Cities Database`** or **`simplemaps US Zip Codes Database`** are deleted,

2. the database **`United States Cities`** is processed, whereby for each zip code in the column **`zips`** an entry in the PostgreSQL table **`io_lat_lng`** is created (not updated) - as latitude and longitude the corresponding values of the affected city are used, with column **`type`** equal to **`ZIPCODE`** and column **`source`** equal to **`simplemaps United States Cities Database`**,

3. the database **`US Zip Codes`** is processed, whereby for each zip code an entry in the PostgreSQL table **`io_lat_lng`** is created or updated with column **`type`** equal to **`ZIPCODE`** and column **`source`** equal to **`simplemaps US Zip Codes Database`**,

4. the database **`United States Cities`** is processed, whereby for each city an entry in the PostgreSQL table **`io_lat_lng`** is created or updated with column **`type`** equal to **`CITY`** and column **`source`** equal to **`simplemaps United States Cities Database`**,

5. the existing rows of the database table **`io_lat_lng`** with column **`source`** equal to **`average`** are deleted,

6. from the lines of the database table **`io_lat_lng`** of **`type`** **`ZIPCODE`** the average of latitude and longitude per city is determined and this value is stored as latitude and longitude of this city in the database table **`io_lat_lng`** with **`source`** equal to **`average`**.   
