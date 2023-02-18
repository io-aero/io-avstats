# Fatality-related

**Important**: All statistics provided below are based on NTSB data as of February 8, 2023 (period 2008 to 2023).

The following is provided to verify that the numbers between the data taken over from NTSB and the application view io_app_ae1982 are consistent.

## 1. Number of Fatalities

### 1.1 Based on events

#### 1.1.1 DB Table `events`

```
ev_year|fatalities|
-------+----------+
2008   |      1201|
2009   |      1184|
2010   |      1370|
2011   |       931|
2012   |      1035|
2013   |       822|
2014   |      1428|
2015   |      1101|
2016   |       820|
2017   |       640|
2018   |      1044|
2019   |       964|
2020   |       776|
2021   |       643|
2022   |       675|
2023   |        21|
       |     14655|
```

**Applied SQL statement:**

```sql92
SELECT ev_year::text, 
       sum(inj_tot_f) fatalities
  FROM events e
 WHERE ev_year >= 2008
 GROUP BY ROLLUP(ev_year)
 ORDER BY 1
```

#### 1.1.2 DB View `io_app_ae1982`

```
ev_year|fatalities|
-------+----------+
2008   |      1201|
2009   |      1184|
2010   |      1370|
2011   |       931|
2012   |      1035|
2013   |       822|
2014   |      1428|
2015   |      1101|
2016   |       820|
2017   |       640|
2018   |      1044|
2019   |       964|
2020   |       776|
2021   |       643|
2022   |       675|
2023   |        21|
       |     14655|
```

**Applied SQL statement:**

```sql92
SELECT ev_year::text, 
       sum(inj_tot_f) fatalities
  FROM io_app_ae1982 e
 WHERE ev_year >= 2008
 GROUP BY ROLLUP(ev_year)
 ORDER BY 1
```

### 1.2 Based on FAR operations parts

- The number of fatalities are stored in the table `events` in the column `inj_tot_f`.
- The same event in the `events` table is associated with one or more aircraft in the `aircraft` table.
- For the view, this results in multiple fatality counts for events involving multiple aircraft with different FAR operations part.

#### 1.2.1 DB Tables `events` and `aircraft`

```
aircraft_key|far_part|fatalities|
------------+--------+----------+
           1|091     |      5501|
           1|121     |        68|
           1|125     |         4|
           1|129     |        55|
           1|133     |        34|
           1|135     |       393|
           1|137     |       119|
           1|437     |         1|
           1|ARMF    |         7|
           1|n/a     |      1420|
           1|NUSC    |      4185|
           1|NUSN    |      2239|
           1|PUBU    |        83|
           1|UNK     |       543|
           1|        |     14652|
           2|091     |       148|
           2|103     |         2|
           2|129     |         5|
           2|135     |        24|
           2|137     |         5|
           2|ARMF    |         2|
           2|n/a     |        10|
           2|NUSC    |         9|
           2|NUSN    |        52|
           2|PUBU    |         3|
           2|UNK     |        18|
           2|        |       278|
           3|091     |         6|
           3|        |         6|
            |        |     14936|
```

- For event '20220818105763' the first aircraft is missing (see below), so the number of fatalities for `aircraft_key` equal to 1 must be corrected to 14655.

```sql92
SELECT a.aircraft_key ,
       COALESCE(a.far_part, 'n/a') far_part,
       sum(e.inj_tot_f) fatalities
  FROM events e INNER JOIN aircraft a 
                ON e.ev_id = a.ev_id
 WHERE e.ev_year >= 2008
   AND e.inj_tot_f > 0
 GROUP BY ROLLUP (a.aircraft_key,
                  COALESCE(a.far_part, 'n/a'))
 ORDER BY a.aircraft_key,
          COALESCE(a.far_part, 'n/a')
```

```
ev_id         |aircraft_key|far_part|inj_tot_f|
--------------+------------+--------+---------+
20100204X45658|           1|091     |        3|
20100204X45658|           2|091     |        3|
20100204X45658|           3|091     |        3|
20220818105763|           2|091     |        3|
20220818105763|           3|091     |        3|
```

```sql92
SELECT e.ev_id,
       a.aircraft_key ,
       COALESCE (a.far_part ,'n/a') far_part,
       e.inj_tot_f
  FROM events e INNER JOIN aircraft a 
                ON e.ev_id = a.ev_id
 WHERE e.ev_id IN (SELECT e.ev_id
                     FROM events e INNER JOIN aircraft a 
                                   ON e.ev_id = a.ev_id
                     WHERE e.ev_year >= 2008
                       AND e.inj_tot_f > 0
                       AND a.aircraft_key = 3)
 ORDER BY e.ev_id,
          a.aircraft_key
```

