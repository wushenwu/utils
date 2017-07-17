CALL adb shell /system/bin/screencap -p /data/local/tmp/xx.png
CALL adb shell chmod 777 /data/local/tmp/xx.png
CALL adb pull /data/local/tmp/xx.png %~dp1ScreenCap.png