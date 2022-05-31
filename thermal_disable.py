import os
import ui_init
from main import MainApp

def thd():
    os.system('adb root')
    print('adb root')
    os.system('adb remount')
    print('adb remount')
    os.system('adb shell setprop sys.retaildemo.enabled 1')
    print('adb shell setprop sys.retaildemo.enabled 1')
    os.system('adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    print('adb shell setprop vendor.disable.usb.overheat.mitigation.control 1')
    os.system('adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    print('adb shell "echo disabled > /dev/thermal/tz-by-name/neutral_therm/mode"')
    os.system('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    print('adb shell cat /dev/thermal/tz-by-name/neutral_therm/mode')
    os.system('adb shell setprop persist.vendor.disable.thermal.control 1')
    print('adb shell setprop persist.vendor.disable.thermal.control 1')
    os.system('adb shell stop vendor.thermal-hal-2-0')
    print('adb shell stop vendor.thermal-hal-2-0')
    os.system('adb shell dumpsys battery set level 100')
    print('adb shell dumpsys battery set level 100')

def main():
    thd()

if __name__ == '__main__':
    main()