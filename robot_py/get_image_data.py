import time
import sys
import array

import rob_lib.sim as sim
import numpy as np
import cv2

sim.simxFinish(-1)
clientID = sim.simxStart(
    '127.0.0.1', 
    19999, 
    True, 
    True, 
    5000, 
    5
)
if(clientID != -1):
    print('connected successfully')
else:
    sys.exit('Failed to connect')
time.sleep(2)


def image_data():
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)
    err, overview_cam = sim.simxGetObjectHandle(clientID, 'overview_cam', sim.simx_opmode_oneshot_wait)
    err, resolution, image = sim.simxGetVisionSensorImage(clientID, overview_cam, 0, sim.simx_opmode_streaming)
    print(type(image))
    if sim.simxGetConnectionId(clientID) != -1:
        image_run = True

    image_ok = False
    while image_run:
        err, resolution, image = sim.simxGetVisionSensorImage(clientID, overview_cam, 0, sim.simx_opmode_buffer)
        if err == sim.simx_return_ok:
            print('iamge ok')
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imshow('image',img)
            image_ok = True
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if image_ok:
                # filename = 'warehouse_img_with_rob.png'
                filename = 'warehouse_img_with_no_rob.png'
                cv2.imwrite(filename, img)
                image_run = False
        elif err == sim.simx_return_novalue_flag:
            print("no image yet")
            pass
        else:
            print(err)


image_data()









