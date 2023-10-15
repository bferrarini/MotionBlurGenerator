import re
import os
import numpy as np
import cv2
from tqdm import tqdm

class SytheticBlur:

    def __init__(self, source_folder, file_filter = ".*\.(jpg|png)") -> None:
        self.folder = source_folder
        self.files = [os.path.join(source_folder,f) for f in os.listdir(source_folder) if re.search(file_filter,f)]
        self.files.sort(reverse=False)

    def blurFrame(self, idx):
        raise NotImplemented()

    def blurDataset(outdir = None):
        raise NotImplemented()

    def _getFileIndex(self, start):
        if type(start) is int:
            return start
        elif type(start) is str:
            idx = self.files.index(os.path.join(self.folder, start))
            return idx
        else:
            raise ValueError(f"Start must be an integer or a string ({start})")
        

    @property
    def image_count(self):
        return len(self.files)
    

class AverageSytheticBlur(SytheticBlur):

    def blurFrame(self, idx, n):
        i0 = self._getFileIndex(idx)
        files = self.files[i0:i0+n]
        blurred = np.float32(cv2.imread(files[0]))
        for i in range(1,n):
            img = cv2.imread(files[i])
            I = i + 1 # Number of imaged used so far to compute blurred
            blurred = (blurred * I + img) / (I + 1)
        blurred = np.uint8(blurred)
        return blurred
    
    def blurDataset(self, outdir = None, nFrames = list()):
        if outdir is None:
            outdir = self.folder
        for n in nFrames:
            subfolder = "AVGBLUR_B-{:03d}".format(n)
            outdir2 = os.path.join(outdir, subfolder)
            if not os.path.exists(outdir2):
                os.makedirs(outdir2)
            for idx in tqdm(range(0,(len(self.files)//n) * n ,n), desc=f"Intensity {n}"):
                fn = self.files[idx]
                blurred = self.blurFrame(idx=idx, n=n)
                out_fn = os.path.join(outdir2,os.path.basename(fn))
                cv2.imwrite(out_fn, blurred)