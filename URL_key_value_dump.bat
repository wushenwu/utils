@echo off
cd %~dp1

python %~dp0URL_key_value_dump.py %1 >> ping_result.txt  2>>&1