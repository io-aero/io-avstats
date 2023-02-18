# Fatalities by FAR Operations Parts

**Important**: All statistics provided below are based on NTSB data as of February 1, 2023 (period 2008 to 2023).

## 1. Data Basis

- In the database table **aircraft** there is the column **far_part** which contains the FAR operations parts.
- In the database table **events** there is a column **inj_tot_f** which contains the number of fatalities per event.
- Several FAR operations parts can be assigned to the same event, depending on the number of aircraft involved. However, this is only critical if the FAR operation parts are different.

## 2. Results 

### 2.1 Events

| Source                          | FAR parts 091x | FAR parts 121 | FAR parst 135 |
|---------------------------------|---------------:|--------------:|--------------:|
| NTSB avall.mdb                  |          3'303 |             9 |           139 |
| IO-Aero's IO-AVSTATS-DB         |          3'297 |             9 |           139 |
| IO-Aero's DB view io_app_ae1982 |          3'297 |             9 |           139 |


### 2.2 Fatalities

| Source                          | FAR parts 091x | FAR parts 121 | FAR parst 135 |
|---------------------------------|---------------:|--------------:|--------------:|
| NTSB avall.mdb                  |          5'519 |            68 |           403 |
| IO-Aero's IO-AVSTATS-DB         |          5'511 |            68 |           403 |
| IO-Aero's DB view io_app_ae1982 |          5'511 |            68 |           403 |
| IO-Aero's application ae1982    |          5'511 |            68 |           403 |

### 2.3 Possible double counting since 2008 as of 02/01/2013

```
ev_id         |ev_year|aircraft_key|far_part|inj_tot_f|
--------------+-------+------------+--------+---------+
20090808X42846|   2009|           1|091     |        9|
20090808X42846|   2009|           2|135     |        9|
20160831X62719|   2016|           1|135     |        5|
20160831X62719|   2016|           2|091     |        5|
20180614X22730|   2018|           1|091     |        1|
20180614X22730|   2018|           2|135     |        1|
20200731X11938|   2020|           1|135     |        7|
20200731X11938|   2020|           2|091     |        7|
20200827X15154|   2020|           1|135     |        2|
20200827X15154|   2020|           2|091     |        2|
```

### 2.4 All possible double counting as of 02/01/2013

