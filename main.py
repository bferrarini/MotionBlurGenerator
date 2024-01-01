import argparse
from utility import GpsExtractor, Unspooler, prune_dataset
from blurLib import AverageSytheticBlur
import os
import shutil
import re

def parse_args():
    parser = argparse.ArgumentParser()

    # GPS Extract
    subparsers = parser.add_subparsers(dest="command")

    gps_parser = subparsers.add_parser("gps")
    
    gps_parser.add_argument("-v", "--video-file", dest="video_fn", type=str, required=True, help="Input Video File with GPS data stream.")
    gps_parser.add_argument("-o", "--out-file", dest="output", type=str, required=False, default=None, help="Output file. It will be CSV.")
    gps_parser.add_argument("--fill-the-gaps", dest="fillgaps", action="store_true", help="If the resultion of GPS is lower than FPS, than the missin raw are added with replicated data.")

    # Frames Extract
    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("-v", "--video-file", dest="video_fn", type=str, required=True, help="Input Video File with GPS data stream.")
    extract_parser.add_argument("-m", "--muted-video-file", dest="muted_fn", type=str, required=False, default=None, help="Input Video File with GPS data stream.")
    extract_parser.add_argument("-o", "--out-folder", dest="output", type=str, required=True, help="Destination Folder for extracted frames.")
    extract_parser.add_argument("--force-audio-strip", dest="strip_audio", action="store_true",help="Set it if you want the stripped-audio file is extracted again.")
    extract_parser.add_argument("--clean-mute-video", dest="clean", action="store_true" ,help="Set it if you want the stripped audio video ios removed at the end.")
    extract_parser.add_argument("-s", "--start-frame", dest="sID", type=int, required=False, default=None ,help="First frame to extract.")
    extract_parser.add_argument("-e", "--end-frame", dest="eID", type=int, required=False, default=None ,help="Last frame to extract.")
    extract_parser.add_argument("-f", "--image-format", dest="img_format", type=str, required=False, default = "png", help="Image compression: png, jpg, etc. PNG is the deafult.")
    extract_parser.add_argument("-W", "--witdh", dest="W", type=int, required=False, default=None ,help="Resize frame to width")
    extract_parser.add_argument("-H", "--height", dest="H", type=int, required=False, default=None ,help="Resize frame to width")

    # Burring
    blur_parser = subparsers.add_parser("avg-blur")
    blur_parser.add_argument("-d", "--dataset-folder", dest="img_dataset_folder", help="Folder where the dataset images are stored.")
    blur_parser.add_argument("-o", "--out-folder", dest="output", type=str, required=True, help="Destination Folder for extracted frames.")
    blur_parser.add_argument("-b", "--blur-intesities", dest="nFrames", type=int, nargs='+', required=True, help="The number of frames to average.")
    
    # prune
    # It is used to create a dataset with lowwer frame rate and then, fewer places.
    # The original framerate of 240 FPS might be to dense to produce significant results on relativeli short traversal due to large number of possible matches for a query.

    all_parser = subparsers.add_parser("prune")
    all_parser.add_argument("-d", "--dataset-folder", dest="img_dataset_folder", help="Folder where the 240FPS images are stored.")
    all_parser.add_argument("-o", "--out-folder", dest="output", type=str, required=True, help="Destination Folder for extracted frames.")
    all_parser.add_argument("-f", "--offset", dest="offset", type=int, required=False, default=0 ,help="The number initial frames to skip. The deafult is 0.")
    all_parser.add_argument("-t", "--tail", dest="tail", type=int, required=False, default=0 ,help="The number terminal frames to skip. The deafult is 0.")
    all_parser.add_argument("-s", "--sfps", dest="source_fps", type=int, required=False, default=240 ,help="Source FPS. The deafult is 240.")
    all_parser.add_argument("-r", "--fps", dest="fps", type=int, required=True ,help="Target FPS.")
    all_parser.add_argument("-O", "--override", dest="override", action="store_true" ,help="Override the output filder's content.")

    # loops
    loop_parser = subparsers.add_parser("loops")
    loop_parser.add_argument("-R", "--reference-dataset", dest="img_reference_folder", help="Folder where the images to be used as a reference are stored (i.e. 1 FPS dataset)")
    loop_parser.add_argument("-o", "--out-folder", dest="output", type=str, required=True, help="Destination Folder for the loops.")
    loop_parser.add_argument("-B", "--blurred-datasets", dest="root_blurred_folder", help="Folder where the blurred versions of a datasets are stored.")
    loop_parser.add_argument("-b", "--blur-intesities", dest="nFrames", type=int, nargs='+', required=True, help="Used to identify the folder where the lurred images are stored (i.e. the product avg-blur)")
    loop_parser.add_argument("--blur-prefix", dest="bPrefix", type=str, default="AVGBLUR_B-", required=False, help="Fix the problem of potentially different namning convention of the blurred directories.")
    #loop_parser.add_argument("--blur-prefix", dest="bPrefix", type=str, default="", required=False, help="Fix the problem of potentially different namning convention of the blurred directories.")
    loop_parser.add_argument("--ref_gps", dest="ref_gps_file", type=str, required=True, help="GPS file for the reference traversal.")
    loop_parser.add_argument("--query_gps", dest="query_gps_file", type=str, required=True, help="GPS file for the query traversal.")
    loop_parser.add_argument("--prune", dest="prune", type=bool, default="false", help="True means that the blurred datasets will be reduced.")
    loop_parser.add_argument("--prune_keep_every", dest="keep", type=int, default=240, help="Only qhen prune==True: Keeps 1 in prune_keep_every frames.")
    loop_parser.add_argument("--prune_offest", dest="prune_offest", type=int, default=0, help="Only qhen prune==True: starts pruning from prune_offest image.")

    return parser.parse_args()

