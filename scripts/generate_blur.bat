set main="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\main.py"
set py="C:\Users\gtgol\VS_CODE\MotionBlurGenerator\.venv\Scripts\python.exe"


echo loop %3
echo SOURCE DATA IN %1
echo BLURRING IMAGES IN %2
set bls="002" "003" "004" "006" "008" "010" "012" "016" "020" "024" "030" "040" "048" "060" "080" "120" "240"

REM STEP 0 GPS
%py% %main% gps -v %1\raw_videos\%3 -o %1\gps\%2.txt --fill-the-gaps

REM STEP 1: unroll
%py% %main% extract -v %1\raw_videos\%3 -o %1\unrolled\%2 -m %1\mute_videos\MUTE_%3 -W 960 -H 540 -f jpg

REM STEP 2: BLURRING
(for %%a in (%bls%) do ( 
   %py% %main% avg-blur -d %1\unrolled\%2 -o %1\blurred\%2 -b %%a
))

REM STEP 3: PRUNING TO 1 FPS

(for %%a in (%bls%) do ( 
    %py% %main% prune -d %1\blurred\%2/AVGBLUR_B-%formatted% -o %1\pruned_blurred\%2\%d%a --fps=%%a --sfps=240 --override 
    echo "BL %%a PROCESSED!"
))

REM STEP 4: GENRATING 1_FPS references
%py% %main% prune -d %1\unrolled\%2 -o %1\low_fps\%2 --fps=1 --sfps=240 --override