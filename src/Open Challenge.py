# Team = Deyaan, Darsh, Dhruv
# First Full Open Challenge Code for WRO2025 FE Date: 01/08/2025
# It used Gyro Straight in Starting Section, then stop before first corner and decide turning direction
# -and accorading truning direction its start left or right wall following
# it increment turning counter on each corner and after 12(3 Laps) corner it stop robot in starting section.
# Servo is connected directly with GPIO13
# 1908 = Servo Changed to GPIO

import RPi.GPIO as GPIO
from gpiozero import OutputDevice, PWMOutputDevice, Servo
import time
import statistics
import board
import busio
import smbus2
import adafruit_vl53l1x
import adafruit_bno055
#from adafruit_pca9685 import PCA9685

# === Motor Pins ===
PWMA = 18
AIN1 = 23
AIN2 = 24
STBY = 25

# Servo Pin
# SERVO_PIN = 13
steering = Servo(13)  # Range: -1 (left) to 1 (right)


# TCA9548A Config
TCA_ADDRESS = 0x70
BNO055_CHANNEL = 3
LEFT_CHANNEL = 0
CENTER_CHANNEL = 1
RIGHT_CHANNEL = 2

# Servo angle limits
STEERING_CENTER = 81
SERVO_DEVIATION_LIMIT = 25
SERVO_MAX_RIGHT = STEERING_CENTER + SERVO_DEVIATION_LIMIT		# 90+30 
SERVO_MAX_LEFT = STEERING_CENTER - SERVO_DEVIATION_LIMIT		# 90-30
last_servo_angle = STEERING_CENTER  # to track previous angle
MAX_SERVO_STEP = 5  # max change in angle per update (degrees)


# PID Configuration
TARGET_DISTANCE = 23   # Initial 0 cm
TOLERANCE = 3      # cm
KP = 1.0 
KI = 0.0
KD = 0.0


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([PWMA, AIN1, AIN2, STBY], GPIO.OUT)

motor_pwm = GPIO.PWM(PWMA, 1000)
motor_pwm.start(0)
#servo_pwm = GPIO.PWM(SERVO_PIN, 50)
#servo_pwm.start(0)


# === Basic Functions ===
def standby(on):
    GPIO.output(STBY, GPIO.HIGH if on else GPIO.LOW)

def forward(speed_percent):
    standby(True)
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    motor_pwm.ChangeDutyCycle(speed_percent)

def stop():
    standby(False)
    motor_pwm.ChangeDutyCycle(0)
    
def set_servo_angle(angle):
    
    angle = max(0, min(180, angle))
    angle = max(STEERING_CENTER - SERVO_DEVIATION_LIMIT, min(STEERING_CENTER + SERVO_DEVIATION_LIMIT, angle))
    
    servo_val = (angle - STEERING_CENTER) / SERVO_DEVIATION_LIMIT      # map to -1 to +1
    steering.value = servo_val
    
    #duty = 2.5 + (angle / 18)
    #servo_pwm.ChangeDutyCycle(duty)
    #time.sleep(0.04)
    #servo_pwm.ChangeDutyCycle(0)

def select_tca_channel(channel):
    with smbus2.SMBus(1) as tca:
        tca.write_byte(TCA_ADDRESS, 1 << channel)
    time.sleep(0.1)

# === Sensor Initialization ===
def init_vl53l1x(channel):
    select_tca_channel(channel)
    i2c = board.I2C()
    sensor = adafruit_vl53l1x.VL53L1X(i2c)
    sensor.distance_mode = 2			# 1=short, 2=medium 3=long
    sensor.timing_budget = 100			# greater timing budget means more accurate reading (100-500)
    sensor.start_ranging()
    return sensor

def init_bno055():
    select_tca_channel(BNO055_CHANNEL)
    i2c = board.I2C()
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    time.sleep(1)
    return sensor

# === Sensor Reading ===
def get_distance(sensor, channel):
    select_tca_channel(channel)
    time.sleep(0.05)
    if sensor.data_ready:
        distance = sensor.distance
        sensor.clear_interrupt()
        if distance is not None:
            return distance
    return None

