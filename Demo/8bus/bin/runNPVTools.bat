@ECHO off
CLS

REM -- @TODO Check that project name is passed as argument and exists	
IF "%1" == "" (
	ECHO "<USAGE> %0 [project_name] [-attack_graph_only]"
    EXIT
)

SET PROJECT=..\projects\%1

REM <---------------------------
REM -- NPVIEW and NPVGRAPH Tasks
REM ----------------------------
REM -- Requirements:
REM -- Folder bin\NPView containing files: npview.exe
REM . Initialize
SET CONTROLLER_PATH=NPView\controller\npview.exe
SET NPVGRAPH_PATH=NPVGraph\np_vgraph.py
SET NPV_INPUT_SCRIPT=npv_input.txt
SET NPV_OUTPUT_DIR=%PROJECT%\npv
SET CRITICAL_ASSET_FILE=%PROJECT%\critical-assets.txt

IF NOT EXIST NPView (
	ECHO ERROR: Could not locate folder NPView. Please add NPView binaries to bin\NPView
    EXIT
)

IF NOT EXIST PW (
	ECHO ERROR: Could not locate folder PW. Please add the CP-PW-Trainer executable to bin\PW
    EXIT
)

IF NOT EXIST %PROJECT% (
	ECHO ERROR: Could not locate folder %PROJECT% needed by NPView
    EXIT
)

IF NOT EXIST %CRITICAL_ASSET_FILE% (
	ECHO ERROR: Could not locate file %CRITICAL_ASSET_FILE% needed by NPVGraph
    EXIT
)

IF "%2" == "-attack_graph_only" (
	GOTO PRODUCE_ATTACK_GRAPH_ONLY
)

IF NOT EXIST %NPV_OUTPUT_DIR% (
	MKDIR %NPV_OUTPUT_DIR%
) ELSE (
	DEL /Q %NPV_OUTPUT_DIR%\*.*
)

IF EXIST %NPV_INPUT_SCRIPT% (
	DEL /F %NPV_INPUT_SCRIPT%
)

REM . Create input script to:
REM .. Import firewall configurations from firewall folder
ECHO -dev %PROJECT%\firewall  -o %NPV_OUTPUT_DIR% >> %NPV_INPUT_SCRIPT%

REM .. Import NMAP files
REM @TODO list all nmap files in one variable as engine cannot take a folder name as input
ECHO -nmapFiles %PROJECT%\nmap -o %NPV_OUTPUT_DIR% >> %NPV_INPUT_SCRIPT%

REM .. Load in engine
ECHO -r %NPV_OUTPUT_DIR%\ruleset.xml -t %NPV_OUTPUT_DIR%\topology.xml -sig %NPV_OUTPUT_DIR%\signature.csv >> %NPV_INPUT_SCRIPT%

REM .. Perform analysis
ECHO -a paths -reqDefault -deagg -intSrc -extSrc -intDst -extDst -xml %NPV_OUTPUT_DIR%\analysis.xml -dict %NPV_OUTPUT_DIR%\dictionary.xml -vwG %NPV_OUTPUT_DIR%\connectivity.csv -sig %NPV_OUTPUT_DIR%\signature.csv >> %NPV_INPUT_SCRIPT%

REM .. Shutdown engine
ECHO -q  >> %NPV_INPUT_SCRIPT%

REM . Start engine providing input script
ECHO Start NPVIEW Engine
START /B /WAIT "" %CONTROLLER_PATH% -is %NPV_INPUT_SCRIPT%

ECHO Done running NPVIEW

REM .. Produce attack graph
REM @TODO Ensure python is installed w/ graph module
:PRODUCE_ATTACK_GRAPH_ONLY
  ECHO %NPVGRAPH_PATH% -c %NPV_OUTPUT_DIR%\connectivity.csv -t %NPV_OUTPUT_DIR%\topology-dict.json -a %PROJECT%\critical_assets.txt
  START /B /WAIT "" %NPVGRAPH_PATH% -c %NPV_OUTPUT_DIR%\connectivity.csv -t %NPV_OUTPUT_DIR%\topology-dict.json -a %PROJECT%\critical_assets.txt
  MOVE /Y "attack_graph.xml" %NPV_OUTPUT_DIR%
