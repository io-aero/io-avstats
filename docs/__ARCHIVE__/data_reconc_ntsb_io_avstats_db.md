# Data Analysis: Reconciliation Queries

## IO-AVSTATS-DB

```sql
SELECT 'aircraft'                                                                                      "DB Table",
       (SELECT count(*) FROM aircraft WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM aircraft WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM aircraft)                                                                 "Total"
UNION
SELECT 'dt_aircraft'                                                                                      "DB Table",
       (SELECT count(*) FROM dt_aircraft WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM dt_aircraft WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM dt_aircraft)                                                                 "Total"
UNION
SELECT 'dt_events'                                                                                      "DB Table",
       (SELECT count(*) FROM dt_events WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM dt_events WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM dt_events)                                                                 "Total"
UNION
SELECT 'dt_flight_crew'                                                                                      "DB Table",
       (SELECT count(*) FROM dt_flight_crew WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM dt_flight_crew WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM dt_flight_crew)                                                                 "Total"
UNION
SELECT 'engines'                                                                                      "DB Table",
       (SELECT count(*) FROM engines WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM engines WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM engines)                                                                 "Total"
UNION
SELECT 'events'                                            "DB Table",
       (SELECT count(*) FROM events WHERE ev_year < 2008)  "< 2008",
       (SELECT count(*) FROM events WHERE ev_year >= 2008) ">= 2008",
       (SELECT count(*) FROM events)                       "Total"
union
SELECT 'events_sequence'                                                                                      "DB Table",
       (SELECT count(*) FROM events_sequence WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM events_sequence WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM events_sequence)                                                                 "Total"
union
SELECT 'findings'                                                                                      "DB Table",
       (SELECT count(*) FROM findings WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM findings WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM findings)                                                                 "Total"
union
SELECT 'flight_crew'                                                                                      "DB Table",
       (SELECT count(*) FROM flight_crew WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM flight_crew WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM flight_crew)                                                                 "Total"
union
SELECT 'flight_time'                                                                                      "DB Table",
       (SELECT count(*) FROM flight_time WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM flight_time WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM flight_time)                                                                 "Total"
union
SELECT 'injury'                                                                                      "DB Table",
       (SELECT count(*) FROM injury WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM injury WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM injury)                                                                 "Total"
union
SELECT 'narratives'                                                                                      "DB Table",
       (SELECT count(*) FROM narratives WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM narratives WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM narratives)                                                                 "Total"
union
SELECT 'ntsb_admin'                                                                                      "DB Table",
       (SELECT count(*) FROM ntsb_admin WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM ntsb_admin WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM ntsb_admin)                                                                 "Total"
union
SELECT 'occurrences'                                                                                      "DB Table",
       (SELECT count(*) FROM occurrences WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM occurrences WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM occurrences)                                                                 "Total"
union
SELECT 'seq_of_events'                                                                                      "DB Table",
       (SELECT count(*) FROM seq_of_events WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year < 2008))  "< 2008",
       (SELECT count(*) FROM seq_of_events WHERE ev_id IN (SELECT ev_id FROM events WHERE ev_year >= 2008)) ">= 2008",
       (SELECT count(*) FROM seq_of_events)                                                                 "Total"
ORDER BY 1
```

## NTSB avall and Pre2008

```sql
SELECT 'aircraft' AS db_table,
       count(*)   AS total
FROM aircraft
UNION
SELECT 'dt_aircraft' AS db_table,
       count(*)      AS total
FROM dt_aircraft
UNION
SELECT 'dt_events' AS db_table,
       count(*)    AS total
FROM dt_events
UNION
SELECT 'dt_flight_crew' AS db_table,
       count(*)         AS total
FROM dt_flight_crew
UNION
SELECT 'engines' AS db_table,
       count(*)  AS total
FROM engines
UNION
SELECT 'events' AS db_table,
       count(*) AS total
FROM events
UNION
SELECT 'events_sequence' AS db_table,
       count(*)          AS total
FROM events_sequence
UNION
SELECT 'findings' AS db_table,
       count(*)   AS total
FROM findings
UNION
SELECT 'flight_crew' AS db_table,
       count(*)      AS total
FROM flight_crew
UNION
SELECT 'flight_time' AS db_table,
       count(*)      AS total
FROM flight_time
UNION
SELECT 'injury' AS db_table,
       count(*) AS total
FROM injury
UNION
SELECT 'narratives' AS db_table,
       count(*)     AS total
FROM narratives
UNION
SELECT 'ntsb_admin' AS db_table,
       count(*)     AS total
FROM ntsb_admin
UNION
SELECT 'occurrences' AS db_table,
       count(*)      AS total
FROM occurrences
UNION
SELECT 'seq_of_events' AS db_table,
       count(*)        AS total
FROM seq_of_events
ORDER BY 1
```
