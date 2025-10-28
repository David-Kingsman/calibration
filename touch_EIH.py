


import os
import cv2
import pyzed.sl as sl
import numpy as np
import math
from UF import *

# 全局变量存储点击点信息
clicked_point = None
point_info = None  # 存储点击点坐标、距离和底座坐标

# Camera2base 变换矩阵（齐次矩阵）
# camera2base = np.array([
#     [ 0.24091124824167154, -0.14899460429941463,  0.9590424278207407, -0.08752472322727768],
#     [-0.9699492432666021, -0.07164085854061653,  0.23252108049402597, -0.17679485043395993],
#     [ 0.03406223652647522, -0.9862394208696103, -0.16177629234714908,  0.24724367376859957],
#     [0.0, 0.0, 0.0, 1.0]
# ])
# 读取 Camera2base.txt
camera2base = np.loadtxt("data_collection_d435_win/images/Camera2base.txt")
# 平移向量部分乘以 1000
camera2base[:3, 3] *= 1000

# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)

def main():
    global clicked_point, point_info

    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30

    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(status)+". Exit program.")
        exit()

    runtime_parameters = sl.RuntimeParameters()
    image = sl.Mat()
    dep = sl.Mat()
    point_cloud = sl.Mat()
    i = 0

    cv2.namedWindow("View")
    cv2.setMouseCallback("View", mouse_callback)

    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_image(dep, sl.VIEW.DEPTH)
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)

            img = image.get_data()
            dep_map = dep.get_data()
            view = np.concatenate((cv2.resize(img,(640,360)), cv2.resize(dep_map,(640,360))), axis=1)

            # 如果有点击点
            if clicked_point is not None:
                x_click, y_click = clicked_point
                scale_x = image.get_width() / 640
                scale_y = image.get_height() / 360
                x_orig = int(x_click * scale_x)
                y_orig = int(y_click * scale_y)

                err, point_cloud_value = point_cloud.get_value(x_orig, y_orig)
                if err == sl.ERROR_CODE.SUCCESS:
                    # 计算距离
                    distance = math.sqrt(point_cloud_value[0]**2 +
                                         point_cloud_value[1]**2 +
                                         point_cloud_value[2]**2)
                    
                    # 转换到机械臂底座坐标系
                    point_homog = np.array([point_cloud_value[0], point_cloud_value[1], point_cloud_value[2], 1.0])
                    point_in_base = camera2base @ point_homog

                    print(f"Clicked pixel ({x_orig},{y_orig})")
                    print(f"Camera coords: {point_cloud_value}, Distance: {distance:.2f} mm")
                    print(f"Base coords: {point_in_base[:3]}")
                    target_point_offset_100mm = point_in_base[:3] + np.array([0, 0, 100])
                    print(f"Target point (offset 100mm): {target_point_offset_100mm}")
                    


                    point_info = (x_click, y_click, distance, point_in_base[:3])
                else:
                    print(f"Cannot get 3D value at ({x_orig},{y_orig})")
                    point_info = None

                clicked_point = None

            # 在图像上显示点击点和距离
            if point_info is not None:
                cx, cy, dist, base_coords = point_info
                cv2.circle(view, (cx, cy), 5, (0, 0, 255), -1)  # 红色圆点
                cv2.putText(view, f"{dist:.1f} mm", (cx+10, cy-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

            cv2.imshow("View", view)
            key = cv2.waitKey(1)
            if key & 0xFF == 27:
                break
            if key & 0xFF == ord('s'):
                savePath = os.path.join("./images", "V{:0>3d}.png".format(i))
                cv2.imwrite(savePath, view)
                i += 1

    zed.close()

if __name__ == "__main__":
    main()
    
# UV坐标: (687, 352)
# 深度值: 0.5080 米