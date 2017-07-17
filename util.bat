for /f "delims=" %%i in ('dir/b *.apk') do (
  apktool d -f %%i 
)

cd %~dp1
call %~dp0APKTool_D.bat >> %~dp1log.txt 2>>&1