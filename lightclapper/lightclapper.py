#!/usr/bin/env python3
"""
light_clapper.py
"""
import RPi.GPIO as GPIO
import time
from led import Led
from mic import Microphone
from thingspeakwriter import ThingSpeakWriter
from constants import L2_M_5C1_WRITE_KEY, GOOD_STATUS
import argparse
import logging

POLL_TIME_SECS = 0.5


class LightClapper:
    """
    Turns on/off light when a clap is detected

    Attributes
    ----------
    __mic : Microphone
        The microphone sensor
    __led : Led
        The LED light
    __write_mode : bool
        True if write to ThingSpeak channel
    __writer : ThingSpeakWriter
        Writer to write to ThingSpeak channel

    Methods
    -------
    poll()
        Polls to inverts the light status based on mic input
    check_and_update_status()
        Inverts the light status based on mic
    __write_status_to_channel()
        Writes information to ThingSpeak channel
    """

    def __init__(self, mic=Microphone(), led=Led(),
                 write=False, write_key=L2_M_5C1_WRITE_KEY):
        """
        Initializes the attributes

        Parameters
        ----------
        mic : Microphone
            The microphone sensor
        led : Led
            The LED light
        write : bool
            True if write to ThingSpeak channel
        write_key : str
            Optional key if writing to ThingSpeak channel
        """
        self.__mic = mic
        self.__led = led
        self.__writer = None

        self.__write_mode = write
        if self.__write_mode:
            self.__writer = ThingSpeakWriter(write_key)

    def poll(self):
        """
        Poll for microphone sensor claps
        """
        try:
            while True:
                toggle = self.check_and_update_status()

                if toggle and self.__write_mode:
                    self.__write_status_to_channel()

                # If light status changed, wait before polling again
                sleep_time = POLL_TIME_SECS if toggle else 0
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print('Exiting')
        except BaseException:
            print('An error or exception occurred!')
        finally:
            self.__led.set_status(False)
            GPIO.cleanup()
            if self.__write_mode:
                self.__write_status_to_channel()

    def check_and_update_status(self):
        """
        Check microphone sensor for a clap
        and set light status if required

        Returns
        -------
        toggle : bool
            True if light status was toggled
        """
        toggle = False
        if self.__mic.check_input():
            self.__led.invert_status()
            toggle = True

        return toggle

    def __write_status_to_channel(self):
        """
        Write status of light clapper to channel
        """
        status = 1 if self.__led.get_status() else 0
        fields = {'field1': status}
        status, reason = self.__writer.write_to_channel(fields)
        if status != GOOD_STATUS:
            raise Exception('Write was unsuccessful')


def parse_args():
    """
    Parses arguments for manual testing of LightClapper

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the LightClapper program (CTRL-C to exit)')
    parser.add_argument('-w',
                        '--write',
                        default=False,
                        action='store_true',
                        help='Write data to channel')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging_level)

    light_clapper = LightClapper(write=args.write)
    light_clapper.poll()
