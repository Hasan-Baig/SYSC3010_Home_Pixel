# SYSC3010_Home_Pixel

Group Project: Building a Smart Home System (This project uses python3)

## Environment Setup
Run the environment script to set up the python path
```
source homepixel_env.sh
```

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
sudo apt update
pip3 install flask
pip3 install flask-wtf
sudo apt install python3-opencv
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
