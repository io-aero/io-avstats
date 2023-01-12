# How to add NTSB accident files

Aviation accident data provided by NTSB can be found at the following [website](https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx){:target="_blank"} under **Downloadable data sets**:

<kbd>![](img/how_to_add_ntsb_01.png)</kbd>

In the database table **`io_processed_files`** you can find the previously processed files:

<kbd>![](img/io_processed_files.png)</kbd>

Any file can be processed several times with the process described in the following, as long as one processes also afterwards all newer files again.

All necessary processing steps can be executed with the **`run_io_avstats`** script.
The script is available in a version for Windows 10 and 11 cmd and for Ubuntu 22.04 bash shell.

## 1. Quick reference

| No. | Task  | Description                                                    |
|----:|-------|----------------------------------------------------------------|
|   1 | d_n_a | Download a NTSB MS Access database file                        |
|   2 | l_n_a | Load NTSB MS Access database data into PostgreSQL              |
|   3 | d_s_f | Download basic simplemaps files                                |
|   4 | l_s_d | **Optional**: Load simplemaps data into PostgreSQL             |
|   5 |       | Download the ZIP Code Database file                            |
|   6 | l_z_d | **Optional**: Load ZIP Code Database data into PostgreSQL      |
|   7 | l_c_d | **Optional**: Load data from a correction file into PostgreSQL |
|   8 | c_l_l | Correct decimal US latitudes and longitudes                    |
|   9 | v_n_d | Verify selected NTSB data                                      |
|  10 | r_d_s | Refresh the PostgreSQL database schema                         |
|  11 |       | Backup the file directory **`data/postgres`**                  |
|  12 |       | Update the Google Drive                                        |
|  13 |       | Update **IO-AVSTATS** in the IO-Aero cloud                     |

## 2. Detailed description

### 2.1 **`d_n_a`** - Download a NTSB MS Access database file

**Relevant cofiguration parameters**:

```
download_chunk_size = 524288
download_timeout = 10
download_url_ntsb_prefix = "https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5C"
download_work_dir = "data/download"
```

**Example protocol**:

