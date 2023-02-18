# Events by Highest Injury Level

**Important**: All statistics provided below are based on NTSB data as of February 1, 2023 (period 2008 to 2023).

## 1. Data Basis

- In the database table **events** there is a column **ev_highest_injury** which contains the highest injury level per event. 
- The available database categories are **`FATL`** (fatal injury), **`MINR`** (minor injury), **`NONE`** (no injury) and **`SERS`** (serious injury). 
- If there is no information about the injuries, then the event appears in the category **`OTHR`** (other).

## 2. Results 

### 2.1 Events

| Source                          |  FATL |  MINR |   NONE |  SERS |  OTHR |
|---------------------------------|------:|------:|-------:|------:|------:|
| NTSB avall.mdb                  | 5'320 | 3'375 | 12'716 | 2'771 | 1'000 | 
| IO-Aero's IO-AVSTATS-DB         | 5'317 | 3'372 | 12'689 | 2'764 | 1'001 | 
| IO-Aero's DB view io_app_ae1982 | 5'317 | 3'372 | 12'689 | 2'764 | 1'001 | 
| IO-Aero's application ae1982    | 5'317 | 3'372 | 12'689 | 2'764 | 1'001 | 

<div style="page-break-after: always;"></div>

## 3. NTSB DB avall.mdb

### 3.1 Database table events

```
no   |ev_highest_injury|
-----+-----------------+
 5320|FATL             |
 2771|SERS             |
 3375|MINR             |
12716|NONE             |
 1000|                 |
 
SELECT count(*)           AS no,
       ev_highest_injury  AS "highest_injury"
FROM events e
GROUP BY ev_highest_injury
ORDER BY ev_highest_injury

ev_year	events	FATL	MINR	NONE	NULL	SERS
2008	1893	382		269		1030	 22		190
2009	1784	359		234		 937	 30		224
2010	1786	363		233		 949	 55		186
2011	1850	398		237		 953	 44		218
2012	1835	389		246		 936	 52		212
2013	1561	344		240		 783	 48		146
2014	1535	361		215		 731	 45		183
2015	1582	365		209		 749	 55		204
2016	1665	341		233		 825	 90		176
2017	1638	338		219		 831	 80		170
2018	1685	360		220		 840	 83		182
2019	1625	379		200		 785	 92		169
2020	1396	295		181		 702	 70		148
2021	1642	322		209		 817	119		175
2022	1637	313		224		 814	106		180
2023	  68	 11	  	  6	 	  34	  9	  	  8

select ev_year, count(*) events events
from events
group by ev_year
order by ev_year

select ev_year, count(*) events_fatl
from events
WHERE ev_highest_injury = 'FATL'
group by ev_year
order by ev_year
```

<div style="page-break-after: always;"></div>

## 4. IO-Aero Database IO-AVSTATS-DB

### 4.1 Database table events

```
no   |ev_highest_injury|
-----+-----------------+
 5317|FATL             |
 2764|SERS             |
 3372|MINR             |
12689|NONE             |
 1001|                 |

SELECT count(*)          AS no,
       ev_highest_injury AS "ev_highest_injury"
FROM events e
WHERE ev_year >= 2008
GROUP BY ev_highest_injury
ORDER BY ev_highest_injury NULLS first

ev_year|events|     fatl|     minr|     none|     null|     sers|
-------+------+---------+---------+---------+---------+---------+
   2008|  1893|      382|      269|     1030|       22|      190|
   2009|  1784|      359|      234|      937|       30|      224|
   2010|  1786|      363|      233|      949|       55|      186|
   2011|  1850|      398|      237|      953|       44|      218|
   2012|  1835|      389|      246|      936|       52|      212|
   2013|  1561|      344|      240|      783|       48|      146|
   2014|  1535|      361|      215|      731|       45|      183|
   2015|  1582|      365|      209|      749|       55|      204|
   2016|  1665|      341|      233|      825|       90|      176|
   2017|  1638|      338|      219|      831|       80|      170|
   2018|  1685|      360|      220|      840|       83|      182|
   2019|  1625|      379|      200|      785|       92|      169|
   2020|  1396|      295|      181|      703|       70|      147|
   2021|  1642|      322|      209|      817|      119|      175|
   2022|  1630|      312|      225|      804|      110|      179|
   2023|    36|        9|        2|       16|        6|        3|
   
SELECT ev_year,
       count(*)                                           AS events,
       count(*) filter (where ev_highest_injury = 'FATL') as fatl,
       count(*) filter (where ev_highest_injury = 'MINR') as minr,
       count(*) filter (where ev_highest_injury = 'NONE') as none,
       count(*) filter (where ev_highest_injury is null)  as null,
       count(*) filter (where ev_highest_injury = 'SERS') as sers
FROM events e
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year
```

