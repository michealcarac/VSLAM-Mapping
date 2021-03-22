# ------------------------------------------------------------------------------
# Name         : JetsonMotorInterface.py
# Date Created : 2/22/2021
# Author(s)    : Micheal Caracciolo, Chris Lloyd, Owen Casciotti
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : A class to control a STM (CDL=> Add model here) microcontroller
#                Controlling two stepper motors with individual (CDL=>
#                Add Motor controller model here) motor controller boards.
# ------------------------------------------------------------------------------

# External Imports
import RPi.GPIO as GPIO  # For interfacing with the Jetson GPIO
import time              # CDL=> Needed?

# Jetson version (Change here for different boards)
JETSON_BOARD_NAME = "NANO"  # AGX or NANO

# Constants for direction and motor selection
# Motor
MOTOR_LEFT  = -1
MOTOR_RIGHT = 1

# Direction
FORWARDS = 1
STOP     = 0
REVERSE  = -1

# Pin Definitons: (BOARD pin notation)
if (JETSON_BOARD_NAME == "NANO"):  # For Jetson Nano
    L_MOTOR_DIR_PIN    = 38
    L_MOTOR_EN_PIN     = 37
    R_MOTOR_DIR_PIN    = 36
    R_MOTOR_EN_PIN     = 35
    JETSON_CTRL_PIN    = 32
    THUMBSTICK_BTN_PIN = 31
elif (JETSON_BOARD_NAME == "AGX"):  # For Jetson AGX
    # L_MOTOR_DIR_PIN    = CDL=> Find pin number
    # L_MOTOR_EN_PIN     = CDL=> Find pin number
    # R_MOTOR_DIR_PIN    = CDL=> Find pin number
    # R_MOTOR_EN_PIN     = CDL=> Find pin number
    # JETSON_CTRL_PIN    = CDL=> Find pin number
    # THUMBSTICK_BTN_PIN = CDL=> Find pin number
else
    print("Unsupported Jetson board!")

# Local variable to control whether the wheelchair is in
# manual control mode (False) or Jetson control mode (True)
jetsonCtrlEn = GPIO.LOW

# Invert control enabled
def invertCtrl():
    jetsonCtrlEn = not jetsonCtrlEn
    GPIO.output(JETSON_CTRL_PIN, jetsonCtrlEn)

def initPins():
    """
    Setup the Jetson GPIO pins for motor control.
    """
    GPIO.setmode(GPIO.BOARD)                  # BOARD pin-numbering scheme
    GPIO.setup(L_MOTOR_DIR_PIN,    GPIO.OUT)
    GPIO.setup(L_MOTOR_EN_PIN,     GPIO.OUT)
    GPIO.setup(R_MOTOR_DIR_PIN,    GPIO.OUT)
    GPIO.setup(R_MOTOR_EN_PIN,     GPIO.OUT)
    GPIO.setup(JETSON_CTRL_PIN,    GPIO.OUT)
    GPIO.setup(THUMBSTICK_BTN_PIN, GPIO.IN)
    GPIO.add_event_detect(THUMBSTICK_BTN_PIN,
                          GPIO.FALLING,
                          callback=invertCtrl,
                          bouncetime=10)
    GPIO.output(JETSON_CTRL_PIN, jetsonCtrlEn)
    stopMotors()                              # Init with motors stopped

def move(direction, motor):
    """
    Move a motor (motor) in a certain direction (direction).

    Arguments:
        motor     (int): The motor you want to control.
                         (MOTOR_LEFT) or (MOTOR_RIGHT).
        direction (int): The direction you want to move.
                         (FORWARDS), (STOP) or (REVERSE).
    """
    if (jetsonCtrlEn):
        dirPin = L_MOTOR_DIR_PIN if (motor == MOTOR_LEFT) else R_MOTOR_DIR_PIN
        enPin  = L_MOTOR_EN_PIN  if (motor == MOTOR_LEFT) else R_MOTOR_EN_PIN

        dirVal = GPIO.HIGH if (direction == FORWARDS) else GPIO.LOW
        enVal  = GPIO.LOW if (direction == STOP) else GPIO.HIGH

        GPIO.output(dirPin, dirVal)  # Change direction (forwards/back)
        GPIO.output(enPin,  enVal)   # Enable/disable motor (moving/stopped)
    else:
        print("In manual control. Can't control motors from Jetson!")

# ------------------------------------------------------------------------------
# High level user control of motors
# ------------------------------------------------------------------------------
def stopMotors():
    move(STOP, MOTOR_LEFT)
    move(STOP, MOTOR_RIGHT)

def goForwards():
    move(FORWARDS, MOTOR_LEFT)
    move(FORWARDS, MOTOR_RIGHT)

def goBackwards():
    move(BACKWARDS, MOTOR_LEFT)
    move(BACKWARDS, MOTOR_RIGHT)

def turnLeft():
    move(BACKWARDS, MOTOR_LEFT)
    move(FORWARDS,  MOTOR_RIGHT)

def turnRight():
    move(FORWARDS,  MOTOR_LEFT)
    move(BACKWARDS, MOTOR_RIGHT)

# Main code for this file. Only runs if this file is the top file
if __name__ == "__main__":
    print("Init GPIO interface")
    initPins()

    print("Moving forwards for 5 seconds!")
    goForwards()
    time.sleep(5)

    print("Rotate left for 5 seconds!")
    turnLeft()
    time.sleep(5)

    print("Stop motors!")
    stopMotors()