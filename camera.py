POKEMON = True;

if not POKEMON:
	from picamera.array import PiRGBArray
	from picamera import PiCamera
import time
import cv2

class Camera():
	def __init__(self):
		if not POKEMON:		
			# initialize the camera and grab a reference to the raw camera capture
			self.camera = PiCamera()
			self.rawCapture = PiRGBArray(camera)
		 
		# allow the camera to warmup
		time.sleep(0.1)

		self.rmin = 0
		self.rmax = 255
		self.bmin = 0
		self.bmax = 255
		self.gmin = 0
		self.gmax = 255

	def getFrame(self):
		if POKEMON:
			return cv2.imread('pokemon.jpg')
		else:
			# grab an image from the camera
			self.camera.capture(self.rawCapture, format='bgr')
			image = rawCapture.array
			return cv2.resize(image, (640, 480))









