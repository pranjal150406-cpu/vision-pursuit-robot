# Vision Pursuit Robot

A ROS 2 robot that finds a colored target using its camera, chases it, and avoids obstacles on the way, built on the RigBetel Labs TortoiseBot platform.

**Demo video:** coming soon

## What it does

The robot runs a finite state machine (FSM) that combines two behaviors:

- **Color detection:** the camera finds a colored object and steers the robot toward its center.
- **Obstacle avoidance:** the lidar detects things in the way, and avoidance always takes priority over searching and chasing so the robot never drives into an obstacle.

States:
- **Search:** look for the target.
- **Pursue:** drive toward the target.
- **Avoid:** steer around obstacles.
- **Stop:** halts the robot when the target is reached.

## Hardware

Built from the [RigBetel Labs TortoiseBot](https://github.com/rigbetellabs/tortoisebot) kit:

- Raspberry Pi 4 Model B
- USB webcam
- 2D YDLIDAR with data converter box
- 2 BO motors with an L298N motor driver
- 11.1 V Li-ion battery and power distribution module

Full list: [hardware/parts-list.md](hardware/parts-list.md)

## Software

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- OpenCV
- Gazebo Ignition and RViz2 for simulation

## Running it

Final robot code: coming soon.

On the robot (over SSH), the sensors are started like this:

```bash
# Lidar and robot bring-up
ros2 launch tortoisebot_bringup autobringup.launch.py use_sim_time:=False exploration:=True slam_only:=True

# Camera feed
ros2 run image_tools cam2image --ros-args \
  -p width:=320 -p height:=240 \
  -p frequency:=10.0 \
  -p reliability:=best_effort \
  -p depth:=1
```

More detail: [docs/hardware-build.md](docs/hardware-build.md)

## How we got here

This project was built by a team of three. We started with Python OOP in June, moved to ROS 2 with turtlesim, then learned Gazebo and RViz2 in simulation. After joining college, we built the real robot and ran our code on it. The whole path is written up in [docs/learning-journey.md](docs/learning-journey.md).

## Project structure

```
vision-pursuit-robot/
├── README.md
├── LICENSE
├── docs/
│   ├── learning-journey.md   # June to now, step by step
│   ├── hardware-build.md     # assembling and testing the robot
│   └── challenges.md         # problems we hit and how we fixed them
├── hardware/
│   └── parts-list.md
└── src/
    ├── 01_python_oops/       # Python OOP practice
    ├── 02_turtlesim/         # shapes, boundary, go-to-goal with PID, FSM
    ├── 03_simulation/        # color detector and obstacle detector
    └── vision_pursuit/       # final robot code (coming soon)
```

## Documentation

- [Learning journey](docs/learning-journey.md)
- [Hardware build](docs/hardware-build.md)
- [Challenges and fixes](docs/challenges.md)

## Credits

Robot platform and assembly guide by [RigBetel Labs](https://github.com/rigbetellabs/tortoisebot).

## License

MIT, see [LICENSE](LICENSE).
