# How to add NTSB accident files

Aviation accident data provided by **NTSB** can be found at the following [website](https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx){:target="_blank"} under **Downloadable data sets**:

<kbd>![](img/how_to_add_ntsb_01.png)</kbd>

**NTSB** provides update databases every month on the 1st, 8th 15th, and 22nd. 
In addition, an up-to-date **avall** database is provided on the first of every month.

In the database table **`io_processed_files`** you can find the files already processed by **IO-Aero**:

<kbd>![](img/io_processed_files.png)</kbd>

Any file provided by **NTSB** can be processed several times with the process described in the following, as long as one processes also afterwards all newer files again.

All necessary processing steps can be executed with the **`run_io_avstats`** script.
The script is available in a version for Windows 10 and 11 cmd and for Ubuntu 22.04 bash shell.

## 1. Quick reference

The following processing steps are performed only on the first of each month:

| No. | Task  | Description                                                    |
|----:|-------|----------------------------------------------------------------|
|   1 | d_s_f | Download basic simplemaps files                                |
|   2 | l_s_d | **Optional**: Load simplemaps data into PostgreSQL             |
|   3 |       | Download the ZIP Code Database file                            |
|   4 | l_z_d | **Optional**: Load ZIP Code Database data into PostgreSQL      |
|   5 | l_c_d | **Optional**: Load data from a correction file into PostgreSQL |

The following processing steps are performed on each of the change files delivered on the 1st, 8th, 15th and 22nd:

|  No. | Task  | Description                                       |
|-----:|-------|---------------------------------------------------|
| 11.0 | u_p_d | Download a NTSB MS Access database file           |
| 11.1 |       | Load NTSB MS Access database data into PostgreSQL |
| 11.2 |       | Correct decimal US latitudes and longitudes       |
| 11.3 |       | Verify selected NTSB data                         |
| 11.4 |       | Refresh the PostgreSQL database schema            |
| 11.5 |       | Optional data quality checks                      |

The following steps are used to back up and to update the database in the cloud:

| No. | Task  | Description                                   |
|----:|-------|-----------------------------------------------|
|  21 |       | Backup the file directory **`data/postgres`** |
|  22 |       | Update the Google Drive                       |
|  23 | c_f_z | Zip the files for the cloud                   |

## 2. Detailed description

### No. 1 - **`d_s_f`** - Download basic simplemaps files

**Relevant configuration parameters**:

```
download_chunk_size = 524288
download_timeout = 10
download_file_simplemaps_us_cities_xlsx = "uscities.xlsx"
download_file_simplemaps_us_cities_zip = "simplemaps_uscities_basicv1.75.zip"
download_file_simplemaps_us_zips_xlsx = "uszips.xlsx"
download_file_simplemaps_us_zips_zip = "simplemaps_uszips_basicv1.81.zip"
download_work_dir = "data/download"
```

**Example protocol**:

```
...\io-avstats>run_io_avstats
Progress update 2023-01-12 08:52:58.915135 : ===============================================================================.
Progress update 2023-01-12 08:52:58.915635 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 08:52:58.917636 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 08:52:58.925635 : INFO.00.005 Argument task='d_s_f'.
Progress update 2023-01-12 08:52:58.925635 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:52:58.926135 : INFO.00.048 Downloading basic simplemaps files.
Progress update 2023-01-12 08:52:58.926135 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:52:59.124166 : INFO.00.030 The connection to the US city file 'simplemaps_uscities_basicv1.75.zip' on the simplemaps download page was successfully established.
Progress update 2023-01-12 08:52:59.625371 : INFO.00.023 From the file 'simplemaps_uscities_basicv1.75.zip' 8 chunks were downloaded.
Progress update 2023-01-12 08:52:59.658871 : INFO.00.024 The file 'simplemaps_uscities_basicv1.75.zip' was successfully unpacked.
Progress update 2023-01-12 08:52:59.736875 : INFO.00.022 The connection to the US zip code file 'simplemaps_uszips_basicv1.81.zip' on the simplemaps download page was successfully established.
Progress update 2023-01-12 08:52:59.838506 : INFO.00.023 From the file 'simplemaps_uszips_basicv1.81.zip' 8 chunks were downloaded.
Progress update 2023-01-12 08:52:59.872006 : INFO.00.024 The file 'simplemaps_uszips_basicv1.81.zip' was successfully unpacked.
Progress update 2023-01-12 08:52:59.872506 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:52:59.872506 :        1,075,371,000 ns - Total time launcher.
Progress update 2023-01-12 08:52:59.872506 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 08:52:59.872506 : ===============================================================================.
```

The downloaded files **`uscities.csv`** and **`uszips.xlsx`** must be checked with the reference files in the file directory **`data/reference`** for a match.
If there is no mismatch, then the next step can be skipped.

### No. 2 - **`l_s_d`** - Load simplemaps data into PostgreSQL

