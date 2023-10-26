from utility import GpsExtractor

fn = "D:\\datasets\\MotionBlur\\GX010091.MP4"
gps_csv = "D:\\datasets\\MotionBlur\\GX010091.CSV" 
start = 0
end = 999

gps = GpsExtractor(fn, fill_the_gaps=True)
if not gps_csv is None:
    gps.writeToCSV(gps_csv)
gps.toConsole()