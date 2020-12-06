#!/usr/bin/env python3

"""
Pan and tilt the servo motors for camera direction
"""
import RPi.GPIO as GPIO
import logging
import sys
from time import sleep

WAIT_TIME_SECS = 0.5
PAN_INPUT_PIN = 15
TILT_INPUT_PIN = 11
PULSE_HZ = 50
GPIO_WARNINGS_OFF = False
POLLING = True


class PanTilt:
    """
    Class to represent the Pan Tilt servo motors
    Attributes
    ----------
    __panpin : int
        GPIO pin number for pan
    __tiltpin : int
        GPIO pin number for tilt
    __panservo : GPIO.PWM
        setting 50Hz pulse to __panpin
    __tiltservo : GPIO.PWM
        setting 50Hz pulse to __tiltpin 
    Methods
    -------
    start_servo()
        Start PWM running on both servos, value of 0 (pulse off) 
    change_pan_angle(angleInDegrees)
        Changes angle of pan servo according to user input
    change_tilt_angle(angleInDegrees)
        Changes angle of tilt servo according to user input
    stop_servo()
        Stops PWM on both servos
    """
    def __init__(self, panpin=PAN_INPUT_PIN, tiltpin=TILT_INPUT_PIN):
        """
        Initializes the Servo motors
        Parameters
        ----------
        panpin : int
            GPIO pin number for pan
        tiltpin : int
            GPIO pin number for tilt
        """
        self.__panpin = panpin
        self.__tiltpin = tiltpin
        # Set GPIO numbering mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(GPIO_WARNINGS_OFF)
        # Set pin for PAN & TILT
        GPIO.setup(self.__panpin,GPIO.OUT)
        GPIO.setup(self.__tiltpin,GPIO.OUT)
        #define PWM servos
        self.__panservo = GPIO.PWM(self.__panpin,PULSE_HZ)
        self.__tiltservo = GPIO.PWM(self.__tiltpin,PULSE_HZ)

    def start_servo(self):
        """
        Start PWM running on both servos, value of 0 (pulse off) 
        """
        logging.info('Start Pan/Tilt Servos')
        self.__panservo.start(0)
        self.__tiltservo.start(0)

    def change_pan_angle(self, angleInDegrees):
        """
        Changes angle of pan servo according to user input
        Parameters
        ----------
        angleInDegrees: int
            angle to turn to in degrees
        """
        self.__panservo.ChangeDutyCycle(2+(angleInDegrees/18))
        sleep(WAIT_TIME_SECS)
        self.__panservo.ChangeDutyCycle(0)
        logging.info('Pan Angle Set')

    def change_tilt_angle(self, angleInDegrees):
        """
        Changes angle of tilt servo according to user input
        Parameters
        ----------
        angleInDegrees: int
            angle to turn to in degrees
        """
        self.__tiltservo.ChangeDutyCycle(2+(angleInDegrees/18))
        sleep(WAIT_TIME_SECS)
        self.__tiltservo.ChangeDutyCycle(0)
        logging.info('Tilt Angle Set')

    def close_servo(self): 
        """
        Stops PWM on both servos
        """
        logging.info('Stop Pan/Tilt Servos')
        self.__panservo.stop()
        self.__tiltservo.stop() 
        GPIO.cleanup()


def pantilt_test():
    """
    Creates an PanTilt object for manual verification
    """
    try:
        servo_test = PanTilt()
        servo_test.start_servo()
        
        while POLLING:
            #Ask user for pan angle
            while True: 
                panangle = float(input('PAN: Enter angle between 0 & 180 (or -1 to EXIT): '))
                if (panangle == -1):
                    logging.info('EXITING')
                    exit()
                if (panangle >= 0) and (panangle <= 180):
                    break
                logging.info('ERROR: angle is not between 0 & 180')

            servo_test.change_pan_angle(panangle)
            sleep(WAIT_TIME_SECS)
            
            #Ask user for tilt angle
            while True: 
                tiltangle = float(input('TILT: Enter angle between 0 & 180 (or -1 to EXIT): '))
                if (tiltangle == -1):
                    logging.info('EXITING')
                    exit()
                if (tiltangle >= 0) and (tiltangle <= 180):
                    break
                logging.info('ERROR: angle is not between 0 & 180')
            
            servo_test.change_tilt_angle(tiltangle)
            sleep(WAIT_TIME_SECS)
                
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException as e:
        logging.error('An error or exception occurred: ' + str(e))
    finally:
        servo_test.close_servo()
        
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    pantilt_test()