@echo off
cd %~dp1

python %~dp0URLChecker_Stat.py %1 >> ping_result.txt  2>>&1