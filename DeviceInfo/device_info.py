#Author of the script: Rafiul Hye
#Email: x2rhye@southernco.com, rafiulhye91@gmail.com

import subprocess
import sys
import os

CMD_ADB_DEVICES = 'adb devices'
CMD_ADB_S = 'adb -s '
CMD_SUFFIX = " | grep -o '[0-9a-f]\{8\} ' | tail -n+3 | while read a; do echo -n \\\\u${a:4:4}\\\\u${a:0:4}; done \" "
CMD_SERVICE_CALL = ' shell "service call iphonesubinfo '
CMD_ANDROID_VERSION= ' shell getprop ro.build.version.sdk'
CMD_CARRIER = ' shell getprop gsm.operator.alpha '
CMD_BUILD_VERSION = ' shell getprop ro.build.fingerprint '
CMD_BUILD_TYPE = ' shell getprop ro.build.type '
TRANSC_IMEI = ' 1 ' #imei code: 1,3,4
TRANSC_PHONE_NUMBER = ' 13 ' # phone number code: 13, 14, 17, 18
TRANSC_SIM_ID = '11' # sim id code: 11, 12
TRANSC_IMSI = ' 7 ' # imsi code: 7, 8
PCKG_WAVE = 'com.southernlinc.cockpit'
PCKG_GROUP_RADIO = 'com.southernlinc.mcptt.apps'

TAG = "Device Info: "
#adb shell "service call iphonesubinfo 21 | grep -o "[0-9a-f]\{8\} " | tail -n+3 | while read a; do echo -n \\u${a:4:4}\\u${a:0:4}; done"

def run_cmd(cmd):
    out = subprocess.check_output(cmd)
    #print("run cmd: "+cmd)
    return out.decode("utf-8").rstrip()

def get_devices():
    output = run_cmd(CMD_ADB_DEVICES)
    output = output.replace('List of devices attached', '')
    output = output.replace('device', '')
    output = output.replace('unauthorized', '')
    output = output.replace('\t', '')
    output = output.replace('\r', '')
    devices = output.split("\n")
    devices =  list(filter(None, devices))
    return devices

def get_app_version(pckg_name, device):
    if run_cmd(CMD_ADB_S+device+' shell pm list packages | grep '+pckg_name) != 'package:'+pckg_name:
        return 'App not found'
    return run_cmd(CMD_ADB_S+device+' shell dumpsys package '+ pckg_name +' | grep version')

def device_info(device):
    imei = run_cmd(CMD_ADB_S+device+CMD_SERVICE_CALL+TRANSC_IMEI+CMD_SUFFIX)
    number = run_cmd(CMD_ADB_S+device+CMD_SERVICE_CALL+TRANSC_PHONE_NUMBER+CMD_SUFFIX)
    sim_id = run_cmd(CMD_ADB_S+device+CMD_SERVICE_CALL+TRANSC_SIM_ID+CMD_SUFFIX)
    imsi = run_cmd(CMD_ADB_S+device+CMD_SERVICE_CALL+TRANSC_IMSI+CMD_SUFFIX)
    sdk_version = run_cmd(CMD_ADB_S+device+CMD_ANDROID_VERSION)
    carrier = run_cmd(CMD_ADB_S+device+CMD_CARRIER)
    build_version = run_cmd(CMD_ADB_S+device+CMD_BUILD_VERSION)
    build_type = run_cmd(CMD_ADB_S+device+CMD_BUILD_TYPE)
    #version_wave = get_app_version(PCKG_WAVE, device)
    #version_group_radio = get_app_version(PCKG_GROUP_RADIO, device)

    print(TAG+" Serial number: "+device)
    print(TAG+" Carrier: "+carrier)
    print(TAG+" IMEI: "+imei)
    print(TAG+" Phone Number: "+number)
    print(TAG+" SIM ID: "+sim_id)
    print(TAG+" IMSI: "+imsi)
    print(TAG+" Android version: "+sdk_version)
    print(TAG+" Build version: "+build_version)
    print(TAG+" Build type: "+build_type)
    #print(TAG+" Wave: "+version_wave)
    #print(TAG+" Group Radio: "+version_group_radio)

    print("====================================")

def main():
    devices = get_devices()
    if not devices:
        print (TAG+'No devices found! Check USB debugging is enabled.')
        return
    for device in devices:
        device_info(device)

if __name__== "__main__":
    main()
