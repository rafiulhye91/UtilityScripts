#Author of the script: Rafiul Hye
#Email: x2rhye@southernco.com, rafiulhye91@gmail.com

import subprocess
import sys
import os
from subprocess import Popen, PIPE, STDOUT

CMD_ADB_DEVICES = 'adb devices'
CMD_ADB_S = 'adb -s '
ERROR_LIST = ['Exception', 'IllegalArgumentException']
NOT_APPLICABLE = "Not applicable"
TAG = "Any CMD: "

def run_cmd(cmd):
    out = "None"
    process =  Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    out, err =  process.communicate()
    if out:
        out = out.decode("utf-8").rstrip()
        does_err_exist = [ele for ele in ERROR_LIST if(ele in out)]
        if does_err_exist:
            return NOT_APPLICABLE
        return out
    if err:
        return NOT_APPLICABLE

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

def exec(devices, args):
    if not devices:
        print (TAG+'No devices found! Check USB debugging is enabled.')
        return
    print (TAG+"Devices: "+str(devices)+"\n")
    for device in devices:
        cmd = CMD_ADB_S + device + " "+args
        print(TAG+"cmd: "+cmd)
        try:
            #print(TAG+device+": running...")
            out = run_cmd(cmd)
            if out == NOT_APPLICABLE:
                print(TAG+device+": Bad CMD")
                return;
            print(TAG+device+": "+out)
        except:
            print(TAG+device+": \nFailed" )

if __name__== "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        cmd = ''

        for arg in args:
            cmd += " " + arg
        print(TAG+"cmd: "+cmd)
        cmd = cmd.replace("adb", " ")
        devices = get_devices()
        exec(devices, cmd)
    else:
        print(TAG+"Cannot find CMD")
