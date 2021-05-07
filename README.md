# Autonomous Movement from Simultaneous Localization and Mapping

#  

### About us

Built by a group of Clarkson University students with the help from Professor Masudul Imtiaz and his Lab Resources. 

```
Micheal Caracciolo           - Sophomore, ECE Department
Owen Casciotti               - Senior, ECE Department
Chris lloyd                  - Senior, ECE Department
Ernesto Schumann-Sola        - Freshman, ECE Department
Kyle Bielby                  - Senior, ECE Department
Baset Sarker                 - Graduate Student, ECE Department
Tipu Sultan                  - Graduate Student, ME Department
Masudul Imtiaz               - Professor, Clarkson University ECE Department
```

This project began in January 2021 and was finished May 5th 2021. 

### Synopsis



### Supported Devices:

```
Jetson AGX
Jetson Nano
```
 ### Hardware:
```
Wheelchair
Jetson Development board
Any Arduino
Development Computer to install Jetson Jetpack SDK (For AGX)
One Intel Realsense D415
One Motor controller ()
2 12V Batteries For Motors
2 12V Lipo Batteries for Jetson
```

### Software:

Tensorflow Version: ```2.3.1```

OpenVSLAM

We will need to install a few different Python 3.8 packages. We recommend using Conda environments as then you will not have to compile a few packages.  However, some packages are not available in Conda, for those just install via pip while inside of the appropriate Conda env. 

```
csv
heapq
Jetson.GPIO (Can only be installed on Jetson)
keyboard
matplotlib
msgpack
numpy
scipy (Greater than 1.5.0)
signal
websockets
```



## Initial Setup

OpenVSLAM, Official Documentation: link

* Refer to vslamsetup.md (link)



Webserver, Not needed unless want to interface with phone

* Move the ```www``` folder into your /var directory in your root file system. 
* Open up python server files and insert your static IP of your Jetson 
* Run ```python server.py```

Note: There is some example data and maps in the csv format. This format is required to correctly transmit maps/paths to the device that is listening to the server.



Android Phone,

* Insert the IP wanting to connect to, in this instance, the static IP of the Jetson
* Build the Java app to your Android Phone

Note: This can only be used if the Webserver is set up and the ```server.py``` is on. We recommend to have it be turned on via startup. We do not have this implemented in our current code, but can be easily added. If you plan on using a Android Phone for a Map/Path/End point interface, you will need to edit some lines in ```/src/main.py``` and add to ```send_location.py```. This is all untested code currently. 



Source Code, ensure you're in the right Conda Environment

* To use your own map/.msg file from OpenVSLAM, you will need to put it in the /data folder. There are a few options with this, you can either use the raw .msg file which our ```MapFileUnpacker.py``` will take care of, or you can create a csv format of 0 and 1's in the format of a map. 0 being unoccupied and 1 being occupied in the Occupancy Grid Map. For even easier storage, you could run ```MapFileUnpacker.py``` and have it extract the keyframes into a csv, which then you can use for ```OLD_main.py``` or ```main.py```. We recommend to use the map file you created which is in the form of .msg. 
* You can either use ```OLD_main.py``` or ```main.py```. ```OLD_main.py``` can be ran without having to run the motors on the connected Jetson. This is helpful for debugging and testing before you decide to implement the map onto a Jetson. ```main.py``` will ONLY work on a Jetson as it will call ```JetsonMotorInterface.py``` which contains Jetson.GPIO libraries which can only be installed on a Jetson.
* If the Android Phone is set up, you will need to edit ```main.py``` to send the start position via ```send_location.py``` to the webserver. You will also need to uncomment a few lines so that the current map is sent to the /var/www/html filepath. Then, the phone should be able to send back a end value which calls ``` def main``` with that end value. Otherwise, ```def main``` will run with a predefined end value in code. 
* To set up the pinout, you will need to first build ```arduino_motor_ctrl.ino``` onto the Arduino that is connected to the motor controller. You can use virtually any pins on the Arduino, depending on what Arduino you use. Set these pins in the .ino file. Next, we want to set the pins on the Jetson that output the data to the Arduino pins. Set these pins in ```JetsonMotorInterface.py```. Be careful not to use any I2C or USART pins as these cannot be configured as GPIO Output. 

Note: To properly run ```main.py``` without any issues, it is recommended to follow https://github.com/NVIDIA/jetson-gpio#setting-user-permissions so that you do not need to run Sudo for any of the /src files. If you were to run Sudo, you would have a bunch of different libraries and it will not run properly. If you get an ```Illegal Instruction``` error, please try to create a Conda environment to run these scripts. 

Note: We are using a Sabertooth 2x32 Dual 32A Motor Driver to drive our dual Wheelchair motors. The Arduino also gets it's power from the Motor Driver, but do not connect it there while it is connected to the computer for building. 

A few things to be weary of, in the ```main.py```, since we are not using the Localization from VSLAM, we are simulating the created map into a path. This path will run differently depending on how accurate it is and the speed of your motors. We recommend you to scale your room to your map, so you will want to section out your map in code and have a timing ratio to ensure it moves the right distance of "Occupancy Grid Map spaces". This is explained better in the code. 












