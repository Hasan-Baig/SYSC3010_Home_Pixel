#!/usr/bin/env python3
"""
lightclapper.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import RPi.GPIO as GPIO
import argparse
import logging
from time import sleep
from led import Led
from mic import Microphone
from thingspeakwriter import ThingSpeakWriter
import constants as c

DEFAULT_ID = 0
ID_INCREMENT = 1
ZERO_SECS = 0
POLL_TIME_SECS = 0.5
POLLING = True


class LightClapper:
    """
    Turns on/off light when a clap sound is detected

    Attributes
    ----------
    __location : str
        Location of LightClapper node
    __node_id : str
        Unique ID of LightClapper on node
    __mic : Microphone
        The microphone sensor
    __led : Led
        The LED light
    __write_mode : bool
        True if write to ThingSpeak channel
    __writer : ThingSpeakWriter
        Writer to write to ThingSpeak channel if __write_mode True

    Methods
    -------
    poll()
        Polls to get mic input and invert the light status accordingly
    check_and_update_status()
        Inverts the light status based on mic input
    __write_status_to_channel()
        Writes information to ThingSpeak channel
    """
    light_clapper_id = DEFAULT_ID   # Static ID of LightClapper unit

    def __init__(self, location, mic=Microphone(), led=Led(),
                 write=False, write_key=c.L2_M_5C1_WRITE_KEY):
        """
        Initializes the attributes

        Parameters
        ----------
        location : str
            location of LightClapper
        mic : Microphone
            The microphone sensor
        led : Led
            The LED light
        write : bool
            True if write to ThingSpeak channel
        write_key : str
            Optional key if writing to ThingSpeak channel
        """
        LightClapper.light_clapper_id += ID_INCREMENT
        self.__node_id = '{node_name}_{id}'.format(
            node_name=c.LIGHT_CLAPPER_NAME,
            id=LightClapper.light_clapper_id)

        self.__location = location
        self.__mic = mic
        self.__led = led

        self.__write_mode = write
        self.__writer = ThingSpeakWriter(write_key) if write else None

    def poll(self):
        """
        Poll for microphone sensor claps.
        Update LED based on mic input.
        Write update to ThingSpeak channel.
        """
        logging.info('LightClapper program running')
        logging.info('Writing to channel mode enabled?: {}'.format(
            self.__write_mode))
        try:
            while POLLING:
                toggled = self.check_and_update_status()

                if toggled:
                    logging.info('LightClapper toggled the LED')
                    if self.__write_mode:
                        self.__write_status_to_channel()

                # If light status changed, wait before polling again
                sleep_time = POLL_TIME_SECS if toggled else ZERO_SECS
                sleep(sleep_time)

        except KeyboardInterrupt:
            logging.info('Exiting due to keyboard interrupt')

        except BaseException as e:
            logging.error('An error or exception occurred!')
            logging.error('Error traceback: {}'.format(e))

        finally:
            # Attempt to reset LED status and cleanup GPIO
            if self.__led.get_status() == c.LED_ON:
                self.__led.invert_status()
                if self.__write_mode:
                    self.__write_status_to_channel()
            GPIO.cleanup()

    def check_and_update_status(self):
        """
        Check microphone sensor for a clap
        and invert light status if clap detected

        Returns
        -------
        toggled : bool
            True if light status was toggled
        """
        toggled = False
        if self.__mic.check_input() == c.SOUND_DETECTED:
            self.__led.invert_status()
            toggled = True
        return toggled

    def __write_status_to_channel(self):
        """
        Write status of light clapper to channel
        """
        led_status = c.OFF_INT
        if self.__led.get_status() == c.LED_ON:
            led_status = c.ON_INT

        fields = {c.LOCATION_FIELD: self.__location,
                  c.NODE_ID_FIELD: self.__node_id,
                  c.LIGHT_STATUS_FIELD: led_status}

        status, reason = self.__writer.write_to_channel(fields)
        if status != c.GOOD_STATUS:
            logging.error('Write to ThingSpeak channel was unsuccessful')


def parse_args():
    """
    Parses arguments for manual operation of the LightClapper

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
                        help='Write data to ThingSpeak channel')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-l',
                        '--location',
                        type=str,
                        required=True,
                        metavar='<owner_room>',
                        help='Specify owner and room')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    light_clapper = LightClapper(args.location, write=args.write)
    light_clapper.poll()
