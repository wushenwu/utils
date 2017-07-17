CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.DATE_CHANGED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.REBOOT
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.PACKAGE_ADDED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.MEDIA_EJECT
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.TIME_SET
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.PACKAGE_REPLACED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.MEDIA_REMOVED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.NEW_OUTGOING_CALL
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.MEDIA_UNMOUNTED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.MEDIA_CHECKING
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.PACKAGE_REMOVED
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.USER_PRESENT
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.SCREEN_ON
CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.USER_PRESENT
CALL adb -s 7eb51b43  shell input keyevent 3

::This is special
::CALL adb -s 7eb51b43  shell am  broadcast -a android.intent.action.BOOT_COMPLETED -p  yourpkg