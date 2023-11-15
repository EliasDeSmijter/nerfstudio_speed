import numpy as np
import json
import pandas as pd

from transforms import *

import os 
from PIL import Image
from matplotlib import pyplot as plt

Nfiles = 1
N = 100

for n in range(Nfiles):
    data = {}
    data["camera_type"] = "perspective"
    data["render_height"] = 1200
    data["render_width"] = 1920

    last_line = np.zeros((1,4))
    last_line[0,3] = 1.0

    dist_min = 2.5
    dist_max = 10.0

    dist_min /= 3.0 # account for NeRFStudio scaling
    dist_max /= 3.0 # account for NeRFStudio scaling

    gt = {}

    temp_gt = []

    camera_path = []
    for index in range(N):
        q = random_quaternion()
        d = np.random.random() * (dist_max - dist_min) + dist_min
        dx = ((np.random.random()*2.0)-1.0) * d * 0.15
        dy = ((np.random.random()*2.0)-1.0) * d * 0.15
        t = np.array([[dx],[dy],[d]])

        Rinv = quaternion2rotation(q).T
        T = -Rinv@t
        Rx180 = np.array([[1.0, 0.0, 0.0],[0.0, -1.0, 0.0],[0.0, 0.0, -1.0]])
        R = Rinv @ Rx180
        M = np.concatenate((R,T), axis=1)
        M = np.concatenate((M,last_line), axis=0).reshape(16,)

        frame = {}
        frame["camera_to_world"] = M.tolist()
        frame["fov"] = 22.595
        frame["aspect"] = 1.6
        camera_path.append(frame)
        
        gt_frame = {}
        gt_frame["index"] = index
        gt_frame["q_gt"] = (q).tolist()
        gt_frame["t_gt"] = (t * 3.0).tolist()
        temp_gt.append(gt_frame)

    data["camera_path"] = camera_path

    data["fps"] = 1
    data["seconds"] = N
    data["smoothness_value"] = 0.0
    data["is_cycle"] = False
    data["crop"] = None

    with open('camera_path_' + str(n) + '.json', 'w') as f: # Camera Path for NeRFStudio
        json.dump(data, f, indent=2)
        
    gt["frames"] = temp_gt
    with open('gt_camera_path_' + str(n)  + '.json', 'w') as f: # GT in SPEED-style format
        json.dump(gt, f, indent=2)