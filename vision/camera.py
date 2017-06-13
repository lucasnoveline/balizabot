# Código de inicialização da câmera. Caso a variável POKEMON == True
# a câmera inicia com uma imagem externa ('pokemon.jpg'). Caso contrário
# inicia a captura de imagens da câmera.

POKEMON = False;

#if not POKEMON:
#	from picamera.array import PiRGBArray
#	from picamera import PiCamera
import cv2

class Camera():
    def __init__(self):
        if not POKEMON:
            # Caso não POKEMON == False, inicia a captura da câmera
            # com a biblioteca cv2.
            self.cap = cv2.VideoCapture(1)
            #self.cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0.3)
            #self.cap.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.5)
            #self.cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, .3)
            #self.cap.set(cv2.cv.CV_CAP_PROP_GAIN, 0.1)


    def getFrame(self):
        # Método getFrame
        if POKEMON:
            # Caso POKEMON == True, abre 'pokemon.jpg'
            return cv2.imread('pokemon.jpg')
        else:
            # Caso POKEMON == False, lê imagem da câmera.
            ret, img = self.cap.read()
            return img
            # grab an image from the camera
            # with picamera.array.PiRGBArray(self.camera) as stream:
            # return stream.array
