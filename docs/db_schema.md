# IO-AVSTATS - Data - PostgreSQL Database Schema

The part of the PostgreSQL database schema derived from the Microsoft Acess database is created according to the following rules:

1. The definitions of the legacy database tables and the empty database tables are not included. 
2. All table names and column names are transferred with lowercase letters.
3. The primary keys and the foreign keys are created based on the document `eadmspub.pdf`.
4. The data types are converted as defined in the following table:

| MS Access   | PostgreSQL |
|-------------|------------|
| bit         | boolean    |
| byte        | smallint   |
| datetime    | timestamp  |
| double      | float      |
| integer     | int        |
| longchar    | text       |
