from gpiozero import Servo
from time import sleep

# Use GPIO13 (hardware PWM)
# Adjust pulse widths for typical servos
servo = Servo(13, min_pulse_width=0.00011, max_pulse_width=0.0029)

# Converts angle (0–180) to servo.value (-1 to 1)
def angle_to_value(angle):
    if angle < 80 or angle > 110:
        raise ValueError("Angle must be between 70 and 110")
    return (angle - 90) / 90

try:
    while True:
        user_input = input("Enter angle (70-110) or 'exit': ")
        if user_input.lower() == 'exit':
            break
        try:
            angle = int(user_input)
            value = angle_to_value(angle)
            servo.value = value
            print(f"Moving to {angle}° (servo.value = {value:.2f})")
            sleep(3)
        except ValueError as e:
            print("Invalid angle. Please enter a number between 70 and 110.")

except KeyboardInterrupt:
    print("\nStopped by user.")
