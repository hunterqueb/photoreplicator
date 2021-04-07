from libraries.picamera.CameraModule import CameraModule

width = 1920
height = 1080
framerate = 24
rotation = 0

CAM = CameraModule(width, height, framerate, rotation)

CAM.takePic()
# CAM.takePic()

# vidLength = 6

# CAM.recordVid(vidLength)
# CAM.recordVid(vidLength)
