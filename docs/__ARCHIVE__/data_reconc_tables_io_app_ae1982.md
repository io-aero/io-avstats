# DB Tables vs. DB View io_app_ae1982

**Important**: All statistics provided below are based on NTSB data as of February 8, 2023 (period 2008 to 2023).

## 1. Events & Fatalities

| Source                | Events | Fatalities |
|-----------------------|-------:|-----------:|
| DB Table events       | 25'176 |     14'655 |
| DB View io_app_ae1982 | 25'176 |     14'655 |

```
SELECT count(*)       AS events,
       sum(inj_tot_f) AS fatalities
FROM events
WHERE ev_year >= 2008
```

## 2 cictt_code

### 2.1 DB tables

```
Number events_sequence: 24'752 

SELECT count(*) AS no_rows
FROM events_sequence e
WHERE defining_ev = TRUE
  AND ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)

Number cictt_codes:     24'752 

SELECT count(*) AS no_rows
FROM events_sequence e
WHERE defining_ev = TRUE
  AND ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)
  AND e.eventsoe_no IN (SELECT eventsoe_no FROM io_sequence_of_events isoe WHERE cictt_code IS NOT null)

cictt_code|sum |
----------+----+
SCF-PP    |4086|
LOC-I     |4031|
LOC-G     |3204|
ARC       |2966|
SCF-NP    |1375|
OTHR      |1348|
FUEL      |1235|
UNK       | 922|
CFIT      | 749|
RE        | 641|
CTOL      | 590|
GCOL      | 457|
LALT      | 373|
MAC       | 352|
USOS      | 289|
F-NI      | 285|
TURB      | 277|
UIMC      | 268|
BIRD      | 168|
RAMP      | 167|
AMAN      | 161|
LOLI      | 156|

SELECT cictt_code,
       sum(no_rows)
FROM (select isoe.cictt_code,
             es.no_rows
      FROM (select es.eventsoe_no,
                   count(*) as no_rows
            from events_sequence es
            where es.defining_ev = TRUE
              AND es.ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)
            group by es.eventsoe_no) es
               INNER JOIN io_sequence_of_events isoe ON es.eventsoe_no = isoe.soe_no) a
GROUP BY cictt_code
HAVING sum(no_rows) >= 100
ORDER BY 2 desc
```


### 2.2 DB view io_app_ae1982

