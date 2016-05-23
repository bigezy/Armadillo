@echo off
set pidfile=PIDs.txt
for /F %%i in (%pidfile%) do taskkill /F /PID %%i
del %pidfile%