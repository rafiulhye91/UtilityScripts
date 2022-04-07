#Developer: Rafiul Hye
#Email: x2rhye@southernco.com, rafiulhye91@gmail.com

import os
import sys
import subprocess
import pathlib
import re

OUTPUT_DIRECTORY = ''
APK = ''
RELEASE_KEY = ''
PASSWORD = ''
ANDROID_BUILD_TOOLS_PATH = ''
TAG = "SIGNING APK: "

def zip_align(app_name):
    align_apk = OUTPUT_DIRECTORY+"\\signed\\"+app_name+"_aligned.apk"
    cmd = "zipalign -v -p 4 "+ APK +" " +align_apk
    print(TAG+"zip align CMD: "+cmd)
    try:
        output = subprocess.check_output(cmd)
    except:
        print(TAG+"Waring:error!")
    file = pathlib.Path(align_apk) 
    if file.exists ():
        print(TAG+"aligned apk has been created!")
        return True
    print(TAG+"Unable to create aligned apk")
    return False
    
def sign_apk(app_name):
    signed_apk = OUTPUT_DIRECTORY+"\\signed\\"+app_name+"_signed.apk"
    aligned_apk = OUTPUT_DIRECTORY+"\\signed\\"+app_name+"_aligned.apk"
    cmd = "apksigner sign --ks "+ '"'+RELEASE_KEY +'"'+" --out "+ '"'+ signed_apk + '"'+" "+  '"'+APK+ '"'
    #print(TAG+"Signing CMD: "+cmd)
    try:
        process=subprocess.Popen(cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, shell=True)
        stdoutdata,stderrdata=process.communicate(input=PASSWORD.encode())       
        
    except:
        print(TAG+"Waring:error while signing apk!")
        
    file = pathlib.Path(signed_apk) 
    if file.exists ():
        print(TAG+"signed apk has been created!")
        return True
    print(TAG+"Unable to create signed apk")
    return False
    
def configure_dir():
    try:
        dir = OUTPUT_DIRECTORY+"\\signed"
        if not os.path.exists(dir):
            os.mkdir(dir)
    except OSError:
        print (TAG+"Creation of the directory %s failed" % OUTPUT_DIRECTORY)
        return
    os.chdir(ANDROID_BUILD_TOOLS_PATH)
    
def get_apk_info(apk_path):
    global OUTPUT_DIRECTORY
    file = pathlib.Path(APK)
    if file.exists ():
        dir_list = apk_path.split("\\")
        size = len(dir_list)
        for i in range(size-1):
            OUTPUT_DIRECTORY += dir_list[i]+"\\"
        print(TAG+"OUTPUT_DIRECTORY: "+ OUTPUT_DIRECTORY)
        app_name = dir_list[size-1]
        app_name = app_name.replace('.apk', '')
        return app_name
    else:
        print (TAG+"APK does not exist")
    

def main():
    global OUTPUT_DIRECTORY, APK, RELEASE_KEY, PASSWORD, ANDROID_BUILD_TOOLS_PATH
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(TAG+" Current Directory: "+dir_path)
    config_file = open(dir_path+'\config.txt', 'r')
    configs = config_file.readlines()

    ANDROID_BUILD_TOOLS_PATH = configs[0].replace('SDK_BUILD_TOOLS = ', '').strip('\n')
    RELEASE_KEY = configs[1].replace('KEY = ', '').strip('\n')
    PASSWORD = configs[2].replace('Password = ', '').strip('\n')
    #print(TAG+"Build tools path: "+ANDROID_BUILD_TOOLS_PATH) 
    APK = input("Drag and drop the debug apk:")
    #ANDROID_BUILD_TOOLS_PATH=ANDROID_BUILD_TOOLS_PATH.strip('\"')
    APK=APK.strip('\"')
    print(TAG+"  APK: "+APK) 
    RELEASE_KEY = RELEASE_KEY.strip('\"')
    PASSWORD = PASSWORD.strip('\"')
    app_name=get_apk_info(APK)
    configure_dir()
    is_align_req = input("Is zip aligned required(y/n):")
    if is_align_req=='y':
        if zip_align(app_name) == True:
            sign_apk(app_name)
            
    else:
        sign_apk(app_name)
if __name__== "__main__":
    main()
