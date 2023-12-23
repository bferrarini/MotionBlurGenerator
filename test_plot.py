import gpmf

from utility import GpsExtractor, Visualizer

fn1 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03A.MP4"
fn2 = "D:\\datasets\\MotionBlur\\for_testing\\LUZZARA-03B.MP4"
fn3 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_01.MP4"
fn4 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_02.MP4"
fn5 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_03.MP4"
fn6 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_04.MP4"
fn7 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_05.MP4"
fn8 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_06.MP4"
fn9 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_07.MP4"
fn10 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_08.MP4"
fn11 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_09.MP4"
fn12 = "D:\\datasets\\MotionBlur\\LUZZARA-04\\loop_10.MP4"
gps_map = "D:\\datasets\\MotionBlur\\LUZZARA-04\\plot.html" 

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
gps8 = GpsExtractor(fn8, fill_the_gaps=False)
gps9 = GpsExtractor(fn9, fill_the_gaps=False)
gps10 = GpsExtractor(fn10, fill_the_gaps=False)
gps11 = GpsExtractor(fn11, fill_the_gaps=False)
gps12 = GpsExtractor(fn12, fill_the_gaps=False)
#visualizer.append("A1",gps1)
#visualizer.append("A2", gps2)
visualizer.append("B1", gps3)
visualizer.append("B2", gps4)
#visualizer.append("B3", gps5)
#visualizer.append("B4", gps6)
#visualizer.append("B5", gps7)
visualizer.append("B6", gps8)
#visualizer.append("B7", gps9)
#visualizer.append("B8", gps10)
#visualizer.append("B9", gps11)
#visualizer.append("B10", gps12)

visualizer.draw_map(gps_map)