<div style="page-break-after: always;"></div>

## 5. IO-Aero Database io_app_ae1982

### 5.1 events

```
no   |ev_highest_injury|
-----+-----------------+
 5317|FATL             |
 2764|SERS             |
 3372|MINR             |
12689|NONE             |
 1001|                 |

SELECT count(*)          AS no,
       ev_highest_injury AS "ev_highest_injury"
FROM io_app_ae1982 e
WHERE ev_year >= 2008
GROUP BY ev_highest_injury
ORDER BY ev_highest_injury NULLS first

ev_year|events|fatl|minr|none|null|sers|
-------+------+----+----+----+----+----+
   2008|  1893| 382| 269|1030|  22| 190|
   2009|  1784| 359| 234| 937|  30| 224|
   2010|  1786| 363| 233| 949|  55| 186|
   2011|  1850| 398| 237| 953|  44| 218|
   2012|  1835| 389| 246| 936|  52| 212|
   2013|  1561| 344| 240| 783|  48| 146|
   2014|  1535| 361| 215| 731|  45| 183|
   2015|  1582| 365| 209| 749|  55| 204|
   2016|  1665| 341| 233| 825|  90| 176|
   2017|  1638| 338| 219| 831|  80| 170|
   2018|  1685| 360| 220| 840|  83| 182|
   2019|  1625| 379| 200| 785|  92| 169|
   2020|  1396| 295| 181| 703|  70| 147|
   2021|  1642| 322| 209| 817| 119| 175|
   2022|  1630| 312| 225| 804| 110| 179|
   2023|    36|   9|   2|  16|   6|   3|
   
SELECT ev_year,
       count(*)                                           AS events,
       count(*) filter (where ev_highest_injury = 'FATL') as fatl,
       count(*) filter (where ev_highest_injury = 'MINR') as minr,
       count(*) filter (where ev_highest_injury = 'NONE') as none,
       count(*) filter (where ev_highest_injury is null)  as null,
       count(*) filter (where ev_highest_injury = 'SERS') as sers
FROM io_app_ae1982 e
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year
```

<div style="page-break-after: always;"></div>

## 6. Application ae1982

### 6.1 Bar chart

```
year	Fatal	Serious	Minor	None	Other
2008	382		190		269		1030	 22
2009	359		224		234		 937	 30
2010	363		186		233		 949	 55
2011	398		218		237		 953	 44
2012	389		212		246		 936	 52
2013	344		146		240		 783	 48
2014	361		183		215		 731	 45
2015	365		204		209		 749	 55
2016	341		176		233		 825	 90
2017	338		170		219		 831	 80
2018	360		182		220		 840	 83
2019	379		169		200		 785	 92
2020	295		147		181		 703	 70
2021	322		175		209		 817	119
2022	312		179		225		 804	110
2023	  9		  3		  2		  16	  6
```

### 6.2 Pie chart

```
no   |ev_highest_injury|
-----+-----------------+
 5317|Fatal            |
 2764|Serious          |
 3372|Minor            |
13690|None             |
 1001|Other            |
```
