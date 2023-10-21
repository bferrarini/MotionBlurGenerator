REM video file: Z:\Datasets\MotionBlur\GoPRO\test_Tagliata\DCIM\100GOPRO
set python="c:/Users/main/Documents/vscode_workspace/MotionBlurGenerator/.venv/Scripts/python.exe" 
set main="c:/Users/main/Documents/vscode_workspace/MotionBlurGenerator/main.py"

%python% %main% "gps" -v D:\datasets\MotionBlur\GX010091.MP4 -o D:\datasets\MotionBlur\GX010091.csv --fill-the-gaps
%python% %main% "extract" -v D:\datasets\MotionBlur\GX010091.MP4 -o D:\datasets\MotionBlur\GX010091 -m D:\datasets\MotionBlur\GX010091_MUTE.MP4 -W 960 -H 540 -f jpg
%python% %main% "avg-blur" -d D:\datasets\MotionBlur\GX010091 -o D:\datasets\MotionBlur\\GX010091_BLURRED -b 240 120 80 60 48 40 30 24 20 16 12 10 8 6 4 3 2
%python% %main% "prune" -d D:\datasets\MotionBlur\GX010091 -o D:\datasets\MotionBlur\GX010091_1FPS --fps=1 --sfps=240 --override