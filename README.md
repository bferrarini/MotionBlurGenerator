# MotionBlurGenerator
main.py takes three commands: gps, extract, avg-blur

# gps: extracting GPS coordinates from a video
Please note that this function incorporates the code from [pygmf](https://github.com/alexis-mignon/pygpmf).<br/>
Usage:
```
python main.py gps -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_GAPS.CSV
```
The resolution of GPS might be lower than FPS. This happens, for example, for 240FPS videos.
To fill the gaps between frames add the flag **--fill-the-gaps**:

```
python main.py gps -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_GAPS.CSV --fill-the-gaps
```

Below it is an example of CSV with filled gaps. The frames **0** and **13** are real GPS data (look at the __true_gps__ column). The frames in the between are reported with GPS data replicated. This is done to have a complete list of the frames to facilitate the grownd truth creation.

```
idx,seq,true_gps,frameId,label,latitude,longitude,elevation,speed,pos_diluition,datetime,yy,MM,dd,hh,mm,ss,us
0,S0,1,0,frame_000000,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.755000,2023,10,3,12,53,46,755000
1,S0,0,1,frame_000001,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.759170,2023,10,3,12,53,46,759170
2,S0,0,2,frame_000002,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.763340,2023,10,3,12,53,46,763340
3,S0,0,3,frame_000003,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.767510,2023,10,3,12,53,46,767510
4,S0,0,4,frame_000004,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.771680,2023,10,3,12,53,46,771680
5,S0,0,5,frame_000005,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.775850,2023,10,3,12,53,46,775850
6,S0,0,6,frame_000006,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.780020,2023,10,3,12,53,46,780020
7,S0,0,7,frame_000007,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.784190,2023,10,3,12,53,46,784190
8,S0,0,8,frame_000008,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.788360,2023,10,3,12,53,46,788360
9,S0,0,9,frame_000009,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.792530,2023,10,3,12,53,46,792530
10,S0,0,10,frame_000010,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.796700,2023,10,3,12,53,46,796700
11,S0,0,11,frame_000011,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.800870,2023,10,3,12,53,46,800870
12,S0,0,12,frame_000012,44.9420131,10.6758726,19.462,17.93,1.35,2023-10-03 12:53:46.805040,2023,10,3,12,53,46,805040
13,S0,1,13,frame_000013,44.942005,10.6758678,19.463,17.99,1.35,2023-10-03 12:53:46.810556,2023,10,3,12,53,46,810556
14,S0,0,14,frame_000014,44.942005,10.6758678,19.463,17.99,1.35,2023-10-03 12:53:46.814726,2023,10,3,12,53,46,814726
15,S0,0,15,frame_000015,44.942005,10.6758678,19.463,17.99,1.35,2023-10-03 12:53:46.818896,2023,10,3,12,53,46,818896
```
## extract: Extracting Frames From a Video

A typical usage is as follow:
```
python main.py extract -v YOUR_VIDEO_FULLPATH -o DESTINATION_DIR -m MUTE_VIDEO_FULLPATH -W TARGET_WIDTH -H TARGET_HEIGHT -f IMAGE_FORMAT
```
- YOUR_VIDEO_FULLPATH: it is the go-pro video to unfold into the frames
- DESTINATION_DIR: the folder where all the frames will be stored
- MUTE_VIDEO_FULLPATH: the actual extraction of the frames is from the video without the audio. This file specifies the destination of such muted video. It is not required. 
- TARGET_WIDTH: reshapes the extracted frame. It is not required. 
- TARGET_HEIGHT: reshapes the extracted frame. It is not required. 
- IMAGE_FORMAT: jpg, png, etc...

Some examples:

The setting used to produde the dataset for the paper.
```
python main.py extract -v go_pro/video_01.mp4 -o go_pro/video_01_frames -m video_01_no_audio.mp4 -W 960 -H 540 -f jpg
```
You you do not need the no-audio video:
```
python main.py extract -v go_pro/video_01.mp4 -o go_pro/video_01_frames --clean-mute-video -W 960 -H 540 -f jpg
```
If you do not need any reshape:
```
python main.py extract -v go_pro/video_01.mp4 -o go_pro/video_01_frames --clean-mute-video -f jpg
```
More details can be found in the `parse_args()` of `main.py`

## avg-blur: Creating a Blurred Datasets