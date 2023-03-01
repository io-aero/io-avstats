# Event-related

**Important**: All statistics provided below are based on NTSB data as of February 8, 2023 (period 2008 to 2023).

The following is provided to verify that the numbers between the data taken over from NTSB and the application view io_app_ae1982 are consistent.

## 1. Number of Events

### 1.1 Based on events

#### 1.1.1 DB Tables `events`

```
ev_year|no_rows|
-------+-------+
2008   |   1893|
2009   |   1784|
2010   |   1786|
2011   |   1850|
2012   |   1835|
2013   |   1561|
2014   |   1535|
2015   |   1582|
2016   |   1665|
2017   |   1638|
2018   |   1685|
2019   |   1625|
2020   |   1396|
2021   |   1642|
2022   |   1635|
2023   |     64|
       |  25176|
```

**Applied SQL statement:**

```sql92
SELECT ev_year::text, 
       count(*) no_rows
  FROM events e
 WHERE ev_year >= 2008
 GROUP BY ROLLUP(ev_year)
 ORDER BY 1
```

#### 1.1.2 DB View `io_app_ae1982`

```
ev_year|no_rows|
-------+-------+
2008   |   1893|
2009   |   1784|
2010   |   1786|
2011   |   1850|
2012   |   1835|
2013   |   1561|
2014   |   1535|
2015   |   1582|
2016   |   1665|
2017   |   1638|
2018   |   1685|
2019   |   1625|
2020   |   1396|
2021   |   1642|
2022   |   1635|
2023   |     64|
       |  25176|
```

**Applied SQL statement:**

```sql92
SELECT ev_year::text, 
       count(*) no_rows
  FROM io_app_ae1982 e
 WHERE ev_year >= 2008
 GROUP BY ROLLUP(ev_year)
 ORDER BY 1
```

### 1.2 Based on CICTT codes

- The same event in the `events` table is associated with one or more aircraft in the `aircraft` table.
- The same aircraft in the `aircraft` table can have multiple entries assigned to it in the `events_sequence` table.
- Only the entries in the `events_sequence` table that have the value `true` in the `defining_ev` column and for whose value in the `eventsoe_no` column there is a value in the `cictt_code` column in the `io_sequence_of_events` table are considered.
- Additionally, the same combination `ev_id` and `cictt_code` is considered only once.

#### 1.2.1 DB Tables `events`, `aircraft`, `events_sequence` and `io_sequence_of_events`

```
aircraft_key|cictt_code|events|
------------+----------+------+
           1|ADRM      |    36|
           1|AMAN      |   161|
           1|ARC       |  2966|
           1|ATM       |    70|
           1|BIRD      |   168|
           1|CABIN     |    78|
           1|CFIT      |   749|
           1|CTOL      |   590|
           1|EVAC      |     5|
           1|EXTL      |    24|
           1|F-NI      |   285|
           1|F-POST    |     4|
           1|FUEL      |  1235|
           1|GCOL      |   457|
           1|GTOW      |    14|
           1|ICE       |    31|
           1|LALT      |   373|
           1|LOC-G     |  3202|
           1|LOC-I     |  4029|
           1|LOLI      |   156|
           1|MAC       |   351|
           1|MED       |    26|
           1|n/a       |   157|
           1|NAV       |    39|
           1|OTHR      |  1347|
           1|RAMP      |   167|
           1|RE        |   641|
           1|SCF-NP    |  1373|
           1|SCF-PP    |  4085|
           1|SEC       |    13|
           1|TURB      |   277|
           1|UIMC      |   268|
           1|UNK       |   922|
           1|USOS      |   289|
           1|WILD      |    67|
           1|WSTRW     |    88|
           1|          | 24743|
           2|ADRM      |    12|
           2|AMAN      |     1|
           2|ATM       |    43|
           2|CFIT      |     2|
           2|CTOL      |    25|
           2|FUEL      |     2|
           2|GCOL      |   243|
           2|LALT      |     1|
           2|LOC-G     |     9|
           2|LOC-I     |     3|
           2|MAC       |   337|
           2|n/a       |    31|
           2|OTHR      |    11|
           2|RAMP      |     9|
           2|SCF-NP    |     2|
           2|SCF-PP    |     1|
           2|TURB      |     1|
           2|UIMC      |     1|
           2|UNK       |     1|
           2|USOS      |     2|
           2|          |   737|
           3|ATM       |     2|
           3|FUEL      |     1|
           3|MAC       |     2|
           3|          |     5|
            |          | 25485|
```

