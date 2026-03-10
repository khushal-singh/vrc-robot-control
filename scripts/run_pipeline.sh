#!/bin/bash
cd ros2_ws
source install/setup.bash
ros2 launch vrc_system asr_pipeline.launch.py