```
Progress update 2023-01-12 08:28:16.570266 : ===============================================================================.
Progress update 2023-01-12 08:28:16.570266 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 08:28:16.572266 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 08:28:16.580766 : INFO.00.008 Arguments task='d_n_a' msaccess='up08JAN'.
Progress update 2023-01-12 08:28:16.580766 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:28:16.580766 : INFO.00.047 Downloading NTSB MS Access database file 'up08JAN'.
Progress update 2023-01-12 08:28:16.580766 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:28:17.146039 : INFO.00.013 The connection to the MS Access database file 'up08JAN.zip' on the NTSB download page was successfully established.
Progress update 2023-01-12 08:28:17.528648 : INFO.00.014 From the file 'up08JAN.zip' 1 chunks were downloaded.
Progress update 2023-01-12 08:28:17.546649 : INFO.00.015 The file 'up08JAN.zip' was successfully unpacked.
Progress update 2023-01-12 08:28:17.557648 : INFO.00.051 msaccess_file='D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\IO-AVSTATS.mdb'.
Progress update 2023-01-12 08:28:17.558149 : INFO.00.051 msaccess_file='D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up08JAN.sql'.
Progress update 2023-01-12 08:28:17.558149 : INFO.00.052 razorsql_jar_file='C:\Program Files\RazorSQL\razorsql.jar'.
Progress update 2023-01-12 08:28:17.558149 : INFO.00.053 razorsql_java_path='C:\Program Files\RazorSQL\jre11\bin\java'.
1673508497647: launching RazorSQL . . .
1673508497648: args . . .
-backup
IO-AVSTATS
null
null
;
null
D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up08JAN.sql
NO
tables
YES
null
NO
NO
1673508497683: userName: walte
1673508497683: libraryPath: C:\Program Files\RazorSQL\jre11\bin;C:\WINDOWS\Sun\Java\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\Users\walte\.virtualenvs\io-avstats-zafInMY1\Scripts;C:\Program Files (x86)\VMware\VMware Player\bin\;C:\Program Files (x86)\infogridpacific\AZARDI;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\Calibre2\;C:\Program Files\dotnet\;C:\Program Files\Git LFS;C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Program Files\Pandoc\;C:\Program Files\TortoiseGit\bin;C:\Software\GnuWin32\bin;C:\WINDOWS;C:\WINDOWS\system32;C:\WINDOWS\System32\OpenSSH\;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Users\walte\.nimble\bin;C:\Windows;C:\Windows\system32;C:\Windows\System32\OpenSSH\;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Software\.cargo\bin;C:\Software\gradle-7.6\bin;%HOME_ELIXIR%\bin;%HOME_ERLANG%\bin;%HOME_GO%\bin;%HOME_JULIA%\bin;%HOME_NIM%\bin;C:\Software\PostgreSQL\15\bin;C:\Software\poppler-0.68.0\bin;C:\Software\Python\Python310;C:\Software\Python\Python310\Scripts;C:\Software\rebar3;%HOME_RUST%\bin;C:\Software\Tesseract-OCR;C:\Software\jdk-19\bin;%KOTLIN_HOME%\bin;C:\Software\oracle\instantclient_21_8;C:\Program Files\LLVM\bin;C:\Program Files\Docker\Docker\resources\bin;C:\Program Files\Amazon\AWSCLIV2\;C:\Program Files\Git\cmd;C:\Program Files\PuTTY\;C:\Software\Gpg4win\..\GnuPG\bin;C:\Program Files\nodejs\;C:\Users\walte\.cargo\bin;C:\Users\walte\AppData\Local\Microsoft\WindowsApps;C:\Software\Microsoft VS Code\bin;C:\Users\walte\go\bin;c:\users\walte\.local\bin;C:\Users\walte\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\walte\AppData\Roaming\npm;.
1673508497684: javaVersion: 11.0.13
1673508497684:
1673508497684: Verifying RazorSQL resources location.
1673508497684:
1673508497685: testing base url: / = file:/C:/Program%20Files/RazorSQL/
1673508497685:
1673508497685: testString1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
1673508497685: testString2: file:/C:/Program%20Files/RazorSQL/data/base.ssql
1673508497685: testFile1: C:\Program Files\RazorSQL\razorsql.jar
1673508497685: testFile2: C:\Program Files\RazorSQL\data\base.ssql
1673508497685: both test file exists.  Base URL found.
1673508497685: resource directory: file:/C:/Program%20Files/RazorSQL/
1673508497686: user home: C:\Users\walte
1673508497687: user profile: C:\Users\walte
1673508497687: app data: C:\Users\walte\AppData\Roaming
1673508497687: checking write access to: C:\Users\walte\AppData\Roaming
1673508497687: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
1673508497688: can write to C:\Users\walte\AppData\Roaming
1673508497688: user.home: C:\Users\walte\AppData\Roaming
1673508497688: RazorSQL Scratch Directory: C:\Users\walte\AppData\Roaming\RazorSQL
1673508497688: RazorSQL Scratch Directory exists
1673508497688: checking for sub directories
1673508497688: razorsql launch log: C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
1673508497688: launch log file = C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
1673508497689: Checking for graphics properties
1673508497689: graphics properties file: C:\Users\walte\AppData\Roaming\RazorSQL\data\graphics_properties.txt
1673508497689: gOverride: null
1673508497689: not disabling advanced graphics
1673508497689: path0: file:/C:/Program%20Files/RazorSQL/data/run.ssql
1673508497689: path1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
1673508497690: runArgs: true
1673508497690: showScreen: false
1673508497690: args[0]: -backup
1673508497690: args[1]: IO-AVSTATS
1673508497690: args[2]: null
1673508497690: args[3]: null
1673508497690: args[4]: ;
1673508497690: args[5]: null
1673508497691: args[6]: D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up08JAN.sql
1673508497691: args[7]: NO
1673508497691: args[8]: tables
1673508497691: args[9]: YES
1673508497691: args[10]: null
1673508497691: args[11]: NO
1673508497691: args[12]: NO
1673508497691: Command: -backup
1673508497691: Running -backup
h: name = C:\Program Files\RazorSQL\data\run.ssql
h: name = C:\Program Files\RazorSQL\razorsql.jar
1673508497698: Attempting to load . . .
command found
uOne: file:/C:/Program%20Files/RazorSQL/
h: name = C:\Program Files\RazorSQL\data\run.ssql
1673508497709reading file . . .C:\Program Files\RazorSQL\data\base.ssql
1673508497735done reading . . .
1673508497745done converting
1673508497745starting lib load.
1673508497757lib load complete.
In command line processor
Max Memory: 30688.0
Current Total Memory: 2048.0
Free Memory: 1957.968734741211
1673508497835: r init
1673508497835: d init
1673508497836: get default file encoding
1673508497836: end d init
custom home directory: null
Checking for user data from old versions
1673508497838: user home: C:\Users\walte
1673508497838: user profile: C:\Users\walte
1673508497838: app data: C:\Users\walte\AppData\Roaming
1673508497838: checking write access to: C:\Users\walte\AppData\Roaming
1673508497838: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
1673508497838: can write to C:\Users\walte\AppData\Roaming
newHome: C:\Users\walte\AppData\Roaming\RazorSQL
dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
Profiles Exist
1673508497849: loading icons
1673508498021: done r init
Getting connection data from: IO-AVSTATS
1673508498023: r init
1673508498023: d init
1673508498023: get default file encoding
1673508498023: end d init
custom home directory: null
Checking for user data from old versions
newHome: C:\Users\walte\AppData\Roaming\RazorSQL
dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
Profiles Exist
1673508498023: loading icons
1673508498032: done r init
getting connection . . .
Not using SSH Tunnel
driver: sun.jdbc.odbc.JdbcOdbcDriver
classLocation: C:\Program Files\RazorSQL\drivers\common\odbc.jar
loadedCommonJars: false
commonURL: file:/C:/Program%20Files/RazorSQL/drivers/common/
commonDir: C:\Program Files\RazorSQL\drivers\common
commonFiles[0]: file:/C:/Program%20Files/RazorSQL/drivers/common/activation.jar
commonFiles[1]: file:/C:/Program%20Files/RazorSQL/drivers/common/common.jar
commonFiles[2]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-api.jar
commonFiles[3]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-core.jar
commonFiles[4]: file:/C:/Program%20Files/RazorSQL/drivers/common/jaxb-impl.jar
commonFiles[6]: file:/C:/Program%20Files/RazorSQL/drivers/common/odbc.jar
connection type: ODBC
final classLocation: C:\Program Files\RazorSQL\drivers\common\odbc.jar
classLocation file: C:\Program Files\RazorSQL\drivers\common\odbc.jar
building sql manager
Loading driver
Done loading driver
Getting connection with no login info
JdbcOdbcDriver: in initialize
OdbcApi == null
Creating new OdbcApi, nativePrefix:
JdbcOdbc constructor
Attempting to load JdbcOdbc library
Got OdbcApi: sun.jdbc.odbc.JdbcOdbc@2d127a61
Getting charset
JdbcOdbcDriver.OdbcApi.charSet: Cp1252
Connection obtained
obtained connection
database major version = 2
database product name: ACCESS
multiValueInsert: false
includeIdentifyColumns: false
Calling backup . . .
Retrieving Tables . . .
Generating Table DDL . . .
1 of 20
number of columns 93
column map size: 93
foundNull: false
2 of 20
number of columns 2
column map size: 2
foundNull: false
3 of 20
number of columns 11
column map size: 11
foundNull: false
4 of 20
number of columns 2
column map size: 2
foundNull: false
5 of 20
number of columns 6
column map size: 6
foundNull: false
6 of 20
number of columns 5
column map size: 5
foundNull: false
7 of 20
number of columns 7
column map size: 7
foundNull: false
8 of 20
number of columns 13
column map size: 13
foundNull: false
9 of 20
number of columns 17
column map size: 17
foundNull: false
10 of 20
number of columns 73
column map size: 73
foundNull: false
11 of 20
number of columns 10
column map size: 10
foundNull: false
12 of 20
number of columns 13
column map size: 13
foundNull: false
13 of 20
number of columns 33
column map size: 33
foundNull: false
14 of 20
number of columns 8
column map size: 8
foundNull: false
15 of 20
number of columns 7
column map size: 7
foundNull: false
16 of 20
number of columns 8
column map size: 8
foundNull: false
17 of 20
number of columns 5
column map size: 5
foundNull: false
18 of 20
number of columns 8
column map size: 8
foundNull: false
19 of 20
number of columns 11
column map size: 11
foundNull: false
20 of 20
number of columns 3
column map size: 3
foundNull: false
Generating Alter Table DDL . . .
1 of 20
2 of 20
3 of 20
4 of 20
5 of 20
6 of 20
7 of 20
8 of 20
9 of 20
10 of 20
11 of 20
12 of 20
13 of 20
14 of 20
15 of 20
16 of 20
17 of 20
18 of 20
19 of 20
20 of 20
backup finished
closing connection . . .
connection closed.
Shutting down logging streams
Done shutting down logging streams
Exiting . . .
Progress update 2023-01-12 08:28:18.589894 : INFO.00.011 The DDL script for the MS Access database 'up08JAN.mdb' was created successfully.
Progress update 2023-01-12 08:28:18.594395 : INFO.00.012 The DDL script for the MS Access database 'up08JAN.mdb' is identical to the reference script.
Progress update 2023-01-12 08:28:18.594395 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:28:18.594395 :        2,140,628,800 ns - Total time launcher.
Progress update 2023-01-12 08:28:18.594395 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 08:28:18.594395 : ===============================================================================.
```

