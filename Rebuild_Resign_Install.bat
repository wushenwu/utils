::
::call apktool b -f %~f1 >> %~dp1\error.txt 2>>&1

::
cd %~f1\dist\

call signapk %~n1.apk  >> %~dp1\error.txt 2>>&1

call adb install %~n1.apk_signed.apk  >> %~dp1\error.txt 2>>&1

exit

