# 机器人手眼标定项目

这是一个基于Intel RealSense D435相机的机器人手眼标定项目，支持眼在手内和眼在手外两种标定模式。

## 项目结构

```
calibration/
├── API/                          # API模块
│   └── UF.py                     # 机械臂控制API
├── data_collection_d435_win/     # 数据采集模块
│   ├── main.py                   # 主采集程序
│   └── images/                   # 采集的标定板图像
├── eye_in_hand_homogeneous_matrix/  # 眼在手内标定
│   ├── main.py                   # 眼在手内标定主程序
│   ├── camera_data.py            # 相机数据处理
│   ├── save_poses.py             # 位姿保存模块
│   └── RobotToolPose.csv         # 机械臂末端位姿数据
├── out_of_hand_homogeneous_matrix/ # 眼在手外标定
│   ├── main.py                   # 眼在手外标定主程序
│   ├── camera_data.py            # 相机数据处理
│   ├── save_poses2.py            # 位姿保存模块
│   └── RobotToolPose.csv         # 机械臂末端位姿数据
├── test.py                       # 相机内参测试程序
├── transfer.py                   # 数据转换工具
└── README.md                     # 项目说明文档
```

## 功能特性

### 1. 数据采集
- 使用Intel RealSense D435相机进行实时图像采集
- 支持按's'键保存图像和对应的机械臂位姿
- 自动生成标定板图像序列和位姿文件

### 2. 眼在手内标定 (Eye-in-Hand)
- 计算相机坐标系相对于机械臂末端坐标系的变换矩阵
- 使用OpenCV的`calibrateHandEye`函数
- 支持TSAI算法进行手眼标定

### 3. 眼在手外标定 (Eye-to-Hand)
- 计算相机坐标系相对于机械臂基座坐标系的变换矩阵
- 同样使用OpenCV的`calibrateHandEye`函数
- 适用于相机固定安装的场景

### 4. 相机内参标定
- 自动计算相机内参矩阵和畸变系数
- 支持棋盘格标定板
- 可配置标定板参数（角点数量、格子大小等）

## 依赖库

- `numpy` - 数值计算
- `opencv-python` - 计算机视觉处理
- `pyrealsense2` - Intel RealSense相机SDK
- `scipy` - 科学计算（用于四元数转换）

## 安装和使用

### 1. 安装依赖
```bash
pip install numpy opencv-python pyrealsense2 scipy
```

### 2. 数据采集
```bash
cd data_collection_d435_win
python main.py
```
- 运行程序后，按's'键保存图像和位姿
- 确保机械臂API（UF.py）正常工作

### 3. 眼在手内标定
```bash
cd eye_in_hand_homogeneous_matrix
python main.py
```

### 4. 眼在手外标定
```bash
cd out_of_hand_homogeneous_matrix
python main.py
```

### 5. 相机内参测试
```bash
python test.py
```

## 标定板配置

### 眼在手内标定
- 棋盘格尺寸：11×8
- 格子大小：30mm

### 眼在手外标定
- 棋盘格尺寸：10×7
- 格子大小：14mm

## 输出结果

- **相机内参矩阵**：保存为`CameraIntrinsics.txt`
- **手眼变换矩阵**：保存为`Camera2End.txt`
- **机械臂位姿数据**：保存为`RobotToolPose.csv`

## 注意事项

1. 确保RealSense相机正确连接并安装驱动
2. 机械臂API需要根据实际使用的机械臂型号进行适配
3. 标定板需要平整，角点清晰可见
4. 采集图像时保持标定板在相机视野内
5. 建议采集20-50张不同角度的标定板图像

## 技术原理

手眼标定基于以下方程：
- 眼在手内：A₂⁻¹ × A₁ × X = X × B₂ × B₁⁻¹
- 眼在手外：A₂⁻¹ × A₁ × X = X × B₂ × B₁⁻¹

其中：
- A₁, A₂：机械臂末端在不同位置的变换矩阵
- B₁, B₂：标定板在相机坐标系下的变换矩阵
- X：待求解的手眼变换矩阵

## 许可证

本项目仅供学习和研究使用。

## 作者

机器人视觉标定项目

