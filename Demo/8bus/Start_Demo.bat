start C:\armadillo\Demo\8bus\bin\runCyPSA.bat 8bus 10.31.1.201

cd /d "C:\armadillo\Demo\8bus\www"

start C:\armadillo\Demo\8bus\www\start_tornado.exe C:\armadillo\Demo\8bus\projects\8bus\npv

TIMEOUT /T 10

start "" "c:\program files (x86)\google\chrome\application\chrome.exe" --new-window "http://localhost:8888"