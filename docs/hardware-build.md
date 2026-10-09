# Hardware Build

We followed the official TortoiseBot hardware instructions from RigBetel Labs: [Hardware Assembly guide](https://github.com/rigbetellabs/tortoisebot/wiki/2.-Hardware-Assembly). This page covers what we did and what we ran into along the way.

The full list of parts is in [parts-list.md](../hardware/parts-list.md).

## 1. Unboxing and checking parts

**What we did:** checked everything in the kit against the parts list.

**Photo:** coming soon

## 2. Assembly

**What we did:** assembled the chassis, motors, motor driver, power distribution module and Raspberry Pi following the official guide, layer by layer.

**Photo:** coming soon

## 3. Raspberry Pi setup and check

**What we did:** the Raspberry Pi 4 came with a pre-flashed SD card. After assembly we powered it on and checked that it booted and worked properly.

**Challenge:** the Pi kept turning on and off. [Full story](challenges.md#12-raspberry-pi-turning-on-and-off)

## 4. Motor test

**What we did:** ran a motor test program to confirm both motors spin correctly.

**Code:** [test/](../test) (coming soon)

**Challenge:** the motors were weak. [Full story](challenges.md#11-motors-not-getting-enough-power)

## 5. Camera integration

**What we did:** plugged the USB webcam into the Pi and started the feed with `cam2image`, then viewed it in RViz2 to confirm it was publishing.

```bash
ros2 run image_tools cam2image --ros-args \
  -p width:=320 -p height:=240 \
  -p frequency:=10.0 \
  -p reliability:=best_effort \
  -p depth:=1
```

- `width` and `height`: a small 320x240 image keeps the load on the Pi low.
- `frequency`: 10 frames per second.
- `reliability:=best_effort`: drops a frame instead of waiting to resend it, which avoids lag.
- `depth:=1`: keeps only the latest frame.

**Challenge:** the camera was connected but nothing showed up in ROS 2. [Full story](challenges.md#10-getting-the-camera-onto-ros-2) Later it also lagged, which is why the settings above are so low. [Full story](challenges.md#13-camera-lag-and-late-reactions)

## 6. Lidar integration

**What we did:** launched the TortoiseBot bring-up file on the Pi, then adjusted the RViz2 settings until the scan displayed correctly.

```bash
ros2 launch tortoisebot_bringup autobringup.launch.py use_sim_time:=False exploration:=True slam_only:=True
```

`use_sim_time:=False` means it runs on the real robot, and `slam_only:=True` starts only the sensors and mapping, without the full navigation stack.

## 7. Running our code on the robot

**What we did:** with everything checked, we ran our code on the robot.

**Video:** coming soon
