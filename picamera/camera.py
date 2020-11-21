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
        self.photosPath = self.filePath + "/photos/"
        path,dirs,files = next(os.walk(self.photosPath))
        self.photoCount = len(files)

    def takePic(self):
        self.camera.start_preview(alpha=200)
        self.camera.capture(self.filePath + '/photos/image%s.jpg' % str(self.photoCount))
        sleep(1)
        self.camera.stop_preview()
        self.photoCount = self.photoCount + 1

width = 1920
height = 1080
framerate = 24
rotation = 180


CAM = CameraModule(width,height,framerate,rotation)

CAM.takePic()
    
