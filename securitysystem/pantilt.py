#!/usr/bin/env python3

"""
Pan and tilt the servo motors for camera direction
"""
import RPi.GPIO as GPIO
import logging
from time import sleep
import constants as c

WAIT_TIME_SECS = 0.5
PAN_INPUT_PIN = 15
TILT_INPUT_PIN = 11
PULSE_HZ = 50
GPIO_WARNINGS_OFF = False
ANGLE_SET = True
ANGLE_NOT_SET = True
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
        ddd
    change_angle(angleInDegrees)
        Changes angle of servos according to user input
    start_servo()
        ddd
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

    def change_pan_angle(self):
        """
        Changes angle of pan servo according to user input
        Parameters
        ----------
        angleInDegrees : int
            Angle to turn to in degrees
        """
        #Ask user for angle
        while True: 
            angle = float(input('PAN: Enter angle between 0 & 180 (or -1 to EXIT): '))
            if (angle == -1):
                logging.info('Pan Angle Not Set')
                return ANGLE_NOT_SET
            if (angle >= 0) and (angle <= 180):
                break
            logging.info('ERROR: angle is not between 0 & 180')

        #Turn servo to angle
        self.__panservo.ChangeDutyCycle(2+(angle/18))
        sleep(WAIT_TIME_SECS)
        self.__panservo.ChangeDutyCycle(0)
        logging.info('Pan Angle Set')
        return ANGLE_SET

    def change_tilt_angle(self):
        """
        Changes angle of tilt servo according to user input
        """
        #Ask user for angle
        while True: 
            angle = float(input('TILT: Enter angle between 0 & 180 (or -1 to EXIT): '))
            if (angle == -1):
                logging.info('Tilt Angle Not Set')
                return ANGLE_NOT_SET
            if (angle >= 0) and (angle <= 180):
                break
            logging.info('ERROR: angle is not between 0 & 180')

        #Turn servo to angle
        self.__tiltservo.ChangeDutyCycle(2+(angle/18))
        sleep(WAIT_TIME_SECS)
        self.__tiltservo.ChangeDutyCycle(0)
        logging.info('Tilt Angle Set')
        return ANGLE_SET

    def close_servo(self):
        """
        Stops PWM on both servos
        """
        logging.info('Stop Pan/Tilt Servos')
        self.__panservo.stop()
        self.__tiltservo.stop() 


def pantilt_test():
    """
    Creates an PanTilt object for manual verification
    """
    try:
        servo_test = PanTilt()
        servo_test.start_servo()
        
        while POLLING:
            pan_result = servo_test.change_pan_angle()
            if(pan_result):
                sleep(WAIT_TIME_SECS)

            tilt_result = servo_test.change_tilt_angle()
            if(tilt_result):
                sleep(WAIT_TIME_SECS)
                
    except KeyboardInterrupt:
        logging.info('Exiting')
    except BaseException as e:
        logging.error('An error or exception occurred: ' + str(e))
    finally:
        servo_test.close_servo()
        GPIO.cleanup()
        

# def parse_args():
#     """
#     Parses arguments for manual testing of SecuritySystem
#     Returns
#     -------
#     args : Namespace
#         Populated attributes based on args
#     """
#     parser = argparse.ArgumentParser(description='Run the SecuritySystem program (CTRL-C to exit)')
    
#     parser.add_argument('-v',
#                         '--verbose',
#                         default=False,
#                         action='store_true',
#                         help='Print all debug logs')
    
#     parser.add_argument('-pa',
#                         '--panangle',
#                         type=int,
#                         required=True,
#                         metavar='<owner_room>',
#                         help='Specify pan angle between 0° to 180°')

#     parser.add_argument('-ta',
#                         '--tiltangle',
#                         type=int,
#                         required=True,
#                         metavar='<owner_room>',
#                         help='Specify tilt angle between 0° to 180°')

#     args = parser.parse_args()
#     return args


if __name__ == '__main__':
    # args = parse_args()
    # logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=c.LOGGING_DEFAULT_LEVEL)
    # pan_tilt = PanTilt(args.panangle, args.tiltangle)
    # pan_tilt.start_servo()
    # pan_tilt.poll()
    pantilt_test()