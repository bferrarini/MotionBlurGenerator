from blurLib import AverageSytheticBlur
import cv2
import os
import numpy as np

def __draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 1.0
   color = (0, 0, 0)
   thickness = cv2.FILLED
   margin = 5
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)

   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin

   cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

if __name__ == '__main__':
    images_folder = "/mnt/deimos/Datasets/MotionBlur/GX010091_TEST1"

    blurMachine = AverageSytheticBlur(images_folder)

    # print(blurMachine.image_count)

    # image_label = "frame_020600.png"


    # sample_folder = "/home/main/Documents/blur_example"

    # b240 = blurMachine.blurFrame(image_label, 240)
    # cv2.imwrite(os.path.join(sample_folder, "B240_1FPS.png"), b240)

    # b120 = blurMachine.blurFrame(image_label, 120)
    # cv2.imwrite(os.path.join(sample_folder, "B120_2FPS.png"), b120)

    # b80 = blurMachine.blurFrame(image_label, 80)
    # cv2.imwrite(os.path.join(sample_folder, "B080_3FPS.png"), b80)

    # b60 = blurMachine.blurFrame(image_label, 60)
    # cv2.imwrite(os.path.join(sample_folder, "B060_4FPS.png"), b60)

    # b48 = blurMachine.blurFrame(image_label, 48)
    # cv2.imwrite(os.path.join(sample_folder, "B048_5FPS.png"), b48)

    # b40 = blurMachine.blurFrame(image_label, 40)
    # cv2.imwrite(os.path.join(sample_folder, "B040_6FPS.png"), b40)

    # b30 = blurMachine.blurFrame(image_label, 30)
    # cv2.imwrite(os.path.join(sample_folder, "B030_8FPS.png"), b30)

    # b24 = blurMachine.blurFrame(image_label, 24)
    # cv2.imwrite(os.path.join(sample_folder, "B024_10FPS.png"), b24)

    # b20 = blurMachine.blurFrame(image_label, 20)
    # cv2.imwrite(os.path.join(sample_folder, "B020_12FPS.png"), b20)

    # b16 = blurMachine.blurFrame(image_label, 16)
    # cv2.imwrite(os.path.join(sample_folder, "B016_15FPS.png"), b16)

    # b12 = blurMachine.blurFrame(image_label, 12)
    # cv2.imwrite(os.path.join(sample_folder, "B012_20FPS.png"), b12)   

    # b10 = blurMachine.blurFrame(image_label, 10)
    # cv2.imwrite(os.path.join(sample_folder, "B010_24FPS.png"), b10)   

    # b8 = blurMachine.blurFrame(image_label, 8)
    # cv2.imwrite(os.path.join(sample_folder, "B008_30FPS.png"), b8)   

    # b6 = blurMachine.blurFrame(image_label, 6)
    # cv2.imwrite(os.path.join(sample_folder, "B006_40FPS.png"), b6)  

    # b4 = blurMachine.blurFrame(image_label, 4)
    # cv2.imwrite(os.path.join(sample_folder, "B004_60FPS.png"), b4)     

    # b3 = blurMachine.blurFrame(image_label, 3)
    # cv2.imwrite(os.path.join(sample_folder, "B003_80FPS.png"), b3)     

    # b2 = blurMachine.blurFrame(image_label, 2)
    # cv2.imwrite(os.path.join(sample_folder, "B002_120FPS.png"), b2)  

    # b1 = blurMachine.blurFrame(image_label, 1)
    # cv2.imwrite(os.path.join(sample_folder, "B001_240FPS.png"), b1)

    # blurred_files = [os.path.join(sample_folder, f) for f in os.listdir(sample_folder) if f.endswith("png")]
    # blurred_files.sort(reverse=False)

    # frames = list()

    # for fn in blurred_files:
    #     frame = cv2.imread(fn)
    #     frame_size = np.shape(frame)
    #     __draw_label(frame, os.path.basename(fn), (20,40), (255,255,255))
    #     frames.append(frame)

    # out = cv2.VideoWriter(os.path.join(sample_folder, 'demo.avi'),
    #                       cv2.VideoWriter_fourcc('M','J','P','G'), 
    #                       0.5, 
    #                       (frame_size[1], frame_size[0]))
    
    # for i in range(len(frames)):
    #     out.write(frames[i])
    # out.release()

    blurMachine.blurDataset(outdir = "/mnt/deimos/Datasets/MotionBlur/GX010091_TEST1_BLURRED", nFrames=[4,16])