Only necessary if the file downloaded in the previous step contains changes.

TODO

**Relevant configuration parameters**:

```
download_work_dir = "data/download"
```

**Example protocol**:

```
TODO
```

### No.3 - Download the ZIP Code Database file

The **`Personal Free`** version of the ZIP Code Database file must be downloaded manually from the **`https://www.unitedstateszipcodes.org/zip-code-database/`** website to the file directory according to the **`download_work_dir`** configuration parameter.

<kbd>![](img/Zip Codes.org Verify License Terms.png)</kbd>

The two formats **`Excel Format (data only)`** and **`CSV Format`** must be downloaded one after the other.
The downloaded file **`zip_code_database.csv`** must be checked with the reference files in the file directory **`data/reference`** for a match.
If there is no mismatch, then the next step can be skipped.

**Relevant configuration parameters**:

```
download_work_dir = "data/download"
```

### No. 4 - **`l_z_d`** - Load ZIP Code Database data into PostgreSQL

Only necessary if the file downloaded in the previous step contains changes.

TODO

**Relevant configuration parameters**:

```
download_work_dir = "data/download"
```

**Example protocol**:

```
TODO
```

### No. 5 -  **`l_c_d`** - Load data from a correction file into PostgreSQL

This step only needs to be performed if modified or new correction files are available.

**Relevant configuration parameters**:

```
correction_work_dir = "data/correction"
```

**Example protocol**:

```
TODO
```

### No. 11.1 - **`d_n_a`** - Download a NTSB MS Access database file

