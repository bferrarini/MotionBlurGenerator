import cv2
import math
import os
import sys
import gpmf
import gpxpy
from pathlib import Path
from moviepy import VideoFileClip


from datetime import timedelta
from tqdm import tqdm

class Unspooler:
    
    def __init__(self, video_fn : str) -> None:
        self.fn = video_fn
        self.video = cv2.VideoCapture(video_fn)

    #duration shuld be 'hh:mm:ss.msecs'
    def duration_in_msec(self, duration : str):
        tokens = duration.split(":")
        if len(tokens) == 3:
            hh = int(tokens[0])
            mm = int(tokens[1])
            ms = self._msec_from_ss_token(tokens[2])
        elif len(tokens) == 2:
            hh = 0
            mm = int(tokens[0])
            ms = self._msec_from_ss_token(tokens[1])
        elif len(tokens) == 1:
            hh = 0
            mm = 0
            ms = self._msec_from_ss_token(tokens[0])
        else:
            raise ValueError(f"{duration} is not good as a time")
        
        msec = 1000*(hh*3600 + mm*60) + ms
        return msec
    

    def frameId(self, at : str):
        msec = self.duration_in_msec(at)
        fpms = self.fps/1000
        n = math.floor(msec*fpms)
        return n
    
    def extract_frame(self, id : int):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, id)
        ret, frame = self.video.read()
        return (ret, frame)
    
    def extract_frame_at(self, at : str):
        frame_id = self.frameId(at)
        return self.extract_frame(frame_id)

    def extract_to(self, outdir : str, start : str = None, end : str = None, resize_to = None, img_format = "jpg", verb = True):
        if start is None:
            sid = 0
        else:
            sid = self.frameId(start)
        if end is None:
            eid = sys.maxsize
        else:
            self.frameId(end)
        self.extract_frames(outdir, sid, eid, resize_to, img_format, verb)
    
    def extract_all_to(self, outdir : str, resize_to = None, img_format = "jpg", verb = True):
        self.extract_to(outdir, None, None, resize_to, img_format, verb)

    def extract_frames(self, outdir : str, startID : int = -1, endID : int = sys.maxsize, resize_to = None, img_format = "jpg", verb = True):
        if startID is None:
            sId = 0
        else:
            sId = max(startID,0)
        if endID is None:
            eId = self.frame_count
        else:
            eId = min(endID, self.frame_count)
        if verb:
            print(f"Starting frame esxtration of {eId - sId}\n from {sId} to {eId}\n to {outdir}")
            if not resize_to is None:
                print(f"resized to W:{resize_to[0]}, H:{resize_to[1]}")
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        try:
            for i in tqdm(range(sId, eId)):
                ##print(f" Frame nr: {i}/{eId}")
                self.video.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = self.video.read()
                if ret:
                    if not resize_to is None: 
                        # https://chadrick-kwag.net/cv2-resize-interpolation-methods/
                        frame = cv2.resize(frame, resize_to, interpolation=cv2.INTER_AREA) 
                    self.save_frame_to(frame, outdir, i, fn_idx_offset = 0, img_format = img_format)
        except Exception as ex:
            print(ex)        

    
    def save_frame_to(self, frame, outdir, frame_id, fn_idx_offset = 0, img_format = "jpg"):
        label =  Unspooler.BuildLabel(frame_id - fn_idx_offset)
        name = "{:s}.{:s}".format(label, img_format)
        fullpath = os.path.join(outdir, name)
        cv2.imwrite(fullpath, frame)

    def checkDatasetConsistency(self, outdir, img_format = "jpg"):
        missing_labels = list()
        file_list = [str(Path(f).stem) for f in os.listdir(outdir) if f.endswith(img_format)]
        print(f"Frame series consistency checking in {outdir}")
        for i in tqdm(range(self.frame_count)):
            label = Unspooler.BuildLabel(i)
            if not label in file_list:
                missing_labels.append()
        if len(missing_labels) == 0:
            print("\tNo missing files.")
        else:
            print("\tMissing files:")
            for l in missing_labels:
                print(f"\t\t{l}")

    def _msec_from_ss_token(self, ss_token : str):
        tokens = ss_token.split(".")
        if len(tokens) == 2:
            msec = int(tokens[0])*1000 + int((tokens[1]+"0000")[0:3])
        elif len(tokens) == 1:
            msec = int(tokens[0])*1000
        else:
            raise ValueError(f"{ss_token} is not good as a time")
        return msec


    def __str__(self):
        s = "#####\n"
        s += f"# Path: {self.fn}\n"
        s += f"# Duration {self.duration}\n"
        s += f"# FPS: {self.fps}\n"
        s += f"# Frame Count: {self.frame_count}\n"
        s += f"# (W,H): {self.frame_size[0]}, {self.frame_size[1]}\n"
        s += "#####"
        return s

    @property
    def fps(self):
        return self.video.get(cv2.CAP_PROP_FPS)
    
    @property
    def frame_count(self):
        return int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    @property
    def duration(self):
        count =  self.frame_count // self.fps
        td = timedelta(seconds=count)
        return td
    
    @property
    # (W,H)
    def frame_size(self):
        sz = (self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return sz
    
    @staticmethod
    def BuildLabel(frameId):
        return "frame_{:06d}".format(frameId)
    
    @staticmethod
    def GetFrameID(label):
        l = label.replace("frame_","")
        return int(l.split(".")[0])
    
    @staticmethod
    def stripAudio(input_file, output_file):
        videoclip = VideoFileClip(input_file)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(output_file)   

    @staticmethod
    def getMuteFn(fn):
        parent = Path(fn).parent
        base = Path(fn).stem
        ext = Path(fn).suffix
        fn = str(Path.joinpath(parent,base + "_mute" + ext))
        return fn
     

