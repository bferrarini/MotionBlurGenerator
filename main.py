import argparse
from utility import GpsExtractor, Unspooler
from blurLib import AverageSytheticBlur
import os


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
    
    # All-in-One
    all_parser = subparsers.add_parser("all")
    all_parser.add_argument("-v", "--video-file", help="Input Video File to blur.")

    return parser.parse_args()

# TEST
# extract -v /home/main/Documents/GX010091.MP4 
# extract -v /home/main/Documents/GX010091.MP4 --fill-the-gaps
# extract -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_GAPS.CSV  
# extract -v /home/main/Documents/GX010091.MP4 -o /home/main/Documents/GX010091_FULL.CSV --fill-the-gaps
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
        print(f"Strpping the audio from {video_fn}")
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


COMMANDS = {
    "gps": command_gps_extract,
    "extract": command_frame_extract,
    "avg-blur": command_blur_dataset,
}



def main():
    args = parse_args()
    COMMANDS[args.command](args)


if __name__ == '__main__':
    main()

