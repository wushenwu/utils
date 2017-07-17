monitor-file-start()
{
  touch /mnt/sdcard/timestamp
}

#/acct/uid_10031/pid_4340/cpuacct.stat
#/acct/uid_10031/pid_4340/cpuacct.usage_percpu
#/acct/uid_10031/pid_4340/cpuacct.usage
#/acct/uid_10031/pid_4340/cgroup.clone_children
#/acct/uid_10031/pid_4340/cgroup.event_control
#/acct/uid_10031/pid_4340/notify_on_release
#/acct/uid_10031/pid_4340/cgroup.procs
#/acct/uid_10031/pid_4340/tasks

monitor-file-data()
{
  find /data \( -type f -a -newer /mnt/sdcard/timestamp \) -o -type d -a \( -name dev -o -name proc -o -name sys \) -prune | grep -v -e "^/storage/emulated/0/"  -e "^/mnt/shell/emulated/0" -e "/tencent/MicroMsg"  -e "net.ohrz.coldlaunche" -e "com.ailk.insight" -e "/com.tencent.mm"  -e "/com.sina.weibo"  -e "/com.yibasan.lizhifm"  -e "/com.netease.cloudmusic"  -e "/cn.jianyu.taskmaster" -e "/eu.chainfire.supersu" -e "/com.unicom.gudong.client" -e "/com.android.providers.settings" -e ".oneplus." -e "/com.qihoo360.launcher" -e "/com.google.android.gms" -e "/com.google.android.googlequicksearchbox" -e "^/acct/uid_" -e "^/data/system/dropbox/data_app_crash" -e "/SYSTEM_TOMBSTONE" -e "/360launcher" -e "/360contacts_v2" -e "/360/MobileSafe" -e "/360Browser" -e "/gudong/dump" -e "/sina/weibo" -e "/tencent/MobileQQ" -e "/tencent/msflogs" -e "/netease" -e "/com.autonavi.minimap" -e "/com.qzone/" -e "/com.eg.android.AlipayGphone" -e "/cn.wiz.note" -e "/.QQGame/" -e ".QMiPlugin/" -e "/.wbadcache/" -e "etouch/.eCalendar" -e "com.android.providers.calendar" -e "com.android.chrome/" -e "/data/system/procstats/state-" -e "/data/system/usagestats/0" -e ".eCalendar" -e "/tencent/" -e "dropbox/event" -e "^/data/tombstones/" -e "^/data/system/netstats" -e "/alipay/" -e "/TBS/.logTmp" -e "cn.etouch.ecalendar" -e "com.daimajia.gold" -e "com.android36kr.app" -e "/com.google.android.inputmethod.pinyin/" -e "com.tencent.mobileqq" -e "/com.qihoo360.contacts" -e "com.google.android.music" -e "com.google.android.calendar" -e "com.google.android.deskclock" -e "com.coolapk.market" -e "com.smzdm.client.android" -e "com.qihoo360.mobilesafe" -e "/acct/uid"
}

