Engineering materials
====

This repository contains engineering materials of a self-driven vehicle's model


## INTRODUCTION

We are Team D3 Builders from the Robotronics Club of Ahmedabad. Being part of this club gives us the chance to really explore robotics, coding, and engineering in a hands-on way. With the support of our mentors, teachers, and a well-equipped lab, we get to turn our ideas into actual working robots. Each of us brings in different strengths—whether it’s designing, programming, or problem-solving—and together we make a strong team. Building this robot for the WRO competition has been an amazing experience where we’ve learned a lot, challenged ourselves, and grown as innovators.

## CONTENT

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` is for the files for models used by 3D printers, laser cutting machines and CNC machines to produce the vehicle elements. If there is nothing to add to this location, the directory can be removed.

## ABOUT THE TEAM

### Deyaan Agrawal – Grade 12
Deyaan is our team leader and the one handling all the software for the robot. He loves Legos, which made him suggest building a chassis that we could easily change or adjust—something really helpful since this was our first WRO competition. He writes the code that controls the robot, programs the sensors, and makes sure it can react quickly to obstacles. He’s always testing and improving the robot so it moves smoothly and does exactly what it’s supposed to. Deyaan also keeps the team organized and focused, making sure everyone stays on track while building the robot.

### Darsh Zaveri – Grade 10
Darsh handles the GitHub repository and project journaling, keeping track of every idea, test, and change the team makes. This way, nothing gets lost, and the team can always look back to see what worked and what didn’t. Darsh also makes sure all progress is documented properly so that it’s easy to explain the work to mentors or judges. His efforts help the team stay organized and make sure the project runs smoothly.

### Dhruv Patel – Grade 11
Dhruv is in charge of the hardware. He makes sure the chassis is strong, the motors are mounted properly, and the sensors are in the right positions. He keeps testing and adjusting the mechanical parts so the robot can turn sharply, move steadily, and complete the course without problems. His focus on details makes sure that the robot is not only smart on the inside but also tough and reliable on the outside.

Together, as Team D3 Builders, the team brings skills in software, organization, and hardware together. They work as a team, solve problems collaboratively, and make sure the robot can handle anything the competition throws at it.



## ELECTRONIC COMPONENTS

Lego Technic Chassis – modular and adjustable base for the robot

Raspberry Pi 4 Model B – main processor for sensors, camera, and navigation

Pi Camera 3 – captures live images and video for obstacle detection and line tracking

TB6612FNG Motor Driver – controls the DC motors, receives PWM signals from the Raspberry Pi

DC Motors – provide the driving force for the robot

Servo Motor – controls steering on the front axle

VL53L1X Distance Sensors – mounted on sides and front for wall-following and obstacle detection

3.7V 18650 Li-ion Batteries – power source for motors, sensors, and Raspberry Pi

Jumper Wires – for power and communication between components

Lego Beams and Mounting Accessories – used to secure all components on the chassis


Our robot uses carefully chosen components to make it precise, reliable, and capable of completing the WRO course efficiently. The main chassis is a Lego Technic base, which is strong, modular, and easy to modify, allowing us to adjust the design as needed during testing. The movement of the robot is powered by two DC motors, controlled by a TB6612FNG motor driver. These motors provide smooth and precise motion, while the motor driver allows the Raspberry Pi to adjust speed and direction using PWM signals.

For steering, we use a servo motor mounted on the front axle, giving the robot accurate and responsive turning ability. To detect walls and obstacles, we installed VL53L1X distance sensors, with two on the sides for wall-following and one at the front to measure distances to obstacles ahead. These sensors communicate with the Raspberry Pi through I2C, providing real-time distance data for navigation.

The robot’s brain is a Raspberry Pi 4 Model B, which processes sensor data, runs the obstacle detection program, and handles image processing from the Pi Camera 3. The camera captures live images of the course, detects colored blocks, and tracks lines, allowing the robot to make intelligent navigation decisions. All of these components are powered by 3.7V 18650 Li-ion batteries, providing enough energy for multiple rounds of the competition. A voltage regulator ensures that the Raspberry Pi receives stable and safe power while the motors and sensors draw from the same battery source.

Together, these components create a reliable, efficient, and autonomous robot capable of performing complex navigation and obstacle avoidance tasks in real time. Each part was selected and positioned carefully to work in harmony, ensuring smooth performance during the competition.