```
ev_id         |ev_year|aircraft_key|far_part|inj_tot_f|
--------------+-------+------------+--------+---------+
20001206X01819|   1994|           1|091     |        1|
20001206X01819|   1994|           2|PUBU    |        1|
20001206X02586|   1994|           1|121     |        2|
20001206X02586|   1994|           2|091     |        2|
20001207X03733|   1995|           1|PUBU    |        3|
20001207X03733|   1995|           2|091     |        3|
20001208X07015|   1996|           1|135     |       14|
20001208X07015|   1996|           2|091     |       14|
20001211X09562|   1998|           1|091     |        1|
20001211X09562|   1998|           2|ARMF    |        1|
20001211X09966|   1998|           1|135     |        2|
20001211X09966|   1998|           2|091     |        2|
20001211X10541|   1998|           1|NUSC    |       15|
20001211X10541|   1998|           2|NUSN    |       15|
20001211X10789|   1998|           1|135     |        2|
20001211X10789|   1998|           2|091     |        2|
20001211X14946|   1992|           1|091     |        3|
20001211X14946|   1992|           2|135     |        3|
20001211X15767|   1992|           1|091     |        4|
20001211X15767|   1992|           2|NUSN    |        4|
20001212X16433|   1991|           1|121     |       34|
20001212X16433|   1991|           2|135     |       34|
20001212X16772|   1991|           1|091     |        7|
20001212X16772|   1991|           2|135     |        7|
20001212X19383|   1999|           1|091     |        3|
20001212X19383|   1999|           2|103     |        3|
20001212X20487|   2000|           1|091     |        1|
20001212X20487|   2000|           2|135     |        1|
20001212X21702|   2000|           1|135     |       11|
20001212X21702|   2000|           2|091     |       11|
20001212X22400|   1990|           1|091     |        1|
20001212X22400|   1990|           2|121     |        1|
20001212X22846|   1990|           1|135     |        2|
20001212X22846|   1990|           2|091     |        2|
20001212X23626|   1990|           1|091     |        3|
20001212X23626|   1990|           2|135     |        3|
20001213X25587|   1988|           1|091     |        4|
20001213X25587|   1988|           2|135     |        4|
20001213X28828|   1989|           1|091     |        2|
20001213X28828|   1989|           2|135     |        2|
20001213X30060|   1987|           1|135     |       10|
20001213X30060|   1987|           2|091     |       10|
20001213X30061|   1987|           1|091     |        6|
20001213X30061|   1987|           2|ARMF    |        6|
20001213X30961|   1987|           1|091     |        4|
20001213X30961|   1987|           2|ARMF    |        4|
20001213X31929|   1987|           1|091     |        2|
20001213X31929|   1987|           2|135     |        2|
20001213X34444|   1986|           1|129     |       82|
20001213X34444|   1986|           2|091     |       82|
20001213X35041|   1986|           1|091     |        2|
20001213X35041|   1986|           2|135     |        2|
20001213X35148|   1986|           1|091     |        1|
20001213X35148|   1986|           2|121     |        1|
20001214X36453|   1985|           1|091     |        1|
20001214X36453|   1985|           2|ARMF    |        1|
20001214X36733|   1985|           1|135     |        1|
20001214X36733|   1985|           2|ARMF    |        1|
20001214X38212|   1985|           1|091F    |        6|
20001214X38212|   1985|           2|091     |        6|
20001214X40665|   1984|           1|135     |       17|
20001214X40665|   1984|           2|091     |       17|
20001214X41935|   1983|           1|091     |        7|
20001214X41935|   1983|           2|ARMF    |        7|
20001214X43900|   1983|           1|135     |        4|
20001214X43900|   1983|           2|091     |        4|
20010914X01949|   2001|           1|PUBU    |        2|
20010914X01949|   2001|           2|091     |        2|
20020104X00034|   2001|           1|NUSN    |      118|
20020104X00034|   2001|           2|NUSC    |      118|
20020322X00392|   2002|           1|ARMF    |        1|
20020322X00392|   2002|           2|091     |        1|
20020917X02154|   1982|           1|UNK     |        6|
20020917X02154|   1982|           2|091     |        6|
20050126X00109|   2005|           1|ARMF    |        1|
20050126X00109|   2005|           2|091     |        1|
20050810X01200|   2005|           1|091     |        2|
20050810X01200|   2005|           2|135     |        2|
20061002X01435|   2006|           1|NUSC    |      154|
20061002X01435|   2006|           2|091     |      154|
20090808X42846|   2009|           1|091     |        9|
20090808X42846|   2009|           2|135     |        9|
20111004X45824|   2011|           1|NUSN    |        1|
20111004X45824|   2011|           2|        |        1|
20150707X22207|   2015|           1|091     |        2|
20150707X22207|   2015|           2|ARMF    |        2|
20160831X62719|   2016|           1|135     |        5|
20160831X62719|   2016|           2|091     |        5|
20180107X10632|   2017|           1|NUSN    |        1|
20180107X10632|   2017|           2|NUSC    |        1|
20180614X22730|   2018|           1|091     |        1|
20180614X22730|   2018|           2|135     |        1|
20180804X53521|   2018|           1|UNK     |        1|
20180804X53521|   2018|           2|PUBU    |        1|
20190826X90719|   2019|           1|NUSC    |        7|
20190826X90719|   2019|           2|NUSN    |        7|
20200731X11938|   2020|           1|135     |        7|
20200731X11938|   2020|           2|091     |        7|
20200827X15154|   2020|           1|135     |        2|
20200827X15154|   2020|           2|091     |        2|
20210715103483|   2020|           1|NUSN    |        5|
20210715103483|   2020|           2|129     |        5|
20211221104432|   2021|           1|135     |        2|
20211221104432|   2021|           2|103     |        2|
```

