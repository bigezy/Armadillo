REM start C:\armadillo\Demo\8bus\bin\runCyPSA.bat 8bus 10.31.1.201

cd /d "C:\armadillo\Demo\8bus\www\model-server"

start C:\python27\python.exe C:\armadillo\Demo\8bus\www\model-server\src\server.py

TIMEOUT /T 2

cd /d "C:\armadillo\Demo\8bus\www"

start C:\armadillo\Demo\8bus\www\start_tornado.exe C:\armadillo\Demo\8bus\projects\8bus\npv
REM C:\armadillo\Demo\8bus\projects\8bus\npv

TIMEOUT /T 2

start "" "c:\program files (x86)\google\chrome\application\chrome.exe" --new-window "http://localhost:8888"