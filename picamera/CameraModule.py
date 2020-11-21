from time import sleep
import os
from picamera import PiCamera

class CameraModule: # custom camera module class 
    def __init__(self,width,height,frameRate,rot): # on initialization
        # inputs    width       -   video/photo size width - max of 2592 for photos, 1920 for videos, in pixels
        #           height      -   video/photo size width - max of 1944 for photos, 1080 for videos, in pixels
        #           frameRate   -   framerate that the videos will be captured at, default 30, in frames per second
        #           rot         -   rotation of the pi camera module relative to the object which you want to capture, in degrees

        # initilize camera and set the width, height, framerate and rotation of the camera
        self.camera = PiCamera() 
        self.camera.resolution = (width, height)
        self.camera.framerate = frameRate
        self.camera.rotation = rot

        # get filepath for the system to prevent hard coded file paths
        self.filePath = os.path.dirname(os.path.abspath(__file__))

        self.photosPath = self.filePath + "/photos/"
        self.videosPath = self.filePath + "/videos/"

        # try to generate file paths for folder that will hold the photos, if the files already exist, catch error and tell user the path already exists
        try:
            os.mkdir(self.photosPath)
        except OSError:
            print("Creation of the directory %s failed: This directory must already exist." % self.photosPath)
        else:
            print("Successfully created the directory %s ." % self.photosPath)
        
        # try to generate file paths for folder that will hold the videos, if the files already exist, catch error and tell user the path already exists
        try:
            os.mkdir(self.videosPath)
        except OSError:
            print(
                "Creation of the directory %s failed: This directory must already exist." % self.videosPath)
        else:
            print("Successfully created the directory %s ." % self.videosPath)

        # finding the amount of files in each folder
        # upon initilization, we walk through the paths for photos and videos and find the number of files in each folder
        # _ indicates that the output of the function is no needed and can be dropped/not saved to any variable
        _, _, photoFiles = next(os.walk(self.photosPath))
        self.photoCount = len(photoFiles)

        _, _, videoFiles = next(os.walk(self.videosPath))
        self.videoCount = len(videoFiles)

    def takePic(self): # take a picture
        self.camera.start_preview(alpha=200)
        self.camera.capture(self.photosPath + "image%s.jpg" % str(self.photoCount))
        sleep(1)
        self.camera.stop_preview()
        self.photoCount = self.photoCount + 1

    def recordVid(self, time): # take a video
        self.camera.start_recording(self.videosPath + "video%s.h264" % str(self.videoCount))
        self.camera.wait_recording(time)
        self.camera.stop_recording()
        self.videoCount = self.videoCount + 1