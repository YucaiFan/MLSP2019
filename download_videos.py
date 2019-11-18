import os
import json
import string
import random
import subprocess


save_dir = '../videos/'
with open('data/mlb-youtube-segmented.json', 'r') as f:
    data = json.load(f)
    cnt = 0
    print(len(data))
    #counter = set()
    cnt = 0
    for entry in data:
        cnt += 1
        if cnt >= 2:
            break
        entry = data[entry]
        # cnt += 1
        # if cnt == 5:
        #    break
        yturl = entry['url']
        ytid = yturl.split('=')[-1]
        # counter.add(yturl)

        if os.path.exists(os.path.join(save_dir, ytid+'.mp4')):
            continue
        #print(yturl)

        cmd = 'youtube-dl -f mp4 '+yturl+' -o '+os.path.join(save_dir + ytid+'.mp4')
        os.system(cmd)

