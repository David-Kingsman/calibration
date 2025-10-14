#!/usr/bin/env python
from E15_robot import *
import numpy as np
import cv2
from Rigid_transformation import *
from Mech_mind import *



# Move robot to home pose
robot = E15()

cam = MechEye()
cam.choose_device(1)
robot.initialState()
tool_orientation = [0, 0, -24.358]

# Callback function for clicking on OpenCV window
click_point_pix = ()
camera_color_img, camera_depth_img = cam.ultra_get_data()

def mouseclick_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global cam, robot, click_point_pix 
        click_point_pix = (x,y)
        

        # Get click point in camera coordinates
        click_z = camera_depth_img[y][x]
        # print(click_z)
        click_x = np.multiply(x-cam.Ultra_Instrincs[0][2],click_z/cam.Ultra_Instrincs[0][0])
        click_y = np.multiply(y-cam.Ultra_Instrincs[1][2],click_z/cam.Ultra_Instrincs[1][1])
        if click_z == 0:
            return
        click_point = np.array([click_x,click_y,click_z,1])
        click_point.shape = (4,1)
        print(click_point)
        cam2end = np.loadtxt(r'API\cali_Matrix\ultra_cam2tool0.txt', delimiter=' ')
        TCP_Pose = robot.tcpPose()
        print("1",TCP_Pose)
        Homo_TCP_Pose = pose_to_homogeneous_matrix(TCP_Pose)
        cam2base = np.dot(Homo_TCP_Pose ,cam2end)
        target_position = np.dot(cam2base, click_point)
        target_position = target_position.T

        target_position[0, 2] = target_position[0, 2]
  

        # print(target_position[0])
        execute_point = np.append(target_position[0,:3], tool_orientation)
        print(execute_point)
        TCP_Name = "TCP_3"

        robot.moveP(execute_point, TCP_Name)
        # robot.initialState()
    




# Show color and depth frames
cv2.namedWindow('color')
cv2.setMouseCallback('color', mouseclick_callback)
cv2.namedWindow('depth')

while True:
    camera_color_img, camera_depth_img = cam.ultra_get_data()


    if len(click_point_pix) != 0:
        camera_color_img = cv2.circle(camera_color_img, click_point_pix, 7, (0,0,255), 2)
        camera_depth_img = cv2.circle(camera_depth_img, click_point_pix, 7, (0,0,255), 2)
    cv2.imshow('color', camera_color_img)
    cv2.imshow('depth', camera_depth_img)
    
    if cv2.waitKey(1) == ord('c'):
        break

cv2.destroyAllWindows()