- For event '20220818105763' the first aircraft is missing (see below), so the number of fatalities for `aircraft_key` equal to 1 must be corrected to 14655.

```sql92
SELECT a.aircraft_key ,
       COALESCE(isoe.cictt_code, 'n/a') cictt_code,
       count(*) events
  FROM events e LEFT OUTER JOIN aircraft a 
                ON e.ev_id = a.ev_id
                LEFT OUTER JOIN events_sequence es 
                ON e.ev_id = es.ev_id
                LEFT OUTER JOIN io_sequence_of_events isoe 
                ON es.eventsoe_no = isoe.soe_no
 WHERE e.ev_year >= 2008
   AND es.defining_ev = TRUE
 GROUP BY ROLLUP (a.aircraft_key,
                  COALESCE(isoe.cictt_code, 'n/a'))
 ORDER BY a.aircraft_key,
          COALESCE(isoe.cictt_code, 'n/a')
```

```
ev_id         |aircraft_key|far_part|
--------------+------------+--------+
20100204X45658|           1|091     |
20100204X45658|           2|091     |
20100204X45658|           3|091     |
20101022X34140|           1|UNK     |
20101022X34140|           2|UNK     |
20101022X34140|           3|UNK     |
20220818105763|           2|091     |
20220818105763|           3|091     |
```

```sql92
SELECT e.ev_id,
       a.aircraft_key ,
       COALESCE (a.far_part ,'n/a') far_part
  FROM events e INNER JOIN aircraft a 
                ON e.ev_id = a.ev_id
 WHERE e.ev_id IN (SELECT e.ev_id
                     FROM events e INNER JOIN aircraft a 
                                   ON e.ev_id = a.ev_id
                     WHERE e.ev_year >= 2008
                       AND a.aircraft_key = 3)
 ORDER BY e.ev_id,
          a.aircraft_key
```

#### 1.2.2 DB View `io_app_ae1982`

