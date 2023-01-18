# Data Analysis: DB View **`ae1982`**

Status as of Jan. 1, 2023

## 1. Totals

```sql
SELECT count(*),
       'Total accidents since 1982'
  FROM events
 WHERE ev_year >= 1982 
 UNION
SELECT count(*),
       'Total accidents since 2008'
  FROM events
 WHERE ev_year >= 2008 
 UNION
SELECT count(*),
      'Fatal accidents since 1982'
  FROM events
 WHERE ev_year >= 1982 
   AND inj_tot_f > 0
 UNION
SELECT count(*),
      'Fatal accidents since 2008'
  FROM events
 WHERE ev_year >= 2008 
   AND inj_tot_f > 0
 UNION
SELECT count(*),
       'Total accidents since 1982 by io_app_ae1982'
  FROM io_app_ae1982
 UNION
SELECT count(*),
       'Total accidents since 2008 by io_app_ae1982'
  FROM io_app_ae1982
 WHERE ev_year >= 2008 
 UNION
SELECT count(*),
      'Fatal accidents since 1982 by io_app_ae1982'
  FROM io_app_ae1982
 WHERE inj_tot_f > 0
 UNION
SELECT count(*),
      'Fatal accidents since 2008 by io_app_ae1982'
  FROM io_app_ae1982
 WHERE ev_year >= 2008 
   AND inj_tot_f > 0
 UNION 
SELECT sum(inj_tot_f),
       'Total fatalities since 1982'
  FROM events
 WHERE ev_year >= 1982
 UNION
SELECT sum(inj_tot_f),
       'Total fatalities since 2008'
  FROM events
 WHERE ev_year >= 2008
 UNION
SELECT sum(inj_tot_f),
       'Total fatalities since 1982 by io_app_ae1982'
  FROM io_app_ae1982
 UNION
SELECT sum(inj_tot_f),
       'Total fatalities since 2008 by io_app_ae1982'
  FROM io_app_ae1982
 WHERE ev_year >= 2008
 ORDER BY 2 
```

```
count|?column?                                      |
-----+----------------------------------------------+
17570|Fatal accidents since 1982                    |
17570|Fatal accidents since 1982 by io_app_ae1982 |
 5260|Fatal accidents since 2008                    |
 5260|Fatal accidents since 2008 by io_app_ae1982 |
88084|Total accidents since 1982                    |
88084|Total accidents since 1982 by io_app_ae1982 |
25055|Total accidents since 2008                    |
25055|Total accidents since 2008 by io_app_ae1982 |
48672|Total fatalities since 1982                   |
48672|Total fatalities since 1982 by io_app_ae1982|
14607|Total fatalities since 2008                   |
14607|Total fatalities since 2008 by io_app_ae1982|
```

## 2. FAR operations parts

### 2.1 Accidents since 1982

```sql
SELECT count(*),
       far_part
  FROM io_app_ae1982
 WHERE ev_year >= 1982
 GROUP BY far_part
 ORDER BY 2,
          1 DESC
```

