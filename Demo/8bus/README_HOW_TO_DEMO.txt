The steps :
-----------
1.	Git pull Armadillo
2.	Copy Demo\8bus content to a folder C:\8bus
3.	Start an analysis : C:\8bus\bin>runCyPSA.bat 10.31.1.201
4.	Start Tornado server : double click start_tornado.exe in folder C:\8bus\www\
5.	Use internet browser to go to localhost:8888
6.	Select Cypsa Analaysis
7.	Select project
8.	Enter path : ../projects/8bus/npv
9.	Enter IP:  10.31.1.201


Run alternative use case for 8bus:
----------------------------------

Use case created during January Review

A- .\runCyPSA.bat 8bus 72.36.82.196
B- Apply settings to webapp :(same projects & new IP)
C- then compromise host 10.39.1.22
D- Refresh or wait for new analysis display