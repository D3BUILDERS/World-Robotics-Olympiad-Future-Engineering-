from gpiozero import OutputDevice, PWMOutputDevice, Servo
from time import sleep
import board
import busio
import adafruit_vl53l1x

# === Motor Pins (TB6612FNG) ===
ain1 = OutputDevice(23)       # AIN1 - Forward
ain2 = OutputDevice(24)       # AIN2 - Backward
enable = PWMOutputDevice(18)  # PWMA - Speed control
stby = OutputDevice(25)       # STBY - Enable driver

# === Servo on GPIO13 ===
steering = Servo(13)  # Range: -1 (left) to 1 (right)

# === I2C for TCA9548A and VL53L0X ===
def select_channel(i2c, channel):
    if 0 <= channel <= 7:
        i2c.writeto(0x70, bytes([1 << channel]))

i2c = busio.I2C(board.SCL, board.SDA)

def setup_sensor(channel):
    select_channel(i2c, channel)
    return adafruit_vl53l0x.VL53L0X(i2c)

right_sensor = setup_sensor(2)  # Right side sensor (clockwise)

# === Motor Control ===
def forward(speed=1.0):
    stby.on()       # Enable TB6612FNG
    ain1.on()
    ain2.off()
    enable.value = speed

def stop():
    ain1.off()
    ain2.off()
    enable.value = 0
    stby.off()

# === Servo Angle Control (60–120 deg) ===
def set_servo_angle(degree):
    degree = max(60, min(120, degree))  # clamp
    servo_val = (degree - 90) / 30      # map to -1 to +1
    steering.value = servo_val

# === PID Settings ===
Kp = 0.1
ideal_distance = 275  # mm from wall

# === Main Loop ===
try:
    while True:
        select_channel(i2c, 2)  # RIGHT sensor
        distance = right_sensor.range
        error = distance - ideal_distance  # +ve = too far from wall

        correction = Kp * error
        new_angle = 90 + correction  # Right wall: ADD correction to turn toward wall

        set_servo_angle(new_angle)

        print(f"Right: {distance} mm | Error: {error:.2f} | Servo: {new_angle:.2f}°")

        forward(1.0)
        sleep(0.1)

except KeyboardInterrupt:
    stop()
    set_servo_angle()
    print("Stopped")
