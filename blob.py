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

def Blob(path):
    print("Starting Blob creation for",path)
    folders = glob.glob(path)

    frames_list = []
    for folder in folders:
        for f in sorted(glob.glob(folder + '/*.jpg'), key=numericalSort):
            if ("cir_" not in str(f) and "Trajectory" not in str(f) and "blob" not in str(f)):
                frames_list.append(f)

    gs_image_list = []
    frame_ct = 0
    slice = 250000
    yvals = []
    xvals = []
    for frame in frames_list:
        #slice = 250000
        dist = 150000
        x = 0
        y = 300
        z = 650
        end = 1279
        left_to_right = 30
        row_size = 1280
        image = Image.open(frame)
        image_blur = image.filter(ImageFilter.GaussianBlur(radius=3))
        gs_image = image_blur.convert(mode='L')
        # gs_image.show()
        data = np.asarray(gs_image).astype('float32').flatten()
        #data[:slice] = 0
        #data[(slice + dist):] = 0
        for i in range(720):
            #if frame_ct < 8:
            data[:slice] = 0
            #data[(slice + dist + frame_ct * 10000):] = 0
            data[(x + row_size * i):((y + 20 * frame_ct) + row_size * i)] = 0

            if frame_ct < 6:
                data[(z + row_size * i):(end + row_size * i)] = 0
                data[(slice + dist):] = 0
            else:
                data[((z + 10 * (frame_ct - 5)) + row_size * i):(end + row_size * i)] = 0
                data[(slice + dist + (frame_ct - 5) * 25600):] = 0
        xvals.append(z + 10 * (frame_ct - 5))
        yvals.append(((slice + dist + (frame_ct - 5) * 25600))//1280 - 15)
        #print(xvals)
        #print(yvals)
            #else:
               # y = 575
               # z = 800
               # data[:250000] = 0
               # data[550000:] = 0
               # data[(x + row_size * i):(y + row_size * i)] = 0
               # data[(z + row_size * i):(end + row_size * i)] = 0
        gs_image_list.append(data)
        #slice += 1280
        frame_ct += 1
    frame_subtract_list = [gs_image_list[i] - gs_image_list[i - 1] for i in range(len(gs_image_list)) if i > 0]
    # frame_subtract_list = [0 for frame in frame_subtract_list for value in frame if value < 30]
    # frame_subtract_list = [255 for frame in frame_subtract_list for value in frame if value > 30]

    for frame in frame_subtract_list:
        for j in range(len(frame)):
            if frame[j] < 30:
                frame[j] = 0
            else:
                frame[j] = 255

    frame_subtract_list_reshape = [frame_subtract_list[j].reshape((720, 1280)) for j in range(len(frame_subtract_list))]
    counter = 0
    for frame in frame_subtract_list_reshape:
        if counter > 4:
            frame[:,xvals[counter]:] = 0
            frame[yvals[counter]:,:] = 0
        counter += 1
    ct = 1
    print("Writing Blobs")
    for blob_image in frame_subtract_list_reshape:
        image_no_noise = Image.fromarray(blob_image.astype('uint8'))  # turn into an image
        image_no_noise.save(path+'/blob_image_' + str(ct) + '.jpg')
        ct += 1
    print("Blob.py done")
        # image_no_noise.show()


# np.set_printoptions(threshold=sys.maxsize)

#read in files from folder and create a path to open the folder; place them into a list to access later
