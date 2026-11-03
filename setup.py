import os
from glob import glob
from setuptools import setup

package_name = "robot_a_control"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Youvens Appolon",
    maintainer_email="youvens.appolon@example.com",
    description="Programmation pick and place du Robot A - Youvens Appolon",
    license="MIT",
    entry_points={
        "console_scripts": [
            "pick_node = robot_a_control.pick_node:main",
        ],
    },
)