```
no_aircraft|cictt_codes    |events|
-----------+---------------+------+
          1|{}             |   953|
          1|{ADRM}         |    24|
          1|{AMAN}         |   159|
          1|{AMAN,UNK}     |     1|
          1|{ARC}          |  2954|
          1|{ARC,CTOL}     |     1|
          1|{ARC,LOC-G}    |     1|
          1|{ARC,OTHR}     |     2|
          1|{ARC,RE}       |     1|
          1|{ARC,SCF-PP}   |     1|
          1|{ATM}          |    27|
          1|{BIRD}         |   167|
          1|{CABIN}        |    78|
          1|{CFIT}         |   741|
          1|{CFIT,CTOL}    |     1|
          1|{CFIT,LALT}    |     1|
          1|{CFIT,LOC-I}   |     1|
          1|{CFIT,OTHR}    |     2|
          1|{CTOL}         |   557|
          1|{CTOL,LOLI}    |     1|
          1|{CTOL,OTHR}    |     3|
          1|{CTOL,RE}      |     1|
          1|{CTOL,UNK}     |     1|
          1|{EVAC}         |     5|
          1|{EXTL}         |    24|
          1|{F-NI}         |   284|
          1|{F-NI,OTHR}    |     1|
          1|{F-POST}       |     4|
          1|{FUEL}         |  1225|
          1|{FUEL,OTHR}    |     1|
          1|{FUEL,SCF-PP}  |     4|
          1|{FUEL,UNK}     |     2|
          1|{GCOL}         |   213|
          1|{GCOL,RAMP}    |     1|
          1|{GTOW}         |    14|
          1|{ICE}          |    31|
          1|{LALT}         |   370|
          1|{LALT,LOC-I}   |     1|
          1|{LOC-G}        |  3189|
          1|{LOC-G,LOC-I}  |     1|
          1|{LOC-G,OTHR}   |     2|
          1|{LOC-G,RE}     |     3|
          1|{LOC-I}        |  4015|
          1|{LOC-I,NAV}    |     1|
          1|{LOC-I,OTHR}   |     1|
          1|{LOC-I,SCF-NP} |     2|
          1|{LOC-I,SCF-PP} |     1|
          1|{LOC-I,UNK}    |     6|
          1|{LOLI}         |   154|
          1|{LOLI,UNK}     |     1|
          1|{MAC}          |    15|
          1|{MED}          |    26|
          1|{NAV}          |    37|
          1|{NAV,OTHR}     |     1|
          1|{OTHR}         |  1320|
          1|{OTHR,RE}      |     1|
          1|{OTHR,SCF-PP}  |     1|
          1|{OTHR,UNK}     |     2|
          1|{RAMP}         |   157|
          1|{RE}           |   634|
          1|{RE,SCF-NP}    |     1|
          1|{SCF-NP}       |  1370|
          1|{SCF-NP,SCF-PP}|     1|
          1|{SCF-PP}       |  4073|
          1|{SCF-PP,UNK}   |     2|
          1|{SEC}          |    13|
          1|{TURB}         |   276|
          1|{UIMC}         |   267|
          1|{UNK}          |   904|
          1|{USOS}         |   287|
          1|{WILD}         |    67|
          1|{WSTRW}        |    88|
          1|NULL           | 24777|
          2|{}             |    23|
          2|{ADRM}         |     6|
          2|{ADRM,MAC}     |     1|
          2|{AMAN,GCOL}    |     1|
          2|{ATM}          |    21|
          2|{ATM,MAC}      |     3|
          2|{CFIT}         |     1|
          2|{CTOL}         |    12|
          2|{CTOL,GCOL}    |     2|
          2|{CTOL,MAC}     |     1|
          2|{FUEL}         |     1|
          2|{GCOL}         |   122|
          2|{GCOL,LALT}    |     1|
          2|{GCOL,LOC-G}   |     6|
          2|{GCOL,MAC}     |     1|
          2|{GCOL,OTHR}    |     2|
          2|{GCOL,RAMP}    |     1|
          2|{GCOL,UIMC}    |     1|
          2|{GCOL,USOS}    |     1|
          2|{LOC-G}        |     1|
          2|{LOC-I,MAC}    |     1|
          2|{MAC}          |   176|
          2|{MAC,OTHR}     |     1|
          2|{OTHR}         |     4|
          2|{OTHR,UNK}     |     1|
          2|{RAMP}         |     4|
          2|{TURB}         |     1|
          2|{USOS}         |     1|
          2|NULL           |   397|
          3|{ATM,FUEL}     |     1|
          3|{MAC}          |     1|
          3|NULL           |     2|
           |NULL           | 25176|
```

- This results in the following 80 events as candidates for double counting in the application:

