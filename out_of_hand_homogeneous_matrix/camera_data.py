"""
通过相机本身得 内参和畸变系数 通过相机拍摄得标定板照片  计算  标定板相对于相机得 旋转向量和平移向量

"""


import glob
import math
import time

import cv2,os
import numpy as np

# from inner_pars import cammer_data_

objp = np.zeros((8 * 11, 3), np.float32)
objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
objp = 0.03 * objp   # 打印棋盘格一格的边长为2.32cm



obj_points = objp   # 存储3D点
img_points = []     # 存储2D点

images = glob.glob(r"images\*.jpg")

#data = [1019.5025634765625, 0.0, 616.58837890625, 0.0, 1019.5025634765625, 350.4565124511719, 0.0, 0.0, 1.0]
data = [1022.1959838867188, 0.0, 645.158447265625, 0.0, 1022.1959838867188, 363.9251403808594, 0.0, 0.0, 1.0]
camera_matrix = np.array(data, dtype=np.float64).reshape((3, 3))


#data = [27.257915496826172, -200.5976104736328, 0.0004900884232483804, -0.0003939231391996145, 525.6415405273438, 26.78697967529297, -198.06980895996094, 518.5392456054688]
data = [5.949482440948486, -80.19522857666016, 0.0010946538532152772, 0.0008973159710876644, 323.8226318359375, 5.769560813903809, -78.84636688232422, 318.7254943847656]
dist_coeffs = np.array(data, dtype=np.float64).reshape((1, 8))

camera_output = []



# mtx,dist = cammer_data_()
rvecs,tvecs = [],[]

def cammer_data(tag):

    for i in range(0,50):
        image = f"images{tag}\\{i}.jpg"

        if os.path.exists(image):

            print(image)
            frame = cv2.imread(image)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            size = gray.shape[::-1]
            ret, corners = cv2.findChessboardCorners(gray, (11, 8), None)

            if ret:  # 画面中有棋盘格
                img_points = np.array(corners)


                cv2.drawChessboardCorners(frame, (11, 8), corners, ret)


                _, rvec, tvec = cv2.solvePnP(obj_points, img_points ,camera_matrix,dist_coeffs)  # 解算位姿
                rvecs.append(rvec)
                tvecs.append(tvec)

                # print(tvec)

                distance = math.sqrt(tvec[0] ** 2 + tvec[1] ** 2 + tvec[2] ** 2)  # 计算距离
                rvec_matrix = cv2.Rodrigues(rvec)[0]  # 旋转向量->旋转矩阵
                proj_matrix = np.hstack((rvec_matrix, tvec))  # hstack: 水平合并
                eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角

                pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
                cv2.putText(frame, "dist: %.2fcm, yaw: %.2f, pitch: %.2f, roll: %.2f" % (distance, yaw, pitch, roll),
                            (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('frame', frame)

                camera_output.extend([tvec[0][0], tvec[1][0], tvec[2][0], yaw[0], pitch[0], roll[0]])

                if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
                    break
                # time.sleep(5)
            else:  # 画面中没有棋盘格
                cv2.putText(frame, "Unable to Detect Chessboard", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                            (0, 0, 255), 3)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == 27:  # 按ESC键退出
                    break


        cv2.destroyAllWindows()





    return rvecs,tvecs




if  __name__ == '__main__':
    b = cammer_data()
