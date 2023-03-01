# Events by Types

**Important**: All statistics provided below are based on NTSB data as of February 1, 2023 (period 2008 to 2023).

## 1. Data Basis

- In the database table **events** there is a column **ev_type** which contains the type of the event. 
- The available database categories are **`ACC`** (Accident) and **`INC`** (Incident). 
- If there is no information about the event type, then the event appears in the category **`OTH`** (other).

## 2. Results 

### 2.1 Events

| Source                          | events | accidents | incidents |
|---------------------------------|-------:|----------:|----------:|
| NTSB avall.mdb                  | 25'182 |    23'492 |     1'690 |
| IO-Aero's IO-AVSTATS-DB         | 25'143 |    23'458 |     1'685 |
| IO-Aero's DB view io_app_ae1982 | 25'143 |    23'458 |     1'685 |
| IO-Aero's application ae1982    |        |    23'458 |     1'685 |

<div style="page-break-after: always;"></div>

## 3. NTSB DB avall.mdb

### 3.1 Database table events

```
no       ev_type
23'492   ACC
 1'690   INC
25'182 

SELECT count(*) AS no,
       ev_type  AS "ev_type"
FROM events e
GROUP BY ev_type
ORDER BY ev_type

ev_year	events accidents incidents
2008	1893	1790	 103
2009	1784	1681	 103
2010	1786	1648	 138
2011	1850	1732	 118
2012	1835	1717	 118
2013	1561	1462	  99
2014	1535	1451	  84
2015	1582	1488	  94
2016	1665	1542	 123
2017	1638	1514	 124
2018	1685	1565	 120
2019	1625	1504	 121
2020	1396	1309	  87
2021	1642	1522	 120
2022	1637	1507	 130
2023	  68	  60	   8

select ev_year, count(*)
from events
group by ev_year
order by ev_year

select ev_year, count(*)
from events
WHERE ev_type = 'ACC' 
group by ev_year
order by ev_year
```

<div style="page-break-after: always;"></div>

## 4. IO-Aero Database IO-AVSTATS-DB

### 4.1 Database table events

```
no    |ev_type|
------+-------+
23'458|ACC    |
 1'685|INC    |
25'143

SELECT count(*) AS no,
       ev_type  AS "ev_type"
FROM events e
WHERE ev_year >= 2008
GROUP BY ev_type
ORDER BY ev_type

ev_year|events|accidents|incidents|
-------+------+---------+---------+
   2008|  1893|     1790|      103|
   2009|  1784|     1681|      103|
   2010|  1786|     1648|      138|
   2011|  1850|     1732|      118|
   2012|  1835|     1717|      118|
   2013|  1561|     1462|       99|
   2014|  1535|     1451|       84|
   2015|  1582|     1488|       94|
   2016|  1665|     1542|      123|
   2017|  1638|     1514|      124|
   2018|  1685|     1565|      120|
   2019|  1625|     1504|      121|
   2020|  1396|     1309|       87|
   2021|  1642|     1522|      120|
   2022|  1630|     1500|      130|
   2023|    36|       33|        3|
   
SELECT ev_year,
       count(*)                                AS events,
       count(*) filter (where ev_type = 'ACC') as accidents,
       count(*) filter (where ev_type = 'INC') as incidents
FROM events e
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year   
```

<div style="page-break-after: always;"></div>

## 5. IO-Aero Database io_app_ae1982

### 5.1 events

```
no   |ev_type|
-----+-------+
23458|ACC    |
 1685|INC    |

SELECT count(*) AS no,
       ev_type  AS "ev_type"
FROM io_app_ae1982 e
WHERE ev_year >= 2008
GROUP BY ev_type
ORDER BY ev_type

ev_year|events|accidents|incidents|
-------+------+---------+---------+
   2008|  1893|     1790|      103|
   2009|  1784|     1681|      103|
   2010|  1786|     1648|      138|
   2011|  1850|     1732|      118|
   2012|  1835|     1717|      118|
   2013|  1561|     1462|       99|
   2014|  1535|     1451|       84|
   2015|  1582|     1488|       94|
   2016|  1665|     1542|      123|
   2017|  1638|     1514|      124|
   2018|  1685|     1565|      120|
   2019|  1625|     1504|      121|
   2020|  1396|     1309|       87|
   2021|  1642|     1522|      120|
   2022|  1630|     1500|      130|
   2023|    36|       33|        3|
   
SELECT ev_year,
       count(*)                                AS events,
       count(*) filter (where ev_type = 'ACC') as accidents,
       count(*) filter (where ev_type = 'INC') as incidents
FROM io_app_ae1982 e
WHERE ev_year >= 2008
GROUP BY ev_year
ORDER BY ev_year   
```

<div style="page-break-after: always;"></div>

## 6. Application ae1982

### 6.1 Bar chart

```
year	Accident Incident
2008	1790	 103
2009	1681	 103
2010	1648	 138
2011	1732	 118
2012	1717	 118
2013	1462	  99
2014	1451	  84
2015	1488	  94
2016	1542	 123
2017	1514	 124
2018	1565	 120
2019	1504	 121
2020	1309	  87
2021	1522	 120
2022	1500	 130
2023	  33	   3
```

### 6.2 Pie chart

```
Accidents    23'458
Incidents     1'685
```
