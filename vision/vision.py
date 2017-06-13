# import the necessary packages
import imutils
import json
import cv2
import camera
import numpy as np
from math import atan2

class Vision:
    def __init__(self):  # this feels extremely EXG, sorry pals.
        self.seg = Segmentation()

    ### detecta linhas verdes, que representam marcacoes de estacionamento
    ## recebe:
    # image - arquivo de imagem
    ## retorna:
    # rectangles - [[centerx, centery],[height, width], angle of rotation]
    def detect_lines(self, image):
        # get green mask
        g_img = self.seg.filter_color(image, 'g')
        g_img = cv2.erode(g_img, np.ones((5, 5), np.uint8), iterations=1)
        g_img = cv2.dilate(g_img, np.ones((5, 5), np.uint8), iterations=5)

        # separate contours
        c = cv2.findContours(g_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = c[0] if imutils.is_cv2() else c[1]

        # get CoM for each contour and add it to result
        rectangles = []
        for cnt in c:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
            # line_centers = line_centers + [[cX,cY]]
            rect = cv2.minAreaRect(cnt)
            rectangles += [rect]
        return rectangles

    def detect_other_cars(self, image):
        # get red mask
        r_img = self.seg.filter_color(image, 'r')
        r_img = cv2.erode(r_img, np.ones((5, 5), np.uint8), iterations=2)
        r_img = cv2.dilate(r_img, np.ones((5, 5), np.uint8), iterations=5)

        # separate contours
        c = cv2.findContours(r_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = c[0] if imutils.is_cv2() else c[1]

        # get CoM for each contour and add it to result
        car_centers = []
        for cnt in c:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
            car_centers = car_centers + [[cX, cY]]
        return car_centers

    def detect_car(self, image):
        # get yellow square center:
        y_img = self.seg.filter_color(image, 'y')
        y_img = cv2.erode(y_img, np.ones((5, 5), np.uint8), iterations=1)
        y_img = cv2.dilate(y_img, np.ones((5, 5), np.uint8), iterations=5)
        M = cv2.moments(y_img)

        if M["m00"] == 0:
            return
        cX_y = int((M["m10"] / M["m00"]))
        cY_y = int((M["m01"] / M["m00"]))

        # get blue square center:
        b_img = self.seg.filter_color(image, 'b')
        b_img = cv2.erode(b_img, np.ones((5, 5), np.uint8), iterations=1)
        b_img = cv2.dilate(b_img, np.ones((5, 5), np.uint8), iterations=5)
        M = cv2.moments(b_img)

        if M["m00"] == 0:
            return
        cX_b = int((M["m10"] / M["m00"]))
        cY_b = int((M["m01"] / M["m00"]))

        # get center and orientation
        center = [(cX_y + cX_b) / 2, (cY_y + cY_b) / 2]
        orientation = atan2((cY_y - cY_b), (cX_y - cX_b))
        return [center, orientation]


class Segmentation:
    def __init__(self):
        self.window_name = 'Color filter calibration'
        self.boundaries = [[[0,0,0],[255,255,255]],
                           [[0,0,0],[255,255,255]],
                           [[0,0,0],[255,255,255]],
                           [[0,0,0],[255,255,255]]]

        # try to reach config file
        CONFIG_FILE = 'config.txt'
        try:
            f = open(CONFIG_FILE, 'r')
            self.boundaries = json.load(f)
            f.close()
        except:
            print 'Not able to find configuration file, running calibration'

            # set initial threshold values
            self.hmin, self.hmax = 0, 255
            self.smin, self.smax = 0, 255
            self.vmin, self.vmax = 0, 255

            boundaries = self.calibrate_boundaries()
            f = open(CONFIG_FILE, 'w')
            json.dump(boundaries, f)
            f.close()

    def get_boundaries(self, channel):
        if channel == 'b':
            return self.boundaries[0]
        elif channel == 'g':
            return self.boundaries[1]
        elif channel == 'r':
            return self.boundaries[2]
        elif channel == 'y':
            return self.boundaries[3]
        else:
            return ([self.hmin, self.smin, self.vmin],[self.hmax, self.smax, self.vmax])

    def filter_color(self, image, channel = '', calibration = False):
        # create NumPy arrays from the boundaries
        boundaries = np.asarray(self.get_boundaries(channel))
        # find the colors within the specified boundaries and apply
        # the mask
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, boundaries[0], boundaries[1])
        output = cv2.bitwise_and(hsv_img, hsv_img, mask = mask)

        # show the image
        if calibration:
            return cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
        else:
            return mask

    def calibrate_boundaries(self):
        cv2.namedWindow(self.window_name)
        self.camera = camera.Camera()
        # create filter trackbars
        cv2.createTrackbar('H-', self.window_name, 0, 255, self.setHmin)
        cv2.createTrackbar('H+', self.window_name, 255, 255, self.setHmax)
        cv2.createTrackbar('S-', self.window_name, 0, 255, self.setSmin)
        cv2.createTrackbar('S+', self.window_name, 255, 255, self.setSmax)
        cv2.createTrackbar('V-', self.window_name, 0, 255, self.setVmin)
        cv2.createTrackbar('V+', self.window_name, 255, 255, self.setVmax)

        while(1):
            img = self.camera.getFrame()
            output = self.filter_color(img, calibration = True)

            cv2.imshow(self.window_name, output)
            k = cv2.waitKey(1) & 0xFF
            if k == 114:
                self.rPressed()
            if k == 103:
                self.gPressed()
            if k == 98:
                self.bPressed()
            if k == 121:
                self.yPressed()
            if k == 27 or k == 10:
                break
        cv2.destroyAllWindows()

        return self.boundaries

    ## trackbar callback functions
    def setHmin(self, x):
        self.hmin = x
        if self.hmin >= self.hmax:
            cv2.setTrackbarPos('H+', self.window_name, self.hmin)

    def setSmin(self, x):
        self.smin = x
        if self.smin >= self.smax:
            cv2.setTrackbarPos('S+', self.window_name, self.smin)

    def setVmin(self, x):
        self.vmin = x
        if self.vmin >= self.vmax:
            cv2.setTrackbarPos('V+', self.window_name, self.vmin)

    def setHmax(self, x):
        self.hmax = x
        if self.hmax <= self.hmin:
            cv2.setTrackbarPos('H-', self.window_name, self.hmax)

    def setSmax(self, x):
        self.smax = x
        if self.smax <= self.smin:
            cv2.setTrackbarPos('S-', self.window_name, self.smax)

    def setVmax(self, x):
        self.vmax = x
        if self.vmax <= self.vmin:
            cv2.setTrackbarPos('V-', self.window_name, self.vmax)

    def rPressed(self):
        self.boundaries[2][0] = [self.hmin, self.smin, self.vmin]
        self.boundaries[2][1] = [self.hmax, self.smax, self.vmax]
        print 'red filter calibrated'

    def gPressed(self):
        self.boundaries[1][0] = [self.hmin, self.smin, self.vmin]
        self.boundaries[1][1] = [self.hmax, self.smax, self.vmax]
        print 'green filter calibrated'

    def bPressed(self):
        self.boundaries[0][0] = [self.hmin, self.smin, self.vmin]
        self.boundaries[0][1] = [self.hmax, self.smax, self.vmax]
        print 'blue filter calibrated'

    def yPressed(self):
        self.boundaries[3][0] = [self.hmin, self.smin, self.vmin]
        self.boundaries[3][1] = [self.hmax, self.smax, self.vmax]
        print 'yellow filter calibrated'

if __name__ == "__main__":
    vis = Vision()
    cam = camera.Camera()

    while (1):
        img = cam.getFrame()
        # lines are green
        lines = vis.detect_lines(img)
        for line in lines:
            cv2.circle(img, (int(line[0][0]), int(line[0][1])), 4, (255, 100, 100), 3)

        # car is blue
        car_pos = vis.detect_car(img)
        if car_pos is not None:
            cv2.circle(img, (car_pos[0][0], car_pos[0][1]), 4, (255, 100, 100), 3)

        # other cars are red
        other_cars = vis.detect_other_cars(img)
        for other_car in other_cars:
            cv2.circle(img, (other_car[0], other_car[1]), 4, (255, 100, 100), 3)

        cv2.imshow('img', img)
        key = cv2.waitKey(1)
        if key == 27:
            break