#### 1.2.2 DB View `io_app_ae1982`

```
no_aircraft|far_parts  |fatalities|
-----------+-----------+----------+
          1|{091}      |      5358|
          1|{121}      |        68|
          1|{125}      |         4|
          1|{129}      |        55|
          1|{133}      |        34|
          1|{135}      |       363|
          1|{137}      |       114|
          1|{437}      |         1|
          1|{ARMF}     |         7|
          1|{n/a}      |      1411|
          1|{NUSC}     |      4170|
          1|{NUSN}     |      2187|
          1|{PUBU}     |        81|
          1|{UNK}      |       524|
          1|NULL       |     14377|
          2|{091}      |       131|
          2|{091,135}  |        24|
          2|{091,ARMF} |         2|
          2|{103,135}  |         2|
          2|{129,NUSN} |         5|
          2|{135}      |        14|
          2|{137}      |         5|
          2|{n/a}      |         9|
          2|{n/a,NUSN} |         1|
          2|{NUSC}     |         8|
          2|{NUSC,NUSN}|         8|
          2|{NUSN}     |        45|
          2|{PUBU}     |         2|
          2|{PUBU,UNK} |         1|
          2|{UNK}      |        18|
          2|NULL       |       275|
          3|{091}      |         3|
          3|NULL       |         3|
           |NULL       |     14655|
```

- This results in the following 43 fatalities as candidates for double counting in the application:

```
          2|{091,135}  |        24|
          2|{091,ARMF} |         2|
          2|{103,135}  |         2|
          2|{129,NUSN} |         5|
          2|{n/a,NUSN} |         1|
          2|{NUSC,NUSN}|         8|
          2|{PUBU,UNK} |         1|
           |Total      |        43| 
```

```sql92
SELECT no_aircraft ,
       far_parts,
       sum(inj_tot_f) fatalities
  FROM io_app_ae1982 iaa 
 WHERE ev_year >= 2008
   AND inj_tot_f > 0
 GROUP BY ROLLUP (no_aircraft,
                  far_parts)
 ORDER BY no_aircraft,
          far_parts
```

### 1.3 Conclusion

The figures on the number of fatalities are in complete agreement.

<div style="page-break-after: always;"></div>

## 2. FAR Operations Parts

### 2.1 Bar Chart

```
year  below threshold  091  NUSC  NUSN  no data    Total
2008        124        447  462   165     3        1201
2009        104        456  489   144     0        1193
2010        162        418  643   147     0        1370
2011         63        422  253   193     1         932
2012         65        394  383   190     3        1035
2013        119        341   47   158   157         822
2014         38        357  584   139   310        1428
2015         49        361   38   125   530        1103
2016         61        338   39   121   266         825
2017         46        313   56   105   121         641
2018        151        353  396   146     0        1046
2019        106        382  263   220     0         971
2020         83        308  288   111     0         790
2021         88        318   84   146     9         645
2022         68        296  160   134    17         675
2023          0         14    1     2     4          21
Total      1327       5518 4186  2246  1421       14698
Duplicates   18.5       13    4     7     0.5        43 
```

- Contains the expected duplicates from 1.2.2.

### 2.2 Pie Chart

| below threshold | no data |  091 | NUSC | NUSN | Total |
|----------------:|--------:|-----:|-----:|-----:|------:|
|            1327 |    1421 | 5518 | 4186 | 2246 | 14698 |

- Agrees with the bar chart above.

<div style="page-break-after: always;"></div>

## 3. Selected FAR Operations Parts

### 3.1 Bar Chart

```
year  Parts 091x Parts 135 Parts 121      other       Total
2008        447        69         1        684        1201
2009        456        17        51        669        1193
2010        418        17         2        933        1370
2011        422        41         0        468         931
2012        394        12         0        629        1035
2013        341        30         9        442         822
2014        357        20         0       1051        1428
2015        361        28         0        712        1101
2016        338        27         0        460         825
2017        313        16         0        311         640
2018        353        16         1        675        1045
2019        382        34         4        544         964
2020        308        26         0        451         785
2021        318        32         0        293         643
2022        296        18         0        361         675
2023         14         0         0          7          21
Total      5518       403        68       8690       14679
```

- Agrees with the bar chart of 2.1.

### 3.2 Pie Chart

| other | Parts 091x | Parts 121 | Parts 135 | Total |
|------:|-----------:|----------:|----------:|------:|
|  8690 |       5518 |        68 |       403 | 14679 |

- Agrees with the bar chart above.
