import numpy as np
import cv2
# import pyrealsense2 as rs
from UF import *
import pyzed.sl as sl


cam0_path = r'data_collection_d435_win/images/'  # 保存图像的路径
count = 0  # 初始化计数器 
# Global variable 
camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS" 
step_camera_settings = 1
led_on = True 
selection_rect = sl.Rect()
select_in_progress = False
origin_rect = (-1,-1 )


# 回调函数 
def callback(frame):
    # define picture down coefficient of ratio
    scaling_factor = 1.0 # 缩放比例
    global count # 全局计数器

    cv_img = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA) # 图像缩放
    cv2.imshow("Capture_Video", cv_img)  # 窗口显示

    k = cv2.waitKey(30) & 0xFF # 等待按键, 30ms 
    if k == ord('s'):  # 若检测到按键 ‘s’ 
        pose_ = arm.get_pose()  # 获取机械臂状态
        # 保存机械臂位姿
        with open(r'data_collection_d435_win/images/poses.txt', 'a+') as f:
            pose_ = [str(i) for i in pose_]
            new_line = f'{",".join(pose_)}\n'
            f.write(new_line)

        # 保存图像 
        filename = cam0_path + str(count) + '.jpg'
        cv2.imwrite(filename, cv_img) # 保存图像到指定路径
        print(f"Saved: {filename}")

        count += 1

# 显示D435相机图像
# def displayD435():
#     pipeline = rs.pipeline() # 创建管道
#     config = rs.config() # 创建配置
#     config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30) # 配置彩色流
#     pipeline.start(config) # 开始流

#     # 捕获图像
#     try:
#         while True:
#             frames = pipeline.wait_for_frames() # 等待新帧
#             color_frame = frames.get_color_frame() # 获取彩色帧
#             if not color_frame:
#                 continue # 若无帧则继续等待
#             color_image = np.asanyarray(color_frame.get_data()) # 转换为numpy数组
#             callback(color_image) # 调用回调函数处理图像

#     finally:
#         pipeline.stop() # 停止流
#         cv2.destroyAllWindows() # 关闭所有OpenCV窗口
def on_mouse(event, x, y, flags, param):
    pass  # 暂时不处理任何事件
def DisplayZed():
    init = sl.InitParameters()
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(status)+". Exit program.")
        exit()
    
    runtime = sl.RuntimeParameters()
    mat = sl.Mat() 
    win_name = "Camera Control"
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, on_mouse)
    global count

    while True:
        err = cam.grab(runtime) 
        if err <= sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            cvImage = mat.get_data()
            if (not selection_rect.is_empty() and selection_rect.is_contained(sl.Rect(0,0,cvImage.shape[1],cvImage.shape[0]))):
                cv2.rectangle(cvImage,(selection_rect.x,selection_rect.y),(selection_rect.width+selection_rect.x,selection_rect.height+selection_rect.y),(220, 180, 20), 2)
            cv2.imshow(win_name, cvImage)
            k = cv2.waitKey(30) & 0xFF
            if k == ord('s'):
                pose_ = arm.get_pose()
                with open(r'data_collection_d435_win/images/poses.txt', 'a+') as f:
                    pose_ = [str(i) for i in pose_]
                    new_line = f'{",".join(pose_)}\n'
                    f.write(new_line)
                filename = cam0_path + str(count) + '.jpg'
                cv2.imwrite(filename, cvImage)
                print(f"Saved: {filename}")
                count += 1
            elif k == ord('q'):
                break
        else:
            print("Error during capture : ", err)
            break

    cv2.destroyAllWindows()
    cam.close()



if __name__ == '__main__':
    arm = UF()
    DisplayZed()
