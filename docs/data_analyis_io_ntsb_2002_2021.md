# Data Analysis **`io_ntsb_2002_2021`**

Status as of Jan. 1, 2023

## 1. Totals

## 1.1 2010

```sql
SELECT count(*)                                     number,
       ev_year::varchar(4) || ' accidents all ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2010
GROUP BY ev_year
UNION
SELECT count(*)                                       number,
       ev_year::varchar(4) || ' accidents fatal ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2010
  AND highest_injury_level = 'Fatal'
GROUP BY ev_year
UNION
SELECT sum(fatal_injuries)                             number,
       ev_year::varchar(4) || ' fatalities total ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2010
  AND highest_injury_level = 'Fatal'
GROUP BY ev_year
UNION
SELECT count(*)                                        number,
       ev_year::varchar(4) || ' accidents all io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2010
GROUP BY ev_year
UNION
SELECT count(*)                                          number,
       ev_year::varchar(4) || ' accidents fatal io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2010
  AND fatalities > 0
GROUP BY ev_year
UNION
SELECT sum(fatalities)                                    number,
       ev_year::varchar(4) || ' fatalities total io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2010
GROUP BY ev_year
ORDER BY 2    
```

```
number|description                  |
------+-----------------------------+
  1541|2010 accidents all io-aero   |
  1486|2010 accidents all ntsb      |
   259|2010 accidents fatal io-aero |
   263|2010 accidents fatal ntsb    |
   439|2010 fatalities total io-aero|
   452|2010 fatalities total ntsb   |
```


## 1.2 2020

```sql
SELECT count(*)                                     number,
       ev_year::varchar(4) || ' accidents all ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2020
GROUP BY ev_year
UNION
SELECT count(*)                                       number,
       ev_year::varchar(4) || ' accidents fatal ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2020
  AND highest_injury_level = 'Fatal'
GROUP BY ev_year
UNION
SELECT sum(fatal_injuries)                             number,
       ev_year::varchar(4) || ' fatalities total ntsb' description
FROM io_ntsb_2002_2021 in2
WHERE ev_state IS NOT NULL
  AND ev_country = 'USA'
  AND ev_year = 2020
  AND highest_injury_level = 'Fatal'
GROUP BY ev_year
UNION
SELECT count(*)                                        number,
       ev_year::varchar(4) || ' accidents all io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2020
GROUP BY ev_year
UNION
SELECT count(*)                                          number,
       ev_year::varchar(4) || ' accidents fatal io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2020
  AND fatalities > 0
GROUP BY ev_year
UNION
SELECT sum(fatalities)                                    number,
       ev_year::varchar(4) || ' fatalities total io-aero' description
FROM io_app_aaus1982 iaa
WHERE ev_year = 2020
GROUP BY ev_year
ORDER BY 2    
```

```
number|description                  |
------+-----------------------------+
  1133|2020 accidents all io-aero   |
  1128|2020 accidents all ntsb      |
   202|2020 accidents fatal io-aero |
   206|2020 accidents fatal ntsb    |
   334|2020 fatalities total io-aero|
   353|2020 fatalities total ntsb   |
```

## 2. Missing fatal accidents in NTSB

### 2.1 2010

```sql
SELECT ev_id, ntsb_no
 FROM io_app_aaus1982 iaa
WHERE ev_year = 2010
  AND fatalities > 0
  AND ntsb_no NOT IN (SELECT ntsb_number FROM io_ntsb_2002_2021 in2 WHERE ev_year = 2010)
ORDER BY ntsb_no
```

```
ev_id         |ntsb_no   |
--------------+----------+
20100503X31325|CEN10LA234|
20100119X95202|ERA10LA119|
20100919X72723|ERA10LA488|
20101125X11507|WPR11FA059|
```


### 2.2 2020

```sql
SELECT ev_id, ntsb_no
 FROM io_app_aaus1982 iaa
WHERE ev_year = 2020
  AND fatalities > 0
  AND ntsb_no NOT IN (SELECT ntsb_number FROM io_ntsb_2002_2021 in2 WHERE ev_year = 2020)
ORDER BY ntsb_no
```

```
ev_id         |ntsb_no   |
--------------+----------+
20200125X95855|ERA20FA086|
```

## 3. Missing fatal accidents in IO-AVSTATS

### 3.1 2010

```sql
SELECT ntsb_number
 FROM io_ntsb_2002_2021 iaa
WHERE ev_year = 2010
  AND highest_injury_level = 'Fatal'
  AND ntsb_number NOT IN (SELECT ntsb_no FROM io_app_aaus1982 iaa2 WHERE ev_year = 2010)
ORDER BY ntsb_number
```

```
ntsb_number|
-----------+
ANC10WA073 |
CEN10RA579 |
CEN10WA096 |
CEN10WA273 |
CEN10WA379 |
CEN11RA024 |
CEN11WA042 |
CEN12WA547 |
DCA10RA092 |
ERA10LA158 |
ERA10LA207 |
ERA10LA511 |
ERA10WA116 |
ERA10WA133 |
ERA10WA281 |
ERA10WA394 |
ERA11LA056 |
ERA11WA088 |
ERA11WA090 |
WPR10LA464 |
WPR10WA321 |
```

### 3.2 2020

```sql
SELECT ntsb_number
 FROM io_ntsb_2002_2021 iaa
WHERE ev_year = 2020
  AND highest_injury_level = 'Fatal'
  AND ntsb_number NOT IN (SELECT ntsb_no FROM io_app_aaus1982 iaa2 WHERE ev_year = 2020)
ORDER BY ntsb_number
```

```
ntsb_number|
-----------+
CEN20WA408 |
CEN20WA409 |
CEN20WA426 |
CEN20WA441 |
ERA20LA202 |
GAA20WA110 |
GAA20WA139 |
WPR20WA076 |
WPR21WA062 |
```
