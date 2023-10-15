import cv2
import math
import os
import sys
import gpmf
import gpxpy
import multiprocessing
from pathlib import Path
from utility import Unspooler
from joblib import Parallel, delayed

from datetime import timedelta
from tqdm import tqdm

class ParallelUnspooler(Unspooler):
    
    def __init__(self, video_fn : str) -> None:
        super().__init__(video_fn)

 
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
            #pool = multiprocessing.Pool(4)
            #self._resize_to = resize_to
            #self._img_format = img_format
            #self._outdir = outdir
            #pool.map(self._core_extraction, range(sId, eId))
            batch = list()
            for frameId in range(sId, eId):
                batch.append([self.video, frameId, outdir, resize_to, img_format])
            P = Parallel(n_jobs=4)(delayed(core_extraction)(i) for i in batch)
            P.start()
            P.join()
        except Exception as ex:
            print(ex)        
    
    
def core_extraction(video, frameId, outdir, resize_to = None, img_format = 'jpg'):
    video.set(cv2.CAP_PROP_POS_FRAMES, frameId)
    ret, frame = video.read()
    if ret:
        if not resize_to is None: 
            frame = cv2.resize(frame, resize_to, interpolation=cv2.INTER_AREA) 
        save_frame_to(frame, outdir, frameId, fn_idx_offset = 0, img_format = img_format)        


def save_frame_to(self, frame, outdir, frame_id, fn_idx_offset = 0, img_format = "jpg"):
    label =  Unspooler.BuildLabel(frame_id - fn_idx_offset)
    name = "{:s}.{:s}".format(label, img_format)
    fullpath = os.path.join(outdir, name)
    cv2.imwrite(fullpath, frame)