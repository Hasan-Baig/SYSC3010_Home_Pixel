#!/usr/bin/env python3
"""
Polls the motion sensor to upload to ThingSpeak and record video
"""
import time
from camera import Camera
from motionsensorclass import MotionSensorClass
from thingspeakwriter import ThingSpeakWriter
import nexmo
import smtplib
from subprocess import call  
import subprocess
import argparse
import logging
from constants import (L2_M_5A1_WRITE_KEY, 
                       GOOD_STATUS,
                       SMS_API_KEY, 
                       SMS_API_SECRET,
                       FROM_NUMBER,
                       TO_NUMBER,
                       SMTP_SERVER,
                       SMTP_PORT,
                       GMAIL_USERNAME,
                       GMAIL_PASSWORD)

POLL_TIME_SECS = 0.5 


class SecuritySystem:

    def __init__(self, mts=MotionSensorClass(), cam=Camera(), 
                 writer=ThingSpeakWriter(L2_M_5A1_WRITE_KEY)):
        """
        Initializes the attributes
        Parameters
        ----------
        mic : MotionSensorClass
            The motion sensor
        led : Camera
            The camera
        writer : ThingSpeakWriter
            ThingSpeak channel
        """
        self.__mts = mts
        self.__cam = cam
        self.__writer = writer
        self.__link = ""
        
    def poll(self):
        """
        Poll for motion
        """
        try:
            self.__cam.start_camera()
            while True:
                motionDetected = self.update_status()

                if motionDetected[0]:
                    self.__write_to_channel(motionDetected[1], motionDetected[2])
                    self.__send_notification(motionDetected[1], motionDetected[2])
                    self.__upload_video(motionDetected[1], motionDetected[2])
                    self.__email_link(motionDetected[1], motionDetected[2], self.__link)

                # Wait before polling again
                sleep_time = POLL_TIME_SECS if motionDetected[0] else 0
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print('Exiting')
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
        finally:
            self.__cam.close_camera()
            self.__mts.close_sensor()
            self.__delete_local_videos()

    def update_status(self):
        """
        Check motion sensor for detected motion
        and set camera to record
        Returns
        -------
        result : bool, str, str
            True if motion detected, date of motion, time of motion
        """
        result = self.__mts.check_input()
        if(result[0]):
            self.__cam.record_video(result[1], result[2])
            self.__convert_to_mp4(result[1], result[2])
        return result[0], result[1], result[2]

    def __convert_to_mp4(self, date, time):                             #TEST
        """
        Convert video to mp4 file (playable on Windows)
        """
        try: 
            path = "/home/pi/Desktop/Security_Cam/"
            file_h264 = "{}{}_{}.h264".format(path, date, time)
            file_mp4 = "{}{}_{}.mp4".format(path, date, time)
            file_temp = "{}covert.h264".format(path)

            #rename file_h264 to file_temp
            command0 = "mv {} {}".format(file_h264, file_temp)
            call([command0], shell=True)
            
            #convert file_temp to file_mp4
            command1 = "MP4Box -add {} {}".format(file_temp, file_mp4)
            call([command1], shell=True) 

            #remove file_temp
            command2 = "rm {}".format(file_temp)
            call([command2], shell=True)
            
            logging.debug("Video converted to MP4 successfully!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()
    
    def __write_to_channel(self, date, time):
        """
        Write status of motion to channel
        """
        try:
            fields = {'field1': "{} {}".format(date, time)}
            status, reason = self.__writer.write(fields)
            if status != GOOD_STATUS:
                raise Exception('Write was unsuccessful')

        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def __send_notification(self, date, time):
        """
        Send notification via SMS to mobile phone
        """
        try:
            client = nexmo.Client(key=SMS_API_KEY, secret=SMS_API_SECRET)

            responseData = client.send_message({
                'from': FROM_NUMBER,
                'to': TO_NUMBER,
                'text': 'Motion Detected at {} {}\n'.format(date, time),
            })

            if responseData["messages"][0]["status"] == "0":
                logging.debug("Message sent successfully.")
            else:
                logging.debug("Message failed with error: {}".format(responseData['messages'][0]['error-text']))

        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def __upload_video(self, date, time):
        """
        Upload video to Google Drive
        """
        try: 
            uploadPath = "/home/pi/Desktop/Home_Pixel/Dropbox-Uploader/dropbox_uploader.sh" 
            vidfile = "/home/pi/Desktop/Security_Cam/{}_{}.mp4".format(date, time)
            upl = "{} upload {} /HOMEPIXEL".format(uploadPath, vidfile)   
            call ([upl], shell=True)  

            h, m, s = time.split(":")
            self.__link = "https://www.dropbox.com/home/HOMEPIXEL?preview={}_{}%3A{}%3A{}.mp4".format(date, h, m, s)
            
            logging.debug("Video uploaded successfully!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()
        

    def __email_link(self, date, time, link):
        """
        Email link to gmail of Google Drive access link 
        """
        try:
            #Create Headers
            headers = ["From: " + GMAIL_USERNAME, 
                    "Subject: Video for Motion Detected at {} {}".format(date, time), 
                    "To: " + GMAIL_USERNAME,
                    "MIME-Version: 1.0", 
                    "Content-Type: text/html"]
            headers = "\r\n".join(headers)
    
            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()
    
            #Login to Gmail
            session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    
            #Send Email & Exit
            session.sendmail(GMAIL_USERNAME, GMAIL_USERNAME, headers + "\r\n\r\n" + "The 10 second video when motion is detected is shown here: " + link)
            session.quit

            logging.debug("Email sent successfully!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def __delete_local_videos(self):
        """
        Deletes all videos stored locally 
        """
        try: 
            removeLocal = "rm /home/pi/Desktop/Security_Cam/*"  
            call ([removeLocal], shell=True)

            logging.debug("Removed all local video files!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()     


def parse_args():
    """
    Parses arguments for manual testing of LightClapper
    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(description='Run the SecuritySystem program (CTRL-C to exit)')
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

    security_system = SecuritySystem()
    security_system.poll()