## 3. NTSB DB avall.mdb

### 3.1 Database table events

```
Number events:      25'182
Number fatalities:  14'649

SELECT count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM events e

ev_year	events	fatalities
2008	1893	1201
2009	1784	1184
2010	1786	1370
2011	1850	 931
2012	1835	1035
2013	1561	 822
2014	1535	1428
2015	1582	1101
2016	1665	 820
2017	1638	 640
2018	1685	1044
2019	1625	 964
2020	1396	 776
2021	1642	 643
2022	1637	 673
2023	  68	  17
```

### 3.2 Database table aircraft

```
Number aircraft:    25'448 

far_part    no_aircraft_1    no_aircraft_2    no_aircraft_3  
              678             17
091         18329            226                2
091K           14
103             2              1
107             4              3
121           694             49
125             5
129           256             14
133           108
135           748             20
137          1011             10
437             1
ARMF            8              4
NUSC         1045             25
NUSN         1635             19
PUBU          251              6
UNK           385             11                1

select far_part,
       count(*) as no_aircraft_1
from aircraft
where aircraft_key = 1
group by far_part
order by far_part

ev_id           ev_year aircraft_key    far_part    inj_tot_f
20090808X42846  2009    1               091         9
20090808X42846  2009    2               135         9
20160831X62719  2016    1               135         5
20160831X62719  2016    2               091         5
20180614X22730  2018    1               091         1
20180614X22730  2018    2               135         1
20200731X11938  2020    1               135         7
20200731X11938  2020    2               091         7
20200827X15154  2020    1               135         2
20200827X15154  2020    2               091         2

select events.ev_id,
       ev_year,
       aircraft_key,
       far_part,
       inj_tot_f
from events
         inner join aircraft on events.ev_id = aircraft.ev_id
where events.ev_id in
      (select ev_id from aircraft where aircraft_key > 1 and far_part in ('091', '091K', '121', '135'))
  and far_part in ('091', '091K', '121', '135')
  and inj_tot_f > 0
  and events.ev_id in (select ev_id
                       from aircraft
                       where far_part in ('091', '091K', '121', '135')
                       group by ev_id, far_part
                       having count(*) = 1)
order by events.ev_id,
         ev_year,
         aircraft_key
```

### 3.3 Number events by selected FAR operations parts

```
events  far_part
3303    091
   9    121
 139    135
 
select count(*) as events,
       far_part
from (select distinct events.ev_id,
                      far_part
      from events
               inner join aircraft on events.ev_id = aircraft.ev_id
      where inj_tot_f > 0
        and far_part in ('091', '091K', '121', '135'))
group by far_part
order by far_part
```

### 3.4 Number fatalities by selected FAR operations parts

```
**** 
fatalities  far_part
5519        091
  68        121
 403        135
 
select sum(inj_tot_f) as fatalities,
       far_part
from (select distinct events.ev_id,
                      far_part,
                      inj_tot_f
      from events
               inner join aircraft on events.ev_id = aircraft.ev_id
      where inj_tot_f > 0
        and far_part in ('091', '091K', '121', '135'))
group by far_part
order by far_part
```

<div style="page-break-after: always;"></div>

## 4. IO-Aero Database IO-AVSTATS-DB

### 4.1 Database table events

```
Number events:      25'143
Number fatalities:  14'645

SELECT count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM events e
WHERE ev_year >= 2008

ev_year|events|fatalities|
-------+------+----------+
   2008|  1893|      1201|
   2009|  1784|      1184|
   2010|  1786|      1370|
   2011|  1850|       931|
   2012|  1835|      1035|
   2013|  1561|       822|
   2014|  1535|      1428|
   2015|  1582|      1101|
   2016|  1665|       820|
   2017|  1638|       640|
   2018|  1685|      1044|
   2019|  1625|       964|
   2020|  1396|       776|
   2021|  1642|       643|
   2022|  1630|       672|
   2023|    36|        14|
   
SELECT ev_year,
       count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM events e
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year   
```

### 4.2 Database table aircraft

