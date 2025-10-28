import cv2
import pyzed.sl as sl
import time


AUTO = False  # 自动拍照，或手动按s键拍照
INTERVAL = 2 # 自动拍照间隔

camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1

counter = 0
utc = time.time()
pattern = (12, 8) # 棋盘格尺寸
folder = "./snapshot/" # 拍照文件目录


init = sl.InitParameters()

# 可选分辨率（只保留你需要的，其他注释掉）
# init.camera_resolution = sl.RESOLUTION.HD2K    # 2208*1242
# init.camera_resolution = sl.RESOLUTION.HD1080  # 1920*1080
init.camera_resolution = sl.RESOLUTION.HD720     # 1280*720
# init.camera_resolution = sl.RESOLUTION.VGA     # 672*376

cam = sl.Camera()
status = cam.open(init)
if status != sl.ERROR_CODE.SUCCESS:
    print("Failed to open camera:", status)
    exit()

# 获取并打印左目内参
left_cam_params = cam.get_camera_information().camera_configuration.calibration_parameters.left_cam
print("Left Camera Intrinsics:")
print("fx:", left_cam_params.fx)
print("fy:", left_cam_params.fy)
print("cx:", left_cam_params.cx)
print("cy:", left_cam_params.cy)
print("distortion:", left_cam_params.disto)

step_camera_settings = 1
runtime = sl.RuntimeParameters()
mat1 = sl.Mat()
mat2 = sl.Mat()

def shot(pos, frame):
    global counter
    path = folder + pos + "_" + str(counter) + ".jpg"

    cv2.imwrite(path, frame)
    print("snapshot saved into: " + path)

key = ''
while True:
    err = cam.grab(runtime)
    cam.retrieve_image(mat1, sl.VIEW.LEFT)
    cam.retrieve_image(mat2, sl.VIEW.RIGHT)
    cv2.imshow("ZED-R", mat2.get_data())
    cv2.imshow("ZED-L", mat1.get_data())
    now = time.time()
    if AUTO and now - utc >= INTERVAL:
        shot("left", mat1.get_data())
        shot("right", mat2.get_data())
        counter += 1
        utc = now

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot("left", mat1.get_data())
        shot("right", mat2.get_data())
        counter += 1

# cv2.waitKey(5)
cv2.destroyWindow("ZED-R")
cv2.destroyWindow("ZED-L")
