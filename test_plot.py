import gpmf

from utility import GpsExtractor, Visualizer

fn1 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03A.MP4"
fn2 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03B.MP4"
gps_map = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03.html" 

visualizer = Visualizer()

#fn = "D:\\datasets\\MotionBlur\\GX010091.MP4"
#gps_csv = "D:\\datasets\MotionBlur\\GX010091.csv" 

gps1 = GpsExtractor(fn1, fill_the_gaps=False)
gps2 = GpsExtractor(fn2, fill_the_gaps=False)
visualizer.append("AAA",gps1)
visualizer.append("BBB", gps2)
visualizer.draw_map(gps_map)