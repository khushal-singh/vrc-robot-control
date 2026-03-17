from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='vrc_system',
            executable='asr_node',
            name='asr_node',
            output='screen'
        ),

        Node(
            package='vrc_system',
            executable='voice_motion',
            name='voice_motion',
            output='screen'
        ),

    ])
