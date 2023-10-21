import os
import re
import shutil
from tqdm import tqdm

def prune_dataset(data_dir, out_dir, source_FPS, target_FPS, offset = 0, tail = 0, override = False, file_filter = ".*\.(jpg|png)"):
    source_file_names = [f for f in os.listdir(data_dir) if re.search(file_filter,f)]
    source_file_names.sort(reverse=False)
    source_full = list(map(lambda x: os.path.join(data_dir, x), source_file_names))
    print(f"Source Frame rate {source_FPS}")
    print(f"Target Frame rate {target_FPS}")
    skip = source_FPS // target_FPS
    print(f"Source frame to skip: {skip}")
    print(f"{offset} source file will be skipped")
    print(f"{tail} terminal frames will be skipped")
    expected = (len(source_file_names) - offset - tail) // skip + 1 # at least one image is copied

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    elif override:
        shutil.rmtree(out_dir)
        os.makedirs(out_dir)
    else:
        print(f"{out_dir} is not empty")
        exit()

    c = 0
    for i in tqdm(range(offset, len(source_full) - tail, skip)):
        src = source_full[i]
        dst = os.path.join(out_dir, source_file_names[i])
        shutil.copyfile(src, dst)
        c += 1

    print(f"{c} out of {expected} expected files were copied in {out_dir}")

if __name__ == '__main__':

    data_dir = f"D:\datasets\MotionBlur\GX010091"
    out_dir = f"D:\datasets\MotionBlur\GX010091_REF"
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    source_FPS = 240
    target_FPS = 1
    offset = 0
    #tail = 65879 - 240
    tail = 0
    prune_dataset(data_dir, out_dir, source_FPS,  target_FPS, offset, tail,  file_filter = ".*\.(jpg|png)")