from picamera import PiCamera
from os import system
from time import sleep
import random

camera = PiCamera()
camera.resolution = (1944, 1944)
camera.framerate = 15

for i in range(1000):
    sleep(1)
    camera.brightness = 50 + random.randint(-10, 10)
    camera.contrast =  50 + random.randint(-10, 10)
    #print(camera.brightness, camera.contrast)
    #camera.capture('/home/pi/Shared/Closed/Closed{0:04d}.jpg'.format(i))
    camera.capture('/home/pi/Shared/Open/Open{0:04d}.jpg'.format(i))


