echo off

REM for a dataset place here:
REM D:\datasets\MotionBlur\CASONI-01
REM     dataset_name is CASONI-01
REM     the parent directory is D:\datasets\MotionBlur
REM The root directory is the dataset directery itself
REM dataset_name and parent are given as separated args to keep the script simpler (e.g. prefix=dataset_name in the naming convension used for directories)

REM Example
REM .\scripts\assemble_benchmark.bat D:\datasets\MotionBlur CASONI-01 01 07

set main="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\main.py"
set py="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\.venv\Scripts\python.exe"

set dataset_name=%2
set root_dir=%1\%2
set prefix=%dataset_name%
set query=%3
set reference=%4

set ref_dir=%root_dir%\low_fps\%prefix%-%reference%
set query_dir=%root_dir%\pruned_blurred\%prefix%-%query%
set destination=%root_dir%\benchmark\%prefix%-%query%_to_%reference%

REM add the no no-blurred folder
set query_no_blurred=%root_dir%\low_fps\%prefix%-%query%
del %query_dir%\001
xcopy /E %root_dir%\low_fps\%prefix%-%query% %query_dir%\001

set rGPS=%root_dir%\gps\%prefix%-%reference%.txt
set qGPS=%root_dir%\gps\%prefix%-%query%.txt

%py% %main% loops -R %ref_dir% -o %destination% -B %query_dir% --ref_gps="%rGPS%" --query_gps="%qGPS%" --blur-prefix="" -b 1 2 3 4 6 8 10 12 16 20 24 30 40 48 60 80 120 240
