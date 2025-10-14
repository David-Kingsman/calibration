import os
import cv2
import pyzed.sl as sl
import numpy as np
import math

# 全局变量存储点击点信息
clicked_point = None
point_info = None  # 存储点击点坐标和距离

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
                    distance = math.sqrt(point_cloud_value[0]**2 +
                                         point_cloud_value[1]**2 +
                                         point_cloud_value[2]**2)
                    print(f"Clicked point ({x_orig},{y_orig}) -> 3D: {point_cloud_value}, Distance: {distance:.2f} mm")
                    point_info = (x_click, y_click, distance)
                else:
                    print(f"Cannot get 3D value at ({x_orig},{y_orig})")
                    point_info = None

                clicked_point = None

            # 在图像上显示点击点和距离
            if point_info is not None:
                cx, cy, dist = point_info
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