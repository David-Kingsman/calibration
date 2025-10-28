import time
import numpy as np
from xarm.wrapper import XArmAPI
from typing import List 

def main(robot: str = "xarm6",   # "xarm6" | "lite6" |
         ip: str = "192.168.1.235",   
         pose: List[float] = None):

    pose = np.array(pose, dtype=np.float32)

    print(f"Connecting to {robot} at {ip} ...")
    arm = XArmAPI(ip)
    arm.motion_enable(True)
    arm.clean_error()

    # switch to position control (mode 0) and move
    print(f"current position: {np.asarray(arm.get_position_aa(is_radian=True)[1])}")
    # import pdb; pdb.set_trace()
    
    arm.set_mode(0)
    arm.set_state(0)
    time.sleep(0.5)

    print(f"Moving to pose: {pose} (units: mm, deg)")
    arm.set_position(*pose, wait=True) 
    arm.disconnect()
    print("Reset finished.")

# ==========================================================================
# Configure your robot here
# We will get in to the manual mode first, after the user confirms, we will switch to position control mode
# ==========================================================================

if __name__ == "__main__":
    ROBOT = "xarm6"                 # "xarm6" | "lite6" |
    IP    = "192.168.1.235"                    # None → use default for ROBOT

    central_pose = [333.84437993, -125.8113633, 269.37551534, -179.1, -1.8, -95.1]   # for xarm6

    # import pdb; pdb.set_trace()
    main(robot=ROBOT, ip=IP, pose=central_pose)