### 2.2 **`l_n_a`** - Load NTSB MS Access database data into PostgreSQL

**Relevant cofiguration parameters**:

```
download_work_dir = "data/download"
```

**Example protocol**:

```
Progress update 2023-01-12 08:48:38.901504 : ===============================================================================.
Progress update 2023-01-12 08:48:38.901504 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 08:48:38.903505 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 08:48:38.912005 : INFO.00.008 Arguments task='l_n_a' msaccess='up08JAN'.
Progress update 2023-01-12 08:48:38.912005 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:48:38.912005 : INFO.00.049 Loading NTSB MS Access database data from file 'up08JAN'.
Progress update 2023-01-12 08:48:38.912505 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:48:38.912505 : INFO.00.054 ODBC driver='DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up08JAN.mdb;'.
Progress update 2023-01-12 08:48:39.082506 : INFO.00.021 The following database table is not processed: 'MSysAccessObjects'.
Progress update 2023-01-12 08:48:39.083005 : INFO.00.021 The following database table is not processed: 'MSysACEs'.
Progress update 2023-01-12 08:48:39.083005 : INFO.00.021 The following database table is not processed: 'MSysIMEXColumns'.
Progress update 2023-01-12 08:48:39.083005 : INFO.00.021 The following database table is not processed: 'MSysIMEXSpecs'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysModules2'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroupCategories'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroups'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroupToObjects'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysNavPaneObjectIDs'.
Progress update 2023-01-12 08:48:39.083506 : INFO.00.021 The following database table is not processed: 'MSysObjects'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'MSysQueries'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'MSysRelationships'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'Country'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'ct_iaids'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'ct_seqevt'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'eADMSPUB_DataDictionary'.
Progress update 2023-01-12 08:48:39.084005 : INFO.00.021 The following database table is not processed: 'states'.
Progress update 2023-01-12 08:48:39.084506 :
Progress update 2023-01-12 08:48:39.084506 : Database table       : events              <-----------------------------------.
Progress update 2023-01-12 08:48:40.440649 : Number rows selected :     43.
Progress update 2023-01-12 08:48:40.440649 : Number rows inserted :     25.
Progress update 2023-01-12 08:48:40.440649 : Number rows updated  :     18.
Progress update 2023-01-12 08:48:40.441148 :
Progress update 2023-01-12 08:48:40.441148 : Database table       : aircraft            <-----------------------------------.
Progress update 2023-01-12 08:48:42.847990 : Number rows selected :     45.
Progress update 2023-01-12 08:48:42.848502 : Number rows inserted :     26.
Progress update 2023-01-12 08:48:42.848502 : Number rows updated  :     19.
Progress update 2023-01-12 08:48:42.848502 :
Progress update 2023-01-12 08:48:42.848502 : Database table       : dt_events           <-----------------------------------.
Progress update 2023-01-12 08:48:46.705623 : Number rows selected :    121.
Progress update 2023-01-12 08:48:46.706125 : Number rows inserted :     99.
Progress update 2023-01-12 08:48:46.706125 : Number rows updated  :     22.
Progress update 2023-01-12 08:48:46.706125 :
Progress update 2023-01-12 08:48:46.706125 : Database table       : ntsb_admin          <-----------------------------------.
Progress update 2023-01-12 08:48:47.929869 : Number rows selected :     43.
Progress update 2023-01-12 08:48:47.930382 : Number rows inserted :     25.
Progress update 2023-01-12 08:48:47.930382 : Number rows updated  :     18.
Progress update 2023-01-12 08:48:47.930382 :
Progress update 2023-01-12 08:48:47.930382 : Database table       : dt_aircraft         <-----------------------------------.
Progress update 2023-01-12 08:48:52.845636 : Number rows selected :    184.
Progress update 2023-01-12 08:48:52.845636 : Number rows inserted :    135.
Progress update 2023-01-12 08:48:52.846137 : Number rows updated  :     49.
Progress update 2023-01-12 08:48:52.846137 :
Progress update 2023-01-12 08:48:52.846137 : Database table       : engines             <-----------------------------------.
Progress update 2023-01-12 08:48:52.987200 : Number rows selected :      5.
Progress update 2023-01-12 08:48:52.987200 : Number rows inserted :      5.
Progress update 2023-01-12 08:48:52.987200 :
Progress update 2023-01-12 08:48:52.987700 : Database table       : events_sequence     <-----------------------------------.
Progress update 2023-01-12 08:48:54.411812 : Number rows selected :     55.
Progress update 2023-01-12 08:48:54.411812 : Number rows inserted :     36.
Progress update 2023-01-12 08:48:54.411812 : Number rows updated  :     19.
Progress update 2023-01-12 08:48:54.412313 :
Progress update 2023-01-12 08:48:54.412313 : Database table       : findings            <-----------------------------------.
Progress update 2023-01-12 08:48:54.412313 : Number rows selected :      0.
Progress update 2023-01-12 08:48:54.412814 :
Progress update 2023-01-12 08:48:54.412814 : Database table       : flight_crew         <-----------------------------------.
Progress update 2023-01-12 08:48:54.603417 : Number rows selected :      7.
Progress update 2023-01-12 08:48:54.603417 : Number rows inserted :      7.
Progress update 2023-01-12 08:48:54.603917 :
Progress update 2023-01-12 08:48:54.603917 : Database table       : injury              <-----------------------------------.
Progress update 2023-01-12 08:48:58.010842 : Number rows selected :    130.
Progress update 2023-01-12 08:48:58.010842 : Number rows inserted :     82.
Progress update 2023-01-12 08:48:58.011343 : Number rows updated  :     48.
Progress update 2023-01-12 08:48:58.011343 :
Progress update 2023-01-12 08:48:58.011343 : Database table       : narratives          <-----------------------------------.
Progress update 2023-01-12 08:48:58.377303 : Number rows selected :     11.
Progress update 2023-01-12 08:48:58.377803 : Number rows inserted :      6.
Progress update 2023-01-12 08:48:58.377803 : Number rows updated  :      5.
Progress update 2023-01-12 08:48:58.377803 :
Progress update 2023-01-12 08:48:58.377803 : Database table       : occurrences         <-----------------------------------.
Progress update 2023-01-12 08:48:58.378304 : Number rows selected :      0.
Progress update 2023-01-12 08:48:58.378304 :
Progress update 2023-01-12 08:48:58.378304 : Database table       : dt_flight_crew      <-----------------------------------.
Progress update 2023-01-12 08:48:59.251969 : Number rows selected :     31.
Progress update 2023-01-12 08:48:59.252469 : Number rows inserted :     31.
Progress update 2023-01-12 08:48:59.252469 :
Progress update 2023-01-12 08:48:59.252469 : Database table       : flight_time         <-----------------------------------.
Progress update 2023-01-12 08:49:00.726981 : Number rows selected :     55.
Progress update 2023-01-12 08:49:00.726981 : Number rows inserted :     55.
Progress update 2023-01-12 08:49:00.727478 :
Progress update 2023-01-12 08:49:00.727478 : Database table       : seq_of_events       <-----------------------------------.
Progress update 2023-01-12 08:49:00.727978 : Number rows selected :      0.
Progress update 2023-01-12 08:49:00.830481 : INFO.00.065 Cleansing PostgreSQL data.
Progress update 2023-01-12 08:49:00.830481 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:00.883977 : INFO.00.066 Cleansing table 'aircraft' column 'acft_category'.
Progress update 2023-01-12 08:49:02.290479 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:02.290479 : INFO.00.066 Cleansing table 'aircraft' column 'dest_country'.
Progress update 2023-01-12 08:49:05.342310 : Number cols trimmed  :  51898.
Progress update 2023-01-12 08:49:07.125171 : Number cols nullified:  49506.
Progress update 2023-01-12 08:49:07.125171 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:07.125171 : INFO.00.066 Cleansing table 'aircraft' column 'dprt_country'.
Progress update 2023-01-12 08:49:08.925566 : Number cols trimmed  :  52168.
Progress update 2023-01-12 08:49:11.221030 : Number cols nullified:  49506.
Progress update 2023-01-12 08:49:11.221528 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:11.221528 : INFO.00.066 Cleansing table 'aircraft' column 'far_part'.
Progress update 2023-01-12 08:49:11.955568 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:11.955568 : INFO.00.066 Cleansing table 'aircraft' column 'oper_country'.
Progress update 2023-01-12 08:49:14.889496 : Number cols trimmed  :  56292.
Progress update 2023-01-12 08:49:18.105772 : Number cols nullified:  49334.
Progress update 2023-01-12 08:49:18.105772 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:18.105772 : INFO.00.066 Cleansing table 'aircraft' column 'owner_country'.
Progress update 2023-01-12 08:49:22.221440 : Number cols trimmed  :  63195.
Progress update 2023-01-12 08:49:26.403080 : Number cols nullified:  49334.
Progress update 2023-01-12 08:49:26.403080 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:26.403080 : INFO.00.066 Cleansing table 'aircraft' column 'regis_no'.
Progress update 2023-01-12 08:49:28.094702 : Number cols trimmed  :     46.
Progress update 2023-01-12 08:49:29.439609 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:29.440109 : INFO.00.066 Cleansing table 'events' column 'ev_city'.
Progress update 2023-01-12 08:49:31.476251 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:31.476251 : INFO.00.066 Cleansing table 'events' column 'ev_site_zipcode'.
Progress update 2023-01-12 08:49:33.503356 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:33.503855 : INFO.00.066 Cleansing table 'events' column 'latitude'.
Progress update 2023-01-12 08:49:35.487772 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:49:35.488274 : INFO.00.066 Cleansing table 'events' column 'longitude'.
Progress update 2023-01-12 08:49:37.535237 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:49:37.535237 :       58,753,232,100 ns - Total time launcher.
Progress update 2023-01-12 08:49:37.535737 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 08:49:37.535737 : ===============================================================================.
```

