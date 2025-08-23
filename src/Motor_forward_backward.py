from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep

# Motor direction pins (AIN1 and AIN2)
ain1 = OutputDevice(23)  # Forward
ain2 = OutputDevice(24)  # Backward

# Enable pin (PWMA) as PWM
enable = PWMOutputDevice(18)

# Standby pin (STBY) — must be HIGH to enable motor
stby = OutputDevice(25)
stby.on()  # Wake up the motor driver

def motor_forward(speed=1.0):
    ain1.on()
    ain2.off()
    enable.value = speed

def motor_backward(speed=1.0):
    ain1.off()
    ain2.on()
    enable.value = speed

def motor_stop():
    ain1.off()
    ain2.off()
    enable.value = 0

# Run the motor: Forward → Backward → Stop
motor_forward(1)   # 80% speed forward
sleep(2)

motor_backward(1)  # 60% speed backward
sleep(2)

motor_stop()


