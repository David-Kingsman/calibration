import numpy as np

# 相机内参
fx, fy = 732.96, 732.96
cx, cy = 640.86, 350.15

camera2base = np.array([
    [ 0.24091124824167154, -0.14899460429941463,  0.9590424278207407, -0.08752472322727768],
    [-0.9699492432666021, -0.07164085854061653,  0.23252108049402597, -0.17679485043395993],
    [ 0.03406223652647522, -0.9862394208696103, -0.16177629234714908,  0.24724367376859957],
    [0.0, 0.0, 0.0, 1.0]
])

def pixel_to_world(u, v, depth):
    # 像素坐标转相机坐标
    x = (u - cx) * depth / fx
    y = (v - cy) * depth / fy
    z = depth
    cam_point = np.array([x, y, z, 1.0])
    # 相机坐标转世界坐标
    world_point = camera2base @ cam_point
    return world_point[:3]

# 示例
u, v, depth = 631, 346, 0.5464  # 你可以替换为实际值
world_xyz = pixel_to_world(u, v, depth)
print("World coordinates:", world_xyz)

# UV坐标: (631, 346)
# 深度值: 0.5464 米