```
no_aircraft|cictt_codes    |events|
-----------+---------------+------+
          1|{AMAN,UNK}     |     1|
          1|{ARC,CTOL}     |     1|
          1|{ARC,LOC-G}    |     1|
          1|{ARC,OTHR}     |     2|
          1|{ARC,RE}       |     1|
          1|{ARC,SCF-PP}   |     1|
          1|{CFIT,CTOL}    |     1|
          1|{CFIT,LALT}    |     1|
          1|{CFIT,LOC-I}   |     1|
          1|{CFIT,OTHR}    |     2|
          1|{CTOL,LOLI}    |     1|
          1|{CTOL,OTHR}    |     3|
          1|{CTOL,RE}      |     1|
          1|{CTOL,UNK}     |     1|
          1|{F-NI,OTHR}    |     1|
          1|{FUEL,OTHR}    |     1|
          1|{FUEL,SCF-PP}  |     4|
          1|{FUEL,UNK}     |     2|
          1|{GCOL,RAMP}    |     1|
          1|{LALT,LOC-I}   |     1|
          1|{LOC-G,LOC-I}  |     1|
          1|{LOC-G,OTHR}   |     2|
          1|{LOC-G,RE}     |     3|
          1|{LOC-I,NAV}    |     1|
          1|{LOC-I,OTHR}   |     1|
          1|{LOC-I,SCF-NP} |     2|
          1|{LOC-I,SCF-PP} |     1|
          1|{LOC-I,UNK}    |     6|
          1|{LOLI,UNK}     |     1|
          1|{NAV,OTHR}     |     1|
          1|{OTHR,RE}      |     1|
          1|{OTHR,SCF-PP}  |     1|
          1|{OTHR,UNK}     |     2|
          1|{RE,SCF-NP}    |     1|
          1|{SCF-NP,SCF-PP}|     1|
          1|{SCF-PP,UNK}   |     2|
          2|{ADRM,MAC}     |     1|
          2|{AMAN,GCOL}    |     1|
          2|{ATM,MAC}      |     3|
          2|{CTOL,GCOL}    |     2|
          2|{CTOL,MAC}     |     1|
          2|{GCOL,LALT}    |     1|
          2|{GCOL,LOC-G}   |     6|
          2|{GCOL,MAC}     |     1|
          2|{GCOL,OTHR}    |     2|
          2|{GCOL,RAMP}    |     1|
          2|{GCOL,UIMC}    |     1|
          2|{GCOL,USOS}    |     1|
          2|{LOC-I,MAC}    |     1|
          2|{MAC,OTHR}     |     1|
          2|{OTHR,UNK}     |     1|
          3|{ATM,FUEL}     |     1|
           1|Total         |    55| 
           2|Total         |    24| 
           3|Total         |     1| 
            |Total         |    80| 
```

```sql92
SELECT no_aircraft,
       cictt_codes,
       count(*) events
  FROM io_app_ae1982 iaa 
 WHERE ev_year >= 2008
 GROUP BY ROLLUP (no_aircraft,
                  cictt_codes)
 ORDER BY no_aircraft,
          cictt_codes
```

### 1.3 Conclusion

The figures on the number of events are in complete agreement.

<div style="page-break-after: always;"></div>

## 2. CICTT Code

### 2.1 Bar Chart

```
year  below threshold  ARC        LOC-G      LOC-I      SCF-PP     Total
2008        677        211        218        298        301        1705
2009        667        203        231        299        277        1677
2010        746        215        190        229        274        1654
2011        668        235        212        329        292        1736
2012        666        205        247        308        292        1718
2013        576        194        180        273        251        1474
2014        539        189        182        299        259        1468
2015        647        190        186        265        277        1565
2016        688        217        225        264        261        1655
2017        675        190        242        279        245        1631
2018        739        188        245        259        247        1678
2019        650        186        236        290        258        1620
2020        609        161        211        226        179        1386
2021        691        196        184        210        336        1617
2022        732        178        210        195        319        1634
2023         34          2          4          7         15          62
Total     10004       2960       3203       4030       4083       24280
Duplicates   58          3          6.5        7.5        5          80
```

- Contains the expected duplicates from 1.2.2.

### 2.2 Pie Chart

| below threshold | SCF-PP | LOC-I | LOC-G |  ARC | Total |
|----------------:|-------:|------:|------:|-----:|------:|
|           10004 |   4083 |  4030 |  3203 | 2960 | 24280 |

- Agrees with the bar chart above.

<div style="page-break-after: always;"></div>

## 3. Event Type

Event type evaluations must be identical with event evaluations.

### 3.1 Bar Chart

```
year        Accident    Incident   Total
2008        1790        103        1893
2009        1681        103        1784
2010        1648        138        1786
2011        1732        118        1850
2012        1717        118        1835
2013        1462         99        1561
2014        1451         84        1535
2015        1488         94        1582
2016        1542        123        1665
2017        1514        124        1638
2018        1565        120        1685
2019        1504        121        1625
2020        1309         87        1396
2021        1522        120        1642
2022        1505        130        1635
2023          58          6          64
Total      23488        1688      25176
```

- The figures on the number of events are in complete agreement.

### 3.2 Pie Chart

| Accident | Incident  | Total  |
|---------:|----------:|-------:|
|    23488 |      1688 |  25176 |

- Agrees with the bar chart above.

<div style="page-break-after: always;"></div>

## 4. Highest Injury Level

Highest injury level evaluations must be identical with event evaluations.

