# Door Recognition System

## Getting Started
These instructions will give you opportunity to buil your own Smart Door with Face Recognition

What you need to install 
- OpenCV 
I am using a Raspberry Pi V3 updated to the last version of Raspbian (Stretch), so the best way to have OpenCV installed, is to follow the excellent tutorial developed by Adrian Rosebrock
```
https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
```
Adrian recommends run the command "source" each time you open up a new terminal to ensure your system variables have been set up correctly.
```
source ~/.profile
```
Next, let's enter on our virtual environment:
```
workon cv
```
If you see the text (cv) preceding your prompt, then you are in the cv virtual environment:

```
(cv) pi@raspberry:~$
```
In case you get an errar like: OpenCV Error: Assertion failed , you can try solve the issue, using the command:
```
sudo modprobe bcm2835-v4l2
```

### Installing

A step by step series of examples that tell you how to get a development env running

Face Detection
Download the file:
* [Face Dataset](https://github.com/tranvinhliem/Face-Recognition---RPi-version/blob/master/face_dataset.py) - We added, was an "input command" to capture a user id, that should be an integer number (1, 2, 3, etc)
* [Face Training](https://github.com/tranvinhliem/Face-Recognition---RPi-version/blob/master/face_training.py) -  We must take all user data from our dataset and "trainer" the OpenCV Recognizer. This is done directly by a specific OpenCV function. The result will be a .yml file that will be saved on a "trainer/" directory.
* [Door](https://github.com/tranvinhliem/Door-Recognition/blob/master/door.py) - The main program of this project

## Authors
Based on project of Mr.Marcelo Provai
* **Marcelo Provai** - *Initial work* - [Github](https://github.com/Mjrovai/OpenCV-Face-Recognition)
Developed by Tran Vinh Liem

See also the list of [my Git](https://github.com/your/project/contributors) who participated in this project.