# TEST
# gps-v /home/main/Documents/GX010091.MP4 
# gps -v /home/main/Documents/GX010091.MP4 --fill-the-gaps
# gps -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_GAPS.CSV  
# gps -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_FULL.CSV --fill-the-gaps
def command_gps_extract(args):
    video_fn = args.video_fn
    gps_csv = args.output
    fgaps = args.fillgaps
    gps = GpsExtractor(video_fn, fill_the_gaps=fgaps)
    if gps_csv is None:
        gps.toConsole()
    else:
        if not gps_csv is None:
            gps.writeToCSV(gps_csv)

# TEST
# extract -v /home/main/Documents/GX010091.MP4 -o /mnt/deimos/Datasets/MotionBlur/GX010091_TEST1 -s 1000 -e 1300 -W 480 -H 270
# extract -v /home/main/Documents/GX010091.MP4 -o /mnt/deimos/Datasets/MotionBlur/GX010091_TEST2 -s 3000 -e 3300 --force-audio-strip 
# extract -v /home/main/Documents/GX010091.MP4 -o /mnt/deimos/Datasets/MotionBlur/GX010091_TEST3 -s 4000 -e 4300 --clean-mute-video -f jpg -W 480 -H 270
# extract -v /home/main/Documents/GX010091.MP4 -o /mnt/deimos/Datasets/MotionBlur/GX010091_TEST4 -m /mnt/deimos/Datasets/MotionBlur/GX010091_MUTE_TEST4.MP4 -s 5000 -e 5300 -W 480 -H 270
def command_frame_extract(args):

    video_fn = args.video_fn
    if os.path.exists(args.output) and os.path.isfile(args.output):
        print(f"{args.output} is not valid: it is an existing file.")
        exit()

    #build a name for the video w/o audio from the video_fn
    if args.muted_fn is None:
        fn_mute = Unspooler.getMuteFn(fn=video_fn)
    else:
        fn_mute = args.muted_fn
    force_strip_audio = args.strip_audio


    #audio must be removed otherwise opencv cannot unspoil the video
    if force_strip_audio or not os.path.exists(fn_mute):
        print(f"Stripping the audio from {video_fn}")
        print(f"Writing the file: {fn_mute}")
        Unspooler.stripAudio(video_fn, fn_mute)
        fn = fn_mute
    else:
        print(f"A muted file found.")
        print(f"Loading {fn_mute}.")
        fn = fn_mute

    unspooler = Unspooler(fn)

    new_size = [int(unspooler.frame_size[0]), int(unspooler.frame_size[1])]
    if not args.W is None:
        new_size[0] = args.W
    if not args.H is None:
        new_size[1] = args.H    

    print(unspooler)
    unspooler.extract_frames(startID = args.sID, endID = args.eID, outdir=args.output, resize_to=new_size, img_format=args.img_format)

    if args.clean:
        os.remove(fn_mute)

# TEST
# avg-blur -d /mnt/deimos/Datasets/MotionBlur/GX010091_TEST1 -o /mnt/deimos/Datasets/MotionBlur/GX010091_TEST1_BLURRED -b 4 12
def command_blur_dataset(args):
    
    blurMachine = AverageSytheticBlur(args.img_dataset_folder)
    print(f"Blurred images is going to be stored in {args.output}, a subfolder for each intesity.")
    blurMachine.blurDataset(outdir = args.output, nFrames=args.nFrames)
    print(f"\tFind blurred images in {args.output}")

