import numpy as np
from xarm.wrapper import XArmAPI
from scipy.spatial.transform import Rotation


class xArm6Controller:
    # INITIAL_ARM_JOINT_POS = [0.8, -36.7, -22.6, -0.1, 58.4, 0.3, 0]  # degree
    # INITIAL_ARM_JOINT_POS = [1.5,-57.6,-21.5,-2.3,63.2,170.7,0]  # degree
    INITIAL_ARM_JOINT_POS =[3.7,-58.6,-17.8,6.6,66.8,189.3,0]
    def __init__(self, ip, init_arm_joint_pos=None):
        self.xarm = XArmAPI(ip)
        
        if init_arm_joint_pos is None:
            init_arm_joint_pos = self.INITIAL_ARM_JOINT_POS
        self.init_arm_joint_pos = init_arm_joint_pos
        
    def reset(self):
        self.xarm.motion_enable(enable=True)
        self.xarm.clean_error()

        self.xarm.set_mode(0)
        self.xarm.set_state(state=0)
        
        self.xarm.set_gripper_mode(0)
        self.xarm.set_gripper_enable(True)
        self.xarm.set_gripper_speed(2000)
        # self.xarm.set_gripper_position(0, wait=True)
        self.xarm.set_gripper_position(850, wait=True)
        self.target_gripper_position = 850
        self.xarm.set_gripper_position(self.target_gripper_position, wait=True)
        
        
        self.xarm.set_servo_angle(angle=self.init_arm_joint_pos, wait=True)
        _, self.target_position = self.xarm.get_position()
        # self.xarm.set_position(*self.target_position, speed=100, wait=True)

        # NOTE: Must set to mode 7 for non-blocking gripper action
        self.xarm.set_mode(7)
        self.xarm.set_state(state=0)


    def set_delta_eef_pose(self, delta_eef_pose):
        assert len(delta_eef_pose), "x, y, z, roll, pitch, yall"
        _, currnet_posi= self.xarm.get_position()
        x, y, z = np.array(currnet_posi[0:3]) + 1000*np.array(delta_eef_pose[0:3])

        R = Rotation.from_euler("xyz", currnet_posi[3:6], degrees=True)
        dR = Rotation.from_euler("xyz", delta_eef_pose[3:6], degrees=True)
        # Rotation is represented in the tool frame
        target_R = dR*R
        roll, pitch, yaw = target_R.as_euler("xyz", degrees=True)

        # print(self.xarm.last_used_tcp_speed)
        code = self.xarm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw)
        if code == 0:
            self.target_position = [x, y, z, roll, pitch, yaw]
        return code
    
    def set_position(self,pos):
        self.xarm.set_position(pos)
    def set_delta_xyz(self, xyz):
        assert len(xyz) == 3
        return self.set_delta_eef_pose(list(xyz) + [0.0] * 3)

    def set_gripper_position(self, gripper_position):
        gripper_position = np.clip(gripper_position, 0, 800)
        if gripper_position>400:
            gripper_position=800
        else:
            gripper_position=400
        code = self.xarm.set_gripper_position(gripper_position)
        if code == 0:
            self.target_gripper_position = gripper_position
        return code

    def set_delta_gripper_position(self, delta):
        target_gripper_position = self.target_gripper_position + delta
        target_gripper_position = np.clip(target_gripper_position, 0, 800)
        self.set_gripper_position(target_gripper_position)

    def get_proprio_state(self):
        code, (qpos, qvel, qeff) = self.xarm.get_joint_states()
        code, position=self.xarm.get_position()
        code, gripper_pos = self.xarm.get_gripper_position()
        return dict(
            qpos=qpos,
            qvel=qvel,
            qeff=qeff,
            position=position,
            gripper_pos=gripper_pos,
            target_position=self.target_position,
            target_gripper_position=self.target_gripper_position,
        )
   

    def close(self):
        self.xarm.disconnect()