POKEMON = False;

#if not POKEMON:
#	from picamera.array import PiRGBArray
#	from picamera import PiCamera
import time
import cv2

class Camera():
	def __init__(self):
		if not POKEMON:		
			# initialize the camera and grab a reference to the raw camera capture
			#self.camera = PiCamera()
			#self.camera.resolution(640,480)
			self.cap = cv2.VideoCapture(1)

	def getFrame(self):
		if POKEMON:
			return cv2.imread('pokemon.jpg')
		else:
			# grab an image from the camera
			#with picamera.array.PiRGBArray(self.camera) as stream:
			#	return stream.array
			ret, img = self.cap.read()
			return img



