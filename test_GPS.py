from utility import GpsExtractor

fn = "D:\\datasets\\MotionBlur\\LUZZARA-03\\LUZZARA-03B.MP4"
gps_csv = "D:\\datasets\\MotionBlur\\LUZZARA-03\\LUZZARA-03B.csv" 

#fn = "D:\\datasets\\MotionBlur\\GX010091.MP4"
#gps_csv = "D:\\datasets\MotionBlur\\GX010091.csv" 

gps = GpsExtractor(fn, fill_the_gaps=True)
if not gps_csv is None:
    gps.writeToCSV(gps_csv)
gps.toConsole()