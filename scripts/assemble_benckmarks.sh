#!/bin/bash

#source /home/main/vscode_workplace/MotionBlurGenerator/.venv/bin/activate
py=python3
main=/home/main/vscode_workplace/MotionBlurGenerator/main.py
#dataset_name=LUZZARA-04
#dataset_name=GUASTALLA-03
dataset_name=CASONI-01
prefix=${dataset_name}
root_dir=/home/main/Documents/MotionBlur/${dataset_name}

#query:reference
#target_pairs=("02:01" "03:01" "04:01" "05:01" "06:01" "04:02")
#target_pairs=("04:04")
#target_pairs=("03:09" "09:05" "05:09" "09:03" "09:09")
target_pairs=("09:07" "11:07" "01:09" "01:11" "07:09" "07:11")

for pair in ${target_pairs[@]}
do 
    tokens=(${pair//:/ })
    Q=${tokens[0]}
    R=${tokens[1]}

    ref_dir=${root_dir}/low_fps/${prefix}-${R}
    query_dir=${root_dir}/pruned_blurred/${prefix}-${Q}
    destination=${root_dir}/benchmark/${prefix}-${Q}_to_${R}

    #add the no no-blurred folder
    query_no_blurred=${root_dir}/low_fps/${prefix}-${Q}
    rm -rf ${query_dir}/001
    cp -R ${root_dir}/low_fps/${prefix}-${Q} ${query_dir}/001

    rGPS=${root_dir}/gps/${prefix}-${R}.txt
    qGPS=${root_dir}/gps/${prefix}-${Q}.txt

    $py $main loops -R ${ref_dir} -o ${destination} -B ${query_dir} --ref_gps=${rGPS} --query_gps=${qGPS} --blur-prefix="" -b 1 2 3 4 6 8 10 12 16 20 24 30 40 48 60 80 120 240

done