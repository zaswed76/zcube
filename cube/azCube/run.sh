#!/bin/sh

buildozer -v android debug
echo "-----------------------------------------------"
echo "run install >>>>>>>>>>>>>>>>>>>>>>>"
adb install -r bin/*.apk
echo "-----------------------------------------------"
echo "run app >>>>>>>>>>>>>>>>>>>>>>>"
adb logcat -s "python"