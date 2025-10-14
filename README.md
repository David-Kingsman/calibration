# Robot Hand-Eye Calibration Project

This is a hand-eye calibration project for UFACTORY XARM robots using the Intel RealSense D435 camera. It supports both Eye-in-Hand and Eye-to-Hand calibration modes.

![Project Overview](assets/0.jpg)
*Overview of the robot hand-eye calibration system*

## Project Structure

```
calibration/
├── API/                          # API module
│   └── UF.py                     # UFACTORY XARM robot control API
├── data_collection_d435_win/     # Data collection module
│   ├── main.py                   # Main data collection script
│   └── images/                   # Collected calibration board images
├── eye_in_hand_homogeneous_matrix/  # Eye-in-Hand calibration (camera mounted on robot end-effector)
│   ├── main.py                   # Eye-in-Hand calibration script
│   ├── camera_data.py            # Camera data processing
│   ├── save_poses.py             # Pose saving module
│   └── RobotToolPose.csv         # Robot end-effector pose data
├── out_of_hand_homogeneous_matrix/ # Eye-to-Hand calibration (camera fixed on the workspace)
│   ├── main.py                   # Eye-to-Hand calibration script
│   ├── camera_data.py            # Camera data processing
│   ├── save_poses2.py            # Pose saving module
│   └── RobotToolPose.csv         # Robot end-effector pose data
├── test.py                       # Camera intrinsic test script
├── transfer.py                   # Data conversion tool
└── README.md                     # Project documentation
```

## Features

### 1. Data Collection
- Real-time image capture using Intel RealSense D435
- Save images and corresponding robot poses by pressing 's'
- Automatically generates calibration board image sequences and pose files

### 2. Eye-in-Hand Calibration
- Computes the transformation matrix from the camera to the robot end-effector
- Uses OpenCV's `calibrateHandEye` function
- Supports the TSAI algorithm for hand-eye calibration

### 3. Eye-to-Hand Calibration
- Computes the transformation matrix from the camera to the robot base
- Also uses OpenCV's `calibrateHandEye` function
- Suitable for scenarios where the camera is fixed

### 4. Camera Intrinsic Calibration
- Automatically computes camera intrinsic matrix and distortion coefficients
- Supports chessboard calibration boards
- Configurable board parameters (number of corners, square size, etc.)

## Environment Setup

### System Requirements
- Windows 10/11
- Python 3.7+
- Intel RealSense D435 camera
- xArm robot (or other compatible robots)

### Hardware Connections
1. **Camera**: Connect the RealSense D435 to the PC via USB 3.0
2. **Robot**: Ensure the robot is connected to the same network via Ethernet
3. **Calibration Board**: Prepare a chessboard calibration board (see board configuration section)

## Installation Steps

### 1. Clone the Project
```bash
git clone https://github.com/David-Kingsman/calibration.git
cd calibration
```

### 2. Install Python Dependencies
```bash
# Basic dependencies
pip install numpy opencv-python scipy

# RealSense SDK
pip install pyrealsense2

# If the above fails, install RealSense SDK first:
# 1. Download and install Intel RealSense SDK
# 2. Then run: pip install pyrealsense2
```

### 3. Verify Installation
```bash
# Test camera connection
python test.py

# If you see camera parameter output, installation is successful
```

## Full Calibration Workflow

### Step 1: Data Collection

#### 1.1 Prepare Calibration Board
- **Eye-in-Hand**: 11×8 chessboard, 30mm square size
- **Eye-to-Hand**: 10×7 chessboard, 14mm square size
- Ensure the board is flat, undamaged, and corners are clear

#### 1.2 Start Data Collection
```bash
cd data_collection_d435_win
python main.py
```

#### 1.3 Collection Instructions
1. The program will display the camera feed
2. Place the calibration board in the camera view
3. Move the robot to different positions and orientations
4. Press **'s'** to save the current image and pose
5. Repeat steps 3-4; 20-50 images are recommended
6. Press **'q'** to exit

#### 1.4 Verify Collected Data
```bash
# Check collected images
ls data_collection_d435_win/images/

# Check pose file
cat data_collection_d435_win/images/poses.txt
```

### Step 2: Eye-in-Hand Calibration

#### 2.1 Run Calibration Script
```bash
cd eye_in_hand_homogeneous_matrix
python main.py
```

#### 2.2 Check Output
The script outputs:
- Camera intrinsic matrix
- Distortion coefficients
- Hand-eye transformation matrix

#### 2.3 Verify Output Files
```bash
# Check generated files
ls data_collection_d435_win/images/
# Should see: CameraIntrinsics.txt, Camera2End.txt
```

