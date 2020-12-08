# SYSC3010_Home_Pixel: Smart Home System 

<p align="center">
  <img src="static\image\logo.png" alt="Home Pixel Logo" align="middle" width="487" height="300" />
</p>

This group project uses:
* HTML5 with Bootstrap
* CSS3
* JS with jQuery
* Python3 
* Bash 

## Introduction
This HomePixel smart home system monitors and controls specific home environment services that will improve one’s quality of life: **Security**, **Lighting**, and 
**Temperature**. Having a comfortable and safe home environment has recently become very important since an unprecedented amount of people are working from home due to the 
COVID-19 pandemic. The HomePixel system provides the services of security, lighting, and temperature because these can have a positive effect on an individual’s well-being, 
productivity and quality of life.  

## Contributors
* Asad Waheed
* Hasan Baig
* Mariana Rafael-White

<hr></hr>

## Hardware Required
To operate this system in a similar fashion, you will require 3 Raspberry Pis Model 4B+, a Vonage account for SMS notifications, a smart phone which can recieve SMS, a Gmail email account, a Dropbox account and an internet connection. The additional hardware used is:

* HC-SR501 passive infrared motion sensor
* Two 5V servo motors placed in camera pan/tilt structure (used: https://shop.pimoroni.com/products/pan-tilt-hat?variant=22408353287)
* Pi Camera module 
* 5V Fan
* BME280 Temperature Sensor
* LED
* LM393 sound detection sensor

## Environment Setup
Run the environment script to set up the python path
```
source homepixel_env.sh
```
Also run the following command to update the system
```
sudo apt update
``` 

## Packages
Before running the program, make sure these packages are installed on the RaspberryPi:
```
sudo apt-get install http.client
sudo apt-get install python3-urllib3
sudo apt install python3-gpiozero
pip3 install nexmo
sudo apt-get install rclone
sudo apt install -y gpac
```
For Flask WebServer:
```
pip3 install flask
pip3 install flask-wtf
sudo apt install python3-opencv
```

## Pi Camera Module Setup
Setting up the Pi Camera Module on the RPi
```
sudo raspi-config --> Interfacing Options --> Enable Camera (Yes)`--> Reboot
```

## BME280 Temperature Sensor Setup
Setting up the BME280 Temperature Sensor on the RPi
```
sudo raspi-config --> Interfacing Options --> Enable I2C (Yes)
sudo apt-get install i2c-tools python -pip
```
The command below checks whether the device is communicating with the RaspberryPi properly:
```
i2cdetect -y 1
```
The number printed out (Either 76 or 77) is the address of your device. You will need to set the address equal to the outputted number in the code.

## Deployment
### SecuritySystem
Run SecuritySystem program on the SecuritySystem node:
```
cd securitysystem/
python3 securitysystem.py -v --location <name_room>
```
Run SecuritySystem client program on the SecuritySystem node:
```
cd securitysystem/
python3 securitysystemclient.py -v
```

### TempSensor
Run TempSensor program on the TempSensor node:
```
cd tempsensor/
python3 tempsensor.py --location <name_room> -w
```
Run TempSensor client program on the SecuritySystem node:
```
cd tempsensor/
python3 tempsensorclient.py
```

### LightClapper
Run LightClapper program on the LightClapper node:
```
cd lightclapper/
python3 lightclapper.py --location <name_room> -w
```
Run LightClapper client program on the Security System node:
```
cd lightclapper/
python3 lightclapperclient.py
```

## Testing
Run test scripts to ensure all hardware and software are fully functional
```
source securitysystem_tests.sh
source lightclapper_tests.sh
source tempsensor_tests.sh
```

## Flask Webpage (GUI)

### Set up environment variables for Unix/Mac
```
export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=1
```
### Set up environment variables for Windows
```
set FLASK_APP=main.py
set FLASK_ENV=development
set FLASK_DEBUG=1
```
**Note: if you already ran "source homepixel_env.sh" then the environment variables are already setup**

### Start the application
```
flask run
```
or
```
flask run --host=0.0.0.0 --port=5000
```
Fill in the above with these parameters:
```
--host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
--port=5000    - specify the app port (default 5000)  
```

## Possible Problems with Solutions
### Problem 1

#### Problem:
```
picamera.exc.PiCameraMMALError: Camera component couldn't be enabled: out of resources (other than memory)
```
#### Background:
The Raspberry Pi Camera Module uses the onboard GPU and its memory. Since the error message mentions being out of resources, consider adding at least the recommended minimum of 128MB to the GPU's allotment (then change to 256MB if needed).

#### Solution:
The process will still be running in the background, in the terminal add:
```
ps -a
```
This will list all of the currently running processes. Look for one that says "python" or "python3" in the output, like this:
```
PID  TTY      TIME       CMD
1218 tty1     00:00:00   bash
2203 pts/0    00:00:00   python
8960 pts/1    00:00:00   ps
```
To stop the python process, use the command:
```
kill -KILL [PID#]
```
For this case, the command was "kill -KILL 2203". After doing this, use "ps -a" again to make sure the python process is not listed. Next add the following in terminal:
```
sudo raspi-config
```
select: Advanced options -> Memory split -> and set 128MB or 256MB -> Finish -> Reboot

## **FINAL NOTE: CONSTRAINTS OF THE SYSTEM (LIMITATION OF RESOURCES)**
On the webserver, the localhost will crash if you access the Security page at the same time as running the SecuritySystem node. This is because the Security page livestreams a video of the camera and the SecuritySystem node has to record a video. The Raspberry Pi does not have enough recources to access the camera module port to record and livestream at the same time, therefore the following message will pop up on the console, and exit the script.

<img src="static\image\cameraResourcesCrash.PNG" alt="Console Crash from Accessing Camera Port" style="float: left;" />

This is a constraint of the system and cannot be fixed while using a Raspberry Pi.