```
Number cictt_codes: 25'256 

SELECT sum(array_length(cictt_codes, 1)) no_cictt_codes
FROM io_app_ae1982 iaa
WHERE ev_year >= 2008

Number cictt_codes 1: 25'096 
Number cictt_codes 2:     80 
Number cictt_codes 3:      0 

SELECT count(*) no_cictt_codes
FROM io_app_ae1982 iaa
WHERE ev_year >= 2008
AND array_length(cictt_codes, 1) = 1

AND array_length(cictt_codes, 1) = 2

AND array_length(cictt_codes, 1) >= 3

cictt_codes|no_rows|
-----------+-------+
{SCF-PP}   |   4073|
{LOC-I}    |   4015|
{LOC-G}    |   3190|
{ARC}      |   2954|
{SCF-NP}   |   1370|
{OTHR}     |   1324|
{FUEL}     |   1226|
{n/a}      |    976|
{UNK}      |    904|
{CFIT}     |    742|
{RE}       |    634|
{CTOL}     |    569|
{LALT}     |    370|
{GCOL}     |    335|
{USOS}     |    288|
{F-NI}     |    284|
{TURB}     |    277|
{UIMC}     |    267|
{MAC}      |    192|
{BIRD}     |    167|
{RAMP}     |    161|
{AMAN}     |    159|
{LOLI}     |    154|

SELECT cictt_codes,
       count(*) AS no_rows
FROM io_app_ae1982 iaa
WHERE ev_year >= 2008
GROUP BY cictt_codes
having count(*) >= 100
ORDER BY 2 desc, 1

cictt_codes    |count|
---------------+-----+
{AMAN,UNK}     |    1|
{ARC,LOC-G}    |    1|
{ARC,OTHR}     |    2|
{ARC,RE}       |    1|
{ATM,MAC}      |    3|
{CTOL,ARC}     |    1|
{CTOL,CFIT}    |    1|
{CTOL,MAC}     |    1|
{CTOL,OTHR}    |    3|
{CTOL,RE}      |    1|
{CTOL,UNK}     |    1|
{FUEL,ATM}     |    1|
{GCOL,AMAN}    |    1|
{GCOL,CTOL}    |    2|
{GCOL,MAC}     |    1|
{GCOL,RAMP}    |    2|
{LALT,CFIT}    |    1|
{LALT,GCOL}    |    1|
{LOC-G,GCOL}   |    6|
{LOC-I,CFIT}   |    1|
{LOC-I,LALT}   |    1|
{LOC-I,LOC-G}  |    1|
{LOC-I,SCF-PP} |    1|
{LOC-I,UNK}    |    6|
{LOLI,CTOL}    |    1|
{LOLI,UNK}     |    1|
{MAC,ADRM}     |    1|
{MAC,LOC-I}    |    1|
{MAC,OTHR}     |    1|
{NAV,LOC-I}    |    1|
{NAV,OTHR}     |    1|
{OTHR,CFIT}    |    2|
{OTHR,F-NI}    |    1|
{OTHR,FUEL}    |    1|
{OTHR,GCOL}    |    2|
{OTHR,LOC-G}   |    2|
{OTHR,LOC-I}   |    1|
{OTHR,RE}      |    1|
{OTHR,SCF-PP}  |    1|
{OTHR,UNK}     |    3|
{RE,LOC-G}     |    3|
{SCF-NP,LOC-I} |    2|
{SCF-NP,RE}    |    1|
{SCF-PP,ARC}   |    1|
{SCF-PP,FUEL}  |    4|
{SCF-PP,SCF-NP}|    1|
{UIMC,GCOL}    |    1|
{UNK,FUEL}     |    2|
{UNK,SCF-PP}   |    2|
{USOS,GCOL}    |    1|

SELECT cictt_codes, count(*)
FROM io_app_ae1982 iaa
WHERE ev_year >= 2008
  AND array_length(cictt_codes, 1) >= 2
GROUP BY cictt_codes
ORDER BY 1
```

<div style="page-break-after: always;"></div>

## 3. NTSB DB avall.mdb

```
Number events_sequence:  24'861

SELECT count(*) AS no_rows
FROM Events_Sequence e
WHERE defining_ev = TRUE

ev_id          ev_year    aircraft_key    eventsoe_no
20080505X00589    2008    1               200
20080505X00589    2008    2               230
20080829X01354    2008    1               260
20080829X01354    2008    2               100
20090202X21409    2009    1               250
20090202X21409    2009    2               490
20091010X63931    2009    1               250
20091010X63931    2009    2               240
20100317X00948    2010    1               260
20100317X00948    2010    2               070
20100704X92306    2010    1               380
20100704X92306    2010    2               200
20100803X25950    2010    1               200
20100803X25950    2010    2               900
20101022X34140    2010    1               190
20101022X34140    2010    2               100
20101022X34140    2010    3               100
20110904X00636    2011    1               250
20110904X00636    2011    2               440
20111019X85758    2011    1               900
20111019X85758    2011    2               260
20120523X33839    2012    1               230
20120523X33839    2012    2               200
20120529X21628    2012    1               230
20120529X21628    2012    2               200
20120705X51659    2012    1               320
20120705X51659    2012    2               900
20120811X13221    2012    1               000
20120811X13221    2012    2               900
20121027X42304    2012    1               230
20121027X42304    2012    2               200
20121118X14342    2012    1               220
20121118X14342    2012    2               200
20140425X84104    2014    1               100
20140425X84104    2014    2               260
20150210X11721    2015    1               230
20150210X11721    2015    2               200
20150416X33824    2015    1               260
20150416X33824    2015    2               320
20150508X60256    2015    1               230
20150508X60256    2015    2               200
20151123X43413    2015    1               200
20151123X43413    2015    2               402
20160413X30204    2016    1               320
20160413X30204    2016    2               100
20160413X94401    2016    1               320
20160413X94401    2016    2               070
20160418X44917    2016    1               100
20160418X44917    2016    2               260
20171019X45158    2017    1               200
20171019X45158    2017    2               490
20180403X00427    2018    1               200
20180403X00427    2018    2               490
20200603X55158    2019    1               080
20200603X55158    2019    2               200
20201023102180    2020    2               230
20201030102217    2020    2               230
20210219102650    2021    2               900
20210311102742    2021    2               333
20210726103541    2021    1               200
20210726103541    2021    2               270
20210822103737    2021    2               333
20220111104514    2022    1               200
20220111104514    2022    2               900
20220309104755    2022    2               240
20220818105763    2022    2               250
20220826105805    2022    2               341
20221121106336    2022    1               200
20221121106336    2022    2               250

select events.ev_id,
       ev_year,
       aircraft_key,
       eventsoe_no
from events
         inner join events_sequence on events.ev_id = events_sequence.ev_id
where events.ev_id in
      (select ev_id from events_sequence where aircraft_key > 1 and defining_ev = True)
  and defining_ev = True
  and events.ev_id in (select ev_id
                       from events_sequence
                       where defining_ev = True
                       group by ev_id, eventsoe_no
                       having count(*) = 1)
order by events.ev_id,
         ev_year,
         aircraft_key
```

