#!/bin/bash

# ARG #1
# ARG #1: THE ROOT DIR OF THE DATA TO WORK ON
#
# /home/myway/Documents/MotionBlur/LUZZARA-04/
# | - raw_videos
# | - unrolled
# | - mute_videos
# | - gps
# | - blurred
# | - pruned_blurred
# | - low_fps
#
# ARG #2
# The 'working' nome of the loop, i.e. the name of the folder where the freme of the the original video are extractred
# /home/myway/Documents/MotionBlur/LUZZARA-04/
# | - unrolled
#   | - LUZZARA-04-01
# The 'working name will be used for blurred frame as well'
# /home/myway/Documents/MotionBlur/LUZZARA-04/
# | - unrolled
#   | - LUZZARA-04-01
# | - blurred
#   | - LUZZARA-04-01
#     | - AVGBLUR_B-002
#     | - AVGBLUR_B-004
#     | - AVGBLUR_B-006
#     | - ...
#
# ARG3 and ongoing
# blur levels

main="/home/myway/vscode_workspace/MotionBlurGenerator/main.py"

# Args and variable checks
echo "loop $3"
echo "SOURCE DATA IN $1"
echo "BLURRING IMAGES IN $2"
array=( "$@" )
# dal secondo in avanti
bls=( "${array[@]:3}" )
echo "BL: ${bls[@]}"

# STEP 0 GPS
#python $main gps -v $1/raw_videos/$3 -o $1/gps/$2.txt --fill-the-gaps

# STEP 1: unroll

#python $main extract -v $1/raw_videos/$3 -o $1/unrolled/$2 -m $1/mute_videos/MUTE_$3 -W 960 -H 540 -f jpg

# STEP 2: BLURRING
# delim=" "
# array to string with a delimiter
# bls="${bls%$delim}"                  # yields one:two_three
# python $main avg-blur -d $1/unrolled/$2 -o $1/blurred/$2 -b "${bls%$delim}" 


#N=4
#i=0
#for bl in ${bls[@]} 
#do
#    python $main avg-blur -d $1/unrolled/$2 -o $1/blurred/$2 -b "${bl}" &
#    let "$(( ++i%N==0  ))" && wait
#done
#wait # wait for all remaining workers

# STEP 3: PRUNING TO 1 FPS

for bl in ${bls[@]}
do
    formatted=$(printf "%03d" $bl)
    python $main prune -d $1/blurred/$2/AVGBLUR_B-"${formatted}" -o $1/pruned_blurred/$2/"${formatted}" --fps="${bl}" --sfps=240 --override 
    echo "BL ${bl} PROCESSED!"
done

# STEP 4: GENRATING 1_FPS references
#python $main prune -d $1/unrolled/$2 -o $1/low_fps/$2 --fps=1 --sfps=240 --override



