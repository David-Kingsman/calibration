import numpy as np
import cv2
import pyrealsense2 as rs
from UF import *

cam0_path = r'data_collection_d435_win/images/' 
count = 0  # 初始化计数器

# 回调函数
def callback(frame):
    # define picture down coefficient of ratio
    scaling_factor = 1.0
    global count # 全局计数器

    cv_img = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    cv2.imshow("Capture_Video", cv_img)  # 窗口显示

    k = cv2.waitKey(30) & 0xFF
    if k == ord('s'):  # 若检测到按键 ‘s’
        pose_ = arm.get_pose()  # 获取机械臂状态

        # 保存机械臂位姿
        with open(r'data_collection_d435_win/images/poses.txt', 'a+') as f:
            pose_ = [str(i) for i in pose_]
            new_line = f'{",".join(pose_)}\n'
            f.write(new_line)

        # 保存图像
        filename = cam0_path + str(count) + '.jpg'
        cv2.imwrite(filename, cv_img)
        print(f"Saved: {filename}")

        count += 1

# 显示D435相机图像
def displayD435():
    pipeline = rs.pipeline() # 创建管道
    config = rs.config() # 创建配置
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())
            callback(color_image)

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    arm = UF()
    displayD435()