```
count|far_part      |
-----+--------------+
  693|{}            |
69370|{091}         |
  822|{091,091}     |
    2|{091,091,091} |
    1|{091,091,091F}|
    1|{091,091F}    |
    1|{091,091K}    |
    5|{091,103}     |
    2|{091,107}     |
   39|{091,121}     |
    1|{091,125}     |
    5|{091,129}     |
   58|{091,135}     |
   10|{091,137}     |
   12|{091,ARMF}    |
    1|{091,NUSC}    |
    1|{091,NUSN}    |
    5|{091,PUBU}    |
    4|{091,UNK}     |
   35|{091F}        |
   14|{091K}        |
  184|{103}         |
    2|{103,103}     |
    1|{103,135}     |
    3|{107}         |
    1|{107,135}     |
    1|{107,ARMF}    |
 2315|{121}         |
   85|{121,121}     |
   24|{121,129}     |
   14|{121,135}     |
    3|{121,ARMF}    |
    5|{121,NUSC}    |
    1|{121,NUSN}    |
    2|{121,PUBU}    |
    1|{121,UNK}     |
   26|{125}         |
  578|{129}         |
   11|{129,129}     |
    2|{129,135}     |
    1|{129,NUSC}    |
    1|{129,NUSN}    |
  448|{133}         |
    1|{133,133}     |
 3694|{135}         |
   45|{135,135}     |
    1|{135,ARMF}    |
 4697|{137}         |
   30|{137,137}     |
    1|{137,ARMF}    |
    1|{437}         |
   10|{ARMF}        |
    1|{ARMF,ARMF}   |
 1507|{NUSC}        |
   23|{NUSC,NUSC}   |
    8|{NUSC,NUSN}   |
    1|{NUSC,PUBU}   |
 2245|{NUSN}        |
   26|{NUSN,NUSN}   |
  553|{PUBU}        |
    3|{PUBU,PUBU}   |
    1|{PUBU,UNK}    |
  437|{UNK}         |
    7|{UNK,UNK}     |
    1|{UNK,UNK,UNK} |
```

### 2.2 Fatalities since 1982

```sql
SELECT count(*),
       far_part
  FROM io_app_ae1982
 WHERE ev_year >= 1982
   AND inj_tot_f > 0 
 GROUP BY far_part
 ORDER BY 1 DESC,
          2
```

```
count|far_part     |
-----+-------------+
13210|{091}        |
 1376|{NUSN}       |
  781|{135}        |
  442|{137}        |
  421|{NUSC}       |
  264|{091,091}    |
  258|{}           |
  192|{UNK}        |
  115|{PUBU}       |
  103|{129}        |
   98|{121}        |
   93|{133}        |
   90|{103}        |
   25|{NUSN,NUSN}  |
   22|{091,135}    |
   17|{137,137}    |
    8|{091,ARMF}   |
    7|{091F}       |
    6|{135,135}    |
    4|{125}        |
    4|{ARMF}       |
    4|{NUSC,NUSN}  |
    4|{UNK,UNK}    |
    3|{091,121}    |
    3|{091,PUBU}   |
    3|{NUSC,NUSC}  |
    1|{091,091,091}|
    1|{091,091F}   |
    1|{091,103}    |
    1|{091,129}    |
    1|{091,NUSC}   |
    1|{091,NUSN}   |
    1|{091,UNK}    |
    1|{103,103}    |
    1|{103,135}    |
    1|{121,121}    |
    1|{121,135}    |
    1|{129,129}    |
    1|{129,NUSN}   |
    1|{135,ARMF}   |
    1|{437}        |
    1|{PUBU,PUBU}  |
    1|{PUBU,UNK}   |
```

### 2.3 Fatalities since 2008

```sql
SELECT count(*),
       far_part
  FROM io_app_ae1982
 WHERE ev_year >= 2008
   AND inj_tot_f > 0 
 GROUP BY far_part
 ORDER BY 1 DESC,
          2
```

```
count|far_part     |
-----+-------------+
 3228|{091}        |
  953|{NUSN}       |
  258|{}           |
  212|{NUSC}       |
  170|{UNK}        |
  129|{135}        |
  113|{137}        |
   53|{091,091}    |
   43|{PUBU}       |
   25|{133}        |
   22|{129}        |
   14|{NUSN,NUSN}  |
    9|{121}        |
    5|{091,135}    |
    4|{137,137}    |
    4|{UNK,UNK}    |
    3|{135,135}    |
    2|{125}        |
    2|{ARMF}       |
    2|{NUSC,NUSC}  |
    2|{NUSC,NUSN}  |
    1|{091,091,091}|
    1|{091,ARMF}   |
    1|{103,135}    |
    1|{129,NUSN}   |
    1|{437}        |
    1|{PUBU,PUBU}  |
    1|{PUBU,UNK}   |
```
