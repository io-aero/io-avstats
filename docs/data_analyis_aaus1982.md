# Data Analysis **`aaus1982`**

Status as of Jan. 1, 2003

## 1. Totals

```sql
SELECT count(*),
       'Total accidents since 1982 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 1982 
 UNION
SELECT count(*),
       'Total accidents since 2008 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 2008 
 UNION
SELECT count(*),
      'Fatal accidents since 1982 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 1982 
   AND inj_tot_f > 0
 UNION
SELECT count(*),
      'Fatal accidents since 2008 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 2008 
   AND inj_tot_f > 0
 UNION
SELECT count(*),
       'Total accidents since 1982 by io_app_aaus1982'
  FROM io_app_aaus1982
 UNION
SELECT count(*),
       'Total accidents since 2008 by io_app_aaus1982'
  FROM io_app_aaus1982
 WHERE ev_year >= 2008 
 UNION
SELECT count(*),
      'Fatal accidents since 1982 by io_app_aaus1982'
  FROM io_app_aaus1982
 WHERE fatalities > 0
 UNION
SELECT count(*),
      'Fatal accidents since 2008 by io_app_aaus1982'
  FROM io_app_aaus1982
 WHERE ev_year >= 2008 
   AND fatalities > 0
 UNION 
SELECT sum(inj_tot_f),
       'Total fatalities since 1982 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 1982
 UNION
SELECT sum(inj_tot_f),
       'Total fatalities since 2008 by io_accidents_us_1982'
  FROM io_accidents_us_1982
 WHERE ev_year >= 2008
 UNION
SELECT sum(fatalities),
       'Total fatalities since 1982 by io_app_aaus1982'
  FROM io_app_aaus1982
 UNION
SELECT sum(fatalities),
       'Total fatalities since 2008 by io_app_aaus1982'
  FROM io_app_aaus1982
 WHERE ev_year >= 2008
 ORDER BY 2 
```

```
count|description                                        |
-----+---------------------------------------------------+
14683|Fatal accidents since 1982 by io_accidents_us_1982 |
14683|Fatal accidents since 1982 by io_app_aaus1982      |
 3501|Fatal accidents since 2008 by io_accidents_us_1982 |
 3501|Fatal accidents since 2008 by io_app_aaus1982      |
81100|Total accidents since 1982 by io_accidents_us_1982 |
81100|Total accidents since 1982 by io_app_aaus1982      |
20750|Total accidents since 2008 by io_accidents_us_1982 |
20750|Total accidents since 2008 by io_app_aaus1982      |
28958|Total fatalities since 1982 by io_accidents_us_1982|
28958|Total fatalities since 1982 by io_app_aaus1982     |
 5939|Total fatalities since 2008 by io_accidents_us_1982|
 5939|Total fatalities since 2008 by io_app_aaus1982     |
```

## 2. FAR parts

### 2.1 Accidents since 1982

```sql
SELECT count(*),
       far_part
  FROM io_app_aaus1982
 WHERE ev_year >= 1982
 GROUP BY far_part
 ORDER BY 2,
          1 DESC
```

```
count|far_part      |
-----+--------------+
   25|{}            |
68393|{091}         |
  814|{091,091}     |
    2|{091,091,091} |
    1|{091,091,091F}|
    1|{091,091F}    |
    1|{091,091K}    |
    5|{091,103}     |
    2|{091,107}     |
   38|{091,121}     |
    1|{091,125}     |
    5|{091,129}     |
   57|{091,135}     |
   10|{091,137}     |
   12|{091,ARMF}    |
    5|{091,PUBU}    |
    4|{091,UNK}     |
   34|{091F}        |
   13|{091K}        |
  184|{103}         |
    2|{103,103}     |
    1|{103,135}     |
    2|{107}         |
    1|{107,135}     |
    1|{107,ARMF}    |
 1968|{121}         |
   81|{121,121}     |
   20|{121,129}     |
   13|{121,135}     |
    3|{121,ARMF}    |
    2|{121,PUBU}    |
    1|{121,UNK}     |
   20|{125}         |
  144|{129}         |
    7|{129,129}     |
    2|{129,135}     |
  441|{133}         |
    1|{133,133}     |
 3433|{135}         |
   43|{135,135}     |
    1|{135,ARMF}    |
 4686|{137}         |
   30|{137,137}     |
    1|{137,ARMF}    |
    1|{437}         |
    1|{ARMF}        |
    1|{ARMF,ARMF}   |
   15|{NUSC}        |
    7|{NUSN}        |
  538|{PUBU}        |
    3|{PUBU,PUBU}   |
   21|{UNK}         |
    1|{UNK,UNK}     |
    1|{UNK,UNK,UNK} |
```

### 2.2 Fatalities since 1982

```sql
SELECT count(*),
       far_part
  FROM io_app_aaus1982
 WHERE ev_year >= 1982
   AND fatalities > 0 
 GROUP BY far_part
 ORDER BY 1 DESC,
          2
```

```
count|far_part     |
-----+-------------+
12813|{091}        |
  696|{135}        |
  438|{137}        |
  259|{091,091}    |
  114|{PUBU}       |
   91|{133}        |
   90|{103}        |
   79|{121}        |
   22|{091,135}    |
   17|{137,137}    |
   12|{129}        |
    8|{091,ARMF}   |
    7|{091F}       |
    5|{135,135}    |
    5|{UNK}        |
    4|{NUSN}       |
    3|{091,121}    |
    3|{091,PUBU}   |
    3|{NUSC}       |
    2|{125}        |
    1|{091,091,091}|
    1|{091,091F}   |
    1|{091,103}    |
    1|{091,129}    |
    1|{091,UNK}    |
    1|{103,103}    |
    1|{103,135}    |
    1|{121,121}    |
    1|{121,135}    |
    1|{135,ARMF}   |
    1|{437}        |
    1|{PUBU,PUBU}  |
```

### 2.3 Fatalities since 2008

```sql
SELECT count(*),
       far_part
  FROM io_app_aaus1982
 WHERE ev_year >= 2008
   AND fatalities > 0 
 GROUP BY far_part
 ORDER BY 1 DESC,
          2
```

```
count|far_part     |
-----+-------------+
 3132|{091}        |
  113|{135}        |
  109|{137}        |
   51|{091,091}    |
   43|{PUBU}       |
   25|{133}        |
    5|{091,135}    |
    5|{121}        |
    4|{137,137}    |
    3|{135,135}    |
    2|{UNK}        |
    1|{091,091,091}|
    1|{091,ARMF}   |
    1|{103,135}    |
    1|{125}        |
    1|{129}        |
    1|{437}        |
    1|{NUSC}       |
    1|{NUSN}       |
    1|{PUBU,PUBU}  |
```
