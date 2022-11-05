from PIL import Image
import cv2
import os
import promptlib
from natsort import natsorted
import glob
from tqdm import tqdm
from typing import Any, Union
import shutil
import imageio
import decimal
import pathlib
import numpy as np
from scipy import spatial


parent_path = 'C:/Personal Projects/'


def split_frames(video,video_path):

    path = parent_path + 'frames'
    print(path)
    if os.path.exists(path):
        print('frames folder already exists')
        purge_folders(path)
    else:
        try:
            os.makedirs(path, exist_ok = True)
            print("Directory for frames created successfully")
        except OSError as error:
            print("Directory for frames can not be created")


    #create the frames in the created folder
    cap = cv2.VideoCapture(video_path + '/' + video)
    success, frame = cap.read()
    currentFrame = 0
    while success:
        # capture frames one by one
        success, frame = cap.read()

        if success is True:
            # save image of the current frame in jpg format


            name = path + '/' + str(currentFrame) + '.jpg'
            print('Creating...' + name, success)
            cv2.imwrite(name, frame)
        currentFrame += 1

    print('All frames created')

def compute(image):
    gt = Image.open('frames/'+image)
    gt_crop = Image.open('test_crop.png')


    temp_crop = gt.crop((852, 766 , 1065 ,970 ))
    # temp_crop.show()

    #convert images into array for computation
    gt_crop_ar = np.array(gt_crop)
    temp_crop_ar = np.array(temp_crop)


    #flatten so that they are 1D arrrays
    gt_crop_ar = gt_crop_ar.flatten()
    temp_crop_ar = temp_crop_ar.flatten()

    #normalise the 1D array values
    gt_crop_ar = gt_crop_ar/255.0
    temp_crop_ar = temp_crop_ar/255.0

    similarity = -1 * (spatial.distance.cosine(gt_crop_ar, temp_crop_ar) -1 )
    # print(similarity)

    record_key_frames(similarity, image)

    return similarity


def purge_folders(path):
    files = glob.glob(path+'/*')
    for f in files:
        os.remove(f)



def record_key_frames(similarity, image):

    # similarity threshold can be modified eventually down the lane
    if similarity >= 0.8 :
        # print('found a kill')
        shutil.copy('frames/'+ image, 'key_frames/'+image)



def initiate(video_path):

    videos = os.listdir(video_path)
    videos = natsorted(videos)

    for video in videos:

        split_frames(video, video_path)
        path = parent_path+'key_frames'


        #folder check for key_frames
        if os.path.exists(path):
            print('key_frames folder already exists')
            purge_folders(path)

        else:
            try:
                os.makedirs(path, exist_ok = True)
                print("Directory for frames created successfully")
            except OSError as error:
                print("Directory for frames can not be created")


        for image in tqdm(os.listdir('frames')):
            compute(image)


    print('no more videos found')








if __name__ == '__main__':
    print("STARTING ENGINES")

    #open promt to select a folder where all the video clips are present
    prompter = promptlib.Files()
    dir = prompter.dir()

    initiate(dir)