### 4.1 Bar Chart

```
 fatal      serious    minor     none   no data       Total 
 382        190        269       1030        22        1893
 359        224        234        937        30        1784
 363        186        233        949        55        1786
 398        218        237        953        44        1850
 389        212        246        936        52        1835
 344        146        240        783        48        1561
 361        183        215        731        45        1535
 365        204        209        749        55        1582
 341        176        233        825        90        1665
 338        170        219        831        80        1638
 360        182        220        840        83        1685
 379        169        200        785        92        1625
 295        147        181        703        70        1396
 322        175        209        817       119        1642
 313        179        224        811       108        1635
  14          4          9         24        13          64
5323       2765       3378      12704      1006       25176
```

### 4.2 Pie Chart

|  none | fatal | minor | serious | no data | Total  |
|------:|------:|------:|--------:|--------:|-------:|
| 12704 |  5323 |  3378 |    2765 |    1006 |  25176 |

- Agrees with the bar chart above.

<div style="page-break-after: always;"></div>

## 5. Required Safety System

Required safety system depends on the following flags:

- is_midair_collision
- is_rss_forced_landing
- is_rss_spin_stall_prevention_and_recovery
- is_rss_terrain_collision_avoidance

Several of these can occur for the same event. This then leads to the multiple counting of an event.
In the category 'no data' the events are listed where none of the flags apply.

```
no_rows|airborne_coll|forced_landing|spin_stall|terrain_coll|
-------+-------------+--------------+----------+------------+
   1098|             |              |          |            |
  13689|             |              |          |true        |
   1002|             |              |true      |true        |
   8466|             |true          |          |true        |
    764|             |true          |true      |true        |
      1|true         |              |          |            |
    137|true         |              |          |true        |
     19|true         |true          |          |true        |
```

```sql92
SELECT count(*)                                  AS no_rows,
       is_midair_collision                       AS airborne_coll,
       is_rss_forced_landing                     AS forced_landing,
       is_rss_spin_stall_prevention_and_recovery AS spin_stall,
       is_rss_terrain_collision_avoidance        AS terrain_coll
FROM io_app_ae1982
WHERE ev_year >= 2008
GROUP BY is_midair_collision,
         is_rss_forced_landing,  
         is_rss_spin_stall_prevention_and_recovery,
         is_rss_terrain_collision_avoidance
ORDER BY 2,3,4,5
```

### 5.1 Bar Chart

```
year    Terrain Coll... Spin Stall...  Forced Landing  Airborne Coll... no data    Total 
2008    1813            112    			663    			13     			80    		2681
2009    1694            128    			676    			12     			90    		2600
2010    1694            109    			658    			11     			92    		2564
2011    1745            138    			675    			11    		   105    		2674
2012    1741            102    			663    			12     			94    		2612
2013    1499            115    			576    			 7     			62    		2259
2014    1476            146    			593    			 8     			59    		2282
2015    1508            139    			651    			13     			74    		2385
2016    1584            143    			661    			13     			81    		2482
2017    1575            141    			618    			 8     			63    		2405
2018    1612            137    			623    			13     			73    		2458
2019    1560            145    			632    			10     			64    		2411
2020    1342             97    			484    			11     			54    		1988
2021    1582             65    			579    			 6     			60    		2292
2022    1588             48    			481    			 7     			47    		2171
2023      64              1    			 16  			 2      		 0      	  83
Total  24077           1766    		   9249    		   157    		  1098    	   36347
```

Since the flagging for the Required safety systems is done only in the view, a reconciliation with the database tables is not possible.
With consideration of this limitation the figures on the number of required safety systems are in complete agreement.

### 5.2 Pie Chart

| Terrain Collision Avoidance | Forced Landing | Spin Stall Prevention and Recovery | no data | Airborne Collision Avoidance | Total |
|----------------------------:|---------------:|-----------------------------------:|--------:|-----------------------------:|------:|
|                       24077 |           9249 |                               1766 |    1098 |                          157 | 36347 |

- Agrees with the bar chart above.

<div style="page-break-after: always;"></div>

## 6. Top Level Logical Parameter

Top level logical parameter depends on the following flags:

