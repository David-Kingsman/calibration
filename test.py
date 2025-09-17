# import pyrealsense2 as rs

# # 创建管道
# pipeline = rs.pipeline()
# config = rs.config()

# # 配置流，分辨率 1280x720，RGB 彩色
# config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# # 启动管道
# profile = pipeline.start(config)

# # 获取彩色流参数
# intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

# print("Width:", intr.width)
# print("Height:", intr.height)
# print("Fx:", intr.fx)
# print("Fy:", intr.fy)
# print("Ppx:", intr.ppx)
# print("Ppy:", intr.ppy)
# print("Distortion model:", intr.model)   # 畸变模型
# print("Distortion coeffs:", intr.coeffs) # 畸变系数

# # 内参矩阵 K
# K = [[intr.fx, 0, intr.ppx],
#      [0, intr.fy, intr.ppy],
#      [0, 0, 1]]

# print("Intrinsic Matrix K:")
# for row in K:
#     print(row)

# # 停止管道
# pipeline.stop()


#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Interface for obtaining information
"""

import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

print('=' * 50)
print('version:', arm.get_version())
print('state:', arm.get_state())
print('cmdnum:', arm.get_cmdnum())
print('err_warn_code:', arm.get_err_warn_code())
print('position(°):', arm.get_position(is_radian=False))
print('position(radian):', arm.get_position(is_radian=True))
print('angles(°):', arm.get_servo_angle(is_radian=False))
print('angles(radian):', arm.get_servo_angle(is_radian=True))
print('angles(°)(servo_id=1):', arm.get_servo_angle(servo_id=1, is_radian=False))
print('angles(radian)(servo_id=1):', arm.get_servo_angle(servo_id=1, is_radian=True))

arm.disconnect()