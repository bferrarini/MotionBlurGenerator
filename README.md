# MotionBlurGenerator
main.py takes three commands: gps, extract, avg-blur

# gps: extracting GPS coordinates from a video
Please note that this function incorporates the code from [pygmf](https://github.com/alexis-mignon/pygpmf).<br/>
Usage:
```
python main.py gps -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_GAPS.CSV
```
The resolution of GPS might be lower than FPS. This happens, for example, for 240FPS videos.
To fill the gaps between frames add the flag --fill-the-gaps

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



## gpmf
All credits to [pygmf](https://github.com/alexis-mignon/pygpmf)