```
Number aircraft:    25'542 

SELECT count(*)
FROM aircraft
WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)

far_part|no_aircraft_1|no_aircraft_2|no_aircraft_3|
--------+-------------+-------------+-------------+
        |          687|           17|            0|
091     |        18294|          226|            2|
091K    |           14|            0|            0|
103     |            2|            1|            0|
107     |            4|            3|            0|
121     |          692|           48|            0|
125     |            5|            0|            0|
129     |          253|           14|            0|
133     |          107|            0|            0|
135     |          748|           20|            0|
137     |         1011|           10|            0|
437     |            1|            0|            0|
ARMF    |            8|            4|            0|
NUSC    |         1041|           25|            0|
NUSN    |         1633|           19|            0|
PUBU    |          251|            6|            0|
UNK     |          384|           11|            1|

select far_part,
       count(*) filter (where aircraft_key = 1) as no_aircraft_1,
       count(*) filter (where aircraft_key = 2) as no_aircraft_2,
       count(*) filter (where aircraft_key = 3) as no_aircraft_3
from aircraft
where ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)
group by far_part
order by far_part NULLS first

ev_id         |ev_year|aircraft_key|far_part|inj_tot_f|
--------------+-------+------------+--------+---------+
20090808X42846|   2009|           1|091     |        9|
20090808X42846|   2009|           2|135     |        9|
20160831X62719|   2016|           1|135     |        5|
20160831X62719|   2016|           2|091     |        5|
20180614X22730|   2018|           1|091     |        1|
20180614X22730|   2018|           2|135     |        1|
20200731X11938|   2020|           1|135     |        7|
20200731X11938|   2020|           2|091     |        7|
20200827X15154|   2020|           1|135     |        2|
20200827X15154|   2020|           2|091     |        2|

select e.ev_id,
       ev_year,
       aircraft_key,
       far_part,
       inj_tot_f
from events e
         inner join aircraft a on e.ev_id = a.ev_id
where e.ev_year >= 2008 AND e.ev_id in
      (select ev_id from aircraft where aircraft_key > 1 and far_part in ('091', '091K', '121', '135'))
  and far_part in ('091', '091K', '121', '135')
  and inj_tot_f > 0
  and e.ev_id in (select ev_id
                       from aircraft
                       where far_part in ('091', '091K', '121', '135')
                       group by ev_id, far_part
                       having count(*) = 1)
order by e.ev_id,
         ev_year,
         aircraft_key
```

### 4.3 Number events by selected FAR operations parts

```
events|far_part|
------+--------+
  3297|091     |
     9|121     |
   139|135     |
   
select count(*) as events,
       far_part
from (select DISTINCT e.ev_id,
                      far_part
      from events e
               inner join aircraft a on e.ev_id = a.ev_id
      where e.ev_year >= 2008
        AND inj_tot_f > 0
        and far_part in ('091', '091K', '121', '135')) ea
group by far_part
order by far_part
```

### 4.4 Number fatalities by selected FAR operations parts

```
fatalities|far_part|
----------+--------+
      5511|091     |
        68|121     |
       403|135     |
       
select sum(inj_tot_f) as fatalities,
       far_part
from (select DISTINCT e.ev_id,
                      far_part,
                      inj_tot_f
      from events e
               inner join aircraft a on e.ev_id = a.ev_id
      where e.ev_year >= 2008
        AND inj_tot_f > 0
        and far_part in ('091', '091K', '121', '135')) ea
group by far_part
order by far_part
```

<div style="page-break-after: always;"></div>

## 5. IO-Aero Database io_app_ae1982

### 5.1 events

```
Number events:      25'143
Number fatalities:  14'645

SELECT count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM io_app_ae1982
WHERE ev_year >= 2008

ev_year|events|fatalities|
-------+------+----------+
   2008|  1893|      1201|
   2009|  1784|      1184|
   2010|  1786|      1370|
   2011|  1850|       931|
   2012|  1835|      1035|
   2013|  1561|       822|
   2014|  1535|      1428|
   2015|  1582|      1101|
   2016|  1665|       820|
   2017|  1638|       640|
   2018|  1685|      1044|
   2019|  1625|       964|
   2020|  1396|       776|
   2021|  1642|       643|
   2022|  1630|       672|
   2023|    36|        14|
   
SELECT ev_year,
       count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM io_app_ae1982
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year   
```

