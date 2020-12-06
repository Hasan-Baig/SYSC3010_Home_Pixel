# SYSC3010_Home_Pixel

Group Project: Building a Smart Home System (This project uses python3)

## Environment Setup
Run the environment script to set up the python path
```
source homepixel_env.sh
```

## Testing
Run test scripts to ensure all hardware and software are fully functional
```
source securitysystem_tests.sh
source lightclapper_tests.sh
source tempsensor_tests.sh
```

## BME280 Temperature Sensor Setup
Setting up the BME280 Temperature Sensor on the RPi
```
sudo raspi-config --> Interfacing options --> Enable I2C (Yes)
sudo apt-get install i2c-tools python-pip
```
The command below checks whether the device is communicating with the Raspberry Pi properly
```
i2cdetect -y 1
```
The number printed out (Either 76 or 77) is the address of your device. You will set the address equal to that number in the code.
