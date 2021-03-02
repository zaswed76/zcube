#!/bin/sh

buildozer -v android debug
echo "-----------------------------------------------"
echo "run install >>>>>>>>>>>>>>>>>>>>>>>"
adb install -r bin/*.apk
#echo 'Please connect on transfer files mode the cellphone'
#adb logcat -s "python"