### 2.2.1 Data quality check

**Query**:

```sql92
SELECT count(*) "Count",
       'Events Total' "Description"
  FROM events e
 UNION
SELECT count(*) ,
       'Events Total with Fatalities'
  FROM events e
 WHERE inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US'
  FROM events e
 WHERE ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities'
  FROM events e
 WHERE inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) "Count",
       'Events Total since 1982' "Description"
  FROM events e
 WHERE ev_year >= 1982
 UNION
SELECT count(*) ,
       'Events Total with Fatalities since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities since 1982'
  FROM events e
 WHERE ev_year >= 1982
   AND inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) "Count",
       'Events Total since 2008' "Description"
  FROM events e
 WHERE ev_year >= 2008
 UNION
SELECT count(*) ,
       'Events Total with Fatalities since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND inj_tot_f > 0
 UNION
SELECT count(*) ,
       'Events US since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 UNION
SELECT count(*) ,
       'Events US with Fatalities since 2008'
  FROM events e
 WHERE ev_year >= 2008
   AND inj_tot_f > 0
   AND ev_state IS NOT NULL
   AND ev_state IN (SELECT state
                      FROM io_states is2)
 ORDER BY 2
```

**Results**:

```
Count|Description                            |
-----+---------------------------------------+
88116|Events Total                           |
88109|Events Total since 1982                |
25080|Events Total since 2008                |
17582|Events Total with Fatalities           |
17576|Events Total with Fatalities since 1982|
 5266|Events Total with Fatalities since 2008|
81122|Events US                              |
81115|Events US since 1982                   |
20765|Events US since 2008                   |
14693|Events US with Fatalities              |
14687|Events US with Fatalities since 1982   |
 3505|Events US with Fatalities since 2008   | 
```

