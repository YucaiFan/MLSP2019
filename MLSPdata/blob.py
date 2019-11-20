import cv2
import numpy as np
import glob
import pylab as plt
import sys
from PIL import Image
from PIL import ImageFilter
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

np.set_printoptions(threshold=sys.maxsize)

#read in files from folder and create a path to open the folder; place them into a list to access later
folders = glob.glob('frames/RHlEdXq2DuI_7')

frames_list = []
for folder in folders:
    for f in sorted(glob.glob(folder+'/*.jpg'), key=numericalSort):
        frames_list.append(f)

gs_image_list = []

for frame in frames_list:
    image = Image.open(frame)
    image_blur = image.filter(ImageFilter.GaussianBlur(radius = 3))
    gs_image = image_blur.convert(mode = 'L')
    #gs_image.show()
    data = np.asarray(gs_image).astype('float32').flatten()
    data[:250000] = 0
    data[650000:] = 0
    gs_image_list.append(data)
    #gs_image_2 = gs_image_list[i]

frame_subtract_list = [gs_image_list[i] - gs_image_list[i-1] for i in range(len(gs_image_list)) if i > 0]
#frame_subtract_list = [0 for frame in frame_subtract_list for value in frame if value < 40]
'''
for frame in frame_subtract_list:
    frame[:250000] = 0
    frame[600000:] = 0
    for j in range(len(frame)):git 
        if frame[j] < 30:
            frame[j] = 0
'''
frame_subtract_list_reshape = [frame_subtract_list[j].reshape((720, 1280)) for j in range(len(frame_subtract_list))]
frame_subtract_list_reshape[120][frame_subtract_list_reshape[120] < 25] = 0
frame_subtract_list_reshape[120][frame_subtract_list_reshape[120] > 25] = 255
image_no_noise = Image.fromarray(frame_subtract_list_reshape[120].astype('uint8'))  # turn into an image
image_no_noise.show()
#    if i > 0:
 #       frame_subtract = gs_image_list[i] - gs_image_list[i-1]
  #      frame_subtract[:300000] = 0
  #      frame_subtract[600000:] = 0
  #      for j in range(len(frame_subtract)):
  #          if frame_subtract[j] < 30:
  #              gs_image_2[j] = 0
    #frame_subtract[frame_subtract < 40] = 0
    #frame_subtract[frame_subtract > 200] = 0
    #print(frame_subtract)
       # image_reshape = gs_image_2.reshape((720, 1280))
        #image_no_noise = Image.fromarray(image_reshape.astype('uint8'))  # turn into an image
        #image_no_noise.show()