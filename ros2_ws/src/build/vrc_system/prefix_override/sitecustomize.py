import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/mnt/d/AIS Project/vrc-robot-control/ros2_ws/src/install/vrc_system'
