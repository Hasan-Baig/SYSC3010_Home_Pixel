# SYSC3010_Home_Pixel
Group Project: Building a Smart Home System

This project uses python3

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

## Problems with Solutions
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