### 5.2 aircraft

```
Number aircraft:

by_aircraft_categories|by_far_parts|
----------------------+------------+
                 25542|       25542| 

SELECT sum(array_length (acft_categories, 1)) by_aircraft_categories,
--     sum(array_length (dest_countries, 1))  by_dest_countries,
--     sum(array_length (dprt_countries, 1))  by_dprt_countries,
       sum(array_length (far_parts, 1))       by_far_parts
--     sum(array_length (oper_countries, 1))  by_oper_countries,
--     sum(array_length (owner_countries, 1)) by_owner_countries,
--     sum(array_length (regis_countries, 1)) by_regis_countries,
--     sum(array_length (regis_nos, 1))       by_regis_nos
FROM io_app_ae1982
WHERE ev_year >= 2008

count|array_length|
-----+------------+
24746|           1|
  395|           2|
    2|           3|
    
SELECT count(*),
       array_length(acft_categories, 1)
FROM io_app_ae1982 iaa
WHERE ev_year >= 2008
GROUP BY array_length(acft_categories, 1)
ORDER BY 2    
```

### 5.3 Number events by selected FAR operations parts

```
far_part_091|far_part_091f|far_part_091k|far_part_091x|far_part_121|far_part_135|
------------+-------------+-------------+-------------+------------+------------+
        3297|            0|            0|         3297|           9|         139|
   
select count(*) FILTER (WHERE '091' = ANY (far_parts))                            AS far_part_091,
       count(*) FILTER (WHERE '091F' = ANY (far_parts))                           AS far_part_091F,
       count(*) FILTER (WHERE '091K' = ANY (far_parts))                           AS far_part_091K,
       count(*) FILTER (WHERE ARRAY ['091', '091F', '091K'] && far_parts::TEXT[]) AS far_part_091x,
       count(*) FILTER (WHERE '121' = ANY (far_parts))                            AS far_part_121,
       count(*) FILTER (WHERE '135' = ANY (far_parts))                            AS far_part_135
from io_app_ae1982
where ev_year >= 2008
  AND inj_tot_f > 0
```

### 5.4 Number fatalities by selected FAR operations parts

```
far_part_091|far_part_091f|far_part_091k|far_part_091x|far_part_121|far_part_135|
------------+-------------+-------------+-------------+------------+------------+
        5511|             |             |         5511|          68|         403|
       
select sum(inj_tot_f) FILTER (WHERE '091' = ANY (far_parts))                            AS far_part_091,
       sum(inj_tot_f) FILTER (WHERE '091F' = ANY (far_parts))                           AS far_part_091F,
       sum(inj_tot_f) FILTER (WHERE '091K' = ANY (far_parts))                           AS far_part_091K,
       sum(inj_tot_f) FILTER (WHERE ARRAY ['091', '091F', '091K'] && far_parts::TEXT[]) AS far_part_091x,
       sum(inj_tot_f) FILTER (WHERE '121' = ANY (far_parts))                            AS far_part_121,
       sum(inj_tot_f) FILTER (WHERE '135' = ANY (far_parts))                            AS far_part_135
from io_app_ae1982
where ev_year >= 2008
  AND inj_tot_f > 0
```

<div style="page-break-after: always;"></div>

## 6. Application ae1982

### 6.1 Bar chart

```
Year    Parts 091x  Parts 121   Parts 135
2008    447          1          69
2009    456         51          17
2010    418          2          17
2011    422          0          41
2012    394          0          12
2013    341          9          30
2014    357          0          20
2015    361          0          28
2016    338          0          27
2017    313          0          16
2018    353          1          16
2019    382          4          34
2020    308          0          26
2021    318          0          32
2022    294          0          18
2023      9          0           0

```

### 6.2 Pie chart

```
FAR 091x     5'511
FAR 121         68
FAR 135        403
```
