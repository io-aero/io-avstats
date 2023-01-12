# Data Analysis: DB Table **`io_ntsb_2002_2021`**

**Note**: The **`IO-AVSTATS`** database used here contains NTSB aircraft accident data as of January 1, 2023.

This report is about comparing the **`IO-AVSTATS`** database to common public records for aviation accidents.  

In the November 17, 2021, news release [U.S. Civil Aviation Fatalities and Flight Activity Decreased in 2020](https://www.ntsb.gov/news/press-releases/Pages/NR20211117.aspx){:target="_blank"}, the NTSB published, among other things, the [US Civil Aviation Accident Statistics](https://www.ntsb.gov/safety/Pages/research.aspx){:target="_blank"}.
These are available on this website at this [link](https://www.ntsb.gov/safety/data/Documents/AviationAccidentStatistics_2002-2021_20221208.xlsx){:target="_blank"} as a Microsoft Execel file.

## 1.Worksheet no. 29

Worksheet no. 29 obviously contains the detailed events underlying the statistics in the previous worksheets.
Now, in order to make the data in the **`IO-AVSTATS`** database comparable to this MS Excel file, the data from Worksheet no. 29 was loaded into the **`IO-AVSTATS`** database as database table **`io_ntsb_2002_2021`**, unchanged.

### Observation 1 - Fatalities

#### Observation: Discrepancy between `Fatal Injuries` and `Highest Injury Level`:

```sql
SELECT ev_year                                                "Year",
       count(*) FILTER (WHERE highest_injury_level = 'Fatal') "Accidents Fatal 1",
       count(*) FILTER (WHERE fatal_injuries > 0)             "Accidents Fatal 2"
FROM io_ntsb_2002_2021
GROUP BY ev_year
HAVING count(*) FILTER (WHERE highest_injury_level = 'Fatal') != count(*) FILTER (WHERE fatal_injuries > 0)
ORDER BY ev_year
```

```
Year|Accidents Fatal 1|Accidents Fatal 2|
----+-----------------+-----------------+
2008|              298|              305|
```

#### Events affected - Table 29:

```sql
SELECT ntsb_number, event_date, fatal_injuries, highest_injury_level
FROM io_ntsb_2002_2021
WHERE fatal_injuries > 0
  AND highest_injury_level != 'Fatal'
```

```
ntsb_number|event_date             |fatal_injuries|highest_injury_level|
-----------+-----------------------+--------------+--------------------+
ANC09FA001 |2008-10-01 00:00:00.000|             2|                    |
DFW08FA237 |2008-09-28 00:00:00.000|             2|                    |
LAX08FA300 |2008-09-28 00:00:00.000|             1|                    |
MIA08MA203 |2008-09-27 00:00:00.000|             4|                    |
NYC08FA319 |2008-09-23 00:00:00.000|             1|                    |
NYC08FA324 |2008-09-26 00:00:00.000|             1|                    |
NYC08LA322 |2008-09-23 00:00:00.000|             1|                    |
```

#### This problem does not occur in the **`IO-AVSTATS`** database!

```sql
SELECT ntsb_no, ev_year, inj_f_grnd, inj_tot_f, ev_highest_injury
FROM io_app_aaus1982 iaa
WHERE (inj_f_grnd > 0 OR inj_tot_f > 0)
  AND ev_highest_injury != 'FATL'
ORDER BY ntsb_no 
```

```
ntsb_no|ev_year|inj_f_grnd|inj_tot_f|ev_highest_injury|
-------+-------+----------+---------+-----------------+
```

#### The corrupted data in the MS Excel file looks correct in the **`IO-AVSTATS`** database:

```sql
SELECT ntsb_no, ev_year, inj_f_grnd, inj_tot_f, ev_highest_injury
FROM io_app_aaus1982 iaa
WHERE ntsb_no
          IN ('NYC08FA319',
              'NYC08LA322',
              'NYC08FA324',
              'MIA08MA203',
              'DFW08FA237',
              'LAX08FA300',
              'ANC09FA001')
ORDER BY ntsb_no
```

```
ntsb_no   |ev_year|inj_f_grnd|inj_tot_f|ev_highest_injury|
----------+-------+----------+---------+-----------------+
ANC09FA001|   2008|         0|        2|FATL             |
DFW08FA237|   2008|         0|        2|FATL             |
LAX08FA300|   2008|         0|        1|FATL             |
MIA08MA203|   2008|         0|        4|FATL             |
NYC08FA319|   2008|         0|        1|FATL             |
NYC08FA324|   2008|         0|        1|FATL             |
NYC08LA322|   2008|         0|        1|FATL             |
```

#### Conclusion: The `Highest Injury Level` column in the MS Excel file cannot be used to determine fatalities!

### Observation 2 - Incidents

#### Observation: If the worksheet no. 29+ also contains events of type **`INC`** (incident):

```sql
SELECT ntsb_number, event_date
FROM io_ntsb_2002_2021
WHERE ntsb_number IN (SELECT ntsb_no FROM io_app_aaus1982 WHERE ev_type = 'INC')
```

```
ntsb_number|event_date|
-----------+----------+
```

#### Conclusion: Worksheet no. 29 does not contain any events of type **`INC`**!

### Observation 3 - Duplicates 1

#### Observation: Are more than 1 line included for the same **`NTSB Number`**:

```sql
SELECT count(ntsb_number)
FROM (SELECT count(*), ntsb_number
      FROM io_ntsb_2002_2021 in2
      GROUP BY ntsb_number
      HAVING count(*) > 1) g
```

```
count|
-----+
  336|
```

```sql
SELECT ntsb_number, event_date, state_or_region, city, country, fatal_injuries
FROM io_ntsb_2002_2021 in3
WHERE ntsb_number in (SELECT ntsb_number
                      FROM io_ntsb_2002_2021 in2
                      GROUP BY ntsb_number
                      HAVING count(*) > 1)
ORDER BY ntsb_number
```

```
ntsb_number|event_date             |state_or_region     |city                       |country      |fatal_injuries|
-----------+-----------------------+--------------------+---------------------------+-------------+--------------+
ANC02LA053 |2002-06-19 00:00:00.000|Alaska              |Ketchikan                  |United States|              |
ANC02LA053 |2002-06-19 00:00:00.000|Alaska              |Ketchikan                  |United States|              |
ANC02LA086 |2002-07-30 00:00:00.000|Alaska              |Fairbanks                  |United States|              |
ANC02LA086 |2002-07-30 00:00:00.000|Alaska              |Fairbanks                  |United States|              |
ANC02LA098 |2002-08-19 00:00:00.000|Alaska              |Ketchikan                  |United States|              |
ANC02LA098 |2002-08-19 00:00:00.000|Alaska              |Ketchikan                  |United States|              |
ANC03LA005 |2002-10-22 00:00:00.000|Alaska              |BETHEL                     |United States|              |
ANC03LA005 |2002-10-22 00:00:00.000|Alaska              |BETHEL                     |United States|              |
ANC04FA016 |2003-12-28 00:00:00.000|Arizona             |Peoria                     |United States|             4|
ANC04FA016 |2003-12-28 00:00:00.000|Arizona             |Peoria                     |United States|             4|
ANC06FA048 |2006-04-23 00:00:00.000|Alaska              |Chugiak                    |United States|             5|
ANC06FA048 |2006-04-23 00:00:00.000|Alaska              |Chugiak                    |United States|             5|
ANC08LA106 |2008-08-18 00:00:00.000|Alaska              |Bethel                     |United States|              |
ANC08LA106 |2008-08-18 00:00:00.000|Alaska              |Bethel                     |United States|              |
ANC09LA004 |2008-10-07 00:00:00.000|Alaska              |Bethel                     |United States|              |
ANC09LA004 |2008-10-07 00:00:00.000|Alaska              |Bethel                     |United States|              |
ANC09LA011 |2008-11-14 00:00:00.000|Alaska              |Fairbanks                  |United States|              |
ANC09LA011 |2008-11-14 00:00:00.000|Alaska              |Fairbanks                  |United States|              |
ANC10LA094 |2010-09-15 00:00:00.000|Alaska              |Dillingham                 |United States|              |
ANC10LA094 |2010-09-15 00:00:00.000|Alaska              |Dillingham                 |United States|              |
ANC11FA062 |2011-07-10 00:00:00.000|Alaska              |Port Alsworth              |United States|              |
ANC11FA062 |2011-07-10 00:00:00.000|Alaska              |Port Alsworth              |United States|              |
```

#### Conclusion: There are 336 events with more than 1 line included in worksheet 29.


### Observation 4 - Duplicates 2

#### Observation: How many lines are there in the events with multiple lines:

```sql
SELECT count(*), ntsb_number, ev_year
FROM io_ntsb_2002_2021 in2
GROUP BY ntsb_number, ev_year
HAVING count(*) > 1
ORDER BY 1 desc
```

```
count|ntsb_number|ev_year|
-----+-----------+-------+
    3|CEN10FA115 |   2010|
    2|ERA11CA296 |   2011|
    2|WPR12CA163 |   2012|
    2|MIA04FA043 |   2004|
    2|LAX08FA265 |   2008|
    2|NYC07LA209 |   2007|
    2|ERA09TA466 |   2009|
    2|GAA19CA346 |   2019|
    2|SEA07FA264 |   2007|
    2|DCA15CA012 |   2014|
    2|ANC02LA086 |   2002|
```

#### Conclusion: Only in 2010 there is an event with 3 lines, otherwise there are always 2 lines.

## 2.Worksheet no. 10 vs. no. 29

[Worksheet no. 10](./img/AviationAccidentStatistics_2002-2021_20221208.pdf){:target="_blank"}

### Observation 1 - Completeness

#### Observation: Are all events from worksheet 29 included in worksheet 10:

```sql
SELECT ev_year                                    "Year",
       count(*)                                   "Accidents All",
       count(*) FILTER (WHERE fatal_injuries > 0) "Accidents Fatal",
       sum(fatal_injuries)                        "Fatalities"
FROM io_ntsb_2002_2021
GROUP BY ev_year
ORDER BY ev_year
```

```
Year|Accidents All|Accidents Fatal|Fatalities|
----+-------------+---------------+----------+
2002|         1837|            367|       624|
2003|         1890|            381|       723|
2004|         1735|            346|       648|
2005|         1804|            340|       613|
2006|         1626|            326|       787|
2007|         1765|            308|       551|
2008|         1688|            305|       593|
2009|         1572|            285|       559|
2010|         1527|            284|       491|
2011|         1578|            293|       510|
2012|         1556|            285|       456|
2013|         1306|            238|       436|
2014|         1302|            268|       451|
2015|         1296|            239|       411|
2016|         1355|            228|       427|
2017|         1331|            212|       349|
2018|         1366|            234|       402|
2019|         1322|            255|       467|
2020|         1152|            215|       369|
2021|         1233|            221|       378|
```

#### Conclusion: Worksheet no. 29 always contains more events than are included in Worksheet no. 10!

<kbd>![](img/table_10-table_29.png)</kbd>


### Observation 2 - Duplicates

#### Observation: Look for reasons for the discrepancies:

```sql
SELECT ev_year                                    "Year",
       count(*)                                   "Accidents All",
       count(*) FILTER (WHERE fatal_injuries > 0) "Accidents Fatal",
       sum(fatal_injuries)                        "Fatalities"
FROM io_ntsb_2002_2021
WHERE ntsb_number IN (SELECT ntsb_number
                      FROM io_ntsb_2002_2021 in2
                      GROUP BY ntsb_number
                      HAVING count(*) > 1)
GROUP BY ev_year
ORDER BY ev_year
```

```
Year|Accidents All|Accidents Fatal|Fatalities|
----+-------------+---------------+----------+
2002|           30|              8|        16|
2003|           42|             16|        48|
2004|           32|             14|        22|
2005|           46|             12|        24|
2006|           30|             10|        26|
2007|           38|             10|        22|
2008|           56|             12|        50|
2009|           28|             12|        36|
2010|           39|             11|        25|
2011|           42|             14|        22|
2012|           32|              8|        12|
2013|           20|              6|        14|
2014|           24|             10|        18|
2015|           30|              2|        10|
2016|           38|             14|        38|
2017|           28|              2|         4|
2018|           38|              6|        14|
2019|           40|             10|        24|
2020|           24|             10|        40|
2021|           16|              2|         4|
```

#### Conclusion: The ominous existence of duplicates unfortunately does not explain the difference between worksheets no. 10 and no. 29.

## 3.Worksheet no. 29 vs. IO-AVSTATS

### Observation 1 - Missing in IO-AVSTATS

#### Observation: Are all events of worksheet no. 29 contained in IO-AVSTATS:

```sql
SELECT ntsb_number, ev_year, city, state_or_region, country, fatal_injuries
FROM io_ntsb_2002_2021 in3
WHERE ntsb_number NOT IN (SELECT ntsb_no FROM events)
ORDER BY ev_year, ntsb_number
```

```
ntsb_number|ev_year|city    |state_or_region|country      |fatal_injuries|
-----------+-------+--------+---------------+-------------+--------------+
CEN21LA236 |   2021|Longmont|Colorado       |United States|              |
```

#### Conclusion: This minimal difference can certainly be explained by a subsequent correction.

### Observation 2 - Missing in Worksheet

#### Observation: Are all events of IO-AVSTATS contained in worksheet no. 29:

```sql
SELECT ntsb_no, ev_id, ev_year, ev_site_zipcode, ev_city, ev_country, inj_tot_f
FROM events e
WHERE ev_year >= 2002
  AND ev_year <= 2021
  AND ev_type = 'ACC'
  AND ntsb_no NOT IN (SELECT ntsb_number FROM io_ntsb_2002_2021 in2)
ORDER BY ev_year, ev_id
```

```
ntsb_no   |ev_id         |ev_year|ev_site_zipcode|ev_city                                    |ev_country|inj_tot_f|
----------+--------------+-------+---------------+-------------------------------------------+----------+---------+
WAS02WA015|20020109X00049|   2002|00000          |Tarapoto                                   |PE        |         |
MIA02LA054|20020201X00157|   2002|34142          |Immokalee                                  |USA       |        1|
LAX02LA072|20020201X00161|   2002|92145          |San Diego                                  |USA       |        2|
WAS02RA017|20020212X00207|   2002|00000          |Ishpingo                                   |EC        |         |
WAS02WA019|20020220X00235|   2002|00000          |Santa Elena                                |VE        |         |
WAS02RA021|20020221X00240|   2002|00000          |CACKCHILA                                  |GT        |        2|
CHI02WA080|20020225X00253|   2002|               |Libourne                                   |FR        |        3|
DCA02WA023|20020226X00261|   2002|               |San Juan                                   |AR        |         |
SEA02LA039|20020228X00289|   2002|97009          |Boring                                     |USA       |        1|
SEA02LA042|20020228X00290|   2002|98282          |Concrete                                   |USA       |         |
WAS02WA023|20020301X00296|   2002|               |Indore                                     |IN        |         |
IAD02WA031|20020302X00298|   2002|               |Zernez                                     |SZ        |        2|
WAS02WA026|20020306X00311|   2002|00000          |San Antonio                                |PE        |        2|
MIA02WA065|20020308X00318|   2002|               |Montevideo                                 |UY        |         |
WAS02RA025|20020308X00319|   2002|00000          |El Tigre                                   |CO        |       26|
```

```sql
SELECT count(*), ev_year
FROM (SELECT ntsb_no, ev_id, ev_year, ev_site_zipcode, ev_city, ev_country, inj_tot_f
      FROM events e
      WHERE ev_year >= 2002
        AND ev_year <= 2021
        AND ev_type = 'ACC'
        AND ntsb_no NOT IN (SELECT ntsb_number FROM io_ntsb_2002_2021 in2)
      ORDER BY ev_year, ev_id) g
GROUP BY ev_year
ORDER BY ev_year
```

```
count|ev_year|
-----+-------+
  115|   2002|
  128|   2003|
  141|   2004|
  147|   2005|
  141|   2006|
  152|   2007|
  130|   2008|
  124|   2009|
  140|   2010|
  175|   2011|
  177|   2012|
  166|   2013|
  162|   2014|
  206|   2015|
  207|   2016|
  196|   2017|
  218|   2018|
  203|   2019|
  169|   2020|
  291|   2021|
```

#### Conclusion: 3388 Events of IO-AVSTATS are not included in worksheet no. 29!

### Observation 3 - Non-US aircraft registration number

#### Observation: All events involving only aircraft with missing or non-U.S. registration numbers are missing from Worksheet No. 29.:

```sql
SELECT ntsb_number,
       event_date,
       city,
       state_or_region,
       country,
       aircraft_number,
       registration_number,
       fatal_injuries
FROM io_ntsb_2002_2021 in2
WHERE ntsb_number IN (SELECT e.ntsb_no
                      FROM events e
                               INNER JOIN aircraft a ON (e.ev_id = a.ev_id)
                      WHERE ev_year >= 2002
                        AND ev_year <= 2021
                        AND ev_type = 'ACC'
                        AND (a.regis_no IS NULL
                          or upper(a.regis_no) = 'NONE'
                          or a.regis_no NOT LIKE 'N%')
                        AND RTRIM(a.owner_country) != 'USA'
                        AND RTRIM(a.oper_country) != 'USA'
                        AND RTRIM(a.dprt_country) != 'USA'
                        AND RTRIM(a.dest_country) != 'USA')
ORDER BY ev_year, ntsb_number
```

```
ntsb_number|event_date             |city           |state_or_region|country   |aircraft_number|registration_number|fatal_injuries|
-----------+-----------------------+---------------+---------------+----------+---------------+-------------------+--------------+
ANC08TA028 |2007-12-20 00:00:00.000|McMurdo Station|               |Antarctica|              1|C-FMKB             |              |
```

```sql
SELECT e.ev_id,
       a.aircraft_key,
       a.regis_no,
       a.dprt_country,
       a.dest_country,
       a.owner_country,
       a.oper_country
FROM events e
         INNER JOIN aircraft a ON (e.ev_id = a.ev_id)
WHERE e.ev_year >= 2002
  AND e.ev_year <= 2021
  AND a.regis_no LIKE 'N%'
  AND rtrim(a.dest_country) != 'USA'
  AND rtrim(a.dprt_country) != 'USA'
  AND rtrim(a.owner_country) != 'USA'
  AND rtrim(a.oper_country) != 'USA'
```

```
ev_id         |aircraft_key|regis_no|dprt_country|dest_country|owner_country|oper_country|
--------------+------------+--------+------------+------------+-------------+------------+
20081202X25642|           1|N400SA  |BR          |BR          |BR           |BR          |
20081230X00408|           1|N104BN  |BP          |BP          |NH           |NH          |
20120327X14319|           1|N27TR   |AR          |AR          |AR           |AR          |
20130305X21219|           1|N471M   |PP          |PP          |NH           |NH          |
20140922X90145|           1|N1027G  |FR          |UK          |UK           |UK          |
20150707X14422|           1|N642RM  |RS          |RS          |RS           |RS          |
20150903X44600|           1|N9068F  |KR          |KR          |NH           |NH          |
20151112X63511|           1|N692BE  |TU          |LY          |AS           |AS          |
20160630X91359|           1|N188RU  |CO          |CO          |CO           |CO          |
20170308X31846|           1|N805LA  |UN          |UN          |NH           |NH          |
20170728X93637|           1|N1001R  |BR          |BR          |BR           |BR          |
20180301X63457|           1|N3AD    |CA          |GL          |GE           |GE          |
20180329X93928|           1|N561LC  |SZ          |UN          |UN           |UN          |
20180813X53624|           1|N2451J  |DR          |DR          |DR           |DR          |
20181029X14552|           1|N474CG  |GE          |SZ          |UK           |SZ          |
20190212X72918|           1|N842CD  |FR          |FR          |FR           |FR          |
20190708X33047|           1|N3294P  |IC          |IC          |IC           |IC          |
20190805X10835|           1|N989AE  |CO          |CO          |CB           |CO          |
20200924X51906|           1|N9056K  |SA          |SA          |SA           |SA          |
20061214X01789|           1|N79KD   |AU          |GE          |UK           |GE          |
20090512X15548|           1|N1116G  |CO          |CO          |CO           |CO          |
```

#### Conclusion: Only events where either an aircraft with a U.S. registration number (N1 - N99999, N1A - N9999Z, N1AA - N999ZZ) is involved or the U.S. is either the departure country, destination country, owner country or operator country are considered. 
