from setuptools import find_packages, setup

package_name = 'vrc_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/asr_pipeline.launch.py',
            'launch/gazebo_integration.launch.py',
            'launch/voice_system.launch.py'
        ]),
        ('share/' + package_name + '/config', [
            'config/commands.yaml',
            'config/parameters.yaml'
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='raka',
    maintainer_email='raka@todo.todo',
    description='VRC voice-controlled robot system',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'audio_selector_node = vrc_system.audio_selector_node:main',
            'audio_input_node = vrc_system.audio_input_node:main',
            'asr_node = vrc_system.asr_node:main',
            'voice_motion = vrc_system.voice_motion:main',
            'intent_node = vrc_system.intent_node:main',
            'state_machine_node = vrc_system.state_machine_node:main',
            'command_node = vrc_system.command_node:main',
        ],
    },
)