def get_heading(imu_sensor):
    select_tca_channel(BNO055_CHANNEL)
    time.sleep(0.04)
    euler_data = imu_sensor.euler
    if euler_data is not None and euler_data[0] is not None:
        return round(euler_data[0])
    return None

def decide_target_heading(turn_number, turn_direction):
    """
    Returns the target heading based on turn number (t) and turn direction ("left" or "right").
    """

    if turn_direction == "right":
        if turn_number in (1, 5, 9):
            return 0
        elif turn_number in (2, 6, 10):
            return 90
        elif turn_number in (3, 7, 11):
            return 180
        elif turn_number in (4, 8, 12):
            return 270

    elif turn_direction == "left":
        if turn_number in (1, 5, 9):
            return 360
        elif turn_number in (2, 6, 10):
            return 270
        elif turn_number in (3, 7, 11):
            return 180
        elif turn_number in (4, 8, 12):
            return 90

    return None  # In case of invalid input

def perform_forward_turn_to_heading(direction, target_heading, motor_speed=95):
    """
    Forward turn until the IMU heading reaches the given target heading.
    direction: "left" or "right"
    target_heading: target compass heading (0–360)
    """
    if direction == "right":
        set_servo_angle(SERVO_MAX_RIGHT)
        target_heading = (target_heading + 95) % 360
    else:
        set_servo_angle(SERVO_MAX_LEFT)
        target_heading = (target_heading - 95) % 360

    time.sleep(0.05)
    print(f"**Forward Turning {direction.upper()}... Target: {target_heading}°")
    forward(motor_speed)

    while True:
        current_heading = get_heading(imu_sensor)
        if current_heading is None:
            continue

        # Calculate signed heading difference (-180 to 180)
        diff = (current_heading - target_heading + 540) % 360 - 180
        print(f"Forward Turning {direction.upper()}... Heading: {current_heading:.1f}°, "
              f"Target: {target_heading}°, Δ: {diff:.1f}°", end="\r")

        # Stop condition based on direction
        if (direction == "right" and diff >= 0) or \
           (direction == "left" and diff <= 0):
            break

        time.sleep(0.02)

    stop()
    set_servo_angle(STEERING_CENTER)
    print(f"\n✅ Forward {direction.capitalize()} turn complete. Final heading: {current_heading:.1f}°")

#Turn the robot by specified degrees either left or right from current heading.
def turn_to_heading(current_heading, turn_direction, degrees=90, speed=95):
    
    if turn_direction == "right":
        target = (current_heading + degrees) % 360
    else:
        target = (current_heading - degrees + 360) % 360

    print(f"@ Turning {turn_direction.upper()} to {target}°.........")

    # Set turn direction using servo steering
    turn_angle = STEERING_CENTER + SERVO_DEVIATION_LIMIT if turn_direction == "right" else STEERING_CENTER - SERVO_DEVIATION_LIMIT
    set_servo_angle(turn_angle)
    forward(speed)

    while True:
        heading = get_heading(imu_sensor)
        if heading is None:
            continue

        #error = (heading - target + 180) % 360 - 180
        error = (heading - target + 540) % 360 - 180  # gives range [-180, +180]
        print(f"Turning... Heading: {heading}°, Target: {target}°, Error: {error}°")
        if (turn_direction == "left" and error < 0) or \
           (turn_direction == "right" and error > 0):
            break
        #if abs(error) < 5:
        #    break
        time.sleep(0.05)

    stop()
    set_servo_angle(STEERING_CENTER)
    print(f"✅ Turn complete. Current Heading: {heading}°")
    time.sleep(0.05)

def wait_for_distance(sensor, channel, label, resume_speed=95, max_wait=2):
    
    value = get_distance(sensor, channel)
    
    if value is None:
        stop()
        print(f"⚠️ {label} sensor read failed. Waiting...")

        start_time = time.time()
        while value is None:
            value = get_distance(sensor, channel)
            if time.time() - start_time > max_wait:
                print(f"❌ {label} sensor timeout after {max_wait}s — resuming anyway.")
                value = 150.0
                break
            time.sleep(0.03)

        if value is not None:
            print(f"✅ {label} sensor recovered: {value:.2f} cm")

    forward(resume_speed)
    #time.sleep(0.05)
    return value

