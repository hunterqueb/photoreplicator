from time import sleep
from picamera import PiCamera

# initialize the camera object
camera = PiCamera()
camera.start_preview(alpha=200)
sleep(1)
camera.capture('/home/pi/Desktop/photoreplicator/picamera/photos/image.jpg')
camera.stop_preview()