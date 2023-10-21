REM video file: Z:\Datasets\MotionBlur\GoPRO\test_Tagliata\DCIM\100GOPRO
set python="c:/Users/main/Documents/vscode_workspace/MotionBlurGenerator/.venv/Scripts/python.exe" 
set main="c:/Users/main/Documents/vscode_workspace/MotionBlurGenerator/main.py"

set maindir="D:\datasets\MotionBlur"
set video_name=%1

%python% %main% "gps" -v %maindir%\%video_name%.MP4 -o %maindir%\%video_name%.csv --fill-the-gaps
%python% %main% "extract" -v %maindir%\%video_name%.MP4 -o %maindir%\%video_name% -m %maindir%\%video_name%_MUTE.MP4 -W 960 -H 540 -f jpg
%python% %main% "avg-blur" -d %maindir%\%video_name% -o %maindir%\%video_name%_BLURRED -b 240 120 80 60 48 40 30 24 20 16 12 10 8 6 4 3 2
%python% %main% "prune" -d %maindir%\%video_name% -o %maindir%\%video_name%_1FPS --fps=1 --sfps=240 --override