def wait_for_heading(sensor, label="Heading", resume_speed=95):
    """Read heading from IMU, stop if None, wait until valid, then resume."""
    value = get_heading(sensor)
    if value is None:
        stop()
        print(f"⚠️ {label} read failed. Waiting...")
        while value is None:
            value = get_heading(sensor)
            time.sleep(0.03)
        print(f"✅ {label} recovered: {value}°")
    forward(resume_speed)
    #time.sleep(0.05)
    return value

    
# === Main Execution ===
if __name__ == '__main__':
    try:
        time.sleep(5)
        left_sensor = init_vl53l1x(LEFT_CHANNEL)
        time.sleep(0.1)
        center_sensor = init_vl53l1x(CENTER_CHANNEL)
        time.sleep(0.1)
        right_sensor = init_vl53l1x(RIGHT_CHANNEL)
        time.sleep(0.1)
        imu_sensor = init_bno055()
        #imu_sensor.mode = 0x08
        time.sleep(0.5)
        print("✅ Left, Rigth, Center and BNO55 are ready")

        base_heading = get_heading(imu_sensor)
        print(f"✅ Initial Heading: {base_heading}°")

        # Go straight until left or right distance > 120
        startsection = True
        turnDir = None
        turnCount = 1			# We are updating it form Trun 2
        loop_start = 0
        loop_end = 0
        last_print_time = 0
        FRONT_DISTANCE = 80			# Front Wall Distance required before trun in cm
        DC_Speed = 95				# DC Motor Speed
        set_servo_angle(STEERING_CENTER)
        forward(DC_Speed)  # Set desired speed
        
        while True:
            loop_start = time.time()
            # === Read Center Sensor ===
            distanceC = wait_for_distance(center_sensor, CENTER_CHANNEL, "Center")
        
            print(f"Center: {distanceC:.2f} cm")
            #print(f"H: {heading}°, L: {distanceL:.2f}, R: {distanceR:.2f}, C: {distanceC:.2f}, Loop time: {1000 * (loop_end - loop_start):.1f} ms")
            '''
            current_time = time.time()
            if current_time - last_print_time > 0.5:  # print every 300 ms
                print(f"H: {heading}°, L: {distanceL:.2f}, R: {distanceR:.2f}, C: {distanceC:.2f}, Loop time: {1000 * (loop_end - loop_start):.1f} ms")
                last_print_time = current_time
            '''
            #print(f"Heading: {heading}°, Left: {distanceL:.2f} cm, Center: {distanceC:.2f} cm, Right: {distanceR:.2f} cm")
            
            if distanceC > FRONT_DISTANCE:
                if startsection is True:
                    heading   = wait_for_heading(imu_sensor)
                    gerror = (heading - base_heading + 180) % 360 - 180
                    gcorrection = int(gerror * 2.0 )
                    target_angle = STEERING_CENTER - gcorrection
                    set_servo_angle(target_angle)
                    print(f"Heading: {heading}°, TargetAngle: {target_angle}°, Center: {distanceC:.2f} cm")
                    #print(f"TargetAngle: {target_angle}°")
                
                else:
                    if turnDir == "right":
                        distanceL = wait_for_distance(left_sensor, LEFT_CHANNEL, "Left")
                        error = TARGET_DISTANCE - distanceL
                        #print(f"Left Wall: {distanceL:.2f} cm")
                    
                    elif turnDir == "left":
                        distanceR = wait_for_distance(right_sensor, RIGHT_CHANNEL, "Right")
                        error = distanceR - TARGET_DISTANCE
                        #print(f"Right Wall: {distanceR:.2f} cm")
                        
                    correction = int(error * 4)
                    target_angle = STEERING_CENTER + correction
                    set_servo_angle(target_angle)
                    #print(f"TargetAngle: {target_angle}°")
                    
        
            elif distanceC < FRONT_DISTANCE:
                if startsection is True:
                    distanceL = wait_for_distance(left_sensor, LEFT_CHANNEL, "Left")
                    distanceR = wait_for_distance(right_sensor, RIGHT_CHANNEL, "Right")
                    if distanceL > 120:
                        turnDir = "left"
                        print("✅ Stop: Left is open. Turn direction = LEFT")
                        heading   = wait_for_heading(imu_sensor)
                        target_heading = decide_target_heading(turnCount, turnDir)
                        perform_forward_turn_to_heading(turnDir, target_heading, motor_speed=95)
                        #turn_to_heading(heading, "left", degrees=90)
                        distanceR = wait_for_distance(right_sensor, RIGHT_CHANNEL, "Right", 0)
                        TARGET_DISTANCE = distanceR
                        TARGET_DISTANCE = max(15, min(distanceR, 30))
                        
                    
                    elif distanceR > 120:
                        turnDir = "right"
                        print("✅ Stop: Right is open. Turn direction = RIGHT")
                        heading   = wait_for_heading(imu_sensor)
                        target_heading = decide_target_heading(turnCount, turnDir)
                        perform_forward_turn_to_heading(turnDir, target_heading, motor_speed=95)
                        #turn_to_heading(heading, "right", degrees=90)
                        distanceL = wait_for_distance(left_sensor, LEFT_CHANNEL, "Left",  0)
                        TARGET_DISTANCE = distanceL
                        TARGET_DISTANCE = max(15, min(distanceL, 30))
                        
                    
                    startsection = False
                    print(" Starting Section Complete...!")
                    #stop()
                    #time.sleep(5)
                    forward(DC_Speed)
                
                else:
                    if turnCount >= 12:
                        print("12 Turns Complete! Driving straight with gyro for 2s...")
                        set_servo_angle(STEERING_CENTER)
                        forward(DC_Speed)

                        start_time = time.time()
                        while time.time() - start_time < 2.0:
                            heading = wait_for_heading(imu_sensor)
                            gerror = (heading - base_heading + 180) % 360 - 180
                            gcorrection = int(gerror * 1.5)
                            target_angle = STEERING_CENTER - gcorrection
                            set_servo_angle(target_angle)
                            time.sleep(0.01)

                        stop()
                        print("✅ Robot stopped after final straight")
                        break  # exit the loop

                    # Perform the turn and increment the counter
                    if turnDir == "left":
                        print("Normal Turn Left")
                        heading   = wait_for_heading(imu_sensor)
                        target_heading = decide_target_heading(turnCount, turnDir)
                        perform_forward_turn_to_heading(turnDir, target_heading, motor_speed=95)
                        #turn_to_heading(heading, "left", degrees=90)
                        distanceR = wait_for_distance(right_sensor, RIGHT_CHANNEL, "Right", 0)
                        TARGET_DISTANCE = distanceR
                        TARGET_DISTANCE = max(18, min(distanceR, 23))
                        
                    elif turnDir == "right":
                        print ("Normal Turn Right")
                        heading   = wait_for_heading(imu_sensor)
                        target_heading = decide_target_heading(turnCount, turnDir)
                        perform_forward_turn_to_heading(turnDir, target_heading, motor_speed=95)
                        #turn_to_heading(heading, "right", degrees=90)
                        distanceL = wait_for_distance(left_sensor, LEFT_CHANNEL, "Left", 0)
                        TARGET_DISTANCE = distanceL
                        TARGET_DISTANCE = max(18, min(distanceL, 23))

                    turnCount += 1
                    print(f"Turn #{turnCount} complete")

            time.sleep(0.01)
            loop_end = time.time()
            #print(f"Loop time: {1000 * (loop_end - loop_start):.1f} ms")

    except KeyboardInterrupt:
        print("🛑 Interrupted by user")

    finally:
        print("🔻 Stopping motor and cleaning up GPIO")
        stop()
        #servo_pwm.ChangeDutyCycle(0)
        motor_pwm.ChangeDutyCycle(0)
        time.sleep(0.5)
        GPIO.cleanup()