### 2.3 **`d_s_f`** - Download basic simplemaps files

**Relevant cofiguration parameters**:

```
download_chunk_size = 524288
download_timeout = 10
download_file_simplemaps_us_cities_xlsx = "uscities.xlsx"
download_file_simplemaps_us_cities_zip = "simplemaps_uscities_basicv1.75.zip"
download_file_simplemaps_us_zips_xlsx = "uszips.xlsx"
download_file_simplemaps_us_zips_zip = "simplemaps_uszips_basicv1.81.zip"
download_work_dir = "data/download"
```

**Example protocol**:

```
...\io-avstats>run_io_avstats
Progress update 2023-01-12 08:52:58.915135 : ===============================================================================.
Progress update 2023-01-12 08:52:58.915635 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 08:52:58.917636 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 08:52:58.925635 : INFO.00.005 Argument task='d_s_f'.
Progress update 2023-01-12 08:52:58.925635 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:52:58.926135 : INFO.00.048 Downloading basic simplemaps files.
Progress update 2023-01-12 08:52:58.926135 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:52:59.124166 : INFO.00.030 The connection to the US city file 'simplemaps_uscities_basicv1.75.zip' on the simplemaps download page was successfully established.
Progress update 2023-01-12 08:52:59.625371 : INFO.00.023 From the file 'simplemaps_uscities_basicv1.75.zip' 8 chunks were downloaded.
Progress update 2023-01-12 08:52:59.658871 : INFO.00.024 The file 'simplemaps_uscities_basicv1.75.zip' was successfully unpacked.
Progress update 2023-01-12 08:52:59.736875 : INFO.00.022 The connection to the US zip code file 'simplemaps_uszips_basicv1.81.zip' on the simplemaps download page was successfully established.
Progress update 2023-01-12 08:52:59.838506 : INFO.00.023 From the file 'simplemaps_uszips_basicv1.81.zip' 8 chunks were downloaded.
Progress update 2023-01-12 08:52:59.872006 : INFO.00.024 The file 'simplemaps_uszips_basicv1.81.zip' was successfully unpacked.
Progress update 2023-01-12 08:52:59.872506 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:52:59.872506 :        1,075,371,000 ns - Total time launcher.
Progress update 2023-01-12 08:52:59.872506 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 08:52:59.872506 : ===============================================================================.
```

The downloaded files **`uscities.csv`** and **`uszips.xlsx`** must be checked with the reference files in the file directory **`data/reference`** for a match.
If there is no mismatch, then the next step can be skipped.

### 2.4 **`l_s_d`** - Load simplemaps data into PostgreSQL

Only necessary if the file downloaded in the previous step contains changes.

TODO

**Relevant cofiguration parameters**:

```
download_work_dir = "data/download"
```

**Example protocol**:

```
TODO
```

### 2.5 Download the ZIP Code Database file

