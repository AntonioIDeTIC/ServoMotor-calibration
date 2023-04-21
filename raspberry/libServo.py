import pigpio
import time
from multiprocessing import Process, Value
import sys
import os
import signal

servo_V_Pin = 21
servo_H_Pin = 20
# Vcc = 4
# Gnd = 6

SLEEP = 0.02

# Servo 1
servo_V_minPW = 575
servo_V_maxPW = 2425
servo_V_offset = 0.575

# Servo 2
servo_H_minPW = 525
servo_H_maxPW = 2475
servo_H_offset = 0.525

initPos = 90


# A Servo Motor class with some methods
class ServoMotor:
    # init method or constructor
    def __init__(self, name, pi_handle, initPos, servoPin, minPW, maxPW, offset, sleep):
        self.name = name
        self.pi_handle = pi_handle
        self.initPos = initPos
        self.servoPin = servoPin
        self.minPW = minPW
        self.maxPW = maxPW
        self.offset = offset
        self.sleep = sleep

    """
       Debug function that prints the current connected servo motor
       :param self: reference to the current instance of the class
       :return: None
    """

    def debug_connection_message(self):
        print(self.name + " connected at --> PIN: " + str(self.servoPin))
        time.sleep(0.1)

    """
       Function that initializes the servo Motor
       :param self: reference to the current instance of the class
       :return: servo connected confirmation, current servo position
    """

    def initServo(self):
        if not self.pi_handle.connected:
            pass
        else:
            # initialize GPIO Pin
            self.debug_connection_message()
            servoConnected = True
            self.pi_handle.set_PWM_frequency(self.servoPin, 50)  # 50Hz pulses
            self.pi_handleset_PWM_range(self.servoPin, 20000)  # 20 us
            currentPos = self.moveServo(servoConnected, self.initPos, self.initPos)  # init in 90º

        return servoConnected, currentPos

    """
       Function that calculates the current angle based in the pulse width of the PWM 
       :param self: reference to the current instance of the class
       :param servoConnected: previously connected confirmation 
       :param desiredPos: desired position (in angles)
       :return: angle position
    """

    def setAngle(self, servoConnected, desiredPos):
        if servoConnected:
            pulse_with = (((self.maxPW / 1000 - self.minPW / 1000) / 180) * desiredPos) + self.offset

        else:
            print("Servomotor " + self.name + " its not connected !!")
            pass

        return int(round(pulse_with * 1000, 1))

    """
       Function that moves the servo to a desired position 
       :param self: reference to the current instance of the class
       :param servoConnected: previously connected confirmation 
       :param currentPos: current position (in angles)
       :param desiredPos: desired position (in angles)
       :return: new current position (the desired position)
    """

    def moveServo(self, servoConnected, currentPos, desiredPos):
        newCurrentPos = 0
        if currentPos <= desiredPos:
            for i in range(currentPos, desiredPos + 1):
                pulse_with = self.setAngle(servoConnected, i)
                self.pi_handleset_servo_pulsewidth(self.servoPin, pulse_with)
                newCurrentPos = i
                time.sleep(self.sleep)
        else:
            for i in range(currentPos, desiredPos - 1, -1):
                pulse_with = self.setAngle(servoConnected, i)
                self.pi_handleset_servo_pulsewidth(self.servoPin, pulse_with)
                newCurrentPos = i
                time.sleep(self.sleep)

        return newCurrentPos

    """
       Function that stops the servo in a desired position 
       :param self: reference to the current instance of the class
       :param servoConnected: previously connected confirmation 
       :param currentPos: current position (in angles)
       :param desiredPos: desired position (in angles)
       :return: None
    """

    def stopServoAt(self, servoConnected, currentPos, desiredPos):
        if servoConnected:
            self.moveServo(servoConnected, currentPos, desiredPos)
        else:
            print("Servomotor " + self.name + " its not connected !!")
            pass
