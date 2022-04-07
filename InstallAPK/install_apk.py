#Author of the script: Rafiul Hye
#Email: x2rhye@southernco.com, rafiulhye91@gmail.com

import subprocess
import sys
import os 

CMD_ADB_DEVICES = 'adb devices'
CMD_ADB_S = 'adb -s '
CMD_INSTALL_REPLACE = ' install -r '

TAG = "Install APK: "

def run_cmd(cmd):
    out = subprocess.check_output(cmd)
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
    
def install_apk(devices, apk_path):
    if not devices:
        print (TAG+'No devices found! Check USB debugging is enabled.')
        return
    print (TAG+"Devices: "+str(devices)+"\n")
    apk_path = r'"{}"'.format(apk_path)
    for device in devices:
        cmd = CMD_ADB_S + device + CMD_INSTALL_REPLACE + apk_path
        try:
            print(TAG+device+": Installing...")
            out = run_cmd(cmd)
            print(TAG+device+": "+out)
        except:
            print(TAG+device+": \nFailed" )    
        
if __name__== "__main__":
    if len(sys.argv) > 1:
        apk_arg = str(sys.argv[1])
        print(TAG+"path: "+apk_arg)
        devices = get_devices()
        install_apk(devices, apk_arg)
    else:
        print(TAG+"APK path missing")
    