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

main= "C:\Users\gtgol\VS_CODE\MotionBlurGenerator\main.py"
py = "C:\Users\gtgol\VS_CODE\MotionBlurGenerator\.venv\Scripts\python.exe"


echo loop %3
echo SOURCE DATA IN %1
echo BLURRING IMAGES IN %2
set bls="2" "3" "4" "6" "8" "10" "12" "16" "20" "24" "30" "40" "48" "60" "80" "120" "240"

REM STEP 0 GPS
%py% %main% "gps" -v %1/raw_videos/%3 -o %1/gps/%2.txt --fill-the-gaps

REM STEP 1: unroll
%py% %main% extract -v %1/raw_videos/%3 -o %1/unrolled/%2 -m %1/mute_videos/MUTE_%3 -W 960 -H 540 -f jpg

REM STEP 2: BLURRING
(for %%a in (%bls%) do ( 
   %py% %main% avg-blur -d %1/unrolled/%2 -o %1/blurred/%2 -b %%a
))

REM STEP 3: PRUNING TO 1 FPS

(for %%a in (%bls%) do ( 
    set formatted="00000%%a":~-3!
    %py% %main% prune -d %1/blurred/%2/AVGBLUR_B-%formatted% -o %1/pruned_blurred/%2/%formatted%" --fps=%%a --sfps=240 --override 
    echo "BL %%a PROCESSED!"
))

REM STEP 4: GENRATING 1_FPS references
%py% %main% prune -d %1/unrolled/%2 -o %1/low_fps/%2 --fps=1 --sfps=240 --override