The execution protocol for the entire step 11 is available [here](https://io-aero.github.io/io-avstats-shared/){:target="_blank"} under: **Applications** - **Update Log Files**

**Relevant configuration parameters**:

```
download_chunk_size = 524288
download_timeout = 10
download_url_ntsb_prefix = "https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5C"
download_work_dir = "data/download"
```

### No. 11.2 - **`l_n_a`** - Load NTSB MS Access database data into PostgreSQL

**Relevant configuration parameters**:

```
download_work_dir = "data/download"
```

### No. 11.3 - **`c_l_l`** - Correct decimal US latitudes and longitudes

### No. 11.4 - **`v_n_d`** - Verify selected NTSB data

**Relevant configuration parameters**:

```
max_deviation_latitude = 0.01
max_deviation_longitude = 0.01
```

### No. 11.5 - **`r_d_s`** - Refresh the PostgreSQL database schema

### Optional data quality check: Event completeness

**Query**:

```sql92
SELECT count(*) "Count",
       'Events Total' "Description"
  FROM events e
 UNION
SELECT count(*) ,
       'Events Total with Fatalities'
  FROM events e
 WHERE inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US'
  FROM events e
 WHERE ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities'
  FROM events e
 WHERE inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) "Count",
       'Events Total since 1982' "Description"
  FROM events e
 WHERE ev_year >= 1982
 UNION
SELECT count(*) ,
       'Events Total with Fatalities since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) "Count",
       'Events Total since 2008' "Description"
  FROM events e
 WHERE ev_year >= 2008
 UNION
SELECT count(*) ,
       'Events Total with Fatalities since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 ORDER BY 2
```

**Results**:

```
Count|Description                            |
-----+---------------------------------------+
88137|Events Total                           |
88130|Events Total since 1982                |
25101|Events Total since 2008                |
17585|Events Total with Fatalities           |
17579|Events Total with Fatalities since 1982|
 5269|Events Total with Fatalities since 2008|
81137|Events US                              |
81130|Events US since 1982                   |
20780|Events US since 2008                   |
14695|Events US with Fatalities              |
14689|Events US with Fatalities since 1982   |
 3507|Events US with Fatalities since 2008   | 
```

### Optional data quality check: Latitude &longitude

**Query Total:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                                                                                                                         |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  510|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                           |
 4087|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
  585|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                                                              |
    5|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                      |
    4|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                      |
   13|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                                                         |
   14|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                                                         |
    8|ERROR.00.922 Invalid US state id & INFO.00.033 Correction based on US zip code                                                                                                                                                                                 |
    3|ERROR.00.922 Invalid US state id & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
   91|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                      |
    1|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00|
    2|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                              |
42684|INFO.00.033 Correction based on US zip code                                                                                                                                                                                                                    |
 1293|INFO.00.034 Correction based on US state and city                                                                                                                                                                                                              |
10959|INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                                                         |
  101|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string                                                                                                                                                                  |
    4|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                   |
   64|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & INFO.00.033 Correction based on US zip code                                                                            |
  123|INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                                                                 |  
```

**Query Total since 1982:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE ev_year >= 1982
   AND io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                                                                                                                         |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  510|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                           |
 4087|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
  585|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                                                              |
    5|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                      |
    4|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                      |
   13|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                                                         |
   14|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                                                         |
    8|ERROR.00.922 Invalid US state id & INFO.00.033 Correction based on US zip code                                                                                                                                                                                 |
    3|ERROR.00.922 Invalid US state id & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
   91|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                      |
    1|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00|
    2|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                              |
42680|INFO.00.033 Correction based on US zip code                                                                                                                                                                                                                    |
 1292|INFO.00.034 Correction based on US state and city                                                                                                                                                                                                              |
10957|INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                                                         |
  101|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string                                                                                                                                                                  |
    4|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                   |
   64|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & INFO.00.033 Correction based on US zip code                                                                            |
  123|INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                                                                 |  
```

**Query Total since 2008:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE ev_year >= 2008
   AND io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                   |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------+
    1|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                     |
    6|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                     |
    5|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                        |
    1|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country|
    7|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country   |
   10|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                   |
   13|INFO.00.033 Correction based on US zip code                                                                                                              |
   33|INFO.00.034 Correction based on US state and city                                                                                                        |   
```

### Optional data quality check: Issue summary

**Query Total:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
Count|Description              |
-----+-------------------------+
 3807|Invalid Latitude         |
 4131|Invalid Longitude        |
 6042|Invalid US City          |
16531|Invalid US City & Zipcode|
  290|Invalid US State         |
 6039|Invalid US Zipcode       |
 3726|Latitude deviation       |
 3655|Longitude deviation      | 
```

**Query US until 2008:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE ev_year < 2008 
   AND io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE ev_year < 2008 
   AND io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
Count|Description              |
-----+-------------------------+
  172|Invalid Latitude         |
  196|Invalid Longitude        |
 4851|Invalid US City          |
12421|Invalid US City & Zipcode|
  123|Invalid US State         |
 5113|Invalid US Zipcode       |
    1|Latitude deviation       |
    0|Longitude deviation      |    
```

**Query US Accidents since 2008:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE ev_year >= 2008 
   AND io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
Count|Description              |
-----+-------------------------+
 3635|Invalid Latitude         |
 3935|Invalid Longitude        |
 1191|Invalid US City          |
 4110|Invalid US City & Zipcode|
  167|Invalid US State         |
  926|Invalid US Zipcode       |
 3725|Latitude deviation       |
 3655|Longitude deviation      | 
```

### No. 21 - Backup the file directory **`data/postgres`** 

- Stop the Docker container **`io_avstats_db`**.
- Zip the file directory **`postgres`** in the file directory **`data`** - result is the file **`postgres.zip`**.
- Rename the file **`postgres.sql`** to **`yy.mm.dd_postgres_upDDMON.zip`**.
- Create a copy of the file **`yy.mm.dd_postgres_upDDMON.zip`** with the name **`latest_postgres.zip`**.

### No. 22 - Update the Google Drive 

- Log in to Google Drive with the Google Account **`io-avstats.io-aero@gmail.com`**.
- Upload the file **`yy.mm.dd_postgres_upDDMON.zip`**.
- Share the newly uploaded file.

### No. 23 -  **`c_f_z`** - Zip the files for the cloud 

- Upload the resulting **`cloud.zip`** file to the cloud and process it there.

**Example protocol**:

```
=======================================================================
Start scripts\run_cloud_files_zip
-----------------------------------------------------------------------
File Collection for AWS
-----------------------------------------------------------------------
The current time is: 13:01:26.05
Enter the new time:
=======================================================================

7-Zip (a) [32] 15.14 : Copyright (c) 1999-2015 Igor Pavlov : 2015-12-31

Scanning the drive:
3 files, 339154065 bytes (324 MiB)

Creating archive: cloud.zip

Items to compress: 3


Files read from disk: 3
Archive size: 328965173 bytes (314 MiB)
Everything is Ok

=======================================================================
Archive Content
-----------------------------------------------------------------------

7-Zip (a) [32] 15.14 : Copyright (c) 1999-2015 Igor Pavlov : 2015-12-31

Scanning the drive for archives:
1 file, 328965173 bytes (314 MiB)

Listing archive: cloud.zip

--
Path = cloud.zip
Type = zip
Physical Size = 328965173

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2023-01-31 12:57:21 ....A    339143116    328962979  data\latest_postgres.zip
2023-01-27 06:55:21 ....A         2070          453  docker-compose.yml
2023-01-27 12:31:21 ....A         8879         1241  scripts\run_docker_compose.sh
------------------- ----- ------------ ------------  ------------------------
2023-01-31 12:57:21          339154065    328964673  3 files
=======================================================================

-----------------------------------------------------------------------
The current time is: 13:01:35.98
Enter the new time:
-----------------------------------------------------------------------
End   scripts\run_cloud_files_zip
=======================================================================

-----------------------------------------------------------------------
The current time is: 13:01:35.99
Enter the new time:
-----------------------------------------------------------------------
End   run_io_avstats
=======================================================================
```
