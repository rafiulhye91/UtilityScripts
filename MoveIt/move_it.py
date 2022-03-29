import pyautogui
import math
import time
import sys

print('To exit take the mouse pointer to any corner and hold for 1 sec.')
try:
    while True:
        try:
            pyautogui.press('volumedown')
            time.sleep(1)
            pyautogui.press('volumeup')
            time.sleep(1)
        except pyautogui.FailSafeException:
            print('Exit!!')
            sys.exit()
except KeyboardInterrupt:
    print('Exit!!')
    pass     