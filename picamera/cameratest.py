from CameraModule import CameraModule
# from the camera module file, import the camera module class

width = 1920
height = 1080
framerate = 24
rotation = 180

CAM = CameraModule(width, height, framerate, rotation)

CAM.takePic()
CAM.takePic()

vidLength = 6

CAM.recordVid(vidLength)
CAM.recordVid(vidLength)
