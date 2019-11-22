import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import re
import json


'''This is the command to read in the GIF. You need Videocapture which makes a cv2 Video Object.
Add your GIF file name in the parameter of this function.
'''
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def convert_gif_to_frames(gif):

    # Initialize the frame number and create empty frame list
    frame_num = 0
    frame_list = []

    # Loop until there are frames left
    while True:
        try:
            # Try to read a frame. Okay is a BOOL if there are frames or not
            okay, frame = gif.read()
            # Append to empty frame list
            frame_list.append(frame)
            # Break if there are no other frames to read
            if not okay:
                break
            # Increment value of the frame number by 1
            frame_num += 1
        except KeyboardInterrupt:  # press ^C to quit
            break

    return frame_list


def output_frames_as_pics(frame_list):

    # Reduce the list of frames by half to make the list more managable
    frame_list_reduce = frame_list[0::2]
    # Get the path of the current working directory
    path = os.getcwd()
    # Set then name of your folder
    '''Replace this name with what you want your folder name to be'''
    folder_name = 'Picturebook_Pics_Kiss'
    # If the folder does not exist, then make it
    if not os.path.exists(path + '/' + folder_name):
        os.makedirs(path + '/' + folder_name)

    for frames_idx in range(len(frame_list_reduce)):
        cv2.imwrite(os.path.join(path + '/' + folder_name, str(frames_idx+1) + '.png'), frame_list_reduce[frames_idx])

def detect_and_show_circles(input_img, output_img,box):
    # detect circles in the image
    input_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(input_gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100,param2=1,maxRadius=10,minRadius=7)
    (xmin,ymin,xmax,ymax)=box
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        circles=circles[circles[:, 1].argsort()]
        # print(circles)
        # loop over the (x, y) coordinates and radius of the circles
        foundBall=False
        ball=(0,0,0)
        for (x, y, r) in circles:
        #     # draw the circle in the output image, then draw a rectangle
        #     # corresponding to the center of the circle
            if(x>=xmin and y>=ymin and x<=xmax and y<=ymax and not foundBall):
                print([x,y,r])
                cv2.circle(output_img, (x, y), r, (0, 255, 0), 4)
                ball=(x,y,r)
                foundBall=True
                # cv2.rectangle(output_img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
#         return output_img
#         plt.imshow(np.hstack([input_img, output_img]))
    return output_img,ball

def showArc(img,ballLocal):
    for (x, y, r) in ballLocal:
        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
        # cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return img
def run(directory):
    ball=(0,0,0)
    xmin=300
    xmax=800
    ymin=200
    ymax=480
    box=(xmin,ymin,xmax,ymax)
    firstFrame=True
    baseballs=[]
    img=[]
    for filename in sorted_aphanumeric(os.listdir(directory)):
        if("cir_" not in str(filename) and "Trajectory" not in str(filename) and "blob" in str(filename)):
            if(firstFrame):
                # print("cir" not in filename)
                im_cv = cv2.imread(directory+"/"+filename)
                img=im_cv
                # im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
                output = im_cv.copy()
                out_img,newBall=detect_and_show_circles(im_cv, output,box)
                cv2.imwrite(directory+"/cir_" + filename, out_img)
                ball=newBall
                baseballs.append(ball)
                firstFrame=False
            else:
                print("cir" not in filename)
                (x,y,r)=ball
                if x==0 and y==0 and r==0:
                    xmin = 300
                    xmax = 800
                    ymin = 200
                    ymax = 480
                    box = (xmin, ymin, xmax, ymax)
                else:
                    offset=20
                    xmin = x
                    xmax = x+offset
                    ymin = y-offset
                    ymax = y+offset
                    box = (xmin, ymin, xmax, ymax)
                print(filename)
                im_cv = cv2.imread(directory + "/" + filename)
                # im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
                output = im_cv.copy()
                out_img, newBall = detect_and_show_circles(im_cv, output, box)
                cv2.imwrite(directory + "/cir_" + filename, out_img)
                ball = newBall
                baseballs.append(ball)
    baseballs=np.array(baseballs)
    TrasjectoryImage=showArc(img,baseballs)
    if (baseballs.size!=0):
        cv2.imwrite(directory + "/Trajectory.jpg", TrasjectoryImage)
    return baseballs
# gif_ball = cv2.VideoCapture('haha.mp4')
# print(git_ball)

# frame_list = convert_gif_to_frames(gif_ball)
# print(len(frame_list), len(frame_list[0]), len(frame_list[1]))
# im_cv = frame_list[35]
# path="./videos/frames/RHlEdXq2DuI113_out"
path="./pitch"
baseballs=run(path)
# find label
clipName=path.split('/')[-1].split('_')[0]
labelFile=open("./videos/Videolabels",'r')
lines=labelFile.readlines()
label="N/A"
for line in lines:
    clipNameFile=line.split(" ")[0].split('.')[0].split("_")[0]
    # print(clipName,clipNameFile)
    if clipName==clipNameFile:
        label=line.split(" ")[1].strip('\n')
data={}
data['balls']=[]
data['label']=[]
data['frames']=[]
for x in range(0,baseballs.shape[0]):
    x,y,r=baseballs[0]
    data['balls'].append({
        'X': str(x),
        'Y': str(y),
    })
data['label'].append({
    'label': str(label)
})
data['frames'].append({
    'frames': str(baseballs.shape[0])
})
with open(path+"/"+clipName+".json", 'w') as outfile:
    json.dump(data, outfile)
# im_cv = cv2.imread("test.jpeg")
# im_cv = cv2.imread("ball.png")
# im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
# # plt.imshow(im_rgb)
#
# output = im_rgb.copy()
# # plt.imshow(im_rgb)
# detect_and_show_circles(im_rgb, output)

