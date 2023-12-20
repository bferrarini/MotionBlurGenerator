import gpmf

from utility import GpsExtractor, Visualizer

fn1 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03A.MP4"
fn2 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03B.MP4"
fn3 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop1.MP4"
fn4 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop2.MP4"
fn5 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop3.MP4"
fn6 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop4.MP4"
fn7 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop5.MP4"
gps_map = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03.html" 

visualizer = Visualizer()

#fn = "D:\\datasets\\MotionBlur\\GX010091.MP4"
#gps_csv = "D:\\datasets\MotionBlur\\GX010091.csv" 

gps1 = GpsExtractor(fn1, fill_the_gaps=False)
gps2 = GpsExtractor(fn2, fill_the_gaps=False)
gps3 = GpsExtractor(fn3, fill_the_gaps=False)
gps4 = GpsExtractor(fn4, fill_the_gaps=False)
gps5 = GpsExtractor(fn5, fill_the_gaps=False)
gps6 = GpsExtractor(fn6, fill_the_gaps=False)
gps7 = GpsExtractor(fn7, fill_the_gaps=False)
#visualizer.append("A1",gps1)
#visualizer.append("A2", gps2)
visualizer.append("B1", gps3)
visualizer.append("B2", gps4)
visualizer.append("B3", gps5)
#visualizer.append("B4", gps5)
#visualizer.append("B5", gps7)
visualizer.draw_map(gps_map)