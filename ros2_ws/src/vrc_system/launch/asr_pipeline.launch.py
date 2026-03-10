from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='vrc_system',
            executable='audio_input_node',
            name='audio_input_node'
        ),

        Node(
            package='vrc_system',
            executable='asr_node',
            name='asr_node'
        ),

        Node(
            package='vrc_system',
            executable='intent_node',
            name='intent_node'
        ),

        Node(
            package='vrc_system',
            executable='state_machine_node',
            name='state_machine_node'
        ),

        Node(
            package='vrc_system',
            executable='command_node',
            name='command_node'
        ),

    ])
