from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="robot_a_control",
            executable="pick_node",
            name="robot_a_pick_node",
            output="screen",
            parameters=[{"auto_start": False}],
        ),
    ])
