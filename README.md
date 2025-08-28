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


## ELECTRICAL PROCESSES

## Power Distribution

The entire robot runs on two 18650 Li-ion batteries rated at 3.7V each. These batteries were chosen because they are lightweight but provide enough current for the Raspberry Pi, motors, and sensors. I positioned the batteries at the bottom of the chassis so the weight was evenly balanced and the robot would not tip over when moving. Since I did not use a voltage regulator, I had to carefully check that each component received the correct voltage directly from the batteries. The Raspberry Pi and motor driver were both connected in a way that avoided unnecessary power loss. I also kept the jumper wires as short as possible so that less energy was wasted in transmission.

## Signal Flow

The Raspberry Pi 4 acted as the brain of the system. It collected input data from the Pi Camera and the VL53L1X distance sensor, then processed it to make decisions about movement. After processing, the Pi sent electrical signals to the TB6612FNG motor driver and the servo motor. The distance sensor communicated with the Pi using the I²C protocol, which is like a two-wire digital conversation system where one wire carries data and the other synchronizes it. The motors and the servo, on the other hand, were controlled using PWM (Pulse Width Modulation) signals. By changing how long each pulse stayed high or low, I could adjust the motor speed or the servo’s turning angle very precisely.

## Motor Control

The TB6612FNG motor driver was a key part of the robot’s electrical system. The Raspberry Pi’s GPIO pins cannot supply enough current to drive motors directly, so the motor driver acted as an amplifier. It took the weak control signals from the Raspberry Pi and boosted them into stronger currents that could actually power the DC motors. By using PWM signals, I could smoothly vary the speed of the wheels, make the robot accelerate or decelerate, and even bring it to a controlled stop instead of a sudden halt. This made the robot’s motion look much more natural and car-like.

## Sensor Connections

The VL53L1X distance sensor was connected to the Raspberry Pi through the SDA and SCL pins that handle I²C communication. This sensor allowed the robot to measure how far away obstacles were and react before collisions happened. The Pi Camera 3 was connected through a flat ribbon cable to the dedicated CSI port on the Raspberry Pi. Together, the camera and the distance sensor gave the robot both vision and depth awareness. Both sensors were powered by the same battery source, so it was important that all ground pins were connected properly. Without a common ground, the signals could become unstable or unreliable.

## Safety and Reliability

Because no voltage regulator was used in this setup, I had to make sure the components were always operating within safe voltage limits. To do this, I ensured that the jumper wires were firmly connected so they would not loosen during movement. I also avoided long or tangled wiring to reduce resistance and power drops. The 18650 Li-ion batteries provided enough current so that even if the motors drew more power during acceleration, the Raspberry Pi did not shut down or restart unexpectedly. This stability was very important because a sudden restart could stop the robot in the middle of a test.

## Step-by-Step Assembly

The electrical connections were assembled in stages to avoid mistakes. First, I connected the motor driver to the DC motors and tested simple forward and backward movement using basic code. Once this was working, I added the servo motor for steering and wrote small test programs to check the turning angles. After confirming the steering worked, I connected the VL53L1X distance sensor and tested distance readings. Then I installed the Pi Camera with the ribbon cable and ensured that the Raspberry Pi detected it correctly. Finally, I connected the power supply through the batteries and tested the full system together. This step-by-step approach made it easier to identify wiring errors and fix them early instead of troubleshooting everything at once.




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

## MOBILITY MANAGEMENT
### Core Design

The entire mobility system of our robot was built around a car-like steering model instead of the usual skid steering used in many robots. We felt this approach gave our design a more realistic feel and also smoother turns on the WRO field. The main chassis was built with Lego Technic beams, which made it both lightweight and modular. Since we were new to WRO, the Lego-based frame gave us flexibility—whenever we faced problems, we could rebuild or adjust sections quickly. For propulsion, we used two DC motors at the rear, connected through the TB6612FNG motor driver. The rear wheels provided the driving force, while the front wheels were mounted on a servo-controlled axle for steering. This separation of driving and steering made the robot more predictable and stable, especially during alignment tasks and when taking curves.

### Sensor Placement and Functionality

For the robot to navigate and react to its surroundings, we placed sensors carefully in positions where they could give the most useful data. The Pi Camera 3 was mounted in the front so it could detect lines and capture what lay ahead of the robot. This camera acted as the main “eye” of the system. Alongside it, the VL53L1X time-of-flight distance sensor was positioned to detect obstacles and walls in close range. To strengthen navigation, we also experimented with placing VL53L1X sensors on the sides so the robot could measure distances from boundaries and adjust its course accordingly. This combination allowed the robot to stay in its lane, avoid crashing, and follow the intended path on the field. Each sensor was chosen not only for accuracy but also for speed, since in competitions the robot has to make decisions within fractions of a second.

### Steering Mechanism

