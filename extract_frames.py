import os
os.environ['OPENCV_FFMPEG_READ_ATTEMPTS'] = "18192"

import argparse
from pathlib import Path
from moviepy.editor import VideoFileClip
#from blurLib import AverageSynth
from utility import Unspooler, GpsExtractor, ParallelUnspooler

def stripAudio(input_file, output_file):
    videoclip = VideoFileClip(input_file)
    new_clip = videoclip.without_audio()
    new_clip.write_videofile(output_file)   

def getMuteFn(fn):
    parent = Path(fn).parent
    base = Path(fn).stem
    ext = Path(fn).suffix
    fn = str(Path.joinpath(parent,base + "_mute" + ext))
    return fn

def main(video_fn, 
         start = None,
         end = None,
         video_fn_no_audio = None, 
         image_out_dir = None, 
         img_format = "png", 
         force_strip_audio = False, 
         gps_csv = None):

    #fn = "/home/main/Documents/GX010091.MP4"
    #fn_mute = "/home/main/Documents/GX010091_mute.MP4"

    #audio must be removed otherwise opencv cannot unspoil the video
    if force_strip_audio or not os.path.exists(fn_mute):
        stripAudio(video_fn, fn_mute)
        fn = fn_mute
    else:
        fn = fn_mute

    #outdir = "/mnt/deimos/Datasets/MotionBlur/GX010091"
    unspooler = Unspooler(fn)
    print(unspooler)
    new_size = (int(unspooler.frame_size[0]/2), int(unspooler.frame_size[1]/2))
    #unspooler.extract_frames(startID = start, endID = end, outdir=outdir, resize_to=new_size, img_format=img_format)
    #unspooler.extract_all_to(outdir=image_out_dir, resize_to=new_size, img_format=img_format)
    gps = GpsExtractor(video_fn, fill_the_gaps=True)
    if not gps_csv is None:
        gps.writeToCSV(gps_csv)
    gps.toConsole()


if __name__ == '__main__':
    fn = "/home/main/Documents/GX010091.MP4"
    fn_mute = getMuteFn(fn)
    outdir = "/mnt/deimos/Datasets/MotionBlur/GX010091"
    gps_csv = "/mnt/deimos/Datasets/MotionBlur/GX010091.CSV" 
    start = 0
    end = 999
    main(fn, 
         video_fn_no_audio = fn_mute, 
         start = 31000,
         end = 32000,
         image_out_dir = outdir, 
         img_format = "jpg",
         force_strip_audio = False,
         gps_csv = gps_csv
         )