REM ARG REM1
REM ARG REM1: THE ROOT DIR OF THE DATA TO WORK ON
REM
REM /home/myway/Documents/MotionBlur/LUZZARA-04/
REM | - raw_videos
REM | - unrolled
REM | - mute_videos
REM | - gps
REM | - blurred
REM | - pruned_blurred
REM | - low_fps
REM
REM ARG REM2
REM The 'working' name of the loop, i.e. the name of the folder where the freme of the the original video are extractred
REM /home/myway/Documents/MotionBlur/LUZZARA-04/
REM | - unrolled
REM   | - LUZZARA-04-01
REM The 'working name will be used for blurred frame as well'
REM /home/myway/Documents/MotionBlur/LUZZARA-04/
REM | - unrolled
REM   | - LUZZARA-04-01
REM | - blurred
REM   | - LUZZARA-04-01
REM     | - AVGBLUR_B-002
REM     | - AVGBLUR_B-004
REM     | - AVGBLUR_B-006
REM     | - ...
REM
REM ARG3 and ongoing
REM MP4 file followed by blur levels

REM Args and variable checks

set main="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\main.py"
set py="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\.venv\Scripts\python.exe"


echo loop %3
echo SOURCE DATA IN %1
echo BLURRING IMAGES IN %2
%set bls="002" "003" "004" "006" "008" "010" "012" "016" "020" "024" "030" "040" "048" "060" "080" "120" "240"
set bls=002 003 004 006 008 010 012 016 020 024 030 040 048 060 080 120 240

REM STEP 0 GPS
rem%py% %main% gps -v %1\raw_videos\%3 -o %1\gps\%2.txt --fill-the-gaps

REM STEP 1: unroll
rem%py% %main% extract -v %1\raw_videos\%3 -o %1\unrolled\%2 -m %1\mute_videos\MUTE_%3 -W 960 -H 540 -f jpg

REMSTEP 2: BLURRING
rem(for %%a in (%bls%) do ( 
rem  %py% %main% avg-blur -d %1\unrolled\%2 -o %1\blurred\%2 -b %%a
rem))

REM STEP 3: PRUNING TO 1 FPS

(for %%a in (%bls%) do ( 
    %py% %main% prune -d %1\blurred\%2/AVGBLUR_B-%%a -o %1\pruned_blurred\%2\%%a --fps=%%a --sfps=240 --override 
    echo "BL %%a PROCESSED!"
))

REM STEP 4: GENRATING 1_FPS references
rem%py% %main% prune -d %1\unrolled\%2 -o %1\low_fps\%2 --fps=1 --sfps=240 --override