# TEST
# prune -d /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_REF --fps=1 --sfps=240 --override 
def command_prune_dataset(args):
    prune_dataset(data_dir=args.img_dataset_folder, out_dir=args.output, 
                  source_FPS=args.source_fps, target_FPS=args.fps, 
                  offset=args.offset, tail=args.tail, 
                  override=args.override, file_filter= ".*\.(jpg|png)")

# TEST
# loops -R D:\\datasets\\MotionBlur\\LUZZARA-03B_1FPS -B D:\\datasets\\MotionBlur\\LUZZARA-03A_BLURRED -o D:\\datasets\\MotionBlur\\LUZZARA-03AB_test --ref_gps=D:\\datasets\\MotionBlur\\LUZZARA-03A.csv --query_gps=D:\\datasets\\MotionBlur\\LUZZARA-03B.csv --prune=True --prune_keep_every=240 --prune_offset=0 -b 2 4 240
def command_build_traversals(args):
    '''
    Copeis the imagtes and file to the reuired structure to run the experiments.
    The GT must be computed later, loop by loop, using the dedicated tool provided in VPR_evelaution_framework
    '''
    # reference data dir. Generally, it is a 'low' frame rate dataset obtained with the 'prune' command
    rDir = args.img_reference_folder
    # blurred directory
    bDir = args.root_blurred_folder
    # blur levels
    outDir = args.output
    # reference GPS
    refGPS = args.ref_gps_file
    # query GPS
    queryGPS = args.query_gps_file
    # blur Levels
    bLevels = args.nFrames
    # blur prefix
    bprefix = args.bPrefix

    # PRUNING
    

    if not os.path.exists(outDir):
        os.makedirs(outDir)

        
    for bl in bLevels:
        print(f" * Working on {bl}")
        blSource = os.path.join(bDir, "{:s}{:03d}".format(bprefix, int(bl)))
        if os.path.exists(blSource) and os.path.isdir(blSource):
            loopDir = os.path.join(outDir, "{:03d}".format(int(bl)))
            if not os.path.exists(loopDir):
                os.makedirs(loopDir)
            target_refGPS = os.path.join(loopDir, "referenceGPS.csv")
            target_queryGPS = os.path.join(loopDir, "queryGPS.csv")
            shutil.copyfile(refGPS, target_refGPS)
            shutil.copyfile(queryGPS, target_queryGPS)

            target_reference = os.path.join(loopDir, "reference")
            if not os.path.exists(target_reference):
                os.makedirs(target_reference)
            source_files = [os.path.join(rDir, f) for f in os.listdir(rDir) if re.search(".*\.(jpg|png)",f)]
            destination_files = [os.path.join(target_reference, f) for f in os.listdir(rDir) if re.search(".*\.(jpg|png)",f)]
            c = 0
            for s,d in zip(source_files,destination_files):
                shutil.copy(src = s, dst= d)
                c += 1
            print(f" # {c} files copied from {rDir} to {target_reference}.")

            target_query = os.path.join(loopDir, "query")
            if not os.path.exists(target_query):
                os.makedirs(target_query)

            source_files = [os.path.join(blSource, f) for f in os.listdir(blSource) if re.search(".*\.(jpg|png)",f)]
            destination_files = [os.path.join(target_query, f) for f in os.listdir(blSource) if re.search(".*\.(jpg|png)",f)]

            if args.prune:
                skip = args.keep // bl
                offset = args.prune_offest
            else:
                skip = 1
                offset = 0

#            c = 0
#            for s,d in zip(source_files,destination_files):
#                shutil.copy(src = s, dst= d)
#                c += 1
#            print(f"{c} files copied from {blSource} to {target_query}.")

            c = 0
            for i in range(offset, len(source_files), skip):
                s = source_files[i]
                d = destination_files[i]
                shutil.copy(src = s, dst= d)
                c += 1
            if args.prune:
                msg = f" # Prune enabled: {c} out of {len(source_files)} copied for BL = {bl}"
            else:
                msg = f" # Prune disabled: {len(source_files)} copied for BL = {bl}"
            print(msg)

        else:
            print(f" # BL {bl} skipped. {blSource} not found.")
        


COMMANDS = {
    "gps": command_gps_extract,
    "extract": command_frame_extract,
    "avg-blur": command_blur_dataset,
    "prune": command_prune_dataset,
    "loops" : command_build_traversals,
}



def main():
    args = parse_args()
    COMMANDS[args.command](args)


if __name__ == '__main__':
    main()