<div style="page-break-after: always;"></div>

## 4. IO-Aero Database IO-AVSTATS-DB

```
Number events_sequence:    24'711 

SELECT count(*) AS no_rows
FROM events_sequence e
WHERE defining_ev = TRUE
  AND ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)

Number cictt_codes:    24'711 

SELECT count(*) AS no_rows
FROM events_sequence e
WHERE defining_ev = TRUE
  AND ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)
  AND e.eventsoe_no IN (SELECT eventsoe_no FROM io_sequence_of_events isoe WHERE cictt_code IS NOT null)

cictt_code|sum |
----------+----+
SCF-PP    |4081|
LOC-I     |4028|
LOC-G     |3202|
ARC       |2962|
SCF-NP    |1374|
OTHR      |1342|

SELECT cictt_code,
       sum(no_rows)
FROM (select isoe.cictt_code,
             es.no_rows
      FROM (select es.eventsoe_no,
                   count(*) as no_rows
            from events_sequence es
            where es.defining_ev = TRUE
              AND es.ev_id in (SELECT ev_id FROM events WHERE ev_year >= 2008)
            group by es.eventsoe_no) es
               INNER JOIN io_sequence_of_events isoe ON es.eventsoe_no = isoe.soe_no
      WHERE isoe.cictt_code IN (
                                'ARC', 'LOC-G', 'LOC-I', 'OTHR', 'SCF-NP', 'SCF-PP'
          )) a
GROUP BY cictt_code
ORDER BY 2 desc

ev_year|SCF-PP|
-------+---+
   2008|301|
   2009|277|
   2010|274|
   2011|292|
   2012|292|
   2013|251|
   2014|259|
   2015|277|
   2016|261|
   2017|245|
   2018|247|
   2019|258|
   2020|181|
   2021|339|
   2022|319|
   2023|  8|

SELECT ev_year,
       sum(no_rows)
FROM (select ev_year,
             es.no_rows
      FROM (select e.ev_year,
                   es.eventsoe_no,
                   count(*) as no_rows
            from events_sequence es inner join events e on es.ev_id = e.ev_id
            where es.defining_ev = TRUE
              AND e.ev_year >= 2008
            group by e.ev_year, es.eventsoe_no) es
               INNER JOIN io_sequence_of_events isoe ON es.eventsoe_no = isoe.soe_no
      WHERE isoe.cictt_code = 'SCF-PP') a
GROUP BY ev_year
ORDER BY 2 desc

ev_id         |
--------------+
20220826105805|

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'SCF-PP'

ev_id         |
--------------+
20091010X63931|
20210822103737|
20220309104755|

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'LOC-I'

ev_id         |
--------------+
20080505X00589|
20201023102180|
20201030102217|

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'LOC-G'

ev_id         |
--------------+

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'ARC'  

ev_id         |
--------------+
20210311102742|
20210822103737|

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'SCF-NP'  

ev_id         |
--------------+
20100224X50823|
20100803X25950|
20110830X71207|
20120705X51659|
20120811X13221|
20210219102650|
20220111104514|

SELECT e.ev_id
FROM events e
         INNER JOIN aircraft a ON e.ev_id = a.ev_id
         INNER JOIN events_sequence es ON e.ev_id = es.ev_id AND a.aircraft_key = es.aircraft_key
         INNER JOIN io_sequence_of_events isoe ON isoe.soe_no = es.eventsoe_no
WHERE e.ev_year >= 2008
  AND a.aircraft_key > 1
  AND es.defining_ev = TRUE
  AND isoe.cictt_code = 'OTHR'  
```

