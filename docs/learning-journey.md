# Learning Journey

My path from Python basics to a working vision-pursuit robot, in the order I learned it.

## 1. Python OOP 
**What I learned:** classes, objects, data members, methods, encapsulation, inheritance, polymorphism.

**What I built:** a Student class that grew step by step.

**Code:** [src/01_python_oops](../src/01_python_oops)

## 2. ROS 2 fundamentals
**What I learned:** how to build a package, create a node and run it with ROS2 commands.

**Code:** [my_first_node.py](../src/02_turtlesim/my_first_node.py)

## 3. Topics, publishers and subscribers
**What I learned:** how nodes talk to each other through topics.

**What I built:** a publisher and a subscriber.

**Code:** [pose_subscriber.py](../src/02_turtlesim/pose_subscriber.py)

## 4. Turtlesim
**What I built:** nodes where the turtle draws different paths, avoids the boundary of the window, moves towards a goal and one turtle following another.

**Code:** [src/02_turtlesim](../src/02_turtlesim)

**Challenges:** 
- How to use the Twist datatype.
- Preventing the turtle from oscillating once it reached its goal.
- Calculating how much angular velocity to be given so it turns to the right angle.
- Implementing PID

## 5. Finite State Machine (FSM)
**What I learned:** structuring behaviour as states and transitions.

**What I built:** a simple FSM in turtlesim.

**Code:** [state_machine.py](../src/02_turtlesim/state_machine.py)

**Challenges:**
- Switching between states

## 6. Gazebo and RViz2
**What I learned:** running a robot in simulation, creating worlds and visualizing its data.

## 7. Color detector and obstacle avoider
**What I built:** a color detector and an obstacle detector, tested in simulation.

**Code:** [src/03_simulation](../src/03_simulation)

**Challenges:**
- Fine tuning the values for obstacle detection

## 8. Vision pursuit robot
**What I built:** a full FSM combining the color detector and the obstacle avoider so the robot finds, chases and avoids.

**Code:** coming soon

**Video:** coming soon
