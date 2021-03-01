#!/bin/sh

buildozer -v android debug
adb install -r bin/*.apk
echo 'Please connect on transfer files mode the cellphone'
adb logcat -s "python"