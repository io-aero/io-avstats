# Update log from file up22JAN in 2023

```
Microsoft Windows [Version 10.0.19045.2486]
(c) Microsoft Corporation. All rights reserved.

D:\SoftDevelopment\Projects\IO-Aero\io-avstats>run_io_avstats
=========================================================
r_s_a   - Run a Streamlit application
---------------------------------------------------------
u_p_d   - Complete processing of a modifying MS Access file
---------------------------------------------------------
d_n_a   - Download a NTSB MS Access database file
l_n_a   - Load NTSB MS Access database data into PostgreSQL
c_l_l   - Correct decimal US latitudes and longitudes
v_n_d   - Verify selected NTSB data
r_d_s   - Refresh the PostgreSQL database schema
---------------------------------------------------------
d_s_f   - Download basic simplemaps files
l_s_d   - Load simplemaps data into PostgreSQL
l_z_d   - Load ZIP Code Database data into PostgreSQL
l_c_d   - Load data from a correction file into PostgreSQL
---------------------------------------------------------
a_o_c   - Load aviation occurrence categories into PostgreSQL
c_d_s   - Create the PostgreSQL database schema
c_p_d   - Cleansing PostgreSQL data
d_d_f   - Delete the PostgreSQL database files
d_d_s   - Drop the PostgreSQL database schema
l_c_s   - Load country and state data into PostgreSQL
l_n_s   - Load NTSB MS Excel statistic data into PostgreSQL
l_s_e   - Load sequence of events data into PostgreSQL
s_d_c   - Set up the PostgreSQL database container
u_d_s   - Update the PostgreSQL database schema
---------------------------------------------------------
c_d_i   - Create or update a Docker image
c_d_c   - Run Docker Compose tasks
c_f_z   - Zip the files for the cloud
---------------------------------------------------------
version - Show the IO-AVSTATS-DB version
---------------------------------------------------------
Enter the desired task [default: r_s_a] u_p_d
=========================================================
upDDMON - New additions and updates until DD day in the month MON
---------------------------------------------------------
Enter the stem name of the desired MS Access database file up22JAN

Script run_io_avstats is now running
=======================================================================
Start run_io_avstats
-----------------------------------------------------------------------
IO-AVSTATS - Aviation Event Statistics.
-----------------------------------------------------------------------
PYTHONPATH :
-----------------------------------------------------------------------
TASK       : u_p_d
MSACCESS   : up22JAN
MSEXCEL    :
-----------------------------------------------------------------------
The current time is: 10:01:28.29
Enter the new time:
=======================================================================
```
## d_n_a - Download a NTSB MS Access database file
```
Progress update 2023-01-22 10:01:29.885955 : ===============================================================================.
Progress update 2023-01-22 10:01:29.885955 : INFO.00.004 Start Launcher.
Progress update 2023-01-22 10:01:29.887955 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-22 10:01:29.896455 : INFO.00.008 Arguments task='d_n_a' msaccess='up22JAN'.
Progress update 2023-01-22 10:01:29.896455 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:01:29.896455 : INFO.00.047 Download NTSB MS Access database file 'up22JAN'.
Progress update 2023-01-22 10:01:29.896455 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:01:30.457016 : INFO.00.013 The connection to the MS Access database file 'up22JAN.zip' on the NTSB download page was successfully established.
Progress update 2023-01-22 10:01:30.870396 : INFO.00.014 From the file 'up22JAN.zip' 2 chunks were downloaded.
Progress update 2023-01-22 10:01:30.891425 : INFO.00.015 The file 'up22JAN.zip' was successfully unpacked.
Progress update 2023-01-22 10:01:30.903925 : INFO.00.051 msaccess_file='D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\IO-AVSTATS.mdb'.
Progress update 2023-01-22 10:01:30.903925 : INFO.00.051 msaccess_file='D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up22JAN.sql'.
Progress update 2023-01-22 10:01:30.903925 : INFO.00.052 razorsql_jar_file='C:\Program Files\RazorSQL\razorsql.jar'.
Progress update 2023-01-22 10:01:30.904426 : INFO.00.053 razorsql_java_path='C:\Program Files\RazorSQL\jre11\bin\java'.
1674378090976: launching RazorSQL . . .
1674378090977: args . . .
-backup
IO-AVSTATS
null
null
;
null
D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up22JAN.sql
NO
tables
YES
null
NO
NO
1674378091011: userName: walte
1674378091011: libraryPath: C:\Program Files\RazorSQL\jre11\bin;C:\WINDOWS\Sun\Java\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\Users\walte\.virtualenvs\io-avstats-zafInMY1\Scripts;C:\Program Files (x86)\VMware\VMware Player\bin\;C:\Program Files (x86)\infogridpacific\AZARDI;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\Calibre2\;C:\Program Files\dotnet\;C:\Program Files\Git LFS;C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Program Files\Pandoc\;C:\Program Files\TortoiseGit\bin;C:\Software\GnuWin32\bin;C:\WINDOWS;C:\WINDOWS\system32;C:\WINDOWS\System32\OpenSSH\;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Users\walte\.nimble\bin;C:\Windows;C:\Windows\system32;C:\Windows\System32\OpenSSH\;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Software\gradle-7.6\bin;C:\Program Files\doxygen\bin;C:\Program Files\Graphviz\bin;C:\Software\PostgreSQL\15\bin;C:\Software\Python\Python310;C:\Software\Python\Python310\Scripts;C:\Software\jdk-19\bin;C:\Program Files\LLVM\bin;C:\Program Files\Amazon\AWSCLIV2\;C:\Program Files\PuTTY\;C:\Software\Gpg4win\..\GnuPG\bin;C:\Program Files\nodejs\;C:\Program Files\Docker\Docker\resources\bin;C:\Program Files\Git\cmd;C:\Software\.cargo\bin;C:\Users\walte\.cargo\bin;C:\Users\walte\AppData\Local\Microsoft\WindowsApps;C:\Software\Microsoft VS Code\bin;C:\Users\walte\go\bin;c:\users\walte\.local\bin;C:\Users\walte\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\walte\AppData\Roaming\npm;.
1674378091011: javaVersion: 11.0.13
1674378091012:
1674378091012: Verifying RazorSQL resources location.
1674378091012:
1674378091012: testing base url: / = file:/C:/Program%20Files/RazorSQL/
1674378091012:
1674378091013: testString1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
1674378091013: testString2: file:/C:/Program%20Files/RazorSQL/data/base.ssql
1674378091013: testFile1: C:\Program Files\RazorSQL\razorsql.jar
1674378091013: testFile2: C:\Program Files\RazorSQL\data\base.ssql
1674378091013: both test file exists.  Base URL found.
1674378091013: resource directory: file:/C:/Program%20Files/RazorSQL/
1674378091013: user home: C:\Users\walte
1674378091015: user profile: C:\Users\walte
1674378091015: app data: C:\Users\walte\AppData\Roaming
1674378091015: checking write access to: C:\Users\walte\AppData\Roaming
1674378091015: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
1674378091015: can write to C:\Users\walte\AppData\Roaming
1674378091015: user.home: C:\Users\walte\AppData\Roaming
1674378091015: RazorSQL Scratch Directory: C:\Users\walte\AppData\Roaming\RazorSQL
1674378091016: RazorSQL Scratch Directory exists
1674378091016: checking for sub directories
1674378091016: razorsql launch log: C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
1674378091016: launch log file = C:\Users\walte\AppData\Roaming\RazorSQL\razorsql_launch_log.txt
1674378091017: Checking for graphics properties
1674378091017: graphics properties file: C:\Users\walte\AppData\Roaming\RazorSQL\data\graphics_properties.txt
1674378091017: gOverride: null
1674378091017: not disabling advanced graphics
1674378091017: path0: file:/C:/Program%20Files/RazorSQL/data/run.ssql
1674378091017: path1: file:/C:/Program%20Files/RazorSQL/razorsql.jar
1674378091017: runArgs: true
1674378091018: showScreen: false
1674378091018: args[0]: -backup
1674378091018: args[1]: IO-AVSTATS
1674378091018: args[2]: null
1674378091018: args[3]: null
1674378091018: args[4]: ;
1674378091018: args[5]: null
1674378091019: args[6]: D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up22JAN.sql
1674378091019: args[7]: NO
1674378091019: args[8]: tables
1674378091019: args[9]: YES
1674378091019: args[10]: null
1674378091019: args[11]: NO
1674378091019: args[12]: NO
1674378091019: Command: -backup
1674378091019: Running -backup
h: name = C:\Program Files\RazorSQL\data\run.ssql
h: name = C:\Program Files\RazorSQL\razorsql.jar
1674378091026: Attempting to load . . .
command found
uOne: file:/C:/Program%20Files/RazorSQL/
h: name = C:\Program Files\RazorSQL\data\run.ssql
1674378091037reading file . . .C:\Program Files\RazorSQL\data\base.ssql
1674378091062done reading . . .
1674378091071done converting
1674378091072starting lib load.
1674378091083lib load complete.
In command line processor
Max Memory: 30688.0
Current Total Memory: 2048.0
Free Memory: 1957.968734741211
1674378091157: r init
1674378091157: d init
1674378091157: get default file encoding
1674378091157: end d init
custom home directory: null
Checking for user data from old versions
1674378091159: user home: C:\Users\walte
1674378091159: user profile: C:\Users\walte
1674378091159: app data: C:\Users\walte\AppData\Roaming
1674378091159: checking write access to: C:\Users\walte\AppData\Roaming
1674378091159: write dir: C:\Users\walte\AppData\Roaming\RichardsonSoftware
1674378091159: can write to C:\Users\walte\AppData\Roaming
newHome: C:\Users\walte\AppData\Roaming\RazorSQL
dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
Profiles Exist
1674378091169: loading icons
1674378091327: done r init
Getting connection data from: IO-AVSTATS
1674378091329: r init
1674378091329: d init
1674378091329: get default file encoding
1674378091329: end d init
custom home directory: null
Checking for user data from old versions
newHome: C:\Users\walte\AppData\Roaming\RazorSQL
dataHome: C:\Users\walte\AppData\Roaming/RazorSQL/data/
preferences file: C:\Users\walte\AppData\Roaming\RazorSQL\data\preferences.txt
Profiles Exist
1674378091330: loading icons
1674378091340: done r init
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
Progress update 2023-01-22 10:01:31.965581 : INFO.00.011 The DDL script for the MS Access database 'up22JAN.mdb' was created successfully.
Progress update 2023-01-22 10:01:31.971082 : INFO.00.012 The DDL script for the MS Access database 'up22JAN.mdb' is identical to the reference script.
Progress update 2023-01-22 10:01:31.971082 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:01:31.971082 :        2,200,627,100 ns - Total time launcher.
Progress update 2023-01-22 10:01:31.971082 : INFO.00.006 End   Launcher.
Progress update 2023-01-22 10:01:31.971082 : ===============================================================================.
```
## l_n_a - Load NTSB MS Access database data into PostgreSQL
```
Progress update 2023-01-22 10:01:33.624581 : ===============================================================================.
Progress update 2023-01-22 10:01:33.624581 : INFO.00.004 Start Launcher.
Progress update 2023-01-22 10:01:33.626581 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-22 10:01:33.634581 : INFO.00.008 Arguments task='l_n_a' msaccess='up22JAN'.
Progress update 2023-01-22 10:01:33.634581 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:01:33.635082 : INFO.00.049 Load NTSB MS Access database data from file 'up22JAN'.
Progress update 2023-01-22 10:01:33.635082 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:01:33.635082 : INFO.00.054 ODBC driver='DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\download\up22JAN.mdb;'.
Progress update 2023-01-22 10:01:33.815581 : INFO.00.021 The following database table is not processed: 'MSysAccessObjects'.
Progress update 2023-01-22 10:01:33.815581 : INFO.00.021 The following database table is not processed: 'MSysACEs'.
Progress update 2023-01-22 10:01:33.815581 : INFO.00.021 The following database table is not processed: 'MSysIMEXColumns'.
Progress update 2023-01-22 10:01:33.815581 : INFO.00.021 The following database table is not processed: 'MSysIMEXSpecs'.
Progress update 2023-01-22 10:01:33.815581 : INFO.00.021 The following database table is not processed: 'MSysModules2'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroupCategories'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroups'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysNavPaneGroupToObjects'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysNavPaneObjectIDs'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysObjects'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysQueries'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'MSysRelationships'.
Progress update 2023-01-22 10:01:33.816081 : INFO.00.021 The following database table is not processed: 'Country'.
Progress update 2023-01-22 10:01:33.816581 : INFO.00.021 The following database table is not processed: 'ct_iaids'.
Progress update 2023-01-22 10:01:33.816581 : INFO.00.021 The following database table is not processed: 'ct_seqevt'.
Progress update 2023-01-22 10:01:33.816581 : INFO.00.021 The following database table is not processed: 'eADMSPUB_DataDictionary'.
Progress update 2023-01-22 10:01:33.816581 : INFO.00.021 The following database table is not processed: 'states'.
Progress update 2023-01-22 10:01:33.816581 :
Progress update 2023-01-22 10:01:33.816581 : Database table       : events              <-----------------------------------.
Progress update 2023-01-22 10:01:33.896055 : Updated ev_id=20001211X14762 ev_year=1992.
Progress update 2023-01-22 10:01:33.920831 : Updated ev_id=20001212X22676 ev_year=1990.
Progress update 2023-01-22 10:01:33.945545 : Updated ev_id=20001212X23076 ev_year=1990.
Progress update 2023-01-22 10:01:33.979058 : Updated ev_id=20001212X23897 ev_year=1990.
Progress update 2023-01-22 10:01:34.004081 : Updated ev_id=20001212X23332 ev_year=1990.
Progress update 2023-01-22 10:01:34.029138 : Updated ev_id=20001212X24569 ev_year=1990.
Progress update 2023-01-22 10:01:34.053930 : Updated ev_id=20001212X16779 ev_year=1991.
Progress update 2023-01-22 10:01:34.079443 : Updated ev_id=20001213X28070 ev_year=1989.
Progress update 2023-01-22 10:01:34.103961 : Updated ev_id=20001213X29333 ev_year=1989.
Progress update 2023-01-22 10:01:34.153862 : Updated ev_id=20001212X22536 ev_year=1990.
Progress update 2023-01-22 10:01:34.179292 : Updated ev_id=20001212X24443 ev_year=1990.
Progress update 2023-01-22 10:01:34.203758 : Updated ev_id=20001213X27903 ev_year=1989.
Progress update 2023-01-22 10:01:34.229259 : Updated ev_id=20001213X29965 ev_year=1989.
Progress update 2023-01-22 10:01:34.253863 : Updated ev_id=20001212X22962 ev_year=1990.
Progress update 2023-01-22 10:01:34.279302 : Updated ev_id=20001212X22963 ev_year=1990.
Progress update 2023-01-22 10:01:34.303799 : Updated ev_id=20001212X23204 ev_year=1990.
Progress update 2023-01-22 10:01:34.329319 : Updated ev_id=20001212X23474 ev_year=1990.
Progress update 2023-01-22 10:01:34.378987 : Updated ev_id=20001212X24647 ev_year=1990.
Progress update 2023-01-22 10:01:34.403640 : Updated ev_id=20001212X24648 ev_year=1990.
Progress update 2023-01-22 10:01:34.429164 : Updated ev_id=20001212X16648 ev_year=1991.
Progress update 2023-01-22 10:01:34.453664 : Updated ev_id=20001212X17333 ev_year=1991.
Progress update 2023-01-22 10:01:34.479165 : Updated ev_id=20001213X28160 ev_year=1989.
Progress update 2023-01-22 10:01:34.503664 : Updated ev_id=20001213X29454 ev_year=1989.
Progress update 2023-01-22 10:01:34.529165 : Updated ev_id=20001213X29845 ev_year=1989.
Progress update 2023-01-22 10:01:34.553663 : Updated ev_id=20001212X22977 ev_year=1990.
Progress update 2023-01-22 10:01:34.579165 : Updated ev_id=20001212X23225 ev_year=1990.
Progress update 2023-01-22 10:01:34.603664 : Updated ev_id=20001212X23226 ev_year=1990.
Progress update 2023-01-22 10:01:34.653664 : Updated ev_id=20001212X24086 ev_year=1990.
Progress update 2023-01-22 10:01:34.679028 : Updated ev_id=20001212X24795 ev_year=1990.
Progress update 2023-01-22 10:01:34.703857 : Updated ev_id=20001212X23037 ev_year=1990.
Progress update 2023-01-22 10:01:34.729013 : Updated ev_id=20001212X23564 ev_year=1990.
Progress update 2023-01-22 10:01:34.753638 : Updated ev_id=20001212X24145 ev_year=1990.
Progress update 2023-01-22 10:01:34.778982 : Updated ev_id=20001212X22824 ev_year=1990.
Progress update 2023-01-22 10:01:34.803994 : Updated ev_id=20191219X91426 ev_year=2019.
Progress update 2023-01-22 10:01:34.828993 : Updated ev_id=20200807X30140 ev_year=2020.
Progress update 2023-01-22 10:01:34.878994 : Updated ev_id=20200820X85853 ev_year=2020.
Progress update 2023-01-22 10:01:34.903997 : Updated ev_id=20201004102078 ev_year=2020.
Progress update 2023-01-22 10:01:34.929100 : Updated ev_id=20201019102162 ev_year=2020.
Progress update 2023-01-22 10:01:34.953656 : Updated ev_id=20201112102277 ev_year=2020.
Progress update 2023-01-22 10:01:34.979303 : Updated ev_id=20201123102332 ev_year=2020.
Progress update 2023-01-22 10:01:35.003827 : Updated ev_id=20210205102605 ev_year=2021.
Progress update 2023-01-22 10:01:35.028847 : Updated ev_id=20210209102615 ev_year=2021.
Progress update 2023-01-22 10:01:35.053686 : Updated ev_id=20210216102634 ev_year=2021.
Progress update 2023-01-22 10:01:35.079219 : Updated ev_id=20210218102641 ev_year=2021.
Progress update 2023-01-22 10:01:35.154025 : Updated ev_id=20210219102646 ev_year=2021.
Progress update 2023-01-22 10:01:35.178582 : Updated ev_id=20210224102672 ev_year=2021.
Progress update 2023-01-22 10:01:35.203831 : Updated ev_id=20210304102704 ev_year=2021.
Progress update 2023-01-22 10:01:35.228870 : Updated ev_id=20210304102711 ev_year=2021.
Progress update 2023-01-22 10:01:35.253851 : Updated ev_id=20210305102714 ev_year=2021.
Progress update 2023-01-22 10:01:35.303869 : Updated ev_id=20210418102927 ev_year=2021.
Progress update 2023-01-22 10:01:35.378856 : Updated ev_id=20210429102997 ev_year=2021.
Progress update 2023-01-22 10:01:35.403905 : Updated ev_id=20210502103009 ev_year=2021.
Progress update 2023-01-22 10:01:35.428932 : Updated ev_id=20210513103077 ev_year=2021.
Progress update 2023-01-22 10:01:35.453850 : Updated ev_id=20210527103152 ev_year=2021.
Progress update 2023-01-22 10:01:35.478850 : Updated ev_id=20210529103166 ev_year=2021.
Progress update 2023-01-22 10:01:35.503910 : Updated ev_id=20210617103285 ev_year=2021.
Progress update 2023-01-22 10:01:35.528910 : Updated ev_id=20210630103379 ev_year=2021.
Progress update 2023-01-22 10:01:35.578909 : Updated ev_id=20210702103405 ev_year=2021.
Progress update 2023-01-22 10:01:35.628571 : Updated ev_id=20210705103412 ev_year=2021.
Progress update 2023-01-22 10:01:35.654071 : Updated ev_id=20210714103480 ev_year=2021.
Progress update 2023-01-22 10:01:35.678571 : Updated ev_id=20210718103499 ev_year=2021.
Progress update 2023-01-22 10:01:35.704071 : Updated ev_id=20210727103558 ev_year=2021.
Progress update 2023-01-22 10:01:35.728571 : Updated ev_id=20210805103634 ev_year=2021.
Progress update 2023-01-22 10:01:35.753760 : Updated ev_id=20210809103657 ev_year=2021.
Progress update 2023-01-22 10:01:35.803732 : Updated ev_id=20210810103667 ev_year=2021.
Progress update 2023-01-22 10:01:35.828903 : Updated ev_id=20210816103700 ev_year=2021.
Progress update 2023-01-22 10:01:35.853853 : Updated ev_id=20210830103772 ev_year=2021.
Progress update 2023-01-22 10:01:35.878852 : Updated ev_id=20210830103773 ev_year=2021.
Progress update 2023-01-22 10:01:35.904025 : Updated ev_id=20210830103775 ev_year=2021.
Progress update 2023-01-22 10:01:35.929025 : Updated ev_id=20210903103795 ev_year=2021.
Progress update 2023-01-22 10:01:35.954025 : Updated ev_id=20210908103824 ev_year=2021.
Progress update 2023-01-22 10:01:35.979025 : Updated ev_id=20211006104055 ev_year=2021.
Progress update 2023-01-22 10:01:36.103859 : Updated ev_id=20220503105038 ev_year=2022.
Progress update 2023-01-22 10:01:36.153693 : Updated ev_id=20220525105130 ev_year=2022.
Progress update 2023-01-22 10:01:36.203861 : Updated ev_id=20220607105206 ev_year=2022.
Progress update 2023-01-22 10:01:36.254000 : Updated ev_id=20220731105625 ev_year=2022.
Progress update 2023-01-22 10:01:36.304000 : Updated ev_id=20220912105911 ev_year=2022.
Progress update 2023-01-22 10:01:36.328501 : Updated ev_id=20220913105930 ev_year=2022.
Progress update 2023-01-22 10:01:36.354001 : Updated ev_id=20220928106011 ev_year=2022.
Progress update 2023-01-22 10:01:36.378502 : Updated ev_id=20221003106045 ev_year=2022.
Progress update 2023-01-22 10:01:36.428414 : Updated ev_id=20221006106075 ev_year=2022.
Progress update 2023-01-22 10:01:36.453954 : Updated ev_id=20221012106114 ev_year=2022.
Progress update 2023-01-22 10:01:36.495396 : Updated ev_id=20221013106123 ev_year=2022.
Progress update 2023-01-22 10:01:36.570623 : Updated ev_id=20221024106184 ev_year=2022.
Progress update 2023-01-22 10:01:36.595123 : Updated ev_id=20221026106199 ev_year=2022.
Progress update 2023-01-22 10:01:36.645264 : Updated ev_id=20221103106241 ev_year=2022.
Progress update 2023-01-22 10:01:36.670355 : Updated ev_id=20221108106259 ev_year=2022.
Progress update 2023-01-22 10:01:36.720597 : Updated ev_id=20221128106365 ev_year=2022.
Progress update 2023-01-22 10:01:36.770096 : Updated ev_id=20221208106433 ev_year=2022.
Progress update 2023-01-22 10:01:36.795097 : Updated ev_id=20221212106439 ev_year=2022.
Progress update 2023-01-22 10:01:36.879349 : Updated ev_id=20221213106450 ev_year=2022.
Progress update 2023-01-22 10:01:36.928664 : Updated ev_id=20221215106462 ev_year=2022.
Progress update 2023-01-22 10:01:36.978190 : Updated ev_id=20221219106471 ev_year=2022.
Progress update 2023-01-22 10:01:37.003040 : Updated ev_id=20221222106484 ev_year=2022.
Progress update 2023-01-22 10:01:37.028221 : Updated ev_id=20221222106485 ev_year=2022.
Progress update 2023-01-22 10:01:37.053223 : Updated ev_id=20221228106502 ev_year=2022.
Progress update 2023-01-22 10:01:37.078723 : Updated ev_id=20221229106509 ev_year=2022.
Progress update 2023-01-22 10:01:37.203223 : Updated ev_id=20230104106534 ev_year=2023.
Progress update 2023-01-22 10:01:37.253304 : Updated ev_id=20230106106544 ev_year=2022.
Progress update 2023-01-22 10:01:37.378373 : Updated ev_id=20230114106576 ev_year=2023.
Progress update 2023-01-22 10:01:37.803131 : Number rows selected :    141.
Progress update 2023-01-22 10:01:37.803131 : Number rows inserted :     41.
Progress update 2023-01-22 10:01:37.803131 : Number rows updated  :    100.
Progress update 2023-01-22 10:01:37.803640 :
Progress update 2023-01-22 10:01:37.803640 : Database table       : aircraft            <-----------------------------------.
Progress update 2023-01-22 10:01:37.886638 : Updated ev_id=20001211X14762 aircraft_key=1.
Progress update 2023-01-22 10:01:37.953452 : Updated ev_id=20001212X22676 aircraft_key=1.
Progress update 2023-01-22 10:01:38.028162 : Updated ev_id=20001212X23076 aircraft_key=1.
Progress update 2023-01-22 10:01:38.094626 : Updated ev_id=20001212X23897 aircraft_key=1.
Progress update 2023-01-22 10:01:38.161535 : Updated ev_id=20001212X23332 aircraft_key=1.
Progress update 2023-01-22 10:01:38.236537 : Updated ev_id=20001212X24569 aircraft_key=1.
Progress update 2023-01-22 10:01:38.303259 : Updated ev_id=20001212X16779 aircraft_key=1.
Progress update 2023-01-22 10:01:38.377974 : Updated ev_id=20001213X28070 aircraft_key=1.
Progress update 2023-01-22 10:01:38.461499 : Updated ev_id=20001213X29333 aircraft_key=1.
Progress update 2023-01-22 10:01:38.552954 : Updated ev_id=20001212X22536 aircraft_key=1.
Progress update 2023-01-22 10:01:38.628062 : Updated ev_id=20001212X24443 aircraft_key=1.
Progress update 2023-01-22 10:01:38.694682 : Updated ev_id=20001213X27903 aircraft_key=1.
Progress update 2023-01-22 10:01:38.777829 : Updated ev_id=20001213X29965 aircraft_key=1.
Progress update 2023-01-22 10:01:38.844936 : Updated ev_id=20001212X22962 aircraft_key=1.
Progress update 2023-01-22 10:01:38.911246 : Updated ev_id=20001212X22963 aircraft_key=1.
Progress update 2023-01-22 10:01:39.002762 : Updated ev_id=20001212X23204 aircraft_key=1.
Progress update 2023-01-22 10:01:39.078070 : Updated ev_id=20001212X23474 aircraft_key=1.
Progress update 2023-01-22 10:01:39.144193 : Updated ev_id=20001212X24647 aircraft_key=1.
Progress update 2023-01-22 10:01:39.227829 : Updated ev_id=20001212X24648 aircraft_key=1.
Progress update 2023-01-22 10:01:39.294759 : Updated ev_id=20001212X16648 aircraft_key=1.
Progress update 2023-01-22 10:01:39.361258 : Updated ev_id=20001212X17333 aircraft_key=1.
Progress update 2023-01-22 10:01:39.452630 : Updated ev_id=20001213X28160 aircraft_key=1.
Progress update 2023-01-22 10:01:39.527964 : Updated ev_id=20001213X29454 aircraft_key=1.
Progress update 2023-01-22 10:01:39.594388 : Updated ev_id=20001213X29845 aircraft_key=1.
Progress update 2023-01-22 10:01:39.661108 : Updated ev_id=20001212X22977 aircraft_key=1.
Progress update 2023-01-22 10:01:39.735932 : Updated ev_id=20001212X23225 aircraft_key=1.
Progress update 2023-01-22 10:01:39.802700 : Updated ev_id=20001212X23226 aircraft_key=1.
Progress update 2023-01-22 10:01:39.877621 : Updated ev_id=20001212X24086 aircraft_key=1.
Progress update 2023-01-22 10:01:39.944589 : Updated ev_id=20001212X24795 aircraft_key=1.
Progress update 2023-01-22 10:01:40.011088 : Updated ev_id=20001212X23037 aircraft_key=1.
Progress update 2023-01-22 10:01:40.086094 : Updated ev_id=20001212X23564 aircraft_key=1.
Progress update 2023-01-22 10:01:40.160782 : Updated ev_id=20001212X24145 aircraft_key=1.
Progress update 2023-01-22 10:01:40.235818 : Updated ev_id=20001212X22824 aircraft_key=1.
Progress update 2023-01-22 10:01:40.302326 : Updated ev_id=20191219X91426 aircraft_key=1.
Progress update 2023-01-22 10:01:40.377720 : Updated ev_id=20200807X30140 aircraft_key=1.
Progress update 2023-01-22 10:01:40.444220 : Updated ev_id=20200820X85853 aircraft_key=1.
Progress update 2023-01-22 10:01:40.510856 : Updated ev_id=20201004102078 aircraft_key=1.
Progress update 2023-01-22 10:01:40.585526 : Updated ev_id=20201019102162 aircraft_key=1.
Progress update 2023-01-22 10:01:40.652720 : Updated ev_id=20201112102277 aircraft_key=1.
Progress update 2023-01-22 10:01:40.727307 : Updated ev_id=20201123102332 aircraft_key=1.
Progress update 2023-01-22 10:01:40.794235 : Updated ev_id=20210205102605 aircraft_key=1.
Progress update 2023-01-22 10:01:40.860381 : Updated ev_id=20210209102615 aircraft_key=1.
Progress update 2023-01-22 10:01:40.935813 : Updated ev_id=20210216102634 aircraft_key=1.
Progress update 2023-01-22 10:01:41.002336 : Updated ev_id=20210218102641 aircraft_key=1.
Progress update 2023-01-22 10:01:41.077445 : Updated ev_id=20210219102646 aircraft_key=1.
Progress update 2023-01-22 10:01:41.143945 : Updated ev_id=20210224102672 aircraft_key=1.
Progress update 2023-01-22 10:01:41.210847 : Updated ev_id=20210304102704 aircraft_key=1.
Progress update 2023-01-22 10:01:41.285544 : Updated ev_id=20210304102711 aircraft_key=1.
Progress update 2023-01-22 10:01:41.352546 : Updated ev_id=20210305102714 aircraft_key=1.
Progress update 2023-01-22 10:01:41.444115 : Updated ev_id=20210418102927 aircraft_key=1.
Progress update 2023-01-22 10:01:41.535793 : Updated ev_id=20210429102997 aircraft_key=1.
Progress update 2023-01-22 10:01:41.602292 : Updated ev_id=20210502103009 aircraft_key=1.
Progress update 2023-01-22 10:01:41.677006 : Updated ev_id=20210513103077 aircraft_key=1.
Progress update 2023-01-22 10:01:41.760644 : Updated ev_id=20210527103152 aircraft_key=1.
Progress update 2023-01-22 10:01:41.835556 : Updated ev_id=20210529103166 aircraft_key=1.
Progress update 2023-01-22 10:01:41.902041 : Updated ev_id=20210617103285 aircraft_key=1.
Progress update 2023-01-22 10:01:41.977157 : Updated ev_id=20210630103379 aircraft_key=1.
Progress update 2023-01-22 10:01:42.043772 : Updated ev_id=20210702103405 aircraft_key=1.
Progress update 2023-01-22 10:01:42.135575 : Updated ev_id=20210705103412 aircraft_key=1.
Progress update 2023-01-22 10:01:42.202076 : Updated ev_id=20210714103480 aircraft_key=1.
Progress update 2023-01-22 10:01:42.277346 : Updated ev_id=20210718103499 aircraft_key=1.
Progress update 2023-01-22 10:01:42.343847 : Updated ev_id=20210727103558 aircraft_key=1.
Progress update 2023-01-22 10:01:42.410829 : Updated ev_id=20210805103634 aircraft_key=1.
Progress update 2023-01-22 10:01:42.485516 : Updated ev_id=20210809103657 aircraft_key=1.
Progress update 2023-01-22 10:01:42.552161 : Updated ev_id=20210810103667 aircraft_key=1.
Progress update 2023-01-22 10:01:42.626982 : Updated ev_id=20210816103700 aircraft_key=1.
Progress update 2023-01-22 10:01:42.693981 : Updated ev_id=20210830103772 aircraft_key=1.
Progress update 2023-01-22 10:01:42.759997 : Updated ev_id=20210830103773 aircraft_key=1.
Progress update 2023-01-22 10:01:42.834920 : Updated ev_id=20210830103775 aircraft_key=1.
Progress update 2023-01-22 10:01:42.901992 : Updated ev_id=20210903103795 aircraft_key=1.
Progress update 2023-01-22 10:01:42.976629 : Updated ev_id=20210908103824 aircraft_key=1.
Progress update 2023-01-22 10:01:43.043403 : Updated ev_id=20211006104055 aircraft_key=1.
Progress update 2023-01-22 10:01:43.209740 : Updated ev_id=20220503105038 aircraft_key=1.
Progress update 2023-01-22 10:01:43.284847 : Updated ev_id=20220525105130 aircraft_key=1.
Progress update 2023-01-22 10:01:43.376751 : Updated ev_id=20220607105206 aircraft_key=1.
Progress update 2023-01-22 10:01:43.476438 : Updated ev_id=20220731105625 aircraft_key=1.
Progress update 2023-01-22 10:01:43.584847 : Updated ev_id=20220912105911 aircraft_key=1.
Progress update 2023-01-22 10:01:43.659885 : Updated ev_id=20220913105930 aircraft_key=1.
Progress update 2023-01-22 10:01:43.726748 : Updated ev_id=20220928106011 aircraft_key=1.
Progress update 2023-01-22 10:01:43.793248 : Updated ev_id=20221003106045 aircraft_key=1.
Progress update 2023-01-22 10:01:43.859525 : Updated ev_id=20221006106075 aircraft_key=1.
Progress update 2023-01-22 10:01:43.926846 : Updated ev_id=20221012106114 aircraft_key=1.
Progress update 2023-01-22 10:01:43.992862 : Updated ev_id=20221013106123 aircraft_key=1.
Progress update 2023-01-22 10:01:44.092968 : Updated ev_id=20221024106184 aircraft_key=1.
Progress update 2023-01-22 10:01:44.159740 : Updated ev_id=20221026106199 aircraft_key=1.
Progress update 2023-01-22 10:01:44.243016 : Updated ev_id=20221103106241 aircraft_key=1.
Progress update 2023-01-22 10:01:44.310017 : Updated ev_id=20221108106259 aircraft_key=1.
Progress update 2023-01-22 10:01:44.393289 : Updated ev_id=20221128106365 aircraft_key=1.
Progress update 2023-01-22 10:01:44.493261 : Updated ev_id=20221208106433 aircraft_key=1.
Progress update 2023-01-22 10:01:44.559852 : Updated ev_id=20221212106439 aircraft_key=1.
Progress update 2023-01-22 10:01:44.651828 : Updated ev_id=20221213106450 aircraft_key=1.
Progress update 2023-01-22 10:01:44.734567 : Updated ev_id=20221215106462 aircraft_key=1.
Progress update 2023-01-22 10:01:44.801362 : Updated ev_id=20221219106471 aircraft_key=1.
Progress update 2023-01-22 10:01:44.868390 : Updated ev_id=20221222106484 aircraft_key=1.
Progress update 2023-01-22 10:01:44.934891 : Updated ev_id=20221222106485 aircraft_key=1.
Progress update 2023-01-22 10:01:45.001349 : Updated ev_id=20221228106502 aircraft_key=1.
Progress update 2023-01-22 10:01:45.068021 : Updated ev_id=20221229106509 aircraft_key=1.
Progress update 2023-01-22 10:01:45.192825 : Updated ev_id=20230104106534 aircraft_key=1.
Progress update 2023-01-22 10:01:45.267825 : Updated ev_id=20230106106544 aircraft_key=1.
Progress update 2023-01-22 10:01:45.409751 : Updated ev_id=20230114106576 aircraft_key=1.
Progress update 2023-01-22 10:01:45.784147 : Number rows selected :    142.
Progress update 2023-01-22 10:01:45.784659 : Number rows inserted :     42.
Progress update 2023-01-22 10:01:45.784659 : Number rows updated  :    100.
Progress update 2023-01-22 10:01:45.784659 :
Progress update 2023-01-22 10:01:45.784659 : Database table       : dt_events           <-----------------------------------.
Progress update 2023-01-22 10:01:45.817738 : Updated ev_id=20191219X91426 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:45.851183 : Updated ev_id=20191219X91426 col_name=launch code=None.
Progress update 2023-01-22 10:01:45.884273 : Updated ev_id=20200807X30140 col_name=launch code=None.
Progress update 2023-01-22 10:01:45.926134 : Updated ev_id=20200807X30140 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:45.942758 : Updated ev_id=20200807X30140 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:45.967758 : Updated ev_id=20200807X30140 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:45.984258 : Updated ev_id=20200807X30140 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:46.009758 : Updated ev_id=20200807X30140 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:46.025760 : Updated ev_id=20200807X30140 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:46.042759 : Updated ev_id=20200807X30140 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:46.067759 : Updated ev_id=20200807X30140 col_name=wx_brief_src code=NET.
Progress update 2023-01-22 10:01:46.092796 : Updated ev_id=20200820X85853 col_name=launch code=None.
Progress update 2023-01-22 10:01:46.125809 : Updated ev_id=20200820X85853 col_name=spec_hand code=PA.
Progress update 2023-01-22 10:01:46.150988 : Updated ev_id=20200820X85853 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:46.175862 : Updated ev_id=20200820X85853 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:46.192639 : Updated ev_id=20200820X85853 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:46.217612 : Updated ev_id=20200820X85853 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:46.242543 : Updated ev_id=20200820X85853 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:46.267563 : Updated ev_id=20200820X85853 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:46.301063 : Updated ev_id=20200820X85853 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:46.325880 : Updated ev_id=20200820X85853 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:46.351381 : Updated ev_id=20201004102078 col_name=launch code=None.
Progress update 2023-01-22 10:01:46.401378 : Updated ev_id=20201004102078 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:46.425878 : Updated ev_id=20201004102078 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:46.450897 : Updated ev_id=20201004102078 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:46.475692 : Updated ev_id=20201004102078 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:46.501219 : Updated ev_id=20201004102078 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:46.525850 : Updated ev_id=20201004102078 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:46.550848 : Updated ev_id=20201004102078 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:46.600943 : Updated ev_id=20201019102162 col_name=launch code=None.
Progress update 2023-01-22 10:01:46.625947 : Updated ev_id=20201019102162 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:46.650970 : Updated ev_id=20201019102162 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:46.675679 : Updated ev_id=20201019102162 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:46.700848 : Updated ev_id=20201019102162 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:46.725865 : Updated ev_id=20201019102162 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:46.750756 : Updated ev_id=20201019102162 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:46.775814 : Updated ev_id=20201019102162 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:46.800846 : Updated ev_id=20201019102162 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:46.825909 : Updated ev_id=20201112102277 col_name=launch code=Part.
Progress update 2023-01-22 10:01:46.850700 : Updated ev_id=20201112102277 col_name=spec_hand code=PA.
Progress update 2023-01-22 10:01:46.875506 : Updated ev_id=20201112102277 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:46.901073 : Updated ev_id=20201112102277 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:46.925573 : Updated ev_id=20201112102277 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:46.950822 : Updated ev_id=20201112102277 col_name=icing_forecast_type code=CLR.
Progress update 2023-01-22 10:01:46.992336 : Updated ev_id=20201112102277 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:47.017354 : Updated ev_id=20201112102277 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:47.042009 : Updated ev_id=20201112102277 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:47.067511 : Updated ev_id=20201112102277 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:47.092010 : Updated ev_id=20201123102332 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.117510 : Updated ev_id=20201123102332 col_name=spec_hand code=GA.
Progress update 2023-01-22 10:01:47.142010 : Updated ev_id=20201123102332 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:47.192010 : Updated ev_id=20210205102605 col_name=launch code=Full.
Progress update 2023-01-22 10:01:47.217397 : Updated ev_id=20210205102605 col_name=spec_hand code=PA.
Progress update 2023-01-22 10:01:47.241946 : Updated ev_id=20210205102605 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:47.267527 : Updated ev_id=20210209102615 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.291950 : Updated ev_id=20210209102615 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:47.317521 : Updated ev_id=20210216102634 col_name=launch code=Part.
Progress update 2023-01-22 10:01:47.342133 : Updated ev_id=20210216102634 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:47.367648 : Updated ev_id=20210216102634 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:47.392149 : Updated ev_id=20210216102634 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:47.417649 : Updated ev_id=20210216102634 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:47.442149 : Updated ev_id=20210216102634 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:47.500649 : Updated ev_id=20210216102634 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:47.525407 : Updated ev_id=20210216102634 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:47.550522 : Updated ev_id=20210216102634 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:47.575408 : Updated ev_id=20210216102634 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:47.600474 : Updated ev_id=20210218102641 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.625347 : Updated ev_id=20210218102641 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:47.650234 : Updated ev_id=20210218102641 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:47.675326 : Updated ev_id=20210218102641 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:47.700508 : Updated ev_id=20210218102641 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:47.725525 : Updated ev_id=20210218102641 col_name=turb_fc_type code=UNKN.
Progress update 2023-01-22 10:01:47.758506 : Updated ev_id=20210218102641 col_name=turb_severity code=UNKN.
Progress update 2023-01-22 10:01:47.784078 : Updated ev_id=20210218102641 col_name=turb_type code=UNKN.
Progress update 2023-01-22 10:01:47.808326 : Updated ev_id=20210218102641 col_name=wx_brief_src code=FSS.
Progress update 2023-01-22 10:01:47.833608 : Updated ev_id=20210219102646 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.883714 : Updated ev_id=20210224102672 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.908306 : Updated ev_id=20210224102672 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:47.933826 : Updated ev_id=20210304102704 col_name=launch code=None.
Progress update 2023-01-22 10:01:47.958444 : Updated ev_id=20210304102704 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:47.983703 : Updated ev_id=20210304102704 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:48.008723 : Updated ev_id=20210304102704 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:48.033764 : Updated ev_id=20210304102704 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:48.058301 : Updated ev_id=20210304102704 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:48.083721 : Updated ev_id=20210304102704 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:48.108737 : Updated ev_id=20210304102704 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:48.133986 : Updated ev_id=20210304102704 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:48.158324 : Updated ev_id=20210304102711 col_name=launch code=Part.
Progress update 2023-01-22 10:01:48.183860 : Updated ev_id=20210304102711 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:48.208859 : Updated ev_id=20210304102711 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:48.233860 : Updated ev_id=20210305102714 col_name=launch code=None.
Progress update 2023-01-22 10:01:48.258862 : Updated ev_id=20210305102714 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:48.383848 : Updated ev_id=20210418102927 col_name=launch code=None.
Progress update 2023-01-22 10:01:48.416921 : Updated ev_id=20210418102927 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:48.450491 : Updated ev_id=20210418102927 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:48.475047 : Updated ev_id=20210418102927 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:48.500550 : Updated ev_id=20210418102927 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:48.525048 : Updated ev_id=20210418102927 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:48.550547 : Updated ev_id=20210418102927 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:48.575049 : Updated ev_id=20210418102927 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:48.600545 : Updated ev_id=20210418102927 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:48.625048 : Updated ev_id=20210418102927 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:48.875213 : Updated ev_id=20210429102997 col_name=launch code=None.
Progress update 2023-01-22 10:01:48.900214 : Updated ev_id=20210429102997 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:48.925214 : Updated ev_id=20210429102997 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:48.974815 : Updated ev_id=20210502103009 col_name=launch code=Part.
Progress update 2023-01-22 10:01:49.000345 : Updated ev_id=20210502103009 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:49.024825 : Updated ev_id=20210502103009 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:49.050154 : Updated ev_id=20210502103009 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:49.074824 : Updated ev_id=20210502103009 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:49.100347 : Updated ev_id=20210502103009 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:49.125182 : Updated ev_id=20210502103009 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:49.150009 : Updated ev_id=20210502103009 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:49.200046 : Updated ev_id=20210502103009 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:49.224835 : Updated ev_id=20210502103009 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:49.250347 : Updated ev_id=20210513103077 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.274825 : Updated ev_id=20210513103077 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:49.300344 : Updated ev_id=20210527103152 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:49.324843 : Updated ev_id=20210527103152 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.350343 : Updated ev_id=20210529103166 col_name=launch code=Part.
Progress update 2023-01-22 10:01:49.375343 : Updated ev_id=20210529103166 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:49.400342 : Updated ev_id=20210529103166 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:49.424842 : Updated ev_id=20210617103285 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.450235 : Updated ev_id=20210617103285 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:49.475006 : Updated ev_id=20210630103379 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.500293 : Updated ev_id=20210630103379 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:49.524721 : Updated ev_id=20210630103379 col_name=wx_brief_src code=ONB.
Progress update 2023-01-22 10:01:49.550222 : Updated ev_id=20210702103405 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.574721 : Updated ev_id=20210702103405 col_name=wx_brief_src code=NET.
Progress update 2023-01-22 10:01:49.650310 : Updated ev_id=20210705103412 col_name=launch code=Part.
Progress update 2023-01-22 10:01:49.674827 : Updated ev_id=20210705103412 col_name=spec_hand code=PA.
Progress update 2023-01-22 10:01:49.700371 : Updated ev_id=20210705103412 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:49.724846 : Updated ev_id=20210714103480 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.750342 : Updated ev_id=20210714103480 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:49.774631 : Updated ev_id=20210714103480 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:49.799987 : Updated ev_id=20210718103499 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.824762 : Updated ev_id=20210718103499 col_name=wx_brief_src code=ONB.
Progress update 2023-01-22 10:01:49.850291 : Updated ev_id=20210727103558 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.874824 : Updated ev_id=20210727103558 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:49.900337 : Updated ev_id=20210805103634 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.925050 : Updated ev_id=20210805103634 col_name=wx_brief_src code=NONE.
Progress update 2023-01-22 10:01:49.949879 : Updated ev_id=20210809103657 col_name=launch code=None.
Progress update 2023-01-22 10:01:49.974630 : Updated ev_id=20210809103657 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:50.024817 : Updated ev_id=20210810103667 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:50.049833 : Updated ev_id=20210810103667 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:50.074690 : Updated ev_id=20210816103700 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.108384 : Updated ev_id=20210816103700 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:50.133260 : Updated ev_id=20210830103772 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.158319 : Updated ev_id=20210830103772 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:50.183009 : Updated ev_id=20210830103773 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.208226 : Updated ev_id=20210830103773 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:50.232840 : Updated ev_id=20210830103775 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.258005 : Updated ev_id=20210830103775 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:50.282590 : Updated ev_id=20210903103795 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.308070 : Updated ev_id=20210903103795 col_name=spec_hand code=TDA.
Progress update 2023-01-22 10:01:50.332733 : Updated ev_id=20210903103795 col_name=wx_brief_src0 code=UNK.
Progress update 2023-01-22 10:01:50.358066 : Updated ev_id=20210908103824 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.383113 : Updated ev_id=20210908103824 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:50.408158 : Updated ev_id=20210908103824 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:50.432672 : Updated ev_id=20211006104055 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:50.458174 : Updated ev_id=20211006104055 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.632978 : Updated ev_id=20220503105038 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:50.657979 : Updated ev_id=20220503105038 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.682977 : Updated ev_id=20220525105130 col_name=launch code=None.
Progress update 2023-01-22 10:01:50.708000 : Updated ev_id=20220525105130 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:50.732759 : Updated ev_id=20220525105130 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:50.757824 : Updated ev_id=20220525105130 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:50.782860 : Updated ev_id=20220525105130 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:50.807912 : Updated ev_id=20220525105130 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:50.832677 : Updated ev_id=20220525105130 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:50.858083 : Updated ev_id=20220525105130 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:50.882596 : Updated ev_id=20220525105130 col_name=wx_brief_src code=NWS.
Progress update 2023-01-22 10:01:50.932596 : Updated ev_id=20220607105206 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:50.958115 : Updated ev_id=20220607105206 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.182557 : Updated ev_id=20220731105625 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:51.232892 : Updated ev_id=20220731105625 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.282787 : Updated ev_id=20220912105911 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.307787 : Updated ev_id=20220912105911 col_name=wx_brief_src code=AUTR.
Progress update 2023-01-22 10:01:51.357787 : Updated ev_id=20220913105930 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.382745 : Updated ev_id=20220928106011 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.466354 : Updated ev_id=20221003106045 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.490763 : Updated ev_id=20221003106045 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:51.516264 : Updated ev_id=20221003106045 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:51.540773 : Updated ev_id=20221003106045 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:51.566273 : Updated ev_id=20221003106045 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:51.591273 : Updated ev_id=20221003106045 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:51.616273 : Updated ev_id=20221003106045 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:51.640773 : Updated ev_id=20221003106045 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:51.690773 : Updated ev_id=20221006106075 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.766273 : Updated ev_id=20221012106114 col_name=launch code=None.
Progress update 2023-01-22 10:01:51.790867 : Updated ev_id=20221012106114 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:51.815950 : Updated ev_id=20221012106114 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:51.840967 : Updated ev_id=20221012106114 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:51.866002 : Updated ev_id=20221012106114 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:51.891035 : Updated ev_id=20221012106114 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:51.916047 : Updated ev_id=20221012106114 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:51.941084 : Updated ev_id=20221012106114 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:52.015965 : Updated ev_id=20221013106123 col_name=launch code=None.
Progress update 2023-01-22 10:01:52.340852 : Updated ev_id=20221024106184 col_name=launch code=None.
Progress update 2023-01-22 10:01:52.365919 : Updated ev_id=20221024106184 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:52.390694 : Updated ev_id=20221024106184 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:52.415806 : Updated ev_id=20221024106184 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:52.440993 : Updated ev_id=20221024106184 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:52.465991 : Updated ev_id=20221024106184 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:52.490975 : Updated ev_id=20221024106184 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:52.515741 : Updated ev_id=20221024106184 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:52.565824 : Updated ev_id=20221026106199 col_name=launch code=None.
Progress update 2023-01-22 10:01:52.823845 : Updated ev_id=20221103106241 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:52.849344 : Updated ev_id=20221103106241 col_name=launch code=None.
Progress update 2023-01-22 10:01:52.898952 : Updated ev_id=20221108106259 col_name=launch code=None.
Progress update 2023-01-22 10:01:52.923629 : Updated ev_id=20221108106259 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:52.949006 : Updated ev_id=20221108106259 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:52.973680 : Updated ev_id=20221108106259 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:52.998769 : Updated ev_id=20221108106259 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:53.023708 : Updated ev_id=20221108106259 col_name=turb_fc_type code=NONE.
Progress update 2023-01-22 10:01:53.048823 : Updated ev_id=20221108106259 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:53.073845 : Updated ev_id=20221108106259 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:53.349179 : Updated ev_id=20221128106365 col_name=launch code=None.
Progress update 2023-01-22 10:01:53.398942 : Updated ev_id=20221128106365 col_name=icing_actual_amt code=NONE.
Progress update 2023-01-22 10:01:53.423639 : Updated ev_id=20221128106365 col_name=icing_actual_type code=NA.
Progress update 2023-01-22 10:01:53.448860 : Updated ev_id=20221128106365 col_name=icing_forecast_amt code=NONE.
Progress update 2023-01-22 10:01:53.473899 : Updated ev_id=20221128106365 col_name=icing_forecast_type code=NA.
Progress update 2023-01-22 10:01:53.498916 : Updated ev_id=20221128106365 col_name=turb_fc_type code=UNKN.
Progress update 2023-01-22 10:01:53.523425 : Updated ev_id=20221128106365 col_name=turb_severity code=NA.
Progress update 2023-01-22 10:01:53.548944 : Updated ev_id=20221128106365 col_name=turb_type code=NONE.
Progress update 2023-01-22 10:01:53.648810 : Updated ev_id=20221208106433 col_name=launch code=None.
Progress update 2023-01-22 10:01:53.673922 : Updated ev_id=20221212106439 col_name=launch code=None.
Progress update 2023-01-22 10:01:53.698844 : Updated ev_id=20221213106450 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:53.723867 : Updated ev_id=20221213106450 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.023844 : Updated ev_id=20221215106462 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.048765 : Updated ev_id=20221215106462 col_name=wx_brief_src code=COMP.
Progress update 2023-01-22 10:01:54.073823 : Updated ev_id=20221219106471 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:54.099004 : Updated ev_id=20221219106471 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.123588 : Updated ev_id=20221222106484 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:54.148612 : Updated ev_id=20221222106484 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.173615 : Updated ev_id=20221222106485 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:54.207006 : Updated ev_id=20221222106485 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.231843 : Updated ev_id=20221228106502 col_name=followup_travel code=N.
Progress update 2023-01-22 10:01:54.256905 : Updated ev_id=20221228106502 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.307291 : Updated ev_id=20221229106509 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.506836 : Updated ev_id=20230104106534 col_name=launch code=None.
Progress update 2023-01-22 10:01:54.607009 : Updated ev_id=20230106106544 col_name=launch code=None.
Progress update 2023-01-22 10:01:55.065082 : Updated ev_id=20230114106576 col_name=launch code=None.
Progress update 2023-01-22 10:01:55.964866 : Number rows selected :    393.
Progress update 2023-01-22 10:01:55.965366 : Number rows inserted :    150.
Progress update 2023-01-22 10:01:55.965366 : Number rows updated  :    243.
Progress update 2023-01-22 10:01:55.965366 :
Progress update 2023-01-22 10:01:55.965366 : Database table       : ntsb_admin          <-----------------------------------.
Progress update 2023-01-22 10:01:55.997847 : Updated ev_id=20001211X14762.
Progress update 2023-01-22 10:01:56.023321 : Updated ev_id=20001212X22676.
Progress update 2023-01-22 10:01:56.048322 : Updated ev_id=20001212X23076.
Progress update 2023-01-22 10:01:56.073321 : Updated ev_id=20001212X23897.
Progress update 2023-01-22 10:01:56.098322 : Updated ev_id=20001212X23332.
Progress update 2023-01-22 10:01:56.123321 : Updated ev_id=20001212X24569.
Progress update 2023-01-22 10:01:56.147821 : Updated ev_id=20001212X16779.
Progress update 2023-01-22 10:01:56.173321 : Updated ev_id=20001213X28070.
Progress update 2023-01-22 10:01:56.198008 : Updated ev_id=20001213X29333.
Progress update 2023-01-22 10:01:56.223118 : Updated ev_id=20001212X22536.
Progress update 2023-01-22 10:01:56.273342 : Updated ev_id=20001212X24443.
Progress update 2023-01-22 10:01:56.297842 : Updated ev_id=20001213X27903.
Progress update 2023-01-22 10:01:56.323256 : Updated ev_id=20001213X29965.
Progress update 2023-01-22 10:01:56.347753 : Updated ev_id=20001212X22962.
Progress update 2023-01-22 10:01:56.373419 : Updated ev_id=20001212X22963.
Progress update 2023-01-22 10:01:56.397973 : Updated ev_id=20001212X23204.
Progress update 2023-01-22 10:01:56.423068 : Updated ev_id=20001212X23474.
Progress update 2023-01-22 10:01:56.447841 : Updated ev_id=20001212X24647.
Progress update 2023-01-22 10:01:56.473032 : Updated ev_id=20001212X24648.
Progress update 2023-01-22 10:01:56.498066 : Updated ev_id=20001212X16648.
Progress update 2023-01-22 10:01:56.523142 : Updated ev_id=20001212X17333.
Progress update 2023-01-22 10:01:56.547822 : Updated ev_id=20001213X28160.
Progress update 2023-01-22 10:01:56.573001 : Updated ev_id=20001213X29454.
Progress update 2023-01-22 10:01:56.598017 : Updated ev_id=20001213X29845.
Progress update 2023-01-22 10:01:56.623070 : Updated ev_id=20001212X22977.
Progress update 2023-01-22 10:01:56.648002 : Updated ev_id=20001212X23225.
Progress update 2023-01-22 10:01:56.673020 : Updated ev_id=20001212X23226.
Progress update 2023-01-22 10:01:56.698020 : Updated ev_id=20001212X24086.
Progress update 2023-01-22 10:01:56.723322 : Updated ev_id=20001212X24795.
Progress update 2023-01-22 10:01:56.748062 : Updated ev_id=20001212X23037.
Progress update 2023-01-22 10:01:56.773104 : Updated ev_id=20001212X23564.
Progress update 2023-01-22 10:01:56.797799 : Updated ev_id=20001212X24145.
Progress update 2023-01-22 10:01:56.823260 : Updated ev_id=20001212X22824.
Progress update 2023-01-22 10:01:56.847758 : Updated ev_id=20191219X91426.
Progress update 2023-01-22 10:01:56.873275 : Updated ev_id=20200807X30140.
Progress update 2023-01-22 10:01:56.898043 : Updated ev_id=20200820X85853.
Progress update 2023-01-22 10:01:56.964761 : Updated ev_id=20201004102078.
Progress update 2023-01-22 10:01:56.989838 : Updated ev_id=20201019102162.
Progress update 2023-01-22 10:01:57.014342 : Updated ev_id=20201112102277.
Progress update 2023-01-22 10:01:57.039896 : Updated ev_id=20201123102332.
Progress update 2023-01-22 10:01:57.064394 : Updated ev_id=20210205102605.
Progress update 2023-01-22 10:01:57.089895 : Updated ev_id=20210209102615.
Progress update 2023-01-22 10:01:57.114394 : Updated ev_id=20210216102634.
Progress update 2023-01-22 10:01:57.139894 : Updated ev_id=20210218102641.
Progress update 2023-01-22 10:01:57.164393 : Updated ev_id=20210219102646.
Progress update 2023-01-22 10:01:57.189894 : Updated ev_id=20210224102672.
Progress update 2023-01-22 10:01:57.239895 : Updated ev_id=20210304102704.
Progress update 2023-01-22 10:01:57.264395 : Updated ev_id=20210304102711.
Progress update 2023-01-22 10:01:57.289897 : Updated ev_id=20210305102714.
Progress update 2023-01-22 10:01:57.339788 : Updated ev_id=20210418102927.
Progress update 2023-01-22 10:01:57.389768 : Updated ev_id=20210429102997.
Progress update 2023-01-22 10:01:57.414603 : Updated ev_id=20210502103009.
Progress update 2023-01-22 10:01:57.439586 : Updated ev_id=20210513103077.
Progress update 2023-01-22 10:01:57.489822 : Updated ev_id=20210527103152.
Progress update 2023-01-22 10:01:57.514339 : Updated ev_id=20210529103166.
Progress update 2023-01-22 10:01:57.539807 : Updated ev_id=20210617103285.
Progress update 2023-01-22 10:01:57.564325 : Updated ev_id=20210630103379.
Progress update 2023-01-22 10:01:57.589565 : Updated ev_id=20210702103405.
Progress update 2023-01-22 10:01:57.639495 : Updated ev_id=20210705103412.
Progress update 2023-01-22 10:01:57.664547 : Updated ev_id=20210714103480.
Progress update 2023-01-22 10:01:57.689762 : Updated ev_id=20210718103499.
Progress update 2023-01-22 10:01:57.714258 : Updated ev_id=20210727103558.
Progress update 2023-01-22 10:01:57.764281 : Updated ev_id=20210805103634.
Progress update 2023-01-22 10:01:57.789334 : Updated ev_id=20210809103657.
Progress update 2023-01-22 10:01:57.814259 : Updated ev_id=20210810103667.
Progress update 2023-01-22 10:01:57.839787 : Updated ev_id=20210816103700.
Progress update 2023-01-22 10:01:57.864305 : Updated ev_id=20210830103772.
Progress update 2023-01-22 10:01:57.889474 : Updated ev_id=20210830103773.
Progress update 2023-01-22 10:01:57.914498 : Updated ev_id=20210830103775.
Progress update 2023-01-22 10:01:57.939509 : Updated ev_id=20210903103795.
Progress update 2023-01-22 10:01:57.964214 : Updated ev_id=20210908103824.
Progress update 2023-01-22 10:01:57.989582 : Updated ev_id=20211006104055.
Progress update 2023-01-22 10:01:58.114320 : Updated ev_id=20220503105038.
Progress update 2023-01-22 10:01:58.141820 : Updated ev_id=20220525105130.
Progress update 2023-01-22 10:01:58.188821 : Updated ev_id=20220607105206.
Progress update 2023-01-22 10:01:58.238840 : Updated ev_id=20220731105625.
Progress update 2023-01-22 10:01:58.289185 : Updated ev_id=20220912105911.
Progress update 2023-01-22 10:01:58.314185 : Updated ev_id=20220913105930.
Progress update 2023-01-22 10:01:58.339185 : Updated ev_id=20220928106011.
Progress update 2023-01-22 10:01:58.364186 : Updated ev_id=20221003106045.
Progress update 2023-01-22 10:01:58.397205 : Updated ev_id=20221006106075.
Progress update 2023-01-22 10:01:58.422714 : Updated ev_id=20221012106114.
Progress update 2023-01-22 10:01:58.447333 : Updated ev_id=20221013106123.
Progress update 2023-01-22 10:01:58.522413 : Updated ev_id=20221024106184.
Progress update 2023-01-22 10:01:58.547428 : Updated ev_id=20221026106199.
Progress update 2023-01-22 10:01:58.597182 : Updated ev_id=20221103106241.
Progress update 2023-01-22 10:01:58.622315 : Updated ev_id=20221108106259.
Progress update 2023-01-22 10:01:58.672262 : Updated ev_id=20221128106365.
Progress update 2023-01-22 10:01:58.722292 : Updated ev_id=20221208106433.
Progress update 2023-01-22 10:01:58.747002 : Updated ev_id=20221212106439.
Progress update 2023-01-22 10:01:58.772845 : Updated ev_id=20221213106450.
Progress update 2023-01-22 10:01:58.822631 : Updated ev_id=20221215106462.
Progress update 2023-01-22 10:01:58.847117 : Updated ev_id=20221219106471.
Progress update 2023-01-22 10:01:58.872381 : Updated ev_id=20221222106484.
Progress update 2023-01-22 10:01:58.897382 : Updated ev_id=20221222106485.
Progress update 2023-01-22 10:01:58.922321 : Updated ev_id=20221228106502.
Progress update 2023-01-22 10:01:58.947332 : Updated ev_id=20221229106509.
Progress update 2023-01-22 10:01:59.047346 : Updated ev_id=20230104106534.
Progress update 2023-01-22 10:01:59.096909 : Updated ev_id=20230106106544.
Progress update 2023-01-22 10:01:59.222650 : Updated ev_id=20230114106576.
Progress update 2023-01-22 10:01:59.646898 : Number rows selected :    141.
Progress update 2023-01-22 10:01:59.647399 : Number rows inserted :     41.
Progress update 2023-01-22 10:01:59.647399 : Number rows updated  :    100.
Progress update 2023-01-22 10:01:59.647399 :
Progress update 2023-01-22 10:01:59.647399 : Database table       : dt_aircraft         <-----------------------------------.
Progress update 2023-01-22 10:01:59.847258 : Updated ev_id=20001212X23897 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:01:59.997150 : Updated ev_id=20001212X24569 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:00.172073 : Updated ev_id=20001213X29333 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:00.247103 : Updated ev_id=20001212X22536 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:00.505301 : Updated ev_id=20001212X23474 aircraft_key=1 col_name=aircar_cert code=TAXI.
Progress update 2023-01-22 10:02:00.738757 : Updated ev_id=20001213X29454 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:00.938559 : Updated ev_id=20001212X23226 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:01.238274 : Updated ev_id=20001212X22824 aircraft_key=1 col_name=aircar_cert code=TAXI.
Progress update 2023-01-22 10:02:01.396818 : Updated ev_id=20200807X30140 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:01.471821 : Updated ev_id=20200807X30140 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:01.521908 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:01.546334 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:01.563344 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:01.579879 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:01.596451 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=addtl_equip code=HGPS.
Progress update 2023-01-22 10:02:01.621470 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:01.646969 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:01.671470 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=airspc_type code=CLD.
Progress update 2023-01-22 10:02:01.696969 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:01.721469 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:01.746468 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:01.771326 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=landing_surf code=CONC.
Progress update 2023-01-22 10:02:01.796859 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:01.829788 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:01.846509 : Updated ev_id=20200820X85853 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:01.921166 : Updated ev_id=20201004102078 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:01.971235 : Updated ev_id=20201004102078 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:01.996415 : Updated ev_id=20201004102078 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:02.029820 : Updated ev_id=20201004102078 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:02.046358 : Updated ev_id=20201004102078 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:02.079819 : Updated ev_id=20201004102078 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:02.112889 : Updated ev_id=20201019102162 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:02.129964 : Updated ev_id=20201019102162 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:02.146320 : Updated ev_id=20201019102162 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:02.163338 : Updated ev_id=20201019102162 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:02.205002 : Updated ev_id=20201019102162 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:02.221116 : Updated ev_id=20201019102162 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:02.237985 : Updated ev_id=20201019102162 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:02.254503 : Updated ev_id=20201019102162 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:02.271341 : Updated ev_id=20201019102162 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:02.296522 : Updated ev_id=20201019102162 aircraft_key=1 col_name=vfr_appr code=TOGO.
Progress update 2023-01-22 10:02:02.312969 : Updated ev_id=20201019102162 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:02.346179 : Updated ev_id=20201019102162 aircraft_key=1 col_name=landing_gear code=SKID.
Progress update 2023-01-22 10:02:02.380102 : Updated ev_id=20201112102277 aircraft_key=1 col_name=acft_awy_cert code=OTH.
Progress update 2023-01-22 10:02:02.396105 : Updated ev_id=20201112102277 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:02.413102 : Updated ev_id=20201112102277 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:02.446451 : Updated ev_id=20201112102277 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:02.479953 : Updated ev_id=20201112102277 aircraft_key=1 col_name=addtl_equip code=OBWX.
Progress update 2023-01-22 10:02:02.512953 : Updated ev_id=20201112102277 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:02.546453 : Updated ev_id=20201112102277 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:02.571470 : Updated ev_id=20201112102277 aircraft_key=1 col_name=airspc_type code=CLD.
Progress update 2023-01-22 10:02:02.587981 : Updated ev_id=20201112102277 aircraft_key=1 col_name=elt_oper_no_reason code=FIRE.
Progress update 2023-01-22 10:02:02.604721 : Updated ev_id=20201112102277 aircraft_key=1 col_name=elt_oper_no_reason code=IMPD.
Progress update 2023-01-22 10:02:02.621341 : Updated ev_id=20201112102277 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:02.646408 : Updated ev_id=20201112102277 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:02.662922 : Updated ev_id=20201112102277 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:02.696441 : Updated ev_id=20201112102277 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:02.721319 : Updated ev_id=20201112102277 aircraft_key=1 col_name=type_clear code=VFRF.
Progress update 2023-01-22 10:02:02.754835 : Updated ev_id=20201112102277 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:02.779835 : Updated ev_id=20201123102332 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:02.812834 : Updated ev_id=20201123102332 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:02.838334 : Updated ev_id=20201123102332 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:02.862834 : Updated ev_id=20201123102332 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:02.896335 : Updated ev_id=20201123102332 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:02.912833 : Updated ev_id=20201123102332 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:02.929334 : Updated ev_id=20201123102332 aircraft_key=1 col_name=airspc_type code=CLC.
Progress update 2023-01-22 10:02:02.946289 : Updated ev_id=20201123102332 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:02.962750 : Updated ev_id=20201123102332 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:02.988310 : Updated ev_id=20201123102332 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:03.021309 : Updated ev_id=20201123102332 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:03.046308 : Updated ev_id=20201123102332 aircraft_key=1 col_name=type_clear code=VFR.
Progress update 2023-01-22 10:02:03.062809 : Updated ev_id=20201123102332 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:03.079810 : Updated ev_id=20210205102605 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:03.096308 : Updated ev_id=20210205102605 aircraft_key=1 col_name=addtl_equip code=HGPS.
Progress update 2023-01-22 10:02:03.112951 : Updated ev_id=20210205102605 aircraft_key=1 col_name=addtl_equip code=SATD.
Progress update 2023-01-22 10:02:03.129462 : Updated ev_id=20210205102605 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:03.146491 : Updated ev_id=20210205102605 aircraft_key=1 col_name=aircar_cert code=COAC.
Progress update 2023-01-22 10:02:03.163005 : Updated ev_id=20210205102605 aircraft_key=1 col_name=aircar_cert code=TAXI.
Progress update 2023-01-22 10:02:03.179866 : Updated ev_id=20210205102605 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:03.204470 : Updated ev_id=20210205102605 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:03.221395 : Updated ev_id=20210205102605 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:03.254501 : Updated ev_id=20210205102605 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:03.271502 : Updated ev_id=20210205102605 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:03.304536 : Updated ev_id=20210205102605 aircraft_key=1 col_name=landing_gear code=SKWH.
Progress update 2023-01-22 10:02:03.337869 : Updated ev_id=20210209102615 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:03.370911 : Updated ev_id=20210209102615 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:03.404471 : Updated ev_id=20210209102615 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:03.421319 : Updated ev_id=20210209102615 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:03.437969 : Updated ev_id=20210209102615 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:03.471082 : Updated ev_id=20210209102615 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:03.487446 : Updated ev_id=20210209102615 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:03.504644 : Updated ev_id=20210209102615 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:03.529143 : Updated ev_id=20210209102615 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:03.563143 : Updated ev_id=20210209102615 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:03.596146 : Updated ev_id=20210209102615 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:03.621161 : Updated ev_id=20210209102615 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:03.637377 : Updated ev_id=20210209102615 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:03.687339 : Updated ev_id=20210209102615 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:03.721341 : Updated ev_id=20210216102634 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:03.762817 : Updated ev_id=20210216102634 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:03.779359 : Updated ev_id=20210216102634 aircraft_key=1 col_name=aircar_cert code=COAC.
Progress update 2023-01-22 10:02:03.812501 : Updated ev_id=20210216102634 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:03.829585 : Updated ev_id=20210216102634 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:03.845700 : Updated ev_id=20210216102634 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:03.862700 : Updated ev_id=20210216102634 aircraft_key=1 col_name=landing_gear code=SKID.
Progress update 2023-01-22 10:02:03.904701 : Updated ev_id=20210218102641 aircraft_key=1 col_name=acft_awy_cert code=STU.
Progress update 2023-01-22 10:02:03.929201 : Updated ev_id=20210218102641 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:03.954201 : Updated ev_id=20210218102641 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:03.979203 : Updated ev_id=20210218102641 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:04.004257 : Updated ev_id=20210218102641 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:04.029272 : Updated ev_id=20210218102641 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:04.054288 : Updated ev_id=20210218102641 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:04.079339 : Updated ev_id=20210218102641 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:04.129018 : Updated ev_id=20210218102641 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:04.154598 : Updated ev_id=20210218102641 aircraft_key=1 col_name=type_clear code=TRAD.
Progress update 2023-01-22 10:02:04.179167 : Updated ev_id=20210218102641 aircraft_key=1 col_name=vfr_appr code=GOAR.
Progress update 2023-01-22 10:02:04.204206 : Updated ev_id=20210218102641 aircraft_key=1 col_name=vfr_appr code=PLND.
Progress update 2023-01-22 10:02:04.237615 : Updated ev_id=20210218102641 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:04.387152 : Updated ev_id=20210224102672 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:04.412841 : Updated ev_id=20210224102672 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:04.437356 : Updated ev_id=20210224102672 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:04.462759 : Updated ev_id=20210224102672 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:04.487296 : Updated ev_id=20210224102672 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:04.537336 : Updated ev_id=20210224102672 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:04.562400 : Updated ev_id=20210224102672 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:04.587400 : Updated ev_id=20210224102672 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:04.612400 : Updated ev_id=20210224102672 aircraft_key=1 col_name=landing_surf code=CONC.
Progress update 2023-01-22 10:02:04.637400 : Updated ev_id=20210224102672 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:04.662401 : Updated ev_id=20210224102672 aircraft_key=1 col_name=type_clear code=IFR.
Progress update 2023-01-22 10:02:04.687418 : Updated ev_id=20210224102672 aircraft_key=1 col_name=vfr_appr code=FSTP.
Progress update 2023-01-22 10:02:04.712699 : Updated ev_id=20210224102672 aircraft_key=1 col_name=vfr_appr code=STIN.
Progress update 2023-01-22 10:02:04.737319 : Updated ev_id=20210304102704 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:04.787755 : Updated ev_id=20210304102704 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:04.812431 : Updated ev_id=20210304102704 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:04.837319 : Updated ev_id=20210304102704 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:04.862693 : Updated ev_id=20210304102704 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:04.887224 : Updated ev_id=20210304102704 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:04.912337 : Updated ev_id=20210304102704 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:04.937338 : Updated ev_id=20210304102704 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:04.962319 : Updated ev_id=20210304102704 aircraft_key=1 col_name=vfr_appr code=STGO.
Progress update 2023-01-22 10:02:04.995818 : Updated ev_id=20210304102711 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:05.029319 : Updated ev_id=20210304102711 aircraft_key=1 col_name=acft_awy_cert code=STU.
Progress update 2023-01-22 10:02:05.053819 : Updated ev_id=20210304102711 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:05.095997 : Updated ev_id=20210304102711 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:05.149980 : Updated ev_id=20210304102711 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:05.179416 : Updated ev_id=20210304102711 aircraft_key=1 col_name=elt_oper_no_reason code=OTHR.
Progress update 2023-01-22 10:02:05.203994 : Updated ev_id=20210304102711 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:05.229056 : Updated ev_id=20210304102711 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:05.253911 : Updated ev_id=20210304102711 aircraft_key=1 col_name=landing_surf code=GRAS.
Progress update 2023-01-22 10:02:05.278946 : Updated ev_id=20210304102711 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:05.303953 : Updated ev_id=20210304102711 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:05.329127 : Updated ev_id=20210304102711 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:05.353763 : Updated ev_id=20210305102714 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:05.378928 : Updated ev_id=20210305102714 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:05.403914 : Updated ev_id=20210305102714 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:05.428949 : Updated ev_id=20210305102714 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:05.453701 : Updated ev_id=20210305102714 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:05.479036 : Updated ev_id=20210305102714 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:05.503863 : Updated ev_id=20210305102714 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:05.528889 : Updated ev_id=20210305102714 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:05.554001 : Updated ev_id=20210305102714 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:05.578799 : Updated ev_id=20210305102714 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:05.604002 : Updated ev_id=20210305102714 aircraft_key=1 col_name=rwy_cond1 code=ROUG.
Progress update 2023-01-22 10:02:05.629264 : Updated ev_id=20210305102714 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:05.653733 : Updated ev_id=20210305102714 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:05.895836 : Updated ev_id=20210418102927 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:05.920337 : Updated ev_id=20210418102927 aircraft_key=1 col_name=addtl_equip0 code=NONE.
Progress update 2023-01-22 10:02:05.945840 : Updated ev_id=20210418102927 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:05.970409 : Updated ev_id=20210418102927 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:05.995819 : Updated ev_id=20210418102927 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.020348 : Updated ev_id=20210418102927 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:06.045603 : Updated ev_id=20210418102927 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:06.070414 : Updated ev_id=20210418102927 aircraft_key=1 col_name=rwy_cond1 code=ROUG.
Progress update 2023-01-22 10:02:06.095569 : Updated ev_id=20210418102927 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:06.120569 : Updated ev_id=20210418102927 aircraft_key=1 col_name=type_clear1 code=UNK.
Progress update 2023-01-22 10:02:06.145569 : Updated ev_id=20210418102927 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.295532 : Updated ev_id=20210429102997 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:06.320536 : Updated ev_id=20210429102997 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:06.345532 : Updated ev_id=20210429102997 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.379032 : Updated ev_id=20210429102997 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:06.412544 : Updated ev_id=20210429102997 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:06.436837 : Updated ev_id=20210429102997 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:06.486905 : Updated ev_id=20210502103009 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:06.512316 : Updated ev_id=20210502103009 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:06.536851 : Updated ev_id=20210502103009 aircraft_key=1 col_name=aircar_cert code=AGR.
Progress update 2023-01-22 10:02:06.561818 : Updated ev_id=20210502103009 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:06.586839 : Updated ev_id=20210502103009 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.611856 : Updated ev_id=20210502103009 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:06.636854 : Updated ev_id=20210502103009 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.661882 : Updated ev_id=20210502103009 aircraft_key=1 col_name=landing_gear code=SKID.
Progress update 2023-01-22 10:02:06.711817 : Updated ev_id=20210513103077 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:06.736819 : Updated ev_id=20210513103077 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:06.761817 : Updated ev_id=20210513103077 aircraft_key=1 col_name=addtl_equip code=AOAI.
Progress update 2023-01-22 10:02:06.786817 : Updated ev_id=20210513103077 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:06.811817 : Updated ev_id=20210513103077 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:06.836500 : Updated ev_id=20210513103077 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:06.862003 : Updated ev_id=20210513103077 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:06.886527 : Updated ev_id=20210513103077 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:06.911748 : Updated ev_id=20210513103077 aircraft_key=1 col_name=landing_gear code=SKID.
Progress update 2023-01-22 10:02:07.036794 : Updated ev_id=20210529103166 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:07.061761 : Updated ev_id=20210529103166 aircraft_key=1 col_name=acft_awy_cert code=STU.
Progress update 2023-01-22 10:02:07.086786 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:07.111785 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=AOAI.
Progress update 2023-01-22 10:02:07.136811 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:07.161726 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:07.186553 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:07.212053 : Updated ev_id=20210529103166 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:07.236553 : Updated ev_id=20210529103166 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:07.262053 : Updated ev_id=20210529103166 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:07.286552 : Updated ev_id=20210529103166 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:07.311553 : Updated ev_id=20210529103166 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:07.361769 : Updated ev_id=20210529103166 aircraft_key=1 col_name=type_clear1 code=UNK.
Progress update 2023-01-22 10:02:07.386339 : Updated ev_id=20210529103166 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:07.411840 : Updated ev_id=20210617103285 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:07.436839 : Updated ev_id=20210617103285 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:07.461838 : Updated ev_id=20210617103285 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:07.486414 : Updated ev_id=20210617103285 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:07.511890 : Updated ev_id=20210617103285 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:07.536622 : Updated ev_id=20210617103285 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:07.561898 : Updated ev_id=20210617103285 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:07.586709 : Updated ev_id=20210617103285 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:07.611997 : Updated ev_id=20210617103285 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:07.636536 : Updated ev_id=20210630103379 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:07.661811 : Updated ev_id=20210630103379 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:07.686345 : Updated ev_id=20210630103379 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:07.711758 : Updated ev_id=20210630103379 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:07.736497 : Updated ev_id=20210630103379 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:07.761510 : Updated ev_id=20210630103379 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:07.786528 : Updated ev_id=20210630103379 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:07.811527 : Updated ev_id=20210630103379 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:07.845028 : Updated ev_id=20210630103379 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:07.870027 : Updated ev_id=20210630103379 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:07.894527 : Updated ev_id=20210630103379 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:07.920076 : Updated ev_id=20210630103379 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:07.944593 : Updated ev_id=20210630103379 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:08.020199 : Updated ev_id=20210702103405 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:08.044695 : Updated ev_id=20210702103405 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:08.070199 : Updated ev_id=20210702103405 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:08.094695 : Updated ev_id=20210702103405 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:08.161696 : Updated ev_id=20210702103405 aircraft_key=1 col_name=elt_oper_no_reason code=OTHR.
Progress update 2023-01-22 10:02:08.186196 : Updated ev_id=20210702103405 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:08.211696 : Updated ev_id=20210702103405 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:08.236213 : Updated ev_id=20210702103405 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:08.261761 : Updated ev_id=20210702103405 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:08.286260 : Updated ev_id=20210702103405 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:08.311788 : Updated ev_id=20210702103405 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:08.486434 : Updated ev_id=20210705103412 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:08.511406 : Updated ev_id=20210705103412 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:08.536316 : Updated ev_id=20210705103412 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:08.561828 : Updated ev_id=20210705103412 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:08.586352 : Updated ev_id=20210705103412 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:08.611351 : Updated ev_id=20210705103412 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:08.636352 : Updated ev_id=20210705103412 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:08.661434 : Updated ev_id=20210705103412 aircraft_key=1 col_name=elt_oper_no_reason code=FIRE.
Progress update 2023-01-22 10:02:08.686292 : Updated ev_id=20210705103412 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:08.711292 : Updated ev_id=20210705103412 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:08.736292 : Updated ev_id=20210705103412 aircraft_key=1 col_name=type_clear code=VFR.
Progress update 2023-01-22 10:02:08.761292 : Updated ev_id=20210705103412 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:08.811293 : Updated ev_id=20210714103480 aircraft_key=1 col_name=acft_awy_cert code=SPR.
Progress update 2023-01-22 10:02:08.836295 : Updated ev_id=20210714103480 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:08.861792 : Updated ev_id=20210714103480 aircraft_key=1 col_name=aircar_cert code=AGR.
Progress update 2023-01-22 10:02:08.886292 : Updated ev_id=20210714103480 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:08.911292 : Updated ev_id=20210714103480 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:08.936292 : Updated ev_id=20210714103480 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:08.961338 : Updated ev_id=20210714103480 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:08.986339 : Updated ev_id=20210714103480 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:09.011385 : Updated ev_id=20210718103499 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:09.044411 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:09.069256 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=AOAI.
Progress update 2023-01-22 10:02:09.094772 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=AUTO.
Progress update 2023-01-22 10:02:09.119336 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:09.144840 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:09.169340 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=HUPD.
Progress update 2023-01-22 10:02:09.194652 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=SATD.
Progress update 2023-01-22 10:02:09.219250 : Updated ev_id=20210718103499 aircraft_key=1 col_name=addtl_equip code=STWS.
Progress update 2023-01-22 10:02:09.244715 : Updated ev_id=20210718103499 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:09.269237 : Updated ev_id=20210718103499 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:09.294428 : Updated ev_id=20210718103499 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.319291 : Updated ev_id=20210718103499 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:09.344813 : Updated ev_id=20210718103499 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:09.369412 : Updated ev_id=20210718103499 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:09.394759 : Updated ev_id=20210718103499 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.419274 : Updated ev_id=20210727103558 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:09.444775 : Updated ev_id=20210727103558 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:09.469275 : Updated ev_id=20210727103558 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:09.494775 : Updated ev_id=20210727103558 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.519274 : Updated ev_id=20210727103558 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:09.544774 : Updated ev_id=20210727103558 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:09.569336 : Updated ev_id=20210727103558 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:09.594400 : Updated ev_id=20210727103558 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:09.619416 : Updated ev_id=20210727103558 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.644495 : Updated ev_id=20210805103634 aircraft_key=1 col_name=acft_awy_cert code=SPR.
Progress update 2023-01-22 10:02:09.669465 : Updated ev_id=20210805103634 aircraft_key=1 col_name=addtl_equip0 code=NONE.
Progress update 2023-01-22 10:02:09.694259 : Updated ev_id=20210805103634 aircraft_key=1 col_name=aircar_cert code=AGR.
Progress update 2023-01-22 10:02:09.718996 : Updated ev_id=20210805103634 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:09.744597 : Updated ev_id=20210805103634 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.769271 : Updated ev_id=20210805103634 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:09.794314 : Updated ev_id=20210805103634 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:09.819332 : Updated ev_id=20210805103634 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:09.844362 : Updated ev_id=20210805103634 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:09.869371 : Updated ev_id=20210809103657 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:09.894363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:09.919363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:09.944363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:09.969364 : Updated ev_id=20210809103657 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:09.994363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=landing_surf code=GRAS.
Progress update 2023-01-22 10:02:10.019363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:10.044363 : Updated ev_id=20210809103657 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:10.069363 : Updated ev_id=20210810103667 aircraft_key=1 col_name=acft_awy_cert code=SPR.
Progress update 2023-01-22 10:02:10.094389 : Updated ev_id=20210810103667 aircraft_key=1 col_name=addtl_equip code=DREC.
Progress update 2023-01-22 10:02:10.119075 : Updated ev_id=20210810103667 aircraft_key=1 col_name=addtl_equip code=SATD.
Progress update 2023-01-22 10:02:10.144201 : Updated ev_id=20210810103667 aircraft_key=1 col_name=aircar_cert code=AGR.
Progress update 2023-01-22 10:02:10.169211 : Updated ev_id=20210810103667 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:10.194232 : Updated ev_id=20210810103667 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:10.219288 : Updated ev_id=20210810103667 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:10.244258 : Updated ev_id=20210810103667 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:10.269328 : Updated ev_id=20210810103667 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:10.294485 : Updated ev_id=20210816103700 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:10.318999 : Updated ev_id=20210816103700 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:10.344151 : Updated ev_id=20210816103700 aircraft_key=1 col_name=addtl_equip code=AOAI.
Progress update 2023-01-22 10:02:10.368904 : Updated ev_id=20210816103700 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:10.394497 : Updated ev_id=20210816103700 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:10.444530 : Updated ev_id=20210816103700 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:10.469356 : Updated ev_id=20210816103700 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:10.494082 : Updated ev_id=20210816103700 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:10.519083 : Updated ev_id=20210816103700 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:10.561081 : Updated ev_id=20210816103700 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:10.586081 : Updated ev_id=20210816103700 aircraft_key=1 col_name=landing_surf code=CONC.
Progress update 2023-01-22 10:02:10.611082 : Updated ev_id=20210816103700 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:10.636083 : Updated ev_id=20210816103700 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:10.701083 : Updated ev_id=20210816103700 aircraft_key=1 col_name=vfr_appr code=FSTP.
Progress update 2023-01-22 10:02:10.718925 : Updated ev_id=20210816103700 aircraft_key=1 col_name=vfr_appr code=STIN.
Progress update 2023-01-22 10:02:10.744294 : Updated ev_id=20210830103772 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:10.769066 : Updated ev_id=20210830103772 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:10.794336 : Updated ev_id=20210830103772 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:10.818928 : Updated ev_id=20210830103772 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:10.844316 : Updated ev_id=20210830103772 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:10.868916 : Updated ev_id=20210830103772 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:10.894430 : Updated ev_id=20210830103772 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:10.918885 : Updated ev_id=20210830103772 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:10.944140 : Updated ev_id=20210830103773 aircraft_key=1 col_name=acft_awy_cert code=SPR.
Progress update 2023-01-22 10:02:10.969170 : Updated ev_id=20210830103773 aircraft_key=1 col_name=addtl_equip0 code=NONE.
Progress update 2023-01-22 10:02:10.994315 : Updated ev_id=20210830103773 aircraft_key=1 col_name=aircar_cert code=AGR.
Progress update 2023-01-22 10:02:11.018861 : Updated ev_id=20210830103773 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:11.044173 : Updated ev_id=20210830103773 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:11.069173 : Updated ev_id=20210830103773 aircraft_key=1 col_name=landing_gear0 code=NONE.
Progress update 2023-01-22 10:02:11.094174 : Updated ev_id=20210830103773 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:11.119173 : Updated ev_id=20210830103773 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:11.144173 : Updated ev_id=20210830103773 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:11.169001 : Updated ev_id=20210830103773 aircraft_key=1 col_name=landing_gear code=SKID.
Progress update 2023-01-22 10:02:11.194316 : Updated ev_id=20210830103775 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:11.218817 : Updated ev_id=20210830103775 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:11.244333 : Updated ev_id=20210830103775 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:11.268832 : Updated ev_id=20210830103775 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:11.294333 : Updated ev_id=20210830103775 aircraft_key=1 col_name=instm_appr1 code=UNK.
Progress update 2023-01-22 10:02:11.318834 : Updated ev_id=20210830103775 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:11.344334 : Updated ev_id=20210830103775 aircraft_key=1 col_name=rwy_cond0 code=UNK.
Progress update 2023-01-22 10:02:11.369336 : Updated ev_id=20210830103775 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:11.394333 : Updated ev_id=20210830103775 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:11.444332 : Updated ev_id=20210903103795 aircraft_key=1 col_name=acft_awy_cert code=SPE.
Progress update 2023-01-22 10:02:11.494108 : Updated ev_id=20210903103795 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:11.518815 : Updated ev_id=20210903103795 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:11.544331 : Updated ev_id=20210903103795 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:11.568830 : Updated ev_id=20210903103795 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:11.594350 : Updated ev_id=20210903103795 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:11.618873 : Updated ev_id=20210903103795 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:11.644315 : Updated ev_id=20210903103795 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:11.668882 : Updated ev_id=20210903103795 aircraft_key=1 col_name=type_clear code=VFR.
Progress update 2023-01-22 10:02:11.694382 : Updated ev_id=20210903103795 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:11.718882 : Updated ev_id=20210908103824 aircraft_key=1 col_name=acft_awy_cert code=STU.
Progress update 2023-01-22 10:02:11.744383 : Updated ev_id=20210908103824 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:11.768884 : Updated ev_id=20210908103824 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:11.793881 : Updated ev_id=20210908103824 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:11.818911 : Updated ev_id=20210908103824 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:11.843932 : Updated ev_id=20210908103824 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:11.869001 : Updated ev_id=20210908103824 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:11.894055 : Updated ev_id=20210908103824 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:11.952365 : Updated ev_id=20210908103824 aircraft_key=1 col_name=rwy_cond1 code=HOLE.
Progress update 2023-01-22 10:02:11.976994 : Updated ev_id=20210908103824 aircraft_key=1 col_name=rwy_cond1 code=ROUG.
Progress update 2023-01-22 10:02:12.002428 : Updated ev_id=20210908103824 aircraft_key=1 col_name=type_clear code=VFR.
Progress update 2023-01-22 10:02:12.026935 : Updated ev_id=20210908103824 aircraft_key=1 col_name=vfr_appr code=FLND.
Progress update 2023-01-22 10:02:12.401998 : Updated ev_id=20220503105038 aircraft_key=1 col_name=acft_awy_cert0 code=NON.
Progress update 2023-01-22 10:02:12.426997 : Updated ev_id=20220503105038 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:12.451997 : Updated ev_id=20220503105038 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:12.476996 : Updated ev_id=20220503105038 aircraft_key=1 col_name=instm_appr1 code=UNK.
Progress update 2023-01-22 10:02:12.501998 : Updated ev_id=20220503105038 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:12.526498 : Updated ev_id=20220503105038 aircraft_key=1 col_name=rwy_cond0 code=UNK.
Progress update 2023-01-22 10:02:12.576997 : Updated ev_id=20220503105038 aircraft_key=1 col_name=vfr_appr1 code=UNK.
Progress update 2023-01-22 10:02:12.601998 : Updated ev_id=20220525105130 aircraft_key=1 col_name=acft_awy_cert code=SPX.
Progress update 2023-01-22 10:02:12.626816 : Updated ev_id=20220525105130 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:12.652046 : Updated ev_id=20220525105130 aircraft_key=1 col_name=addtl_equip code=AOAI.
Progress update 2023-01-22 10:02:12.676764 : Updated ev_id=20220525105130 aircraft_key=1 col_name=addtl_equip code=EFB.
Progress update 2023-01-22 10:02:12.701747 : Updated ev_id=20220525105130 aircraft_key=1 col_name=addtl_equip code=EMFD.
Progress update 2023-01-22 10:02:12.726759 : Updated ev_id=20220525105130 aircraft_key=1 col_name=addtl_equip code=EPFD.
Progress update 2023-01-22 10:02:12.751758 : Updated ev_id=20220525105130 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:12.776759 : Updated ev_id=20220525105130 aircraft_key=1 col_name=airspc_type code=CLE.
Progress update 2023-01-22 10:02:12.802259 : Updated ev_id=20220525105130 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:12.826759 : Updated ev_id=20220525105130 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:12.852259 : Updated ev_id=20220525105130 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:12.877758 : Updated ev_id=20220525105130 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:12.901758 : Updated ev_id=20220525105130 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:13.010240 : Updated ev_id=20220525105130 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:13.060395 : Updated ev_id=20220607105206 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:13.493018 : Updated ev_id=20220731105625 aircraft_key=1 col_name=aircar_cert code=F129.
Progress update 2023-01-22 10:02:13.518551 : Updated ev_id=20220731105625 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:13.542943 : Updated ev_id=20220731105625 aircraft_key=1 col_name=rwy_cond1 code=WET.
Progress update 2023-01-22 10:02:13.568366 : Updated ev_id=20220912105911 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:13.593115 : Updated ev_id=20220912105911 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:13.618496 : Updated ev_id=20220912105911 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:13.643033 : Updated ev_id=20220912105911 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:13.668187 : Updated ev_id=20220912105911 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:13.693128 : Updated ev_id=20220912105911 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:13.718257 : Updated ev_id=20220912105911 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:13.842984 : Updated ev_id=20220928106011 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:14.093329 : Updated ev_id=20221003106045 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:14.168374 : Updated ev_id=20221003106045 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:14.392834 : Updated ev_id=20221006106075 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:14.492813 : Updated ev_id=20221006106075 aircraft_key=1 col_name=landing_gear1 code=TAIL.
Progress update 2023-01-22 10:02:14.767994 : Updated ev_id=20221012106114 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:14.793051 : Updated ev_id=20221012106114 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:14.817815 : Updated ev_id=20221012106114 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:14.893094 : Updated ev_id=20221012106114 aircraft_key=1 col_name=vfr_appr code=FSTP.
Progress update 2023-01-22 10:02:14.917832 : Updated ev_id=20221012106114 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:15.393353 : Updated ev_id=20221024106184 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:15.417854 : Updated ev_id=20221024106184 aircraft_key=1 col_name=acft_awy_cert code=STU.
Progress update 2023-01-22 10:02:15.467720 : Updated ev_id=20221024106184 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:15.517812 : Updated ev_id=20221024106184 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:15.543312 : Updated ev_id=20221024106184 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:15.564327 : Updated ev_id=20221024106184 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:15.592491 : Updated ev_id=20221024106184 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:15.642534 : Updated ev_id=20221024106184 aircraft_key=1 col_name=vfr_appr code=FSTP.
Progress update 2023-01-22 10:02:15.667834 : Updated ev_id=20221024106184 aircraft_key=1 col_name=vfr_appr code=TPAT.
Progress update 2023-01-22 10:02:15.692335 : Updated ev_id=20221026106199 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:15.892320 : Updated ev_id=20221026106199 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:15.992709 : Updated ev_id=20221026106199 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:16.025932 : Updated ev_id=20221026106199 aircraft_key=1 col_name=landing_surf code=ASPH.
Progress update 2023-01-22 10:02:16.151001 : Updated ev_id=20221103106241 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:16.400599 : Updated ev_id=20221108106259 aircraft_key=1 col_name=acft_awy_cert code=LTSP.
Progress update 2023-01-22 10:02:16.426117 : Updated ev_id=20221108106259 aircraft_key=1 col_name=addtl_equip code=AFPC.
Progress update 2023-01-22 10:02:16.526116 : Updated ev_id=20221108106259 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:16.625906 : Updated ev_id=20221108106259 aircraft_key=1 col_name=landing_gear1 code=TRI.
Progress update 2023-01-22 10:02:16.675821 : Updated ev_id=20221108106259 aircraft_key=1 col_name=rwy_cond1 code=ROUG.
Progress update 2023-01-22 10:02:16.700574 : Updated ev_id=20221108106259 aircraft_key=1 col_name=rwy_cond1 code=VEGE.
Progress update 2023-01-22 10:02:17.200769 : Updated ev_id=20221128106365 aircraft_key=1 col_name=aircar_cert code=None.
Progress update 2023-01-22 10:02:17.825332 : Updated ev_id=20221215106462 aircraft_key=1 col_name=acft_awy_cert code=STN.
Progress update 2023-01-22 10:02:17.850493 : Updated ev_id=20221215106462 aircraft_key=1 col_name=addtl_equip code=ADSB.
Progress update 2023-01-22 10:02:17.875731 : Updated ev_id=20221215106462 aircraft_key=1 col_name=addtl_equip code=DREC.
Progress update 2023-01-22 10:02:17.900496 : Updated ev_id=20221215106462 aircraft_key=1 col_name=addtl_equip code=SATD.
Progress update 2023-01-22 10:02:17.925546 : Updated ev_id=20221215106462 aircraft_key=1 col_name=addtl_equip code=VRD.
Progress update 2023-01-22 10:02:17.950605 : Updated ev_id=20221215106462 aircraft_key=1 col_name=aircar_cert code=TAXI.
Progress update 2023-01-22 10:02:17.975318 : Updated ev_id=20221215106462 aircraft_key=1 col_name=airspc_type code=CLG.
Progress update 2023-01-22 10:02:18.000515 : Updated ev_id=20221215106462 aircraft_key=1 col_name=elt_oper_no_reason code=UNK.
Progress update 2023-01-22 10:02:18.025517 : Updated ev_id=20221215106462 aircraft_key=1 col_name=instm_appr0 code=NONE.
Progress update 2023-01-22 10:02:18.050515 : Updated ev_id=20221215106462 aircraft_key=1 col_name=rwy_cond1 code=DRY.
Progress update 2023-01-22 10:02:18.075534 : Updated ev_id=20221215106462 aircraft_key=1 col_name=type_clear0 code=NONE.
Progress update 2023-01-22 10:02:18.100495 : Updated ev_id=20221215106462 aircraft_key=1 col_name=vfr_appr0 code=NONE.
Progress update 2023-01-22 10:02:18.175193 : Updated ev_id=20221219106471 aircraft_key=1 col_name=addtl_equip0 code=UNK.
Progress update 2023-01-22 10:02:21.016492 : Number rows selected :    815.
Progress update 2023-01-22 10:02:21.016492 : Number rows inserted :    358.
Progress update 2023-01-22 10:02:21.016492 : Number rows updated  :    457.
Progress update 2023-01-22 10:02:21.017082 :
Progress update 2023-01-22 10:02:21.017082 : Database table       : engines             <-----------------------------------.
Progress update 2023-01-22 10:02:21.066365 : Updated ev_id=20200820X85853 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.091453 : Updated ev_id=20200820X85853 aircraft_key=1 eng_no=2.
Progress update 2023-01-22 10:02:21.141246 : Updated ev_id=20201019102162 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.166280 : Updated ev_id=20201112102277 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.232804 : Updated ev_id=20201123102332 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.249643 : Updated ev_id=20210205102605 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.266154 : Updated ev_id=20210209102615 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.283155 : Updated ev_id=20210216102634 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.299655 : Updated ev_id=20210218102641 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.316521 : Updated ev_id=20210224102672 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.333022 : Updated ev_id=20210304102704 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.349520 : Updated ev_id=20210304102711 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.366020 : Updated ev_id=20210305102714 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.383021 : Updated ev_id=20210418102927 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.399538 : Updated ev_id=20210429102997 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.416555 : Updated ev_id=20210502103009 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.432620 : Updated ev_id=20210513103077 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.491899 : Updated ev_id=20210529103166 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.515919 : Updated ev_id=20210617103285 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.540417 : Updated ev_id=20210702103405 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.557917 : Updated ev_id=20210705103412 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.574417 : Updated ev_id=20210714103480 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.590917 : Updated ev_id=20210718103499 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.607915 : Updated ev_id=20210727103558 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.624417 : Updated ev_id=20210805103634 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.641417 : Updated ev_id=20210809103657 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.674416 : Updated ev_id=20210816103700 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.690916 : Updated ev_id=20210830103772 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.707918 : Updated ev_id=20210830103773 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.741417 : Updated ev_id=20210903103795 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.757917 : Updated ev_id=20210908103824 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.791417 : Updated ev_id=20220912105911 aircraft_key=1 eng_no=1.
Progress update 2023-01-22 10:02:21.907853 : Number rows selected :     44.
Progress update 2023-01-22 10:02:21.907853 : Number rows inserted :     12.
Progress update 2023-01-22 10:02:21.908353 : Number rows updated  :     32.
Progress update 2023-01-22 10:02:21.908353 :
Progress update 2023-01-22 10:02:21.908353 : Database table       : events_sequence     <-----------------------------------.
Progress update 2023-01-22 10:02:21.932695 : Updated ev_id=20191219X91426 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:21.991335 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.007815 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:22.024341 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.041195 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.057833 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:22.074238 : Updated ev_id=20200820X85853 Aircraft_Key=1 Occurrence_No=6.
Progress update 2023-01-22 10:02:22.124331 : Updated ev_id=20201019102162 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.140856 : Updated ev_id=20201019102162 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.158088 : Updated ev_id=20201112102277 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.174101 : Updated ev_id=20201112102277 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.191238 : Updated ev_id=20201112102277 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:22.207738 : Updated ev_id=20201123102332 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.224238 : Updated ev_id=20201123102332 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.240491 : Updated ev_id=20201123102332 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.257832 : Updated ev_id=20210205102605 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.273879 : Updated ev_id=20210209102615 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.291107 : Updated ev_id=20210216102634 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:22.307610 : Updated ev_id=20210216102634 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.324056 : Updated ev_id=20210218102641 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:22.340873 : Updated ev_id=20210218102641 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:22.357553 : Updated ev_id=20210219102646 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.373783 : Updated ev_id=20210224102672 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.390804 : Updated ev_id=20210304102704 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.407304 : Updated ev_id=20210304102704 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.424304 : Updated ev_id=20210304102711 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.440472 : Updated ev_id=20210305102714 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.474006 : Updated ev_id=20210418102927 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:22.490994 : Updated ev_id=20210418102927 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.507535 : Updated ev_id=20210418102927 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.524090 : Updated ev_id=20210418102927 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:22.607489 : Updated ev_id=20210429102997 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.624333 : Updated ev_id=20210429102997 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.640834 : Updated ev_id=20210429102997 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.657332 : Updated ev_id=20210502103009 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.673832 : Updated ev_id=20210502103009 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.690835 : Updated ev_id=20210513103077 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.707334 : Updated ev_id=20210527103152 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.724117 : Updated ev_id=20210529103166 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.740643 : Updated ev_id=20210529103166 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.757311 : Updated ev_id=20210617103285 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.774006 : Updated ev_id=20210617103285 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.791006 : Updated ev_id=20210630103379 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.891005 : Updated ev_id=20210702103405 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:22.907504 : Updated ev_id=20210702103405 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:22.924005 : Updated ev_id=20210702103405 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:22.974056 : Updated ev_id=20210705103412 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:22.990364 : Updated ev_id=20210705103412 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.007450 : Updated ev_id=20210714103480 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.023961 : Updated ev_id=20210714103480 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:23.040633 : Updated ev_id=20210714103480 Aircraft_Key=1 Occurrence_No=4.
Progress update 2023-01-22 10:02:23.057248 : Updated ev_id=20210714103480 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.074257 : Updated ev_id=20210714103480 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:23.090770 : Updated ev_id=20210718103499 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:23.107285 : Updated ev_id=20210718103499 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.123797 : Updated ev_id=20210727103558 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.140814 : Updated ev_id=20210805103634 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.157314 : Updated ev_id=20210805103634 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.174043 : Updated ev_id=20210809103657 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.190812 : Updated ev_id=20210809103657 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.223863 : Updated ev_id=20210816103700 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.240781 : Updated ev_id=20210830103772 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.257388 : Updated ev_id=20210830103773 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.274097 : Updated ev_id=20210830103773 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.290489 : Updated ev_id=20210830103775 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.323899 : Updated ev_id=20210830103775 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.374583 : Updated ev_id=20210903103795 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:23.391082 : Updated ev_id=20210903103795 Aircraft_Key=1 Occurrence_No=2.
Progress update 2023-01-22 10:02:23.407583 : Updated ev_id=20210908103824 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.424122 : Updated ev_id=20211006104055 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.507408 : Updated ev_id=20220503105038 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.524075 : Updated ev_id=20220525105130 Aircraft_Key=1 Occurrence_No=3.
Progress update 2023-01-22 10:02:23.557075 : Updated ev_id=20220607105206 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.590490 : Updated ev_id=20220731105625 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.623845 : Updated ev_id=20220912105911 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.640846 : Updated ev_id=20220913105930 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.656911 : Updated ev_id=20220928106011 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.673928 : Updated ev_id=20221003106045 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.723930 : Updated ev_id=20221006106075 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.790504 : Updated ev_id=20221012106114 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.840789 : Updated ev_id=20221013106123 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.890330 : Updated ev_id=20221024106184 Aircraft_Key=1 Occurrence_No=5.
Progress update 2023-01-22 10:02:23.907332 : Updated ev_id=20221026106199 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.940830 : Updated ev_id=20221103106241 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:23.957329 : Updated ev_id=20221108106259 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.073829 : Updated ev_id=20221208106433 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.090329 : Updated ev_id=20221212106439 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.107327 : Updated ev_id=20221213106450 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.140843 : Updated ev_id=20221215106462 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.156861 : Updated ev_id=20221219106471 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.207333 : Updated ev_id=20221222106484 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.223775 : Updated ev_id=20221222106485 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.240308 : Updated ev_id=20221228106502 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.257312 : Updated ev_id=20221229106509 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.365332 : Updated ev_id=20230104106534 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.398657 : Updated ev_id=20230106106544 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.531921 : Updated ev_id=20230114106576 Aircraft_Key=1 Occurrence_No=1.
Progress update 2023-01-22 10:02:24.815501 : Number rows selected :    166.
Progress update 2023-01-22 10:02:24.815501 : Number rows inserted :     69.
Progress update 2023-01-22 10:02:24.815501 : Number rows updated  :     97.
Progress update 2023-01-22 10:02:24.815501 :
Progress update 2023-01-22 10:02:24.815501 : Database table       : findings            <-----------------------------------.
Progress update 2023-01-22 10:02:25.140064 : Updated ev_id=20210205102605 aircraft_key=1 finding_no=1.
Progress update 2023-01-22 10:02:26.572830 : Number rows selected :    100.
Progress update 2023-01-22 10:02:26.573331 : Number rows inserted :     99.
Progress update 2023-01-22 10:02:26.573331 : Number rows updated  :      1.
Progress update 2023-01-22 10:02:26.573331 :
Progress update 2023-01-22 10:02:26.573331 : Database table       : flight_crew         <-----------------------------------.
Progress update 2023-01-22 10:02:26.614759 : Updated ev_id=20200820X85853 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.647989 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.665004 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.681320 : Updated ev_id=20201123102332 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.697873 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.714421 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.731432 : Updated ev_id=20210216102634 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.747885 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.764885 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:26.781387 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.797885 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.814416 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:26.831433 : Updated ev_id=20210304102711 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.847696 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.864723 : Updated ev_id=20210418102927 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.881226 : Updated ev_id=20210418102927 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:26.926989 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.939566 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:26.956169 : Updated ev_id=20210502103009 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.972829 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:26.989829 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:27.006156 : Updated ev_id=20210529103166 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.023198 : Updated ev_id=20210617103285 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.056254 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.072767 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:27.089807 : Updated ev_id=20210705103412 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.106309 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.122808 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.139308 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.156308 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.172808 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.189808 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:27.222809 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.239320 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.256084 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:27.272660 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.306161 : Updated ev_id=20210903103795 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.323161 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.356662 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1.
Progress update 2023-01-22 10:02:27.372660 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=2.
Progress update 2023-01-22 10:02:27.556342 : Number rows selected :     57.
Progress update 2023-01-22 10:02:27.556342 : Number rows inserted :     17.
Progress update 2023-01-22 10:02:27.556342 : Number rows updated  :     40.
Progress update 2023-01-22 10:02:27.556342 :
Progress update 2023-01-22 10:02:27.556841 : Database table       : injury              <-----------------------------------.
Progress update 2023-01-22 10:02:29.363559 : Updated ev_id=20191219X91426 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.389199 : Updated ev_id=20191219X91426 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.413673 : Updated ev_id=20191219X91426 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:29.439333 : Updated ev_id=20191219X91426 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:29.463833 : Updated ev_id=20200807X30140 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.488927 : Updated ev_id=20200807X30140 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.513673 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.539174 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:29.564173 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:29.589173 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:29.613673 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.655493 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:29.680309 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:29.705809 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:29.730335 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:29.755559 : Updated ev_id=20200820X85853 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:29.780230 : Updated ev_id=20201004102078 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.805697 : Updated ev_id=20201004102078 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.830254 : Updated ev_id=20201019102162 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:29.855523 : Updated ev_id=20201019102162 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.880549 : Updated ev_id=20201112102277 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.905632 : Updated ev_id=20201112102277 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:29.947525 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:29.972191 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:29.997126 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:30.021966 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:30.047493 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.072129 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:30.097153 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:30.122263 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:30.147092 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:30.172181 : Updated ev_id=20201123102332 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:30.197488 : Updated ev_id=20210205102605 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:30.221988 : Updated ev_id=20210205102605 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.247488 : Updated ev_id=20210205102605 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:30.271988 : Updated ev_id=20210205102605 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:30.296988 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:30.321868 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:30.347200 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:30.371808 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:30.397324 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.421869 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:30.446963 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:30.472151 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:30.497330 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:30.521830 : Updated ev_id=20210209102615 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:30.547307 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:30.571787 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:30.596990 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:30.622026 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:30.647525 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.672026 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:30.697528 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:30.722025 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:30.747026 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:30.772026 : Updated ev_id=20210216102634 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:30.797024 : Updated ev_id=20210218102641 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:30.821808 : Updated ev_id=20210218102641 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.847330 : Updated ev_id=20210218102641 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:30.872021 : Updated ev_id=20210218102641 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:30.897311 : Updated ev_id=20210219102646 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:30.938328 : Updated ev_id=20210219102646 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:30.963829 : Updated ev_id=20210219102646 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:30.996612 : Updated ev_id=20210219102646 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.022326 : Updated ev_id=20210224102672 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.046644 : Updated ev_id=20210224102672 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.063671 : Updated ev_id=20210224102672 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:31.088655 : Updated ev_id=20210224102672 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.113654 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:31.138655 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:31.163681 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.188410 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:31.213759 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:31.238545 : Updated ev_id=20210304102704 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.255545 : Updated ev_id=20210304102711 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:31.280045 : Updated ev_id=20210304102711 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.305545 : Updated ev_id=20210305102714 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.330044 : Updated ev_id=20210305102714 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.355545 : Updated ev_id=20210305102714 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:31.380545 : Updated ev_id=20210305102714 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.480330 : Updated ev_id=20210418102927 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:31.504830 : Updated ev_id=20210418102927 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.521830 : Updated ev_id=20210418102927 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:31.546819 : Updated ev_id=20210418102927 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.605346 : Updated ev_id=20210429102997 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:31.630230 : Updated ev_id=20210429102997 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:31.646746 : Updated ev_id=20210429102997 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.671749 : Updated ev_id=20210502103009 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:31.688749 : Updated ev_id=20210502103009 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.713277 : Updated ev_id=20210513103077 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:31.738778 : Updated ev_id=20210513103077 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.763276 : Updated ev_id=20210513103077 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.788777 : Updated ev_id=20210527103152 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.813276 : Updated ev_id=20210527103152 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.838777 : Updated ev_id=20210529103166 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:31.863276 : Updated ev_id=20210529103166 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.888794 : Updated ev_id=20210617103285 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.904806 : Updated ev_id=20210617103285 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.921746 : Updated ev_id=20210617103285 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:31.938043 : Updated ev_id=20210617103285 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:31.954787 : Updated ev_id=20210630103379 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:31.971286 : Updated ev_id=20210630103379 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:31.988328 : Updated ev_id=20210702103405 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.004851 : Updated ev_id=20210702103405 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.021365 : Updated ev_id=20210702103405 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:32.037988 : Updated ev_id=20210702103405 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:32.088476 : Updated ev_id=20210705103412 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:32.104609 : Updated ev_id=20210705103412 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.138267 : Updated ev_id=20210714103480 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.154828 : Updated ev_id=20210714103480 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.171326 : Updated ev_id=20210718103499 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:32.188503 : Updated ev_id=20210718103499 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.204662 : Updated ev_id=20210718103499 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:32.221342 : Updated ev_id=20210718103499 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:32.237805 : Updated ev_id=20210727103558 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:32.254870 : Updated ev_id=20210727103558 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.271379 : Updated ev_id=20210727103558 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:32.287995 : Updated ev_id=20210727103558 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:32.305008 : Updated ev_id=20210805103634 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:32.322008 : Updated ev_id=20210805103634 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.380009 : Updated ev_id=20210805103634 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.488306 : Updated ev_id=20210809103657 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.529808 : Updated ev_id=20210809103657 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.546324 : Updated ev_id=20210809103657 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:32.562758 : Updated ev_id=20210809103657 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:32.579856 : Updated ev_id=20210810103667 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:32.596489 : Updated ev_id=20210810103667 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.629675 : Updated ev_id=20210816103700 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.646683 : Updated ev_id=20210816103700 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.662877 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:32.679829 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.696486 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.713385 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:32.729552 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:32.746554 : Updated ev_id=20210830103772 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:32.831415 : Updated ev_id=20210830103773 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:32.879978 : Updated ev_id=20210830103773 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:32.954978 : Updated ev_id=20210830103773 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:32.971484 : Updated ev_id=20210830103775 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:33.004807 : Updated ev_id=20210830103775 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.021097 : Updated ev_id=20210830103775 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:33.054357 : Updated ev_id=20210830103775 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:33.071299 : Updated ev_id=20210903103795 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:33.087766 : Updated ev_id=20210903103795 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.104910 : Updated ev_id=20210908103824 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:33.121410 : Updated ev_id=20210908103824 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.138411 : Updated ev_id=20211006104055 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:33.154409 : Updated ev_id=20211006104055 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.171433 : Updated ev_id=20211006104055 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:33.187935 : Updated ev_id=20211006104055 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:33.571379 : Updated ev_id=20220503105038 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:33.587882 : Updated ev_id=20220503105038 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.604673 : Updated ev_id=20220525105130 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:33.621063 : Updated ev_id=20220525105130 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.854476 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:33.870975 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:33.887975 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:33.904329 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:33.921328 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:33.937404 : Updated ev_id=20220607105206 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:33.987827 : Updated ev_id=20220731105625 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:34.004327 : Updated ev_id=20220731105625 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.021327 : Updated ev_id=20220731105625 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:34.037827 : Updated ev_id=20220731105625 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:34.220806 : Updated ev_id=20220912105911 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:34.237260 : Updated ev_id=20220912105911 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.254488 : Updated ev_id=20220913105930 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:34.270998 : Updated ev_id=20220913105930 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.304327 : Updated ev_id=20220928106011 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:34.320908 : Updated ev_id=20220928106011 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.337279 : Updated ev_id=20220928106011 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:34.354289 : Updated ev_id=20220928106011 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:34.370824 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:34.387592 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:34.404258 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:34.420953 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:34.437598 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.454241 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:34.470806 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:34.487806 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:34.504306 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:34.520807 : Updated ev_id=20221003106045 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:34.537306 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:34.554307 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:34.570808 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:34.587870 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:34.603868 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.620870 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Pass injury_level=FATL.
Progress update 2023-01-22 10:02:34.637369 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Pass injury_level=SERS.
Progress update 2023-01-22 10:02:34.670869 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:34.687869 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:34.704309 : Updated ev_id=20221006106075 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:34.720836 : Updated ev_id=20221012106114 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:34.737356 : Updated ev_id=20221012106114 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:34.754501 : Updated ev_id=20221012106114 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:34.770536 : Updated ev_id=20221012106114 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:35.003805 : Updated ev_id=20221024106184 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:35.020818 : Updated ev_id=20221024106184 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.037385 : Updated ev_id=20221024106184 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:35.054486 : Updated ev_id=20221024106184 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:35.070535 : Updated ev_id=20221026106199 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:35.087535 : Updated ev_id=20221026106199 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.104034 : Updated ev_id=20221026106199 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:35.121035 : Updated ev_id=20221026106199 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:35.204047 : Updated ev_id=20221103106241 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:35.221062 : Updated ev_id=20221103106241 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.254380 : Updated ev_id=20221108106259 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:35.270545 : Updated ev_id=20221108106259 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.287398 : Updated ev_id=20221108106259 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:35.303898 : Updated ev_id=20221108106259 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:35.354386 : Updated ev_id=20221128106365 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:35.370397 : Updated ev_id=20221128106365 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.470540 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Crew injury_level=SERS.
Progress update 2023-01-22 10:02:35.487594 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:35.520730 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:35.537387 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.554692 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:35.570691 : Updated ev_id=20221212106439 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:35.770471 : Updated ev_id=20221213106450 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:35.787483 : Updated ev_id=20221213106450 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:35.995489 : Updated ev_id=20221215106462 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:36.011987 : Updated ev_id=20221215106462 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.029002 : Updated ev_id=20221215106462 aircraft_key=1 inj_person_category=Pass injury_level=MINR.
Progress update 2023-01-22 10:02:36.045029 : Updated ev_id=20221215106462 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:36.062060 : Updated ev_id=20221219106471 aircraft_key=1 inj_person_category=Crew injury_level=MINR.
Progress update 2023-01-22 10:02:36.078827 : Updated ev_id=20221219106471 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.095422 : Updated ev_id=20221222106484 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:36.112059 : Updated ev_id=20221222106484 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.128621 : Updated ev_id=20221222106484 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:36.145341 : Updated ev_id=20221222106484 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:36.162087 : Updated ev_id=20221222106485 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:36.178599 : Updated ev_id=20221222106485 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.195599 : Updated ev_id=20221222106485 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:36.212099 : Updated ev_id=20221222106485 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:36.229099 : Updated ev_id=20221228106502 aircraft_key=1 inj_person_category=Crew injury_level=FATL.
Progress update 2023-01-22 10:02:36.245599 : Updated ev_id=20221228106502 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.520322 : Updated ev_id=20230104106534 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:36.537009 : Updated ev_id=20230104106534 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.553438 : Updated ev_id=20230104106534 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:36.570305 : Updated ev_id=20230104106534 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:36.620322 : Updated ev_id=20230106106544 aircraft_key=1 inj_person_category=Crew injury_level=NONE.
Progress update 2023-01-22 10:02:36.637322 : Updated ev_id=20230106106544 aircraft_key=1 inj_person_category=Crew injury_level=TOTL.
Progress update 2023-01-22 10:02:36.653322 : Updated ev_id=20230106106544 aircraft_key=1 inj_person_category=Pass injury_level=NONE.
Progress update 2023-01-22 10:02:36.670322 : Updated ev_id=20230106106544 aircraft_key=1 inj_person_category=Pass injury_level=TOTL.
Progress update 2023-01-22 10:02:38.170116 : Number rows selected :    507.
Progress update 2023-01-22 10:02:38.170616 : Number rows inserted :    263.
Progress update 2023-01-22 10:02:38.170616 : Number rows updated  :    244.
Progress update 2023-01-22 10:02:38.170616 :
Progress update 2023-01-22 10:02:38.170616 : Database table       : narratives          <-----------------------------------.
Progress update 2023-01-22 10:02:38.270331 : Updated ev_id=20200807X30140 aircraft_key=1.
Progress update 2023-01-22 10:02:38.361333 : Updated ev_id=20200820X85853 aircraft_key=1.
Progress update 2023-01-22 10:02:38.428379 : Updated ev_id=20201004102078 aircraft_key=1.
Progress update 2023-01-22 10:02:38.536880 : Updated ev_id=20201019102162 aircraft_key=1.
Progress update 2023-01-22 10:02:38.603332 : Updated ev_id=20201112102277 aircraft_key=1.
Progress update 2023-01-22 10:02:38.678323 : Updated ev_id=20201123102332 aircraft_key=1.
Progress update 2023-01-22 10:02:38.694329 : Updated ev_id=20210205102605 aircraft_key=1.
Progress update 2023-01-22 10:02:38.711664 : Updated ev_id=20210209102615 aircraft_key=1.
Progress update 2023-01-22 10:02:38.778173 : Updated ev_id=20210216102634 aircraft_key=1.
Progress update 2023-01-22 10:02:38.794672 : Updated ev_id=20210218102641 aircraft_key=1.
Progress update 2023-01-22 10:02:38.811172 : Updated ev_id=20210224102672 aircraft_key=1.
Progress update 2023-01-22 10:02:38.827673 : Updated ev_id=20210304102704 aircraft_key=1.
Progress update 2023-01-22 10:02:38.844672 : Updated ev_id=20210304102711 aircraft_key=1.
Progress update 2023-01-22 10:02:38.861173 : Updated ev_id=20210305102714 aircraft_key=1.
Progress update 2023-01-22 10:02:38.878172 : Updated ev_id=20210418102927 aircraft_key=1.
Progress update 2023-01-22 10:02:38.894674 : Updated ev_id=20210429102997 aircraft_key=1.
Progress update 2023-01-22 10:02:38.911315 : Updated ev_id=20210502103009 aircraft_key=1.
Progress update 2023-01-22 10:02:38.977837 : Updated ev_id=20210513103077 aircraft_key=1.
Progress update 2023-01-22 10:02:39.036086 : Updated ev_id=20210529103166 aircraft_key=1.
Progress update 2023-01-22 10:02:39.052962 : Updated ev_id=20210617103285 aircraft_key=1.
Progress update 2023-01-22 10:02:39.069400 : Updated ev_id=20210630103379 aircraft_key=1.
Progress update 2023-01-22 10:02:39.086325 : Updated ev_id=20210702103405 aircraft_key=1.
Progress update 2023-01-22 10:02:39.102546 : Updated ev_id=20210705103412 aircraft_key=1.
Progress update 2023-01-22 10:02:39.119502 : Updated ev_id=20210714103480 aircraft_key=1.
Progress update 2023-01-22 10:02:39.136069 : Updated ev_id=20210718103499 aircraft_key=1.
Progress update 2023-01-22 10:02:39.178140 : Updated ev_id=20210727103558 aircraft_key=1.
Progress update 2023-01-22 10:02:39.194655 : Updated ev_id=20210805103634 aircraft_key=1.
Progress update 2023-01-22 10:02:39.211326 : Updated ev_id=20210809103657 aircraft_key=1.
Progress update 2023-01-22 10:02:39.277912 : Updated ev_id=20210810103667 aircraft_key=1.
Progress update 2023-01-22 10:02:39.294331 : Updated ev_id=20210816103700 aircraft_key=1.
Progress update 2023-01-22 10:02:39.311331 : Updated ev_id=20210830103772 aircraft_key=1.
Progress update 2023-01-22 10:02:39.327821 : Updated ev_id=20210830103773 aircraft_key=1.
Progress update 2023-01-22 10:02:39.344699 : Updated ev_id=20210830103775 aircraft_key=1.
Progress update 2023-01-22 10:02:39.360989 : Updated ev_id=20210903103795 aircraft_key=1.
Progress update 2023-01-22 10:02:39.377910 : Updated ev_id=20210908103824 aircraft_key=1.
Progress update 2023-01-22 10:02:39.411382 : Updated ev_id=20220912105911 aircraft_key=1.
Progress update 2023-01-22 10:02:39.594776 : Updated ev_id=20221215106462 aircraft_key=1.
Progress update 2023-01-22 10:02:39.627777 : Number rows selected :     49.
Progress update 2023-01-22 10:02:39.627777 : Number rows inserted :     12.
Progress update 2023-01-22 10:02:39.627777 : Number rows updated  :     37.
Progress update 2023-01-22 10:02:39.628277 :
Progress update 2023-01-22 10:02:39.628277 : Database table       : occurrences         <-----------------------------------.
Progress update 2023-01-22 10:02:39.628775 : Number rows selected :      0.
Progress update 2023-01-22 10:02:39.628775 :
Progress update 2023-01-22 10:02:39.628775 : Database table       : dt_flight_crew      <-----------------------------------.
Progress update 2023-01-22 10:02:39.727823 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:39.744477 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:39.761004 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:39.778032 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:39.794129 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:39.811129 : Updated ev_id=20200820X85853 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:39.911130 : Updated ev_id=20201019102162 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:39.927630 : Updated ev_id=20201019102162 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=NONE.
Progress update 2023-01-22 10:02:39.944629 : Updated ev_id=20201019102162 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:39.960937 : Updated ev_id=20201019102162 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:39.977777 : Updated ev_id=20201019102162 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:39.994277 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.011277 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.027777 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:40.044561 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.060871 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:40.077898 : Updated ev_id=20201112102277 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.094070 : Updated ev_id=20201123102332 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.111335 : Updated ev_id=20201123102332 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.127542 : Updated ev_id=20201123102332 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.144271 : Updated ev_id=20201123102332 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:40.160890 : Updated ev_id=20201123102332 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.177804 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:40.211327 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:40.227825 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.244324 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:40.261034 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:40.278050 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=IAIR.
Progress update 2023-01-22 10:02:40.294075 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:40.311155 : Updated ev_id=20210205102605 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.327670 : Updated ev_id=20210209102615 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.344702 : Updated ev_id=20210209102615 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.360958 : Updated ev_id=20210209102615 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.377734 : Updated ev_id=20210209102615 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:40.394264 : Updated ev_id=20210209102615 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.411174 : Updated ev_id=20210216102634 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:40.427707 : Updated ev_id=20210216102634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=NONE.
Progress update 2023-01-22 10:02:40.444727 : Updated ev_id=20210216102634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.460758 : Updated ev_id=20210216102634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=HELI.
Progress update 2023-01-22 10:02:40.477988 : Updated ev_id=20210216102634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.494329 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:40.511055 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.552497 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:40.569517 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.586005 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:40.602823 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.619348 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:40.635847 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.652365 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=CFI.
Progress update 2023-01-22 10:02:40.669370 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:40.685865 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:40.702867 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.719367 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:40.736365 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=IAIR.
Progress update 2023-01-22 10:02:40.752366 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:40.769367 : Updated ev_id=20210218102641 Aircraft_Key=1 crew_no=2 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.785867 : Updated ev_id=20210224102672 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.802865 : Updated ev_id=20210224102672 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.819366 : Updated ev_id=20210224102672 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.835961 : Updated ev_id=20210224102672 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:40.860502 : Updated ev_id=20210224102672 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.877322 : Updated ev_id=20210304102704 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.893822 : Updated ev_id=20210304102704 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:40.910822 : Updated ev_id=20210304102704 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:40.927323 : Updated ev_id=20210304102704 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:40.944325 : Updated ev_id=20210304102704 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:40.960823 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:40.977323 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:40.993822 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.010824 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.027324 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:41.044304 : Updated ev_id=20210304102711 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:41.060304 : Updated ev_id=20210305102714 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:41.077303 : Updated ev_id=20210305102714 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.093803 : Updated ev_id=20210305102714 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.110803 : Updated ev_id=20210305102714 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:41.127303 : Updated ev_id=20210305102714 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:41.144322 : Updated ev_id=20210418102927 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:41.160470 : Updated ev_id=20210418102927 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.177234 : Updated ev_id=20210418102927 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.210985 : Updated ev_id=20210418102927 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:41.227396 : Updated ev_id=20210418102927 Aircraft_Key=1 crew_no=2 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:41.243895 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:41.260700 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=RMPT.
Progress update 2023-01-22 10:02:41.277698 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.294198 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:41.310697 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:41.327197 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=SUAS.
Progress update 2023-01-22 10:02:41.344200 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:41.360700 : Updated ev_id=20210429102997 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.377626 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:41.394126 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:41.410648 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.427166 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.443823 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:41.460323 : Updated ev_id=20210502103009 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:41.477627 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:41.493645 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.510983 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.526993 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=HELI.
Progress update 2023-01-22 10:02:41.544208 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:41.560708 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:41.577708 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=NONE.
Progress update 2023-01-22 10:02:41.593804 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=HELI.
Progress update 2023-01-22 10:02:41.610680 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=IHEL.
Progress update 2023-01-22 10:02:41.627195 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instrum code=HELI.
Progress update 2023-01-22 10:02:41.643980 : Updated ev_id=20210513103077 Aircraft_Key=1 crew_no=2 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:41.660231 : Updated ev_id=20210529103166 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=CFI.
Progress update 2023-01-22 10:02:41.677507 : Updated ev_id=20210529103166 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:41.693989 : Updated ev_id=20210529103166 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:41.710506 : Updated ev_id=20210529103166 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.727349 : Updated ev_id=20210529103166 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:41.743864 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=ATP.
Progress update 2023-01-22 10:02:41.760322 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:41.777489 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:41.793989 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:41.810989 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:41.827489 : Updated ev_id=20210617103285 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=GYRO.
Progress update 2023-01-22 10:02:41.968986 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:41.985486 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.002486 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:42.018486 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.035487 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:42.051986 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:42.068986 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=CFI.
Progress update 2023-01-22 10:02:42.085466 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:42.102082 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.118575 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:42.135381 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:42.151899 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct code=IAIR.
Progress update 2023-01-22 10:02:42.168982 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:42.185356 : Updated ev_id=20210702103405 Aircraft_Key=1 crew_no=2 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:42.202063 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=ATP.
Progress update 2023-01-22 10:02:42.218485 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:42.235539 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:42.251893 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:42.269007 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.285547 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:42.302329 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.318854 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:42.335535 : Updated ev_id=20210705103412 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=SUAS.
Progress update 2023-01-22 10:02:42.352062 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=CFI.
Progress update 2023-01-22 10:02:42.385286 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:42.438286 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:42.451787 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.468812 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:42.485303 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:42.501974 : Updated ev_id=20210714103480 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:42.518475 : Updated ev_id=20210718103499 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:42.535352 : Updated ev_id=20210718103499 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:42.551867 : Updated ev_id=20210718103499 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.568734 : Updated ev_id=20210718103499 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:42.585221 : Updated ev_id=20210718103499 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:42.618720 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:42.635723 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.651721 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:42.668721 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.685221 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:42.702252 : Updated ev_id=20210727103558 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:42.718823 : Updated ev_id=20210805103634 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:42.735301 : Updated ev_id=20210805103634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.751882 : Updated ev_id=20210805103634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.768631 : Updated ev_id=20210805103634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:42.785298 : Updated ev_id=20210805103634 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=AIRS.
Progress update 2023-01-22 10:02:42.802303 : Updated ev_id=20210809103657 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:42.818736 : Updated ev_id=20210809103657 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:42.835415 : Updated ev_id=20210809103657 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:42.851804 : Updated ev_id=20210809103657 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:42.868820 : Updated ev_id=20210809103657 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=GYRO.
Progress update 2023-01-22 10:02:42.985320 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:43.002321 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:43.026820 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.043820 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.059820 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:43.076820 : Updated ev_id=20210816103700 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:43.093321 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=ATP.
Progress update 2023-01-22 10:02:43.110321 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.126822 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SES.
Progress update 2023-01-22 10:02:43.143320 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.168491 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:43.201540 : Updated ev_id=20210830103772 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:43.218761 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:43.243558 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:43.268759 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.284774 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.301823 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=HELI.
Progress update 2023-01-22 10:02:43.326551 : Updated ev_id=20210830103773 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=HELI.
Progress update 2023-01-22 10:02:43.468348 : Updated ev_id=20210903103795 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:43.485348 : Updated ev_id=20210903103795 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.501369 : Updated ev_id=20210903103795 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.518402 : Updated ev_id=20210903103795 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:43.534917 : Updated ev_id=20210903103795 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:43.551967 : Updated ev_id=20210908103824 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=PRI.
Progress update 2023-01-22 10:02:43.568484 : Updated ev_id=20210908103824 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.585142 : Updated ev_id=20210908103824 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.601772 : Updated ev_id=20210908103824 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum0 code=NONE.
Progress update 2023-01-22 10:02:43.618286 : Updated ev_id=20210908103824 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:43.726943 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=ATP.
Progress update 2023-01-22 10:02:43.743156 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_cert_code code=CFI.
Progress update 2023-01-22 10:02:43.759972 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:43.776463 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.793423 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=AME.
Progress update 2023-01-22 10:02:43.809958 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=ASE.
Progress update 2023-01-22 10:02:43.826958 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instruct code=IAIR.
Progress update 2023-01-22 10:02:43.842996 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:43.860164 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=1 col_name=crew_rat_roto code=SUAS.
Progress update 2023-01-22 10:02:43.876664 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_cert_code code=COMM.
Progress update 2023-01-22 10:02:43.893341 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=MEL.
Progress update 2023-01-22 10:02:43.910094 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_rat_airpln code=SEL.
Progress update 2023-01-22 10:02:43.926558 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instruct0 code=NONE.
Progress update 2023-01-22 10:02:43.943275 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_rat_instrum code=APLN.
Progress update 2023-01-22 10:02:43.960082 : Updated ev_id=20220912105911 Aircraft_Key=1 crew_no=2 col_name=crew_rat_roto0 code=NONE.
Progress update 2023-01-22 10:02:45.101546 : Number rows selected :    305.
Progress update 2023-01-22 10:02:45.101546 : Number rows inserted :     93.
Progress update 2023-01-22 10:02:45.101546 : Number rows updated  :    212.
Progress update 2023-01-22 10:02:45.102046 :
Progress update 2023-01-22 10:02:45.102046 : Database table       : flight_time         <-----------------------------------.
Progress update 2023-01-22 10:02:45.226044 : Updated ev_id=20200820X85853 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:45.276045 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.301546 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.326046 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:45.351499 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.376369 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:45.401483 : Updated ev_id=20201019102162 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:45.426319 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:45.451079 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.476322 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:45.501258 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.526278 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.551215 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:45.576260 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.601276 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:45.626277 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:45.651278 : Updated ev_id=20201112102277 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:45.676280 : Updated ev_id=20201123102332 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:45.701278 : Updated ev_id=20201123102332 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:45.726286 : Updated ev_id=20201123102332 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:45.751323 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:45.776259 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.801172 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.826115 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:45.851481 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.876042 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:45.901043 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:45.926045 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:45.951223 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:45.976225 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:46.001223 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:46.042758 : Updated ev_id=20210205102605 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SIMU.
Progress update 2023-01-22 10:02:46.067801 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:46.092896 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.117820 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:46.142791 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:46.167793 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.192750 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:46.217777 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:46.243275 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.267775 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:46.292775 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:46.317775 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:46.343276 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.367776 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:46.392776 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:46.417776 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:46.442754 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SIMU.
Progress update 2023-01-22 10:02:46.467509 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:46.517299 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:46.542887 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=GLDR.
Progress update 2023-01-22 10:02:46.575936 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=LTA.
Progress update 2023-01-22 10:02:46.600994 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.625867 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:46.650630 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:46.676159 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:46.700823 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:46.725710 : Updated ev_id=20210209102615 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:46.750727 : Updated ev_id=20210216102634 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:46.776294 : Updated ev_id=20210216102634 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.800874 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.825875 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.850946 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.875903 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:46.900822 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:46.925819 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:46.950820 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:46.975778 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:47.000781 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.025778 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:47.050546 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.076075 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:47.100383 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.125908 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:47.150823 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.175770 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.200516 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=SENG.
Progress update 2023-01-22 10:02:47.225566 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.250622 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:47.275655 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.300657 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.325655 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:47.363660 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=SIMU.
Progress update 2023-01-22 10:02:47.384156 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.409155 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:47.434657 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.459159 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.484156 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:47.508655 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=SIMU.
Progress update 2023-01-22 10:02:47.534323 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.558840 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:47.583880 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.608821 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=MENG.
Progress update 2023-01-22 10:02:47.634300 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.658891 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:47.684192 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=SIMU.
Progress update 2023-01-22 10:02:47.708847 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.733928 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:47.759072 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.783958 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:47.808584 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.834096 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:47.858595 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:47.883758 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:47.908950 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:47.933980 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:47.959007 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:47.983998 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:48.008519 : Updated ev_id=20210218102641 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:48.033799 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:48.058817 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.075815 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:48.100315 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:48.125821 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.150408 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=NGHT.
Progress update 2023-01-22 10:02:48.175800 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:48.200525 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:48.225540 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.250452 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=NGHT.
Progress update 2023-01-22 10:02:48.275657 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:48.300328 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:48.325512 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:48.350475 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.375500 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:48.400257 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:48.425484 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SIMU.
Progress update 2023-01-22 10:02:48.450522 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:48.475802 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:48.500482 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=GLDR.
Progress update 2023-01-22 10:02:48.525481 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.550587 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:48.591982 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:48.616982 : Updated ev_id=20210224102672 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:48.641982 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ACTU.
Progress update 2023-01-22 10:02:48.667008 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:48.691818 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=GLDR.
Progress update 2023-01-22 10:02:48.725762 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=LTA.
Progress update 2023-01-22 10:02:48.750300 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:48.775742 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=MENG.
Progress update 2023-01-22 10:02:48.800239 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=NGHT.
Progress update 2023-01-22 10:02:48.825755 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ROTO.
Progress update 2023-01-22 10:02:48.850293 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=SENG.
Progress update 2023-01-22 10:02:48.875309 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=SIMU.
Progress update 2023-01-22 10:02:48.900403 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ACTU.
Progress update 2023-01-22 10:02:48.925589 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:48.950301 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=GLDR.
Progress update 2023-01-22 10:02:48.975317 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=LTA.
Progress update 2023-01-22 10:02:49.016896 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:49.041922 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MENG.
Progress update 2023-01-22 10:02:49.066952 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=NGHT.
Progress update 2023-01-22 10:02:49.092122 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ROTO.
Progress update 2023-01-22 10:02:49.117156 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:49.141774 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SIMU.
Progress update 2023-01-22 10:02:49.167282 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ACTU.
Progress update 2023-01-22 10:02:49.191801 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:49.217299 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=GLDR.
Progress update 2023-01-22 10:02:49.242019 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=LTA.
Progress update 2023-01-22 10:02:49.267035 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:49.292077 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MENG.
Progress update 2023-01-22 10:02:49.317114 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=NGHT.
Progress update 2023-01-22 10:02:49.341625 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ROTO.
Progress update 2023-01-22 10:02:49.367220 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:49.391983 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SIMU.
Progress update 2023-01-22 10:02:49.417269 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ACTU.
Progress update 2023-01-22 10:02:49.441708 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:49.466829 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=GLDR.
Progress update 2023-01-22 10:02:49.499925 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=LTA.
Progress update 2023-01-22 10:02:49.524959 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:49.549758 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MENG.
Progress update 2023-01-22 10:02:49.575298 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=NGHT.
Progress update 2023-01-22 10:02:49.599876 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ROTO.
Progress update 2023-01-22 10:02:49.625386 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:49.650388 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SIMU.
Progress update 2023-01-22 10:02:49.675387 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:49.699887 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:49.725388 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=GLDR.
Progress update 2023-01-22 10:02:49.749887 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=LTA.
Progress update 2023-01-22 10:02:49.774820 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:49.799882 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:49.825257 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:49.849757 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ROTO.
Progress update 2023-01-22 10:02:49.875260 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:49.899758 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SIMU.
Progress update 2023-01-22 10:02:49.925302 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:49.949824 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:49.974979 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=GLDR.
Progress update 2023-01-22 10:02:50.000034 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=LTA.
Progress update 2023-01-22 10:02:50.025212 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.049710 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:50.083474 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:50.108076 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:50.133276 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:50.158263 : Updated ev_id=20210304102704 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:50.183476 : Updated ev_id=20210304102711 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.208076 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:50.233304 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.258305 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:50.283320 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:50.307989 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.333427 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:50.358261 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SIMU.
Progress update 2023-01-22 10:02:50.383275 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:50.407851 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:50.433223 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.457779 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.483481 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:50.508218 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:50.533334 : Updated ev_id=20210305102714 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:50.557873 : Updated ev_id=20210418102927 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.583412 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:50.607911 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.633097 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:50.657974 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:50.683459 : Updated ev_id=20210429102997 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.708133 : Updated ev_id=20210502103009 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.733304 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:50.758305 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.783304 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ROTO.
Progress update 2023-01-22 10:02:50.808304 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:50.833304 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.857805 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ROTO.
Progress update 2023-01-22 10:02:50.883305 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:50.907804 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:50.933203 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ROTO.
Progress update 2023-01-22 10:02:50.957761 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:50.983265 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.007771 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:51.033272 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:51.074742 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:51.099761 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.124719 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=ROTO.
Progress update 2023-01-22 10:02:51.149448 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:51.174767 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.199743 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:51.225243 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.249389 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=ROTO.
Progress update 2023-01-22 10:02:51.274890 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:51.299890 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.324892 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ROTO.
Progress update 2023-01-22 10:02:51.349390 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:51.374612 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.399627 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ROTO.
Progress update 2023-01-22 10:02:51.424640 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:51.449658 : Updated ev_id=20210513103077 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.474984 : Updated ev_id=20210529103166 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:51.499326 : Updated ev_id=20210529103166 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.524716 : Updated ev_id=20210617103285 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:51.549671 : Updated ev_id=20210617103285 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.857698 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:51.883197 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.908197 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:51.933697 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:51.957698 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:51.983198 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:52.007797 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:52.032813 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.057877 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=NGHT.
Progress update 2023-01-22 10:02:52.082875 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=INST flight_craft=SENG.
Progress update 2023-01-22 10:02:52.107968 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:52.132999 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.157556 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:52.183057 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:52.224557 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.249556 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:52.274056 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ACTU.
Progress update 2023-01-22 10:02:52.299734 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:52.324234 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.349371 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=NGHT.
Progress update 2023-01-22 10:02:52.374389 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:52.399888 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=L90D flight_craft=SIMU.
Progress update 2023-01-22 10:02:52.424625 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ACTU.
Progress update 2023-01-22 10:02:52.449627 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:52.474299 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.499342 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:52.524454 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:52.549469 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:52.574299 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=PIC flight_craft=SIMU.
Progress update 2023-01-22 10:02:52.599417 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:52.632414 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:52.657897 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.682272 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:52.707634 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:52.732594 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:52.757454 : Updated ev_id=20210702103405 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:52.782319 : Updated ev_id=20210705103412 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:52.815839 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:52.840579 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.866012 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=SENG.
Progress update 2023-01-22 10:02:52.890541 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:52.916059 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:52.940565 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:52.966077 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:52.990577 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.016077 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:53.040577 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:53.066079 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.090577 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:53.116077 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:53.140611 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.165966 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:53.190490 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:53.215989 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:53.240508 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.266022 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:53.290799 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:53.315714 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:53.340796 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:53.365813 : Updated ev_id=20210714103480 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:53.390329 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:53.415859 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.440357 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:53.465912 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:53.507483 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.532197 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:53.557609 : Updated ev_id=20210718103499 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:53.582281 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:53.607680 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.632229 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:53.657504 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:53.682124 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.707624 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:53.732125 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:53.757625 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.782123 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=NGHT.
Progress update 2023-01-22 10:02:53.807122 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:53.832389 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:53.857437 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:53.881973 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:53.907481 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:53.932044 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:53.957517 : Updated ev_id=20210727103558 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:53.982296 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:54.007296 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.032296 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:54.057296 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:54.098796 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.123799 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:54.149297 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:54.204796 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.240796 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:54.265325 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:54.290479 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.315449 : Updated ev_id=20210805103634 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:54.340857 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:54.365353 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:54.390353 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.415371 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:54.440918 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:54.465450 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:54.490440 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:54.515479 : Updated ev_id=20210809103657 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:54.540797 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:54.565297 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.590328 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:54.615401 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.640796 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:54.665325 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.690498 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:54.715512 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.748816 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:54.773827 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:54.798867 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:54.823743 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:54.848400 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=GLDR.
Progress update 2023-01-22 10:02:54.873902 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:54.898400 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:54.923901 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:54.965430 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:54.990248 : Updated ev_id=20210816103700 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:55.015295 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:55.040139 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.065672 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:55.090172 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.115671 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:55.140173 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.165673 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:55.190173 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.215817 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:55.240318 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:55.265316 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:55.290316 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:55.315317 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.340318 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:55.365314 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:55.390104 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:55.415344 : Updated ev_id=20210830103772 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:55.440315 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:55.465316 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.490065 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:55.515607 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.540316 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:55.565342 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.590297 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:55.615301 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.639879 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:55.665294 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ROTO.
Progress update 2023-01-22 10:02:55.690224 : Updated ev_id=20210830103773 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:55.923479 : Updated ev_id=20210903103795 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:55.948288 : Updated ev_id=20210903103795 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:55.965167 : Updated ev_id=20210903103795 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:56.006699 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:56.031579 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.048381 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:56.072922 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:56.090053 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.114557 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:56.131912 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:56.181412 : Updated ev_id=20210908103824 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:56.365141 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=ALL.
Progress update 2023-01-22 10:02:56.390144 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.415141 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=MENG.
Progress update 2023-01-22 10:02:56.440142 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=INST flight_craft=SENG.
Progress update 2023-01-22 10:02:56.464643 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=ALL.
Progress update 2023-01-22 10:02:56.481689 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.506262 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=MENG.
Progress update 2023-01-22 10:02:56.523275 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L24H flight_craft=SENG.
Progress update 2023-01-22 10:02:56.547817 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=ALL.
Progress update 2023-01-22 10:02:56.573263 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.597817 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=MENG.
Progress update 2023-01-22 10:02:56.615317 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L30D flight_craft=SENG.
Progress update 2023-01-22 10:02:56.639819 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=ALL.
Progress update 2023-01-22 10:02:56.664856 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.689669 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=MENG.
Progress update 2023-01-22 10:02:56.706668 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=L90D flight_craft=SENG.
Progress update 2023-01-22 10:02:56.731176 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=ALL.
Progress update 2023-01-22 10:02:56.748178 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.773067 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=MENG.
Progress update 2023-01-22 10:02:56.798075 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=PIC flight_craft=SENG.
Progress update 2023-01-22 10:02:56.823076 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ACTU.
Progress update 2023-01-22 10:02:56.840075 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:56.864730 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MAKE.
Progress update 2023-01-22 10:02:56.897928 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=MENG.
Progress update 2023-01-22 10:02:56.914427 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=NGHT.
Progress update 2023-01-22 10:02:56.947992 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SENG.
Progress update 2023-01-22 10:02:56.964992 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=1 flight_type=TOTL flight_craft=SIMU.
Progress update 2023-01-22 10:02:56.981219 : Updated ev_id=20220912105911 aircraft_key=1 crew_no=2 flight_type=TOTL flight_craft=ALL.
Progress update 2023-01-22 10:02:59.522070 : Number rows selected :    620.
Progress update 2023-01-22 10:02:59.522583 : Number rows inserted :    184.
Progress update 2023-01-22 10:02:59.522583 : Number rows updated  :    436.
Progress update 2023-01-22 10:02:59.522583 :
Progress update 2023-01-22 10:02:59.522583 : Database table       : seq_of_events       <-----------------------------------.
Progress update 2023-01-22 10:02:59.523083 : Number rows selected :      0.
Progress update 2023-01-22 10:02:59.629963 : INFO.00.065 Cleansing PostgreSQL data.
Progress update 2023-01-22 10:02:59.629963 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:02:59.693129 : INFO.00.066 Cleansing table 'aircraft' column 'acft_category'.
Progress update 2023-01-22 10:03:06.316342 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:06.316342 : INFO.00.066 Cleansing table 'aircraft' column 'dest_country'.
Progress update 2023-01-22 10:03:09.669607 : Number cols trimmed  :      1.
Progress update 2023-01-22 10:03:13.001368 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:13.001368 : INFO.00.066 Cleansing table 'aircraft' column 'dprt_country'.
Progress update 2023-01-22 10:03:16.343056 : Number cols trimmed  :      1.
Progress update 2023-01-22 10:03:19.649079 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:19.649079 : INFO.00.066 Cleansing table 'aircraft' column 'far_part'.
Progress update 2023-01-22 10:03:26.276061 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:26.276561 : INFO.00.066 Cleansing table 'aircraft' column 'oper_country'.
Progress update 2023-01-22 10:03:29.464282 : Number cols trimmed  :      1.
Progress update 2023-01-22 10:03:32.657518 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:32.657518 : INFO.00.066 Cleansing table 'aircraft' column 'owner_country'.
Progress update 2023-01-22 10:03:35.937795 : Number cols trimmed  :      1.
Progress update 2023-01-22 10:03:39.237316 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:39.237316 : INFO.00.066 Cleansing table 'aircraft' column 'regis_no'.
Progress update 2023-01-22 10:03:42.493778 : Number cols trimmed  :      1.
Progress update 2023-01-22 10:03:45.821235 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:45.821735 : INFO.00.066 Cleansing table 'events' column 'ev_city'.
Progress update 2023-01-22 10:03:48.406287 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:48.406287 : INFO.00.066 Cleansing table 'events' column 'ev_site_zipcode'.
Progress update 2023-01-22 10:03:51.047721 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:51.047721 : INFO.00.066 Cleansing table 'events' column 'latitude'.
Progress update 2023-01-22 10:03:53.637265 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:03:53.637265 : INFO.00.066 Cleansing table 'events' column 'longitude'.
Progress update 2023-01-22 10:03:56.197131 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:03:56.197131 :      142,688,050,500 ns - Total time launcher.
Progress update 2023-01-22 10:03:56.197131 : INFO.00.006 End   Launcher.
Progress update 2023-01-22 10:03:56.197631 : ===============================================================================.
```
## c_l_l - Correct decimal US latitudes and longitudes
```
Progress update 2023-01-22 10:03:57.931984 : ===============================================================================.
Progress update 2023-01-22 10:03:57.931984 : INFO.00.004 Start Launcher.
Progress update 2023-01-22 10:03:57.933983 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-22 10:03:57.943483 : INFO.00.005 Argument task='c_l_l'.
Progress update 2023-01-22 10:03:57.943483 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:03:57.943483 : INFO.00.040 Correct decimal US latitudes and longitudes.
Progress update 2023-01-22 10:03:57.943483 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:04:00.889052 : INFO.00.063 Processed data source 'events'.
Progress update 2023-01-22 10:04:00.889552 : Number cols deleted  :  60551.
Progress update 2023-01-22 10:04:00.889552 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:06:20.784199 : Number of rows so far read :   5000.
Progress update 2023-01-22 10:08:37.438229 : Number of rows so far read :  10000.
Progress update 2023-01-22 10:11:04.089564 : Number of rows so far read :  15000.
Progress update 2023-01-22 10:13:26.566972 : Number of rows so far read :  20000.
Progress update 2023-01-22 10:15:39.838560 : Number of rows so far read :  25000.
Progress update 2023-01-22 10:17:46.029407 : Number of rows so far read :  30000.
Progress update 2023-01-22 10:19:47.537743 : Number of rows so far read :  35000.
Progress update 2023-01-22 10:21:20.478792 : Number of rows so far read :  40000.
Progress update 2023-01-22 10:22:53.878103 : Number of rows so far read :  45000.
Progress update 2023-01-22 10:24:24.769435 : Number of rows so far read :  50000.
Progress update 2023-01-22 10:26:20.937758 : Number of rows so far read :  55000.
Progress update 2023-01-22 10:28:27.311410 : Number of rows so far read :  60000.
Progress update 2023-01-22 10:30:28.186464 : Number of rows so far read :  65000.
Progress update 2023-01-22 10:32:34.693674 : Number of rows so far read :  70000.
Progress update 2023-01-22 10:34:38.526151 : Number of rows so far read :  75000.
Progress update 2023-01-22 10:36:43.009250 : Number of rows so far read :  80000.
Progress update 2023-01-22 10:38:46.891724 : Number of rows so far read :  85000.
Progress update 2023-01-22 10:40:59.155397 : Number of rows so far read :  90000.
Progress update 2023-01-22 10:43:18.201237 : Number of rows so far read :  95000.
Progress update 2023-01-22 10:45:38.603694 : Number of rows so far read : 100000.
Progress update 2023-01-22 10:47:43.327633 : Number of rows so far read : 105000.
Progress update 2023-01-22 10:49:54.008729 : Number of rows so far read : 110000.
Progress update 2023-01-22 10:51:29.782688 : Number of rows so far read : 115000.
Progress update 2023-01-22 10:53:02.740095 : Number of rows so far read : 120000.
Progress update 2023-01-22 10:54:35.031758 : Number of rows so far read : 125000.
Progress update 2023-01-22 10:56:08.364468 : Number of rows so far read : 130000.
Progress update 2023-01-22 10:57:44.712786 : Number of rows so far read : 135000.
Progress update 2023-01-22 10:57:45.899638 : Number rows selected : 135039.
Progress update 2023-01-22 10:57:45.899638 : Number rows updated  : 135039.
Progress update 2023-01-22 10:57:45.899638 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:57:45.900139 :    3,228,090,156,600 ns - Total time launcher.
Progress update 2023-01-22 10:57:45.900139 : INFO.00.006 End   Launcher.
Progress update 2023-01-22 10:57:45.900139 : ===============================================================================.
```
## v_n_d - Verify selected NTSB data
```
Progress update 2023-01-22 10:57:47.735688 : ===============================================================================.
Progress update 2023-01-22 10:57:47.735688 : INFO.00.004 Start Launcher.
Progress update 2023-01-22 10:57:47.737688 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-22 10:57:47.746188 : INFO.00.005 Argument task='v_n_d'.
Progress update 2023-01-22 10:57:47.746188 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 10:57:47.746188 : INFO.00.043 Verify selected NTSB data.
Progress update 2023-01-22 10:57:47.746188 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:57:48.562600 : INFO.00.063 Processed data source 'events'.
Progress update 2023-01-22 10:57:48.562600 : Number cols deleted  :  27428.
Progress update 2023-01-22 10:57:48.562600 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:57:48.620239 : INFO.00.064 Verification of table 'events' column(s) 'latitude & longitude'.
Progress update 2023-01-22 10:57:48.620239 : --------------------------------------------------------------------------------
Progress update 2023-01-22 10:57:49.907368 : Number of rows so far read :   5000.
Progress update 2023-01-22 10:57:55.026940 : Number of rows so far read :  10000.
Progress update 2023-01-22 10:58:42.014136 : Number of rows so far read :  15000.
Progress update 2023-01-22 10:59:54.852353 : Number of rows so far read :  20000.
Progress update 2023-01-22 11:01:01.950446 : Number of rows so far read :  25000.
Progress update 2023-01-22 11:02:05.924822 : Number of rows so far read :  30000.
Progress update 2023-01-22 11:03:06.397024 : Number rows errors   :  12439.
Progress update 2023-01-22 11:03:06.397526 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:06.397526 : INFO.00.064 Verification of table 'events' column(s) 'ev_city'.
Progress update 2023-01-22 11:03:07.600107 : Number rows errors   :   6043.
Progress update 2023-01-22 11:03:07.600107 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:07.600107 : INFO.00.064 Verification of table 'events' column(s) 'ev_city & ev_site_zipcode'.
Progress update 2023-01-22 11:03:08.899669 : Number rows errors   :  16533.
Progress update 2023-01-22 11:03:08.899669 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:08.899669 : INFO.00.064 Verification of table 'events' column(s) 'ev_state'.
Progress update 2023-01-22 11:03:09.574500 : Number rows errors   :    290.
Progress update 2023-01-22 11:03:09.574500 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:09.575005 : INFO.00.064 Verification of table 'events' column(s) 'ev_site_zipcode'.
Progress update 2023-01-22 11:03:09.998973 : Number rows errors   :   6040.
Progress update 2023-01-22 11:03:09.999472 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:10.000473 : Number rows selected :  34454.
Progress update 2023-01-22 11:03:10.000974 : Number rows updated  :  41345.
Progress update 2023-01-22 11:03:10.000974 : Number rows errors   :  41345.
Progress update 2023-01-22 11:03:10.000974 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 11:03:10.000974 :      322,390,785,900 ns - Total time launcher.
Progress update 2023-01-22 11:03:10.000974 : INFO.00.006 End   Launcher.
Progress update 2023-01-22 11:03:10.000974 : ===============================================================================.
```
## r_d_s - Refresh the PostgreSQL database schema
```
Progress update 2023-01-22 11:03:11.724973 : ===============================================================================.
Progress update 2023-01-22 11:03:11.724973 : INFO.00.004 Start Launcher.
Progress update 2023-01-22 11:03:11.726972 : INFO.00.001 The logger is configured and ready.
Progress update 2023-01-22 11:03:11.735473 : INFO.00.005 Argument task='r_d_s'.
Progress update 2023-01-22 11:03:11.735473 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 11:03:11.735473 : INFO.00.071 Refreshing the database schema.
Progress update 2023-01-22 11:03:11.735473 : --------------------------------------------------------------------------------
Progress update 2023-01-22 11:03:50.245845 : INFO.00.069 Materialized database view is refreshed: io_app_ae1982.
Progress update 2023-01-22 11:03:50.245845 : -------------------------------------------------------------------------------.
Progress update 2023-01-22 11:03:50.246348 :       38,646,372,200 ns - Total time launcher.
Progress update 2023-01-22 11:03:50.246348 : INFO.00.006 End   Launcher.
Progress update 2023-01-22 11:03:50.246348 : ===============================================================================.

-----------------------------------------------------------------------
The current time is: 11:03:50.37
Enter the new time:
-----------------------------------------------------------------------
End   run_io_avstats
=======================================================================
```
