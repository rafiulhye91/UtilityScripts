any_cmd.py is a script that can execute any adb command for all the connected android devices simultaneously.
Format: anycmd adb [your comand]
Example: anycmd adb reboot // reboots all the connected devices

To add the script in the system environment:

	For windows:
		Right-click on "This PC"
		Click "Properties"
		Click "Advanced system settings"
		Select tab "Advanced"
		Click "Environment Variables"
		Select "Path"
		Click "Edit"
		Click "New"
		Add path to the created directory, e.g "C:\Users\Your Name\My Scripts"
		Restart the PC
		You should be able to run any of your python scripts from any directory now.