The steering mechanism was one of the most important parts of the robot. Instead of using skid steering where two motors drive opposite sides, we relied on a front-mounted servo motor that physically turned the wheels left and right. This gave the robot car-like steering, which is both smoother and easier to control in narrow spaces. The servo was calibrated so that even small movements in angle created noticeable turns, but without making the robot unstable. This precision made it possible to take clean curves and align accurately with objects on the field. At the same time, the rear DC motors were synced with the steering commands so the robot would always maintain a balance between speed and turning. The biggest advantage of this setup was stability—unlike skid steering, our robot didn’t “drag” wheels while turning, which reduced friction and saved power.

### Power Supply

To power the whole robot, we decided to use 3.7V 18650 Li-ion batteries. These batteries were reliable, rechargeable, and light enough not to weigh the robot down. Since the Raspberry Pi 4 Model B, motors, and sensors all needed stable power, we had to plan the wiring carefully. The Pi was the most sensitive part, as it required consistent current and voltage. To make sure it didn’t drop power mid-run, we balanced the load so that the motors and servo didn’t interfere with it. The batteries were wired using jumper wires, which kept the connections neat and easy to manage. Even though we didn’t use a voltage regulator, the system performed well because of proper distribution and placement of batteries. One of the key things we learned here was how important battery stability is for a robot—without reliable power, even the best code or hardware won’t run properly.

### Assembly Instructions

The assembly of the mobility system was done step by step to make sure everything aligned properly. First, the Lego beams were arranged to form a stable rectangular base. The Raspberry Pi was mounted in the center to act as the brain of the system and to keep the weight balanced. Next, the motor driver was fixed near the rear motors so the connections would be short and reduce energy loss. The servo was attached to the front axle to control steering directly, and the front wheels were secured tightly to respond to even small servo movements. The Pi Camera was positioned at the front with a clear view of the track, while the VL53L1X sensors were placed at the front and sides for maximum coverage. Finally, the Li-ion batteries were secured at the bottom of the chassis to keep the center of gravity low, which reduced wobbling when the robot moved at higher speeds. All components were connected using jumper wires, which gave us the flexibility to make changes quickly if needed.


## POWER AND SENSE MANAGEMENT
Power and sensors are like the brain and heart of our robot. Without stable power, the robot cannot even switch on, and without sensors, it cannot “see” or “feel” the world around it. In this part, I will explain how we managed the sensors, how the robot takes its readings, how it follows the path till the end, and how we wired everything together so that it works smoothly.


### Sense Management

Our robot uses three VL53L1X distance sensors and one Pi Camera 3. These sensors are very special because they work with laser light to measure how far an object is. They are small but very powerful and give accurate results in just milliseconds. Two of these sensors were placed on the sides of the robot. They keep track of the distance from the walls so that the robot can travel in a straight line without crashing. The third sensor was placed at the front and worked like a guard, warning the robot if something came in its way.

The Pi Camera 3 was another very important part. While the sensors could only measure distances, the camera could actually recognize colors. This helped the robot understand instructions like “turn left at green” or “turn right at red.” By combining both distance sensors and the camera, the robot became much smarter because it could sense both objects and colors around it.

### Initial Readings and Wall Following

Before starting its journey, the robot first takes initial readings of the walls using the side sensors. These readings act like a reference point. As the robot moves forward, it keeps checking the distance again and again. If the left sensor suddenly shows a bigger gap, the robot knows the wall has ended and it might be time to turn left. If the right sensor shows the same, then it’s a right turn.

The front sensor makes sure that the robot does not bump into a wall or an obstacle. If something is too close, it either slows the motors or stops them until it figures out a new path. This constant checking of distances is called wall following, and it is one of the main ways the robot manages to stay on track.

### Final Stage and Path Completion

When the robot goes deeper into the course, just depending on walls is not enough. This is where the Pi Camera comes in. Red and green blocks were placed on the course, and the camera had to recognize them. A red block meant turning right, and a green block meant turning left. This made the robot not only depend on walls but also follow “traffic signals” on the path.

Towards the end of the run, both the camera and sensors work together. The sensors keep the robot safe from walls, and the camera makes sure it doesn’t miss the colored signals. This teamwork between sensors and camera helped the robot complete the path successfully.

### Wiring and Sensor Integration

To make all these parts work together, the wiring had to be done very carefully. The three VL53L1X sensors were connected to the Raspberry Pi 4 using the I²C pins, which are special pins that allow the Pi to talk to sensors quickly. The Pi Camera was connected through the CSI camera port on the Pi.

We used jumper wires for all the connections because they are reliable and can be easily adjusted if something goes wrong. While wiring, we made sure that no two wires got mixed up and that all sensors were properly powered. Each sensor was tested separately before combining them. After all the wiring and integration, the sensors and camera worked together as one system, allowing the robot to sense its surroundings, make decisions, and move correctly.

## Video Link

https://youtu.be/Mi98GMMxlPI


