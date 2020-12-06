#!/usr/bin/env python3

"""
Polls the motion sensor to upload to ThingSpeak, records video, converts
to mp4 format, sends SMS notification to user, uploads to Dropbox
and emails access link to gmail
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
import constants as c

#Magic numbers (constants)
DEFAULT_ID = 0
POLL_TIME_SECS = 0.5 
POLLING = True
ID_INCREMENT = 1

class SecuritySystem:
    """
    Recorded video when motion is detected
    Attributes
    ----------
    __location : str
        Location of SecuritySystem node
    __node_id : str
        Unique ID of SecuritySystem node
    __mts : MotionSensorClass
        The motion sensor
    __cam : Camera
        The camera
    __writer : ThingSpeakWriter
        Writer to write to ThingSpeak channel
    __link : str
        Dropbox access link of recorded video
    Methods
    -------
    poll()
        Polls to get motion input
    update_status()
        Records a 10s video based on motion input 
    convert_to_mp4(date, time)   
        Converts video file format from h264 to mp4
    __write_status_to_channel(date, time)
        Writes information to ThingSpeak channel
    send_notification(date, time)
        Send SMS notification to mobile phone based when motion detected
    upload_video(date, time)
        Uploads video to Dropbox
    email_link(date, time, link)
        Email dropbox access link to gmail
    __delete_local_videos()
        Deletes all local recorded videos
    """
    security_system_id = DEFAULT_ID   # Class variable (static)

    def __init__(self, location, mts=MotionSensorClass(), cam=Camera(), 
                 writer=ThingSpeakWriter(c.L2_M_5A1_WRITE_KEY)):
        """
        Initializes the attributes
        Parameters
        ----------
        location : str
            Location of SecuritySystem node
        mts : MotionSensorClass
            The motion sensor
        cam : Camera
            The camera
        writer : ThingSpeakWriter
            ThingSpeak channel
        link : str
            Dropbox access link of recorded video
        """
        SecuritySystem.security_system_id += ID_INCREMENT

        self.__node_id = '{node}_{id}'.format(
            node=c.SECURITY_SYSTEM_NAME,
            id=SecuritySystem.security_system_id)

        self.__location = location
        self.__mts = mts
        self.__cam = cam
        self.__writer = writer
        self.__link = ""
        
    def poll(self):
        """
        Poll for motion.
        Writes information to ThingSpeak channel.
        Send SMS notification to mobile phone. 
        Uploads video to Dropbox.
        Email dropbox access link to gmail.
        """
        
        logging.info('SecuritySystem program running')
        try:
            self.__cam.start_camera()
            while POLLING:
                motionDetected = self.update_status()

                if motionDetected[0]:
                    #Write to Thingspeak, send SMS notifcation, upload to Dropbox and email Dropbox access link
                    self.__write_to_channel(motionDetected[1], motionDetected[2])
                    self.send_notification(motionDetected[1], motionDetected[2])
                    self.upload_video(motionDetected[1], motionDetected[2])
                    self.email_link(motionDetected[1], motionDetected[2], self.__link)
                    # Wait before polling again
                    time.sleep(POLL_TIME_SECS)
                
        except KeyboardInterrupt:
            print('Exiting')
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
        finally:
            #Close camera preview, sensor input, delete local videos
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
            self.convert_to_mp4(result[1], result[2])
        return result[0], result[1], result[2]

    def convert_to_mp4(self, date, time):
        """
        Convert video to mp4 file (compatability with Windows & Linux)
        Parameters
        ----------
        date : str
            Date when motion detected
        time : str
            Time when motion detected
        """
        try: 
            path = "/home/pi/Desktop/Security_Cam/"
            file_h264 = "{}{}_{}.h264".format(path, date, time)
            file_mp4 = "{}{}_{}.mp4".format(path, date, time)
            file_temp = "{}convert.h264".format(path)

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
        Parameters
        ----------
        date : str
            Date when motion detected
        time : str
            Time when motion detected
        """
        try:
            fields = {c.LOCATION_FIELD: self.__location,
                      c.NODE_ID_FIELD: self.__node_id,
                      c.DATE_TIME_FIELD: "{} {}".format(date, time)}

            status, reason = self.__writer.write(fields)
            if status != c.GOOD_STATUS:
                raise Exception('Write was unsuccessful')

        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def send_notification(self, date, time):
        """
        Send notification via SMS to mobile phone
        Parameters
        ----------
        date : str
            Date when motion detected
        time : str
            Time when motion detected
        """
        try:
            client = nexmo.Client(key=c.SMS_API_KEY, secret=c.SMS_API_SECRET)

            responseData = client.send_message({
                'from': c.FROM_NUMBER,
                'to': c.TO_NUMBER,
                'text': 'Motion Detected at {} {}\n'.format(date, time),
            })

            if responseData["messages"][0]["status"] == "0":
                logging.debug("Message sent successfully.")
            else:
                logging.debug("Message failed with error: {}".format(responseData['messages'][0]['error-text']))

        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def upload_video(self, date, time):
        """
        Upload video to Google Drive
        Parameters
        ----------
        date : str
            Date when motion detected
        time : str
            Time when motion detected
        """
        try: 
            uploadPath = "/home/pi/Desktop/Home_Pixel/Dropbox-Uploader/dropbox_uploader.sh" 
            vidfile = "/home/pi/Desktop/Security_Cam/{}_{}.mp4".format(date, time)
            upl = "{} upload {} /HOMEPIXEL".format(uploadPath, vidfile)   
            call ([upl], shell=True)  

            #According to URL syntax ":" = %3A
            h, m, s = time.split(":")
            self.__link = "https://www.dropbox.com/home/HOMEPIXEL?preview={}_{}%3A{}%3A{}.mp4".format(date, h, m, s)
            
            logging.debug("Video uploaded successfully!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()
        

    def email_link(self, date, time, link):
        """
        Email link to gmail of Google Drive access link 
        Parameters
        ----------
        date : str
            Date when motion detected
        time : str
            Time when motion detected
        link : str
            Dropbox access link of video
        """
        try:
            #Create Headers
            headers = ["From: " + c.GMAIL_USERNAME, 
                    "Subject: Video for Motion Detected at {} {}".format(date, time), 
                    "To: " + c.GMAIL_USERNAME,
                    "MIME-Version: 1.0", 
                    "Content-Type: text/html"]
            headers = "\r\n".join(headers)
    
            #Connect to Gmail Server
            session = smtplib.SMTP(c.SMTP_SERVER, c.SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()
    
            #Login to Gmail
            session.login(c.GMAIL_USERNAME, c.GMAIL_PASSWORD)
    
            #Send Email & Exit
            session.sendmail(c.GMAIL_USERNAME, c.GMAIL_USERNAME, headers + "\r\n\r\n" + "The 10 second video when motion is detected is shown here: " + link)
            session.quit

            logging.debug("Email sent successfully!")
        
        except BaseException as e:
            print('An error or exception occurred: ' + str(e))
            exit()

    def __delete_local_videos(self):
        """
        Deletes all videos stored locally.
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
    Parses arguments for manual testing of SecuritySystem
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
    security_system = SecuritySystem(args.location)
    security_system.poll()