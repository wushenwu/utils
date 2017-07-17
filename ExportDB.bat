cd %~dp1
call sqlite3 %~f1 .dump > %~n1_dump.sql