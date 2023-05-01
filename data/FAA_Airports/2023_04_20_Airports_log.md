# Log file 2023-04-20

```
Script run_io_avstats is now running
=======================================================================
Start run_io_avstats
-----------------------------------------------------------------------
IO-AVSTATS - Aviation Event Statistics.
-----------------------------------------------------------------------
PYTHONPATH   :
-----------------------------------------------------------------------
TASK         : l_a_p
APPLICATION  :
COMPOSE_TASK :
MSACCESS     :
MSEXCEL      :
-----------------------------------------------------------------------
The current time is:  9:24:14.14
Enter the new time:
=======================================================================
Progress update 2023-05-01 09:24:16.806641 : ===============================================================================.
Progress update 2023-05-01 09:24:16.807141 : INFO.00.004 Start Launcher.
Progress update 2023-05-01 09:24:16.809141 : INFO.00.001 The logger is configured and ready.
Progress update 2023-05-01 09:24:16.819140 : INFO.00.005 Argument task='l_a_p'.
Progress update 2023-05-01 09:24:16.819140 : -------------------------------------------------------------------------------.
Progress update 2023-05-01 09:24:16.819140 : INFO.00.085 Load airports.
Progress update 2023-05-01 09:24:16.819140 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:16.819641 : INFO.00.081 User connect request host=localhost port=5432 dbname=io_avstats_db user=io_aero.
Progress update 2023-05-01 09:24:16.894542 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:16.894542 : INFO.00.089 Database table io_airports: Load data from file 'D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\FAA_Airports\NPIAS-2023-2027-Appendix-A.xlsx'.
C:\Users\walte\.virtualenvs\io-avstats-zafInMY1\lib\site-packages\openpyxl\worksheet\header_footer.py:48: UserWarning: Cannot parse header or footer so it will be ignored
  warn("""Cannot parse header or footer so it will be ignored""")
Progress update 2023-05-01 09:24:17.167020 : Number rows selected :     3288.
Progress update 2023-05-01 09:24:17.167020 : Number rows usable   :     3267.
Progress update 2023-05-01 09:24:17.167020 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:17.167020 : INFO.00.089 Database table io_airports: Load data from file 'D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\FAA_Airports\Airports.xlsx'.
Progress update 2023-05-01 09:24:22.483538 : Number rows selected :    20127.
Progress update 2023-05-01 09:24:22.484039 : Number rows upserted :     3266.
Progress update 2023-05-01 09:24:22.487539 : INFO.00.081 User connect request host=localhost port=5432 dbname=io_avstats_db user=io_aero.
Progress update 2023-05-01 09:24:22.576059 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:22.576059 : INFO.00.088 Database table io_airports: Load the global identifications.
Progress update 2023-05-01 09:24:22.589074 : Number rows selected :     3266.
Progress update 2023-05-01 09:24:22.589574 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:22.589574 : INFO.00.089 Database table io_airports: Load data from file 'D:\SoftDevelopment\Projects\IO-Aero\io-avstats\data\FAA_Airports\Runways.xlsx'.
Progress update 2023-05-01 09:24:24.330141 : Number rows selected :     5192.
Progress update 2023-05-01 09:24:24.330642 : --------------------------------------------------------------------------------
Progress update 2023-05-01 09:24:24.330642 : INFO.00.090 Database table io_airports: Update the runway data.
Progress update 2023-05-01 09:24:25.891522 : Number rows selected :     3266.
Progress update 2023-05-01 09:24:25.891522 : Number rows updated  :     3266.
Progress update 2023-05-01 09:24:25.894183 : -------------------------------------------------------------------------------.
Progress update 2023-05-01 09:24:25.894683 :        9,088,042,400 ns - Total time launcher.
Progress update 2023-05-01 09:24:25.894683 : INFO.00.006 End   Launcher.
Progress update 2023-05-01 09:24:25.894683 : ===============================================================================.

-----------------------------------------------------------------------
The current time is:  9:24:26.01
Enter the new time:
-----------------------------------------------------------------------
End   run_io_avstats
=======================================================================
```