- is_altitude_controllable
- is_altitude_low
- is_attitude_controllable
- is_emergency_landing
- is_pilot_issue
- is_spin_stall

Several of these can occur for the same event. This then leads to the multiple counting of an event.
In the category 'no data' the events are listed where none of the flags apply.

```
no_rows|altitude_contr|altitude_low|attitude_contr|emergency_land|pilot_issue|aerodyn_spin_stall|
-------+--------------+------------+--------------+--------------+-----------+------------------+
    889|              |            |              |              |           |                  |
    157|              |            |              |              |           |true              |
     43|              |            |              |              |true       |                  |
     10|              |            |              |              |true       |true              |
    937|              |            |true          |              |           |true              |
     65|              |            |true          |              |true       |true              |
   4549|              |            |true          |true          |           |                  |
    734|              |            |true          |true          |           |true              |
    276|              |            |true          |true          |true       |                  |
     30|              |            |true          |true          |true       |true              |
    321|              |true        |              |              |           |                  |
     17|              |true        |              |              |true       |                  |
   3421|              |true        |true          |true          |           |                  |
    239|              |true        |true          |true          |true       |                  |
   8369|true          |            |true          |              |           |                  |
    783|true          |            |true          |              |true       |                  |
   3485|true          |true        |true          |              |           |                  |
    851|true          |true        |true          |              |true       |                  |
-------+--------------+------------+--------------+--------------+-----------+------------------+
Total  |true          |true        |true          |              |true       |                  |
```

```sql92
SELECT count(*)                 AS no_rows,
       is_altitude_controllable AS altitude_contr,
       is_altitude_low          AS altitude_low,
       is_attitude_controllable AS attitude_contr,
       is_emergency_landing     AS emergency_land,
       is_pilot_issue           AS pilot_issue,
       is_spin_stall            AS aerodyn_spin_stall
FROM io_app_ae1982
WHERE ev_year >= 2008
GROUP BY is_altitude_controllable,
         is_altitude_low,  
         is_attitude_controllable,
         is_emergency_landing,
         is_pilot_issue,
         is_spin_stall
ORDER BY 2,3,4,5,6,7
```

### 6.1 Bar Chart

```
year   Attitude Contr. Aircraft Climb Altitude Too Low Aircraft Degr. Contr    no data  Aerodyn. Spin Stall Pilot Unable    Total
2008   1784        	     1058        	 785        		663        				66        124                 182        4662
2009   1678      		  933        	 603        		676        				72        140                 168        4270
2010   1673     		  948        	 574        		658                     77        120                 127        4177 
2011   1715     		  965        	 578        		675                     90        150                 121        4294
2012   1713      		  994        	 583        		663                     75        115                 128        4271
2013   1471       		  824        	 510        		576                     45        129                 142        3697
2014   1448       		  784        	 537        		593                     49        155                 190        3756
2015   1478      		  765       	 553        		651                     55        155                 130        3787
2016   1562       		  821       	 585        		661                     59        159                 210        4057
2017   1548       		  849        	 631        		618                     52        150                 207        4055
2018   1583       		  874       	 585        		623                     52        155                 192        4064
2019   1544        	      830       	 570        		632                     54        154                 170        3954
2020   1329        	      790       	 427        		484                     47        103                 127        3307
2021   1573        	      948       	 444        		579                     52         72                 137        3805
2022   1576        	     1058       	 360        		481                     43         51                  83        3652
2023     64        	       47        	   9        		 16                      0          1                   0         137
Total 23739        	    13488        	8334               9249                    888       1933                2314       59945
```

Since the flagging for the top level logical parameters is done only in the view, a reconciliation with the database tables is not possible.
With consideration of this limitation the figures on the number of top level logical parameters are in complete agreement.

### 6.2 Pie Chart

| Attitude Contr. | Aircraft Climb | Aircraft Degr. Contr. | Altitude Too Low | Pilot Unable | Aerodyn. Spin Stall | no data  | Total |
|----------------:|---------------:|----------------------:|-----------------:|-------------:|--------------------:|---------:|------:|
|           23739 |          13488 |                  9246 |             8334 |         2314 |                1933 |      888 | 59945 |

- Agrees with the bar chart above.
