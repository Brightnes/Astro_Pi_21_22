from sense_hat import SenseHat
from gpiozero import MotionSensor # Comment out if I do not use  PIR
from pathlib import Path

# Variables definitions and settings
envir_light=0
moving_creatures_nearby=0

# Function definitions

def brightness_check():
    sense.color.gain = 16
light = sense.color.clear
if light < 64:
     # Dark
     envir_light==0
else:
    # Light
    envir_light==1

# Object names definitions
sense = SenseHat()


def grab_movement():
    # Inititating motion detection
    pir = MotionSensor(pin=12)
    pir.wait_for_motion()
    moving_creatures_nearby==1
    pir.wait_for_no_motion()


# Program main setup stuff

base_folder = Path(__file__).parent.resolve()