<div style="page-break-after: always;"></div>

## 5. IO-Aero Database io_app_ae1982

```
cictt_scf_pp|cictt_loc_i|cictt_loc_g|cictt_arc|cictt_scf_np|cictt_othr|
------------+-----------+-----------+---------+------------+----------+
        4080|       4028|       3201|     2956|        1373|      1340|
        
SELECT count(*) FILTER (WHERE 'SCF-PP' = ANY (cictt_codes)) AS cictt_scf_pp,
       count(*) FILTER (WHERE 'LOC-I'  = ANY (cictt_codes)) AS cictt_loc_i,
       count(*) FILTER (WHERE 'LOC-G'  = ANY (cictt_codes)) AS cictt_loc_g,
       count(*) FILTER (WHERE 'ARC'    = ANY (cictt_codes)) AS cictt_arc,
       count(*) FILTER (WHERE 'SCF-NP' = ANY (cictt_codes)) AS cictt_scf_np,
       count(*) FILTER (WHERE 'OTHR'   = ANY (cictt_codes)) AS cictt_othr
FROM io_app_ae1982

ev_id         |cictt_codes    |
--------------+---------------+
20200808X63356|{SCF-PP,ARC}   |
20210216102634|{SCF-PP,SCF-NP}|
20210218102641|{SCF-PP,FUEL}  |
20210506103043|{SCF-PP,FUEL}  |
20210702103405|{UNK,SCF-PP}   |
20210816103702|{LOC-I,SCF-PP} |
20220815105734|{SCF-PP,FUEL}  |
20220829105808|{OTHR,SCF-PP}  |
20221213106451|{SCF-PP,FUEL}  |

SELECT ev_id,
       cictt_codes
FROM io_app_ae1982
WHERE 'SCF-PP' = ANY (cictt_codes)
  AND array_length(cictt_codes, 1) > 1
ORDER BY 1
```

<div style="page-break-after: always;"></div>

## 6. Application ae1982

### 6.1 Bar chart

```
year    LOC-I    UNK    SCF-PP    CFIT    OTHR    UIMC    SCF-NP
2008    298       9     301       39      173     21      106   
2009    299      22     277       58       99     18       95   
2010    229      33     274       49      216     18       96   
2011    329      30     292       80       71     19      104   
2012    308      37     292       66       66     15      104   
2013    273      33     251       76       49     21       86   
2014    299      52     259       45       42     17       65   
2015    265      74     277       60       39     23       87   
2016    264      91     261       47       58     19       88   
2017    279      77     245       45       44     29       91   
2018    259      94     247       49       57     15      100   
2019    290      69     258       32       53     24       80   
2020    225      86     180       33       58     10       74   
2021    211      99     338       39      139     14       96   
2022    194     107     319       27      170      4       99   
2023      5       4       8        1        5      0        2   
       4027            4079              1339            1373   
```

### 6.2 Pie chart

```
SCF-PP     4'079
LOC-I      4'027
LOC-G      3'201
ARC        2'956
SCF-NP     1'373
OTHR       1'339
```
