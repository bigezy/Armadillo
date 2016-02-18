@ECHO off
CLS


REM ECHO "START CYPSA Tool"
REM -- @TODO Check that project name is passed as argument and exists	
IF "%1" == "" (
	ECHO "<USAGE> %0 [project_name] [entry node IP]"
    EXIT /B
)
IF "%2" == "" (
	ECHO "<USAGE> %0 [project_name] [entry node IP]"
    EXIT /B
)
REM SET PROJECT_PATH=%cd%\..
SET PROJECT_PATH=C:\armadillo\Demo\8bus

SET PROJECT_NAME=%1
REM for 8bus, use 10.31.1.201
SET ENTRY_NODE=%2
REM <---------------------------
REM --  Cyber-Physical PowerWorld Tasks
REM ----------------------------
REM -- Requirements:
REM -- Folder bin\PW containing files: CPPW.exe
REM Start Trainer and autoconnect to SOCCA server 
REM
REM start /d "path" file.exe

SET PROJECT_FOLDER= %PROJECT_PATH%\projects\%project_name%

SET NPV_GRAPH_ARGS=-d -c %PROJECT_FOLDER%\npv\connectivity.csv -s -t %PROJECT_FOLDER%\npv\topology-dict.json -a %PROJECT_FOLDER%\\critical-assets.txt -i %PROJECT_FOLDER%\\npv\\compromised.csv -p %PROJECT_FOLDER%\\npv\\patched.csv -n %PROJECT_FOLDER% -e %ENTRY_NODE%

REM SET PW_PATH=PW\CPPW.exe
SET PW_PATH=C:\armadillo\Demo\8bus\bin\PW\CPPW.exe
REM SET SOCCA_PATH=CyPsaEngine\CYPSA_Engine.exe
SET SOCCA_PATH=C:\armadillo\Demo\8bus\bin\CyPsaEngine\CYPSA_Engine.exe
REM SET NPV_GRAPH_FILE=NPVGraph\np_vgraph.exe
SET NPV_GRAPH_FILE=C:\armadillo\Demo\8bus\bin\NPVGraph\np_vgraph.exe
REM SET AUTOCONNECT_FILE=PW\AutoConnect.aux
SET AUTOCONNECT_FILE=C:\armadillo\Demo\8bus\bin\PW\AutoConnect.aux

SET PW_ANALYSIS_CURRENT=%PROJECT_FOLDER%\pw_analysis_attack_graph_current.xml
SET PW_ANALYSIS_PREVIOUS=%PROJECT_FOLDER%\pw_analysis_attack_graph_previous.xml
SET COMPROMISED_FILE==%PROJECT_FOLDER%\npv\compromised.csv
SET PATCHED_FILE==%PROJECT_FOLDER%\npv\patched.csv

REM ECHO %PROJECT_FOLDER% here11
REM ECHO %PW_ANALYSIS_CURRENT% here1100

REM IF NOT EXIST PW_PATH (
REM 	ECHO ERROR: Could not locate folder PW. Please add the CP-PW-Trainer executable to bin\PW
REM  	EXIT /B
REM )

IF NOT EXIST %AUTOCONNECT_FILE% (
	ECHO ERROR: Could not locate the autoconnect aux file file %AUTOCONNECT_FILE% needed by CPPW
	EXIT /B
)

IF NOT EXIST %NPV_GRAPH_FILE% (
	ECHO ERROR: Could not locate the npvgraph script file %NPV_GRAPH_FILE% needed
	EXIT /B
)
REM echo here 1
REM ---------------------------->
REM
REM Start NPV analysis and generate attack graph
REM
REM kate 8/27/15 commented out the following for now since this has already been run offline (I think)
REM START /B /WAIT runNPVTools.bat %PROJECT_NAME%

REM ---------------------------->
REM 
REM Delete previous pw_analysis_attack_graph files

REM del %PW_ANALYSIS_CURRENT%

REM del %PW_ANALYSIS_PREVIOUS%

REM Create empty comrpmmoised/patched files:
del %COMPROMISED_FILE%
del %PATCHED_FILE%

ECHO. 2>%COMPROMISED_FILE% 
ECHO. 2>%PATCHED_FILE%  
REM ---------------------------->
REM
REM Start NPV Graph python script
ECHO "Start NPV Graph python script"

REM python start
REM START python %NPV_GRAPH_FILE% %NPV_GRAPH_ARGS%
REM exe script
START %NPV_GRAPH_FILE% %NPV_GRAPH_ARGS%

REM Hack to sleep for a few seconds:
ping 127.0.0.1 -n 4 > nul

REM ---------------------------->
REM
REM Start SOCCA Server
IF EXIST %AUTOCONNECT_FILE% (
	ECHO "Start SOCCA Server"
	cd /d "C:\armadillo\Demo\8bus\bin"
	START %SOCCA_PATH%
)

REM ---------------------------->
REM
REM Run PowerWorld CP-Trainer and autoconnect
REM IF EXIST PW (
	ECHO "START PowerWorld"
	START %PW_PATH% %AUTOCONNECT_FILE%
	
	ECHO "Start Web server"
REM )

