import numpy as np
import RPi.GPIO as GPIO
from src import motor as motor_module
import time

if __name__ == '__main__':

    motor1 = motor_module.Motor({
        "pins": {
            "speed": 23,
            "control1": 23,
            "control2": 24
        }
    })

    speeds = list(np.linspace(0, 10, 11)) + list(np.linspace(0.9, 0, 10))
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(16, GPIO.LOW)
    

