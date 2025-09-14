import pyrealsense2 as rs

# 创建管道
pipeline = rs.pipeline()
config = rs.config()

# 配置流，分辨率 1280x720，RGB 彩色
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# 启动管道
profile = pipeline.start(config)

# 获取彩色流参数
intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()

print("Width:", intr.width)
print("Height:", intr.height)
print("Fx:", intr.fx)
print("Fy:", intr.fy)
print("Ppx:", intr.ppx)
print("Ppy:", intr.ppy)
print("Distortion model:", intr.model)   # 畸变模型
print("Distortion coeffs:", intr.coeffs) # 畸变系数

# 内参矩阵 K
K = [[intr.fx, 0, intr.ppx],
     [0, intr.fy, intr.ppy],
     [0, 0, 1]]

print("Intrinsic Matrix K:")
for row in K:
    print(row)

# 停止管道
pipeline.stop()
