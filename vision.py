# import the necessary packages
import imutils
import json
import cv2
import camera
import numpy as np

class Vision:
	def getVertex(self, vertices):
		# get vertices
		a = vertices[0][0]
		b = vertices[1][0]
		c = vertices[2][0]

		# compute lengths
		ab = ((b[0]-a[0])*(b[0]-a[0]) + (b[1]-a[1])*(b[1]-a[1]))**.5
		bc = ((c[0]-b[0])*(c[0]-b[0]) + (c[1]-b[1])*(c[1]-b[1]))**.5
		ac = ((c[0]-a[0])*(c[0]-a[0]) + (c[1]-a[1])*(c[1]-a[1]))**.5

		# get vertex opposite to smaller side
		if ac > bc and ab > bc:
			return a
		if bc > ac and ab > ac:
			return b
		return c 

	def detect_lines(self, image):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,100,200,apertureSize = 3)

		minLineLength = 30
		maxLineGap = 10
		lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
		for x in range(0, len(lines)):
		    for x1,y1,x2,y2 in lines[x]:
			cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)

		cv2.imshow('hough',image)
		cv2.waitKey(0)
		return lines		

	def detect_triangle(self, image):
		# convert the image to grayscale, blur it slightly,
		# and threshold it
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY_INV)[1]

		# find contours in the thresholded image and initialize the
		# shape detector
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# loop over the contours
		vertex = []
		for c in cnts:
			# check if triangle
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.04 * peri, True)
			if len(approx) != 3:
				continue

			# compute the center of the contour
			M = cv2.moments(c)
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)

			# Draw centroid and direction vertex
			cv2.circle(image, (cX, cY), 10, (0, 0, 0), -1) 
			
			vertex = getVertex(approx)	
			print vertex
			cv2.circle(image, (vertex[0], vertex[1]), 10, (0,0,0), -1)
		 
		# show the output image
		cv2.imshow("Image", image)
		cv2.waitKey(0)
		m = (vertex[1]-vertex[0])/(cX,cY)
		return ((cX,cY), m)


class Segmentation:
	def __init__(self):
		self.window_name = 'Color filter calibration'
		self.camera = camera.Camera()	
		self.boundaries = [[[0,0,0],[255,255,255]],
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
		else:
			return ([self.hmin, self.smin, self.vmin],[self.hmax, self.smax, self.vmax])

	def filter_color(self, image, channel = ''): 
		# create NumPy arrays from the boundaries
		boundaries = np.asarray(self.get_boundaries(channel))
		# find the colors within the specified boundaries and apply
		# the mask 
		hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_img, boundaries[0], boundaries[1])
		output = cv2.bitwise_and(hsv_img, hsv_img, mask = mask)
		 
		# show the image
		return cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

	def calibrate_boundaries(self):
		cv2.namedWindow(self.window_name)

		# create filter trackbars
		cv2.createTrackbar('H-', self.window_name, 0, 255, self.setHmin)
		cv2.createTrackbar('H+', self.window_name, 255, 255, self.setHmax)
		cv2.createTrackbar('S-', self.window_name, 0, 255, self.setSmin)
		cv2.createTrackbar('S+', self.window_name, 255, 255, self.setSmax)
		cv2.createTrackbar('V-', self.window_name, 0, 255, self.setVmin)
		cv2.createTrackbar('V+', self.window_name, 255, 255, self.setVmax)

		while(1):
			img = self.camera.getFrame()		
			output = self.filter_color(img)
			
			cv2.imshow(self.window_name, output)
			k = cv2.waitKey(1) & 0xFF
			if k == 114: 
				self.rPressed()
			if k == 103: 
				self.gPressed()
			if k == 98: 
				self.bPressed() 
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
