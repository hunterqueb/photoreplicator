from time import sleep
from picamera import PiCamera
import os

class CameraModule:
    def __init__(self,width,height,frameRate,rot):
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.camera.framerate = frameRate
        self.camera.rotation = rot
        self.filePath = os.path.dirname(os.path.abspath(__file__))
        self.count = 0
        for path in os.listdir(self.filePath):
            if os.path.isfile(os.path.join(self.filePath, path)):
                self.count += 1

    def takePic(self):
        camera.start_preview(alpha=200)
        self.camera.capture(self.filePath + '/photos/image%s.jpg' % str(self.count))
        sleep(3)
        camera.stop_preview()

    


# filePath = os.path.dirname(os.path.abspath(__file__))
# print(filePath)
# # initialize the camera object
# camera = PiCamera()
# camera.resolution = (1920, 1080) # max res is 2592x1944 for still images, 1920x1080 for vidoes.
# camera.framerate = 24
# camera.rotation = 180
# camera.start_preview(alpha=200)
# sleep(1)
# for i in range(2):
#     camera.capture(filePath + '/photos/image%s.jpg' % str(i+1))
#     camera.resolution = (2592, 1944)
# camera.stop_preview()