monitor-file-system()
{
  find /system \( -type f -a -newer /mnt/sdcard/timestamp \) -o -type d -a \( -name dev -o -name proc -o -name sys \) -prune | grep -v -e "^/storage/emulated/0/"  -e "^/mnt/shell/emulated/0" -e "/tencent/MicroMsg"  -e "net.ohrz.coldlaunche" -e "com.ailk.insight" -e "/com.tencent.mm"  -e "/com.sina.weibo"  -e "/com.yibasan.lizhifm"  -e "/com.netease.cloudmusic"  -e "/cn.jianyu.taskmaster" -e "/eu.chainfire.supersu" -e "/com.unicom.gudong.client" -e "/com.android.providers.settings" -e ".oneplus." -e "/com.qihoo360.launcher" -e "/com.google.android.gms" -e "/com.google.android.googlequicksearchbox" -e "^/acct/uid_" -e "^/data/system/dropbox/data_app_crash" -e "/SYSTEM_TOMBSTONE" -e "/360launcher" -e "/360contacts_v2" -e "/360/MobileSafe" -e "/360Browser" -e "/gudong/dump" -e "/sina/weibo" -e "/tencent/MobileQQ" -e "/tencent/msflogs" -e "/netease" -e "/com.autonavi.minimap" -e "/com.qzone/" -e "/com.eg.android.AlipayGphone" -e "/cn.wiz.note" -e "/.QQGame/" -e ".QMiPlugin/" -e "/.wbadcache/" -e "etouch/.eCalendar" -e "com.android.providers.calendar" -e "com.android.chrome/" -e "/data/system/procstats/state-" -e "/data/system/usagestats/0" -e ".eCalendar" -e "/tencent/" -e "dropbox/event" -e "^/data/tombstones/" -e "^/data/system/netstats" -e "/alipay/" -e "/TBS/.logTmp" -e "cn.etouch.ecalendar" -e "com.daimajia.gold" -e "com.android36kr.app" -e "/com.google.android.inputmethod.pinyin/" -e "com.tencent.mobileqq" -e "/com.qihoo360.contacts" -e "com.google.android.music" -e "com.google.android.calendar" -e "com.google.android.deskclock" -e "com.coolapk.market" -e "com.smzdm.client.android" -e "com.qihoo360.mobilesafe" -e "/acct/uid"
}

monitor-file-list()
{
  find / \( -type f -a -newer /mnt/sdcard/timestamp \) -o -type d -a \( -name dev -o -name proc -o -name sys \) -prune | grep -v -e "^/storage/emulated/0/"  -e "^/mnt/shell/emulated/0" -e "/tencent/MicroMsg"   -e "/com.tencent.mm" -e "net.ohrz.coldlaunche" -e "com.ailk.insight" -e "/com.sina.weibo"  -e "/com.yibasan.lizhifm"  -e "/com.netease.cloudmusic"  -e "/cn.jianyu.taskmaster" -e "/eu.chainfire.supersu" -e "/com.unicom.gudong.client" -e "/com.android.providers.settings" -e ".oneplus." -e "/com.qihoo360.launcher" -e "/com.google.android.gms" -e "/com.google.android.googlequicksearchbox" -e "^/acct/uid_" -e "^/data/system/dropbox/data_app_crash" -e "/SYSTEM_TOMBSTONE" -e "/360launcher" -e "/360contacts_v2" -e "/360/MobileSafe" -e "/360Browser" -e "/gudong/dump" -e "/sina/weibo" -e "/tencent/MobileQQ" -e "/tencent/msflogs" -e "/netease" -e "/com.autonavi.minimap" -e "/com.qzone/" -e "/com.eg.android.AlipayGphone" -e "/cn.wiz.note" -e "/.QQGame/" -e ".QMiPlugin/" -e "/.wbadcache/" -e "etouch/.eCalendar" -e "com.android.providers.calendar" -e "com.android.chrome/" -e "/data/system/procstats/state-" -e "/data/system/usagestats/0" -e ".eCalendar" -e "/tencent/" -e "dropbox/event" -e "^/data/tombstones/" -e "^/data/system/netstats" -e "/alipay/" -e "/TBS/.logTmp" -e "cn.etouch.ecalendar" -e "com.daimajia.gold" -e "com.android36kr.app" -e "/com.google.android.inputmethod.pinyin/" -e "com.tencent.mobileqq" -e "/com.qihoo360.contacts" -e "com.google.android.music" -e "com.google.android.calendar" -e "com.google.android.deskclock" -e "com.coolapk.market" -e "com.smzdm.client.android" -e "com.qihoo360.mobilesafe" -e "/acct/uid"
}
 
monitor-file-search()
{
  find / \( -type f -a -newer /mnt/sdcard/timestamp -exec grep -l $1 {} \; \) -o -type d -a \( -name dev -o -name proc -o -name sys \) -prune
}