The **`Personal Free`** version of the ZIP Code Database file must be downloaded manually from the **`https://www.unitedstateszipcodes.org/zip-code-database/`** website to the file directory according to the **`download_work_dir`** configuration parameter.

<kbd>![](img/Zip Codes.org Verify License Terms.png)</kbd>

The two formats **`Excel Format (data only)`** and **`CSV Format`** must be downloaded one after the other.
The downloaded file **`zip_code_database.csv`** must be checked with the reference files in the file directory **`data/reference`** for a match.
If there is no mismatch, then the next step can be skipped.

**Relevant cofiguration parameters**:

```
download_work_dir = "data/download"
```

### 2.6 **`l_z_d`** - Load ZIP Code Database data into PostgreSQL

Only necessary if the file downloaded in the previous step contains changes.

TODO

**Relevant cofiguration parameters**:

```
download_work_dir = "data/download"
```

**Example protocol**:

```
TODO
```

### 2.7 **`l_c_d`** - Load data from a correction file into PostgreSQL

This step only needs to be performed if modified or new correction files are available.

**Relevant cofiguration parameters**:

```
correction_work_dir = "data/correction"
```

**Example protocol**:

```
TODO
```

### 2.8 **`c_l_l`** - Correct decimal US latitudes and longitudes

**Example protocol**:

```
Progress update 2023-01-12 08:57:14.457012 : ===============================================================================.
Progress update 2023-01-12 08:57:14.457012 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 08:57:14.459012 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 08:57:14.467512 : INFO.00.005 Argument task='c_l_l'.
Progress update 2023-01-12 08:57:14.467512 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 08:57:14.467512 : INFO.00.040 Correct decimal US latitudes and longitudes.
Progress update 2023-01-12 08:57:14.467512 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:57:17.064376 : INFO.00.063 Processed data source 'events'.
Progress update 2023-01-12 08:57:17.064877 : Number cols deleted  :  60558.
Progress update 2023-01-12 08:57:17.064877 : --------------------------------------------------------------------------------
Progress update 2023-01-12 08:59:41.057822 : Number of rows so far read :   5000.
Progress update 2023-01-12 09:01:55.829078 : Number of rows so far read :  10000.
Progress update 2023-01-12 09:04:19.814443 : Number of rows so far read :  15000.
Progress update 2023-01-12 09:06:38.175949 : Number of rows so far read :  20000.
Progress update 2023-01-12 09:08:57.870888 : Number of rows so far read :  25000.
Progress update 2023-01-12 09:11:19.139894 : Number of rows so far read :  30000.
Progress update 2023-01-12 09:13:40.375909 : Number of rows so far read :  35000.
Progress update 2023-01-12 09:16:00.762435 : Number of rows so far read :  40000.
Progress update 2023-01-12 09:18:21.690033 : Number of rows so far read :  45000.
Progress update 2023-01-12 09:20:40.435254 : Number of rows so far read :  50000.
Progress update 2023-01-12 09:23:03.479007 : Number of rows so far read :  55000.
Progress update 2023-01-12 09:25:23.757510 : Number of rows so far read :  60000.
Progress update 2023-01-12 09:27:43.818483 : Number of rows so far read :  65000.
Progress update 2023-01-12 09:30:20.258731 : Number of rows so far read :  70000.
Progress update 2023-01-12 09:32:43.186047 : Number of rows so far read :  75000.
Progress update 2023-01-12 09:35:05.205534 : Number of rows so far read :  80000.
Progress update 2023-01-12 09:37:26.949725 : Number of rows so far read :  85000.
Progress update 2023-01-12 09:39:50.476423 : Number of rows so far read :  90000.
Progress update 2023-01-12 09:42:11.637397 : Number of rows so far read :  95000.
Progress update 2023-01-12 09:44:36.172457 : Number of rows so far read : 100000.
Progress update 2023-01-12 09:47:02.632400 : Number of rows so far read : 105000.
Progress update 2023-01-12 09:49:22.635645 : Number of rows so far read : 110000.
Progress update 2023-01-12 09:51:46.045424 : Number of rows so far read : 115000.
Progress update 2023-01-12 09:54:06.898252 : Number of rows so far read : 120000.
Progress update 2023-01-12 09:56:27.360073 : Number of rows so far read : 125000.
Progress update 2023-01-12 09:58:46.813060 : Number of rows so far read : 130000.
Progress update 2023-01-12 10:01:11.606500 : Number of rows so far read : 135000.
Progress update 2023-01-12 10:01:13.665266 : Number rows selected : 135076.
Progress update 2023-01-12 10:01:13.665766 : Number rows updated  : 135076.
Progress update 2023-01-12 10:01:13.665766 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 10:01:13.665766 :    3,839,322,755,200 ns - Total time launcher.
Progress update 2023-01-12 10:01:13.665766 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 10:01:13.665766 : ===============================================================================.
```

### 2.8.1 Data quality check

**Query Total:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                                                                                                                         |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  510|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                           |
 4087|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
  585|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                                                              |
    5|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                      |
    4|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                      |
   12|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                                                         |
   14|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                                                         |
    8|ERROR.00.922 Invalid US state id & INFO.00.033 Correction based on US zip code                                                                                                                                                                                 |
    3|ERROR.00.922 Invalid US state id & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
   91|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                      |
    1|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00|
    2|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                              |
42687|INFO.00.033 Correction based on US zip code                                                                                                                                                                                                                    |
 1295|INFO.00.034 Correction based on US state and city                                                                                                                                                                                                              |
10959|INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                                                         |
  101|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string                                                                                                                                                                  |
    4|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                   |
   64|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & INFO.00.033 Correction based on US zip code                                                                            |
  123|INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                                                                 |  
