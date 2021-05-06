# ------------------------------------------------------------------------------
# Name         : JetsonMotorInterface.py
# Date Created : 2/22/2021
# Author(s)    : Chris Lloyd, Micheal Caracciolo, Owen Casciotti
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : A class to control an Arduino microcontroller controlling two
#                stepper motors with individual (CDL=>Add Motor controller model
#                here) motor controller boards.
# ------------------------------------------------------------------------------

# External Imports
import RPi.GPIO as GPIO  # For interfacing with the Jetson GPIO
import time
import keyboard  # using module keyboard
import signal
import sys

# Jetson version (Change here for different boards)
JETSON_BOARD_NAME = "AGX"  # AGX or NANO

# Pin Definitons: (BOARD pin notation)
# Careful not to use any I2C or USART pins
if JETSON_BOARD_NAME == "NANO":  # For Jetson Nano
    FORWARDS_PIN = 37
    BACKWARDS_PIN = 35
    LEFT_PIN = 38
    RIGHT_PIN = 36
    # JETSON_CTRL_PIN = 32  // CDL=> Not needed
elif JETSON_BOARD_NAME == "AGX":  # For Jetson AGX
    FORWARDS_PIN = 16  # Dependent on hookup
    BACKWARDS_PIN = 18  # Dependent on hookup
    # GND is PIN 20
    LEFT_PIN = 22  # Dependent on hookup
    RIGHT_PIN = 24  # Dependent on hookup
    # JETSON_CTRL_PIN = CDL=> Find pin number  // CDL=> Not needed
else:
    print("Unsupported Jetson board!")


def initPins():
    """
    Setup the Jetson GPIO pins for motor control.
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(FORWARDS_PIN, GPIO.OUT)  # Setup forwards pin as output
    GPIO.setup(BACKWARDS_PIN, GPIO.OUT)  # Setup backwards pin as output
    GPIO.setup(LEFT_PIN, GPIO.OUT)  # Setup left pin as output
    GPIO.setup(RIGHT_PIN, GPIO.OUT)  # Setup right pin as output
    # GPIO.setup(JETSON_CTRL_PIN, GPIO.IN)      # Setup ctrl pin as input  // CDL=> Not needed
    stopMotors()  # Init with motors stopped


# ------------------------------------------------------------------------------
# High level user control of motors
# ------------------------------------------------------------------------------
def stopMotors():
    GPIO.output(FORWARDS_PIN, GPIO.HIGH)
    GPIO.output(BACKWARDS_PIN, GPIO.HIGH)
    GPIO.output(LEFT_PIN, GPIO.HIGH)
    GPIO.output(RIGHT_PIN, GPIO.HIGH)


def goForwards():
    GPIO.output(FORWARDS_PIN, GPIO.LOW)
    GPIO.output(BACKWARDS_PIN, GPIO.HIGH)
    GPIO.output(LEFT_PIN, GPIO.HIGH)
    GPIO.output(RIGHT_PIN, GPIO.HIGH)


def goBackwards():
    GPIO.output(FORWARDS_PIN, GPIO.HIGH)
    GPIO.output(BACKWARDS_PIN, GPIO.LOW)
    GPIO.output(LEFT_PIN, GPIO.HIGH)
    GPIO.output(RIGHT_PIN, GPIO.HIGH)


def goLeft():
    GPIO.output(FORWARDS_PIN, GPIO.HIGH)
    GPIO.output(BACKWARDS_PIN, GPIO.HIGH)
    GPIO.output(LEFT_PIN, GPIO.LOW)
    GPIO.output(RIGHT_PIN, GPIO.HIGH)


def goRight():
    GPIO.output(FORWARDS_PIN, GPIO.HIGH)
    GPIO.output(BACKWARDS_PIN, GPIO.HIGH)
    GPIO.output(LEFT_PIN, GPIO.HIGH)
    GPIO.output(RIGHT_PIN, GPIO.LOW)


# Keyboard stuff
w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False


def key_pressed(key):
    global w_pressed
    global a_pressed
    global s_pressed
    global d_pressed
    if key.name == 'w' and not w_pressed:
        w_pressed = True
        goForwards()
        # print("w pressed")
    elif key.name == 'a' and not a_pressed:
        a_pressed = True
        goBackwards()
        # print("a pressed")
    elif key.name == 's' and not s_pressed:
        s_pressed = True
        goLeft()
        # print("s pressed")
    elif key.name == 'd' and not d_pressed:
        d_pressed = True
        goRight()
        # print("d pressed")


def key_released(key):
    global w_pressed
    global a_pressed
    global s_pressed
    global d_pressed
    if key.name == 'w':
        w_pressed = False
        stopMotors()
        # print("w released")
    elif key.name == 'a':
        a_pressed = False
        stopMotors()
        # print("a released")
    elif key.name == 's':
        s_pressed = False
        stopMotors()
        # print("s released")
    elif key.name == 'd':
        d_pressed = False
        stopMotors()
        # print("d released")


def main_input():
    keyboard.on_press_key('w', key_pressed)
    keyboard.on_press_key('a', key_pressed)
    keyboard.on_press_key('s', key_pressed)
    keyboard.on_press_key('d', key_pressed)
    keyboard.on_release_key('w', key_released)
    keyboard.on_release_key('a', key_released)
    keyboard.on_release_key('s', key_released)
    keyboard.on_release_key('d', key_released)
    try:
        while (True):
            continue
    except:
        print("Exiting")
    finally:
        keyboard.unhook_all()
        GPIO.cleanup()


def signal_handler(sig, frame):
    stopMotors()
    time.sleep(1)
    sys.exit(0)


# Main code for this file. Only runs if this file is the top file
if __name__ == "__main__":
    initPins()
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        # print("hello")
        # main_input()
        goForwards()
