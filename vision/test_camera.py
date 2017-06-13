from __future__ import print_function
import sys
import cv2

cap = cv2.VideoCapture(1)
B = 0
C = 0
S = 0
G = 0

properties = ["CV_CAP_PROP_FRAME_WIDTH",  # Width of the frames in the video stream.
              "CV_CAP_PROP_FRAME_HEIGHT",  # Height of the frames in the video stream.
              "CV_CAP_PROP_BRIGHTNESS",  # Brightness of the image (only for cameras).
              "CV_CAP_PROP_CONTRAST",  # Contrast of the image (only for cameras).
              ]


def onTrackbar_changedB(x):
    global B
    B = x
    Brightness = float(x) / 100
    cap.set(cv2.cv.CV_CAP_PROP_HUE, Brightness)

def onTrackbar_changedC(x):
    global C
    C = x
    Contrast = float(C) / 100
    cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, Contrast)

def onTrackbar_changedS(x):
    global S
    S = x
    Saturation = float(S) / 100
    cap.set(cv2.cv.CV_CAP_PROP_SATURATION, Saturation)

def onTrackbar_changedG(x):
    global G
    G = x
    Gain = float(G) / 100
    cap.set(cv2.cv.CV_CAP_PROP_GAIN, Gain)

def main(argv):
    winName = 'input'
    cv2.namedWindow(winName)

    Brightness = cap.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)
    Contrast = cap.get(cv2.cv.CV_CAP_PROP_CONTRAST)
    Saturation = cap.get(cv2.cv.CV_CAP_PROP_SATURATION)
    Gain = cap.get(cv2.cv.CV_CAP_PROP_GAIN)

    global B
    B = int(Brightness * 100)
    global C
    C = int(Contrast * 100)
    global S
    S = int(Saturation * 100)
    global G
    G = int(Gain * 100)

    cv2.createTrackbar("Brightness", winName, B, 100, onTrackbar_changedB)
    cv2.createTrackbar("Contrast", winName, C, 100, onTrackbar_changedC)
    cv2.createTrackbar("Saturation", winName, S, 100, onTrackbar_changedS)
    cv2.createTrackbar("Gain", winName, G, 100, onTrackbar_changedG)

    while True:
        ret, img = cap.read()
        cv2.imshow(winName, img)

        key = cv2.waitKey(20)
        if key == 27:
            break

        for prop in properties:
            val = cap.get(eval("cv2.cv." + prop))
            print(prop + ": " + str(val))

    cv2.destroyAllWindows()
    cv2.VideoCapture(1).release()


if __name__ == '__main__':
    main(sys.argv)