```

**Query Total since 1982:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE ev_year >= 1982
   AND io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                                                                                                                         |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  510|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                           |
 4087|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
  585|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                                                                                                                              |
    5|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                      |
    4|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                      |
   12|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country                                                                                                         |
   14|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                                                                                                                         |
    8|ERROR.00.922 Invalid US state id & INFO.00.033 Correction based on US zip code                                                                                                                                                                                 |
    3|ERROR.00.922 Invalid US state id & INFO.00.034 Correction based on US state and city                                                                                                                                                                           |
   91|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                      |
    1|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & ERROR.00|
    2|ERROR.00.922 Invalid US state id & INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                              |
42683|INFO.00.033 Correction based on US zip code                                                                                                                                                                                                                    |
 1294|INFO.00.034 Correction based on US state and city                                                                                                                                                                                                              |
10957|INFO.00.037 Correction based on latitude and longitude                                                                                                                                                                                                         |
  101|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string                                                                                                                                                                  |
    4|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                   |
   64|INFO.00.037 Correction based on latitude and longitude & ERROR.00.920 Invalid latitude string & ERROR.00.921 Invalid longitude string & INFO.00.033 Correction based on US zip code                                                                            |
  123|INFO.00.037 Correction based on latitude and longitude & ERROR.00.921 Invalid longitude string                                                                                                                                                                 |
```

**Query Total since 2008:**:

```sql92
SELECT count(*) "Count",
       io_dec_lat_lng_actions
  FROM events 
 WHERE ev_year >= 2008
   AND io_dec_lat_lng_actions IS NOT NULL 
 GROUP BY io_dec_lat_lng_actions 
 ORDER BY io_dec_lat_lng_actions
```

**Results**:

```
Count|io_dec_lat_lng_actions                                                                                                                                   |
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------+
    1|ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                     |
    6|ERROR.00.915 Unknown US zip code & INFO.00.034 Correction based on US state and city                                                                     |
    5|ERROR.00.916 Unknown US state and city & INFO.00.035 Correction based on US state                                                                        |
    1|ERROR.00.922 Invalid US state id & ERROR.00.915 Unknown US zip code & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country|
    6|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & ERROR.00.917 Unknown US state & INFO.00.036 Correction based on US country   |
   10|ERROR.00.922 Invalid US state id & ERROR.00.916 Unknown US state and city & INFO.00.036 Correction based on US country                                   |
   14|INFO.00.033 Correction based on US zip code                                                                                                              |
   35|INFO.00.034 Correction based on US state and city                                                                                                        |   
```

### 2.9 **`v_n_d`** - Verify selected NTSB data

**Relevant cofiguration parameters**:

```
max_deviation_latitude = 0.01
max_deviation_longitude = 0.01
```

**Example protocol**:

```
Progress update 2023-01-12 10:07:51.651116 : ===============================================================================.
Progress update 2023-01-12 10:07:51.651616 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 10:07:51.653617 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 10:07:51.662117 : INFO.00.005 Argument task='v_n_d'.
Progress update 2023-01-12 10:07:51.662117 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 10:07:51.662117 : INFO.00.043 Verify selected NTSB data.
Progress update 2023-01-12 10:07:51.662117 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:07:52.920456 : INFO.00.063 Processed data source 'events'.
Progress update 2023-01-12 10:07:52.920958 : Number cols deleted  :  27411.
Progress update 2023-01-12 10:07:52.920958 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:07:52.977508 : INFO.00.064 Verification of table 'events' column(s) 'latitude & longitude'.
Progress update 2023-01-12 10:07:52.978009 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:07:53.952560 : Number of rows so far read :   5000.
Progress update 2023-01-12 10:07:59.011120 : Number of rows so far read :  10000.
Progress update 2023-01-12 10:08:46.405547 : Number of rows so far read :  15000.
Progress update 2023-01-12 10:10:00.943546 : Number of rows so far read :  20000.
Progress update 2023-01-12 10:11:13.290400 : Number of rows so far read :  25000.
Progress update 2023-01-12 10:12:22.954238 : Number of rows so far read :  30000.
Progress update 2023-01-12 10:13:25.090708 : Number rows errors   :  12399.
Progress update 2023-01-12 10:13:25.091209 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:13:25.091209 : INFO.00.064 Verification of table 'events' column(s) 'ev_city'.
Progress update 2023-01-12 10:13:26.145729 : Number rows errors   :   6040.
Progress update 2023-01-12 10:13:26.145729 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:13:26.145729 : INFO.00.064 Verification of table 'events' column(s) 'ev_city & ev_site_zipcode'.
Progress update 2023-01-12 10:13:27.270523 : Number rows errors   :  16527.
Progress update 2023-01-12 10:13:27.270523 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:13:27.270523 : INFO.00.064 Verification of table 'events' column(s) 'ev_state'.
Progress update 2023-01-12 10:13:27.795021 : Number rows errors   :    289.
Progress update 2023-01-12 10:13:27.795021 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:13:27.795021 : INFO.00.064 Verification of table 'events' column(s) 'ev_site_zipcode'.
Progress update 2023-01-12 10:13:28.161584 : Number rows errors   :   6039.
Progress update 2023-01-12 10:13:28.162084 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:13:28.163084 : Number rows selected :  34375.
Progress update 2023-01-12 10:13:28.163084 : Number rows updated  :  41294.
Progress update 2023-01-12 10:13:28.163084 : Number rows errors   :  41294.
Progress update 2023-01-12 10:13:28.163585 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 10:13:28.163585 :      336,629,468,100 ns - Total time launcher.
Progress update 2023-01-12 10:13:28.163585 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 10:13:28.163585 : ===============================================================================.
```

