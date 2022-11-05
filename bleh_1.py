import os
from typing import Any, Union
import cv2
import shutil
import imageio
import decimal
import pathlib
import numpy as np
from natsort import natsorted
from PIL import Image
from scipy import spatial
from tqdm import tqdm


# roi coordinates : (852, 766 , 1065 ,970 )



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

    select_frames(similarity, image)

    return similarity


def select_frames(similarity, image):

    if similarity >= 0.8 :
        # print('found a kill')
        shutil.copy('frames/'+ image, 'selected_frames/'+image)

if __name__ == '__main__':

    print("STARTING ENGINES")

    for image in tqdm(os.listdir('frames')):
        compute(image)
