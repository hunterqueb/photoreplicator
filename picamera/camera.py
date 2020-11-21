from time import sleep
from picamera import PiCamera
import os


filePath = os.path.dirname(os.path.abspath(__file__))
print(filePath)
# initialize the camera object
camera = PiCamera()
camera.resolution = (1920, 1080) # max res is 2592x1944 for still images, 1920x1080 for vidoes.
camera.framerate = 24
camera.rotation = 180
camera.start_preview(alpha=200)
sleep(1)
for i in range(2):
    camera.capture('/home/pi/Desktop/photoreplicator/picamera/photos/image%s.jpg' % str(i+1))
    camera.resolution = (2592, 1944)
camera.stop_preview()