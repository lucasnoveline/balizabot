POKEMON = False;

#if not POKEMON:
#	from picamera.array import PiRGBArray
#	from picamera import PiCamera
import cv2

class Camera():
    def __init__(self):
        if not POKEMON:
            self.cap = cv2.VideoCapture(1)
            #self.cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0.3)
            #self.cap.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.5)
            #self.cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, .3)
            #self.cap.set(cv2.cv.CV_CAP_PROP_GAIN, 0.1)


    def getFrame(self):
        if POKEMON:
            return cv2.imread('pokemon.jpg')
        else:
            # grab an image from the camera
            # with picamera.array.PiRGBArray(self.camera) as stream:
            # return stream.array
            ret, img = self.cap.read()
            return img