### 2.9.1 Data quality check

**Query Total:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
Count|Description              |
-----+-------------------------+
 3805|Invalid Latitude         |
 4127|Invalid Longitude        |
 6040|Invalid US City          |
16527|Invalid US City & Zipcode|
  289|Invalid US State         |
 6039|Invalid US Zipcode       |
 3724|Latitude deviation       |
 3653|Longitude deviation      | 
```

**Query US until 2008:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE ev_year < 2008 
   AND io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE ev_year < 2008 
   AND io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE ev_year < 2008 
   AND io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
Count|Description              |
-----+-------------------------+
  172|Invalid Latitude         |
  196|Invalid Longitude        |
 4851|Invalid US City          |
12421|Invalid US City & Zipcode|
  123|Invalid US State         |
 5113|Invalid US Zipcode       |
    1|Latitude deviation       |
    0|Longitude deviation      |
```

**Query US Accidents since 2008:**:

```sql92
SELECT count(*) "Count",
       'Latitude deviation' "Description"
  FROM events e
 WHERE ev_year >= 2008 
   AND io_dec_latitude_deviating IS NOT NULL 
 UNION
SELECT count(*),
       'Longitude deviation'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_dec_longitude_deviating IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Latitude'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_latitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid Longitude'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_longitude IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_city IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US City & Zipcode'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_city_zipcode IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US State'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_state IS NOT NULL 
 UNION
SELECT count(*) ,
       'Invalid US Zipcode'
  FROM events e
 WHERE ev_year >= 2008 
   AND io_invalid_us_zipcode IS NOT NULL 
 ORDER BY 2
```

**Results**:

```
 Count|Description              |
-----+-------------------------+
 3633|Invalid Latitude         |
 3931|Invalid Longitude        |
 1189|Invalid US City          |
 4106|Invalid US City & Zipcode|
  166|Invalid US State         |
  926|Invalid US Zipcode       |
 3723|Latitude deviation       |
 3653|Longitude deviation      |
```

### 2.10 **`r_d_s`** - Refresh the PostgreSQL database schema

**Example protocol**:

```
Progress update 2023-01-12 10:20:36.995036 : ===============================================================================.
Progress update 2023-01-12 10:20:36.995036 : INFO.00.004 Start Launcher.
Progress update 2023-01-12 10:20:36.997036 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-12 10:20:37.005535 : INFO.00.005 Argument task='r_d_s'.
Progress update 2023-01-12 10:20:37.005535 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 10:20:37.005535 : INFO.00.071 Refreshing the database schema.
Progress update 2023-01-12 10:20:37.005535 : --------------------------------------------------------------------------------
Progress update 2023-01-12 10:21:04.010845 : INFO.00.069 Materialized database view is refreshed: io_app_aaus1982.
Progress update 2023-01-12 10:21:04.010845 : -------------------------------------------------------------------------------.
Progress update 2023-01-12 10:21:04.011346 :       27,136,309,100 ns - Total time launcher.
Progress update 2023-01-12 10:21:04.011346 : INFO.00.006 End   Launcher.
Progress update 2023-01-12 10:21:04.011346 : ===============================================================================.
```

### 2.11 Backup the file directory **`data/postgres`** 

- Stop the Docker container **`io_avstats_db`**.
- Zip the file directory **`postgres`** in the file directory **`data`** - result is the file **`postgres.zip`**.
- Rename the file **`postgres.sql`** to **`yy.mm.dd_postgres_upDDMON.zip`**.
- Create a copy of the file **`yy.mm.dd_postgres_upDDMON.zip`** with the name **`latest_postgres.zip`**.

### 2.12 Update the Google Drive 

- Log in to Google Drive with the Google Account **`io-avstats.io-aero@gmail.com`**.
- Upload the file **`yy.mm.dd_postgres_upDDMON.zip`**.
- Share the newly uploaded file.

### 2.13 Update **IO-AVSTATS** in the IO-Aero cloud 

- Run the script **`scripts/run_cloud_files_zip`**.
- Upload the resulting **`cloud.zip`** file to the cloud and process it there.

### 2.14 Update **IO-AVSTATS** in the IO-Aero cloud 

```sql
SELECT count(*)   AS no_rows,
       'aircraft' AS db_table
FROM aircraft
union
SELECT count(*)      AS no_rows,
       'dt_aircraft' AS db_table
FROM dt_aircraft
union
SELECT count(*)    AS no_rows,
       'dt_events' AS db_table
FROM dt_events
union
SELECT count(*)         AS no_rows,
       'dt_flight_crew' AS db_table
FROM dt_flight_crew
union
SELECT count(*)  AS no_rows,
       'engines' AS db_table
FROM engines
union
SELECT count(*) AS no_rows,
       'events' AS db_table
FROM events
union
SELECT count(*)          AS no_rows,
       'events_sequence' AS db_table
FROM events_sequence
union
SELECT count(*)   AS no_rows,
       'findings' AS db_table
FROM findings
union
SELECT count(*)      AS no_rows,
       'flight_crew' AS db_table
FROM flight_crew
union
SELECT count(*)      AS no_rows,
       'flight_time' AS db_table
FROM flight_time
union
SELECT count(*) AS no_rows,
       'injury' AS db_table
FROM injury
union
SELECT count(*)     AS no_rows,
       'narratives' AS db_table
FROM narratives
union
SELECT count(*)     AS no_rows,
       'ntsb_admin' AS db_table
FROM ntsb_admin
union
SELECT count(*)      AS no_rows,
       'occurrences' AS db_table
FROM occurrences
union
SELECT count(*)        AS no_rows,
       'seq_of_events' AS db_table
FROM seq_of_events
order by db_table
```
