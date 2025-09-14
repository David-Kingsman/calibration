
from xarm.core.comm import SocketPort
from xarm.core.utils import convert

class UF():
    # 初始化
    def __init__(self):
        self.sock = SocketPort('192.168.1.235', 30001)

    # 获取机械臂末端位姿
    def get_pose(self):
        data = self.sock.read(timeout=1)  
        poses = convert.bytes_to_fp32s(data[35:59], 6)
        return poses

    # 获取机械臂关节角度
    def get_joint_angle(self):
        data = self.sock.read(timeout=1)
        angles = convert.bytes_to_fp32s(data[7:35], 7)
        return angles


if __name__ == '__main__':
    arm = UF()
    poses = arm.get_pose()
    print(poses)

