@echo off
rem This batch file is used to launch the CYPSA tools and store their PIDs
   
set cmd=%1
set dir=%~dp0
set pidfile=%2
set pid=notfound
:Start
for /F "usebackq tokens=1,2 delims=;=%tab% " %%i in (
    `wmic process call create %cmd%^, "%dir%"`
) do  call :Foo %%i %%j
goto End
   
    rem if /I %%i EQU "	ProcessId " (
    rem    echo PID=%pid%
    rem    set pid=%%j
   rem )
rem )
:Foo
    set z=%1
    set y=%2
    set y=%y:-=%
    rem echo "2 == %y%"
    rem echo."%z%"
    set z=%z: =%
    rem echo after: "%z%"
    if "%z%"=="ProcessId" (
        set pid=%y%
    )
    goto :eof
:End
if pid==notfound goto :Start
echo PID=%pid%
echo %pid% >> %pidfile%