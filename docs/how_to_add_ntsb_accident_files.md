# How to add **NTSB** accident files

Aviation accident data provided by **NTSB** can be found at the following [link](https://data.ntsb.gov/avdata){:target="_blank"}:

<kbd>![](img/how_to_add_ntsb_01.png)</kbd>

**NTSB** provides the following files:

- **`Pre2008.zip`**: data set for 1982 through 2007
- **`avall.zip`**: data set from 2008 to the present 
- **`upDDMON.zip`**: monthly supplements on the 1st, 8th, 15th and 22nd

In the database table **`io_processed_files`** you can find the files already processed by **IO-AVSTATS**:

<kbd>![](img/io_processed_files.png)</kbd>

Any file provided by **NTSB** can be processed several times with the process described in the following, as long as one processes also afterward all newer files again.

All processing tasks can be executed with the **`run_io_avstats`** script.
For a more detailed description of these tasks, see under **Operation**.

## 1. Every first of the month

### 1.1 Prepare the database

- Stop the Docker container **`io_avstats_db`**.
- Remove the directory **`data/postgres`**
- Unzip the latest file **`data/yy.mm.dd_postgres_Pre2008_20.09.30.zip`**
- Start the Docker container **`io_avstats_db`** with **`c_d_l - Run Docker Compose tasks - Local`**

### 1.2 Processing modified non-**NTSB** data sources 

The following steps are performed only if the source files have changed:

| Source(s)                                                                                                                                | Version            | Task  | Description                                         |
|------------------------------------------------------------------------------------------------------------------------------------------|--------------------|-------|-----------------------------------------------------|
| [Airports](https://adds-faa.opendata.arcgis.com/datasets/faa::airports-1/explore?location=0.158824%2C-1.633886%2C2.00){:target="_blank"} | 20 April 2023      | l_a_p | Load airport data into PostgreSQL                   |
| [NPIAS](https://www.faa.gov/airports/planning_capacity/npias){:target="_blank"}                                                          | 2023-2027 NPIAS    |       |                                                     |
| [Runways](https://adds-faa.opendata.arcgis.com/datasets/faa::runways/explore?location=0.059024%2C-1.628764%2C2.00){:target="_blank"}     | 20 April 2023      |       |                                                     |
| [NTSB](https://www.ntsb.gov/safety/data/Documents/datafiles/OccurrenceCategoryDefinitions.pdf){:target="_blank"}                         | October 2013 (4.6) | a_o_c | Load aviation occurrence categories into PostgreSQL |
| [geodatos](https://www.geodatos.net/en/coordinates/united-states){:target="_blank"}                                                      | n/a                | l_c_s | Load country and state data into PostgreSQL         |
| NTSB                                                                                                                                     | n/a                | l_s_e | Load sequence of events data into PostgreSQL        |
| [United States Cities Database](https://simplemaps.com/data/us-cities){:target="_blank"}                                                 | v1.76              | l_s_d | Load simplemaps data into PostgreSQL                |
| [US Zip Codes Database](https://simplemaps.com/data/us-zips){:target="_blank"}                                                           | v1.82              |       |                                                     |
| [ZIP Code Database](https://www.unitedstateszipcodes.org/zip-code-database/){:target="_blank"}                                           | 41'695 active      | l_z_d | Load ZIP Code Database data into PostgreSQL         |


#### 1.2.1 Backup the file directory **`data/postgres`** 

- Stop the Docker container **`io_avstats_db`**.
- Zip the file directory **`postgres`** in the file directory **`data`** - result is the file **`postgres.zip`**.
- Rename the file **`data/postgres.sql`** to **`yy.mm.dd_postgres_upDDMON.zip`**.
- Start the Docker container **`io_avstats_db`** with **`c_d_l - Run Docker Compose tasks - Local`**

### 1.3 **NTSB** file **`avall.zip`**

The following task must be performed on the first of each month:

| Task  | Description                                       |
|-------|---------------------------------------------------|
| l_n_a | Load NTSB MS Access database data into PostgreSQL |

## 2. **NTSB** file **`upDDMON.zip`**

The following tasks must be performed every month on the 1st, 8th, 15th and 22nd:

|    No. | Task  | Description                                                   |
|-------:|-------|---------------------------------------------------------------|
| either | u_p_d | Download a NTSB MS Access database file                       |
| or  1. | l_n_a | Load NTSB MS Access database data into PostgreSQL             |
|     2. | l_c_d | **optional** Load data from a correction file into PostgreSQL |
|     3. | c_l_l | Correct decimal US latitudes and longitudes                   |
|     4. | f_n_a | Find the nearest airports                                     |
|     5. | v_n_d | Verify selected NTSB data                                     |
|     6. | r_d_s | Refresh the PostgreSQL database schema                        |

## 3. Repository io-avstats

- Modify the word document `upload/IO-AVSTATS.docx`
- Create the pdf file `upload/IO-AVSTATS.pdf`
- Modify the word document `upload/IO-AVSTATS-DB.docx`
- Create the pdf file `upload/IO-AVSTATS-DB.pdf`
- Run `make pipenv-dev`
- Run `make final`
- Create a pull request
- Create the new release yy.mm.dd

## 4. Repository io-avstats-shared

- Create the log file `docs/yyyy_mm_dd_log_upddMON.md`
- Modify the release notes file `docs/io_avstats_db_release_notes.md`
- Modify the release notes file `docs/io_avstats_release_notes.md`
- Modify the configuration file `mkdocs.yml`
- Run `make final`
- Create a pull request

## 5. Backup 

The following steps are used to backup the database **IO-AVSTATS-DB**:

| No. | Description                                   |
|----:|-----------------------------------------------|
|  1. | Backup the file directory **`data/postgres`** |
|  2. | Update the Google Drive                       |

### 5.1 Backup the file directory **`data/postgres`** 

- Stop the Docker container **`io_avstats_db`**.
- Zip the file directory **`postgres`** in the file directory **`data`** - result is the file **`postgres.zip`**.
- Rename the file **`data/postgres.sql`** to **`yy.mm.dd_postgres_upDDMON.zip`**.
- Create a copy of the file **`data/yy.mm.dd_postgres_upDDMON.zip`** with the name **`latest_postgres.zip`**.

### 5.2 Update the Google Drive 

- Log in to Google Drive with the Google Account **`io-avstats.io-aero@gmail.com`**.
- Upload the file **`data/yy.mm.dd_postgres_upDDMON.zip`**.
- Share the newly uploaded file.

## 6. Create new application images

| Task  | Description                     |
|-------|---------------------------------|
| c_d_i | Create or update a Docker image |

## 7. Create the new cloud zip file

| Task  | Description                 |
|-------|-----------------------------|
| c_f_z | Zip the files for the cloud |


## 8 Optional data quality checks

#### 8.1 Event completeness

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

#### 8.2 Latitude & longitude

**Query Total:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
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

#### 8.3 Issue summary

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
