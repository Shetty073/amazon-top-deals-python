@ECHO OFF
REM Execute this from current directory: https://stackoverflow.com/questions/4451668/bat-file-to-open-cmd-in-current-directory
cd /d %~dp0

REM https://www.quora.com/How-can-I-check-if-I-have-administrator-right-from-a-batch-file
net session >nul 2>&1
if not %errorLevel% == 0 (
	color 04
    echo Error: Admin rights are missing! Run this script again with admin rights!
	pause
	exit
)

color 0a
pip install -r ./requirements.txt

SET /A waittime_close=3
echo Done. Closing in %waittime_close% seconds
ping -n %waittime_close% localhost >NUL