### Step 3: Eye-to-Hand Calibration

#### 3.1 Run Calibration Script
```bash
cd out_of_hand_homogeneous_matrix
python main.py
```

#### 3.2 Check Output
The script outputs:
- Camera intrinsic matrix
- Distortion coefficients
- Hand-eye transformation matrix

### Step 4: Result Verification

#### 4.1 Test Camera Intrinsics
```bash
cd ..
python test.py
```

#### 4.2 Check All Output Files
```bash
# Camera intrinsics
cat data_collection_d435_win/images/CameraIntrinsics.txt

# Hand-eye transformation matrix
cat data_collection_d435_win/images/Camera2End.txt

# Pose data
cat data_collection_d435_win/images/poses.txt
```

## Calibration Board Configuration

| Mode        | Chessboard Size | Square Size | Usage                        |
|-------------|----------------|-------------|------------------------------|
| Eye-in-Hand | 11×8           | 30mm        | Camera on robot end-effector |
| Eye-to-Hand | 10×7           | 14mm        | Camera fixed on workspace    |

## Output Description

### File Structure
```
data_collection_d435_win/images/
├── 0.jpg, 1.jpg, ..., N.jpg     # Collected calibration images
├── poses.txt                    # Robot pose data
├── CameraIntrinsics.txt         # Camera intrinsic matrix
└── Camera2End.txt               # Hand-eye transformation matrix
```

### Data Formats
- **poses.txt**: Each line contains 6 values [x, y, z, rx, ry, rz]
- **CameraIntrinsics.txt**: 3×3 camera intrinsic matrix
- **Camera2End.txt**: 4×4 homogeneous transformation matrix

## Troubleshooting

### 1. Camera Connection Issues
```bash
# Issue: RealSense camera not detected
# Steps:
# 1. Check USB connection (use USB 3.0)
# 2. Reinstall RealSense SDK
# 3. Restart the computer
# 4. Run the test script
python test.py
```

### 2. Robot Connection Issues
```bash
# Issue: Cannot connect to robot
# Steps:
# 1. Check network connection
# 2. Edit IP address in API/UF.py
# 3. Ensure robot is controllable
# 4. Test connection
python -c "from API.UF import UF; arm = UF(); print(arm.get_pose())"
```

### 3. Chessboard Corner Detection Failure
```bash
# Issue: Cannot detect chessboard corners
# Steps:
# 1. Ensure the board is flat and undamaged
# 2. Adjust lighting to avoid glare
# 3. Check calibration board parameters
# 4. Make sure the board is fully in view
# 5. Try different angles and distances
```

### 4. Low Calibration Accuracy
```bash
# Issue: Low calibration accuracy
# Steps:
# 1. Collect more images (30-50 recommended)
# 2. Ensure diverse robot poses
# 3. Check calibration board quality
# 4. Verify corner detection accuracy
# 5. Re-collect data if needed
```

## Debugging Tips

### 1. Check Data Quality
```python
# Check chessboard corner detection before calibration
import cv2
import numpy as np

img = cv2.imread('data_collection_d435_win/images/0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, corners = cv2.findChessboardCorners(gray, (11, 8), None)
if ret:
    cv2.drawChessboardCorners(img, (11, 8), corners, ret)
    cv2.imshow('Corners', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

### 2. Verify Pose Data
```python
# Check robot pose data format
import numpy as np

poses = np.loadtxt('data_collection_d435_win/images/poses.txt', delimiter=',')
print(f"Pose data shape: {poses.shape}")
print(f"First pose: {poses[0]}")
```

### 3. Validate Calibration Results
```python
# Check transformation matrix validity
import numpy as np

camera2end = np.loadtxt('data_collection_d435_win/images/Camera2End.txt')
R = camera2end[:3, :3]
t = camera2end[:3, 3]

print(f"Rotation matrix determinant: {np.linalg.det(R)}")
print(f"Translation vector: {t}")
print(f"Transformation matrix:\n{camera2end}")
```

## Technical Principle

Hand-eye calibration is based on the following equations:
- Eye-in-Hand: A₂⁻¹ × A₁ × X = X × B₂ × B₁⁻¹
- Eye-to-Hand: A₂⁻¹ × A₁ × X = X × B₂ × B₁⁻¹

Where:
- A₁, A₂: Robot end-effector transformation matrices at different positions
- B₁, B₂: Calibration board transformation matrices in the camera frame
- X: The hand-eye transformation matrix to be solved

## License

This project is for learning and research purposes only.

## Author

Robot Vision Calibration Project
