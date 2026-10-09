# Challenges and Fixes

The problems I ran into while building this project, what I tried, and what I learned. They are listed in the order I met them, from turtlesim to the real robot.

**Software**
1. [Controlling turns with Twist](#1-controlling-turns-with-twist)
2. [Turtle oscillating at the goal](#2-turtle-oscillating-at-the-goal)
3. [Turning to the right angle](#3-turning-to-the-right-angle)
4. [Implementing PID](#4-implementing-pid)
5. [Switching between FSM states](#5-switching-between-fsm-states)
6. [Finding the centroid of a color](#6-finding-the-centroid-of-a-color)
7. [Obstacle avoider: bumping into things](#7-obstacle-avoider-bumping-into-things)
8. [Obstacle avoider: oscillating at walls](#8-obstacle-avoider-oscillating-at-walls)
9. [Obstacle avoider: speeds](#9-obstacle-avoider-speeds)

**Hardware**

10. [Getting the camera onto ROS 2](#10-getting-the-camera-onto-ros-2)
11. [Motors not getting enough power](#11-motors-not-getting-enough-power)
12. [Raspberry Pi turning on and off](#12-raspberry-pi-turning-on-and-off)
13. [Camera lag and late reactions](#13-camera-lag-and-late-reactions)

---

## 1. Controlling turns with Twist

**Problem:** I needed the turtle to turn exactly 90 degrees, but it kept spinning off in some other direction. I had no idea how to pick the right values.

**What I tried:** a lot of trial and error with different values, until I started to see a pattern.

**Fix:** I realised a Twist value is a speed, not a distance. The value I gave is how fast the turtle moves per second, so it keeps turning for as long as the message keeps being published. The angle only comes out right when speed and time are controlled together.

**Lesson:** Twist describes *how fast*, not *how much*. To reach an exact angle, I have to control the duration or use feedback.

## 2. Turtle oscillating at the goal

**Problem:** the turtle reached the goal and then kept swinging left and right instead of stopping.

**What I tried:** I suspected my angle error calculation was wrong and checked it.

**Fix:** the tolerance was too small. The turtle could never get inside such a tight limit, so it kept correcting forever. I widened the tolerance to suit what the simulator can actually achieve.

**Lesson:** a tolerance has to match what the system can realistically do. Too tight and the robot never settles.

## 3. Turning to the right angle

**Problem:** the robot turned in random directions and I didn't know how to make it stop at the right one.

**What I tried:** guessing angular velocity values by hand.

**Fix:** I used an error estimate. The robot takes its current angle, calculates the angle it should face (from the goal point), and the difference is the error. It keeps turning at some speed until that error drops below a limit, then stops.

**Lesson:** rather than guessing how long to turn, measure the error and let it decide when to stop. This idea is what led me to PID.

## 4. Implementing PID

**Problem:** the proportional part was easy, but the derivative and integral parts were hard to turn into code.

**What I tried:** I studied how derivatives and integrals are calculated in code. The derivative is the change in error divided by the time step. The integral is the error added up over time.

**Fix:** I found that the integral can grow too large and make the robot badly overshoot its target. To prevent that, I limit it to a fixed range and clamp it to the nearest limit if it goes past. I also reset the integral and derivative to zero once the error is very small, because tiny errors can otherwise cause big, jumpy corrections.

**Lesson:** each term does a different job, and the real work is controlling them: limiting the integral, and knowing when to use each term.

## 5. Switching between FSM states

**Problem:** I didn't know how to decide when to move from one state to another. I tried flags and other conditions, and sometimes the robot just never entered a state.

**What I tried:** different conditions and flags for each transition.

**Fix:** I found the order of checks matters. Avoidance has to come before search. Otherwise, when the robot can't see the target it goes into search, ignores the obstacle in front of it, and crashes. Once I put priorities in place and placed my flags properly, the states switched correctly.

**Lesson:** states need priorities. Safety behaviours like avoidance must be checked first.

## 6. Finding the centroid of a color

**Problem:** I could detect the color, but finding the centre of the colored object was hard.

**What I tried:** working with the detected region directly.

**Fix:** I took the contour of the color mask and used image moments to calculate its centroid.

**Lesson:** OpenCV already has tools for this. Contours plus moments give a reliable centre point to steer toward.

## 7. Obstacle avoider: bumping into things

**Problem:** in simulation, the robot kept bumping into obstacles.

**What I tried:** checking the lidar readings against my avoidance logic.

**Fix:** my distance tolerance was too low, so the robot reacted too late. I raised it so it starts avoiding earlier.

**Lesson:** the avoidance distance needs a safety margin, because the robot needs room to react and turn.

## 8. Obstacle avoider: oscillating at walls

**Problem:** when the robot met a straight wall, it kept swinging back and forth instead of getting past it.

**What I tried:** looking at what the lidar could actually see at that moment.

**Fix:** the lidar range I was using was too small, so the robot could only see a narrow slice of the wall. Increasing the range gave it enough view to commit to one direction.

**Lesson:** if a robot seems indecisive, check whether its sensor is giving it enough information.

## 9. Obstacle avoider: speeds

**Problem:** even after the other fixes, the robot still crashed here and there. Either it turned too slowly or moved too fast.

**What I tried:** changing the turning speed and moving speed over and over.

**Fix:** trial and error until the two speeds balanced, with turns fast enough to clear obstacles and forward speed low enough to allow it.

**Lesson:** some values can't be calculated and have to be tuned by testing. Change one thing at a time.

## 10. Getting the camera onto ROS 2

**Problem:** the camera was connected to the robot, but there was no image data in ROS 2.

**What I tried:** checking the connection and looking for the topic.

**Fix:** the camera doesn't publish by itself. We had to run a command (`cam2image`) to start it publishing, then subscribe to that topic in our code.

**Lesson:** a connected sensor isn't a running sensor. A node has to publish the data before anything can subscribe to it.

## 11. Motors not getting enough power

**Problem:** the motors weren't getting enough power and didn't run properly.

**What I tried:** checking the setup and the code.

**Fix:** the battery adapter was supplying too little voltage. Changing it to a higher-voltage adapter fixed the problem.

**Lesson:** when the code is right but the motors are weak, check the power supply.

## 12. Raspberry Pi turning on and off

**Problem:** the Raspberry Pi kept turning on and off by itself.

**What I tried:** this took us a long time. We even replaced the motor driver, thinking it was the cause, but nothing changed.

**Fix:** we tested the USB cable with a multimeter and found that the wire simply wasn't working. Once we replaced it, the Pi stayed on.

**Lesson:** test the simple parts first (cables, USB, power) with a multimeter before replacing expensive ones. A broken cable can look exactly like a software or driver problem.

## 13. Camera lag and late reactions

**Problem:** the robot's camera feed was lagging, so it reacted late to commands. We couldn't tell whether the cause was the code, the network or the Raspberry Pi itself.

**What I tried:** we kept researching and testing each possibility one by one: the code, the network, and the Pi's load.

**Fix:** the Pi was overloaded. We made two changes:
- Reduced the weight of the lidar bring-up file so it used less of the Pi's resources.
- Lowered the resolution of the `cam2image` command so it sent smaller images.

After both changes the lag dropped and the robot responded on time.

**Lesson:** when a robot feels slow, the bottleneck can be the hardware's limits rather than the code. Reduce the load (resolution, heavy launch files) before blaming the logic.
