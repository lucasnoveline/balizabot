# import the necessary packages
import imutils
import cv2
import camera
import numpy as np

CONFIG_FILE = 'config.txt'

class Vision:
	def __init__(self):
		self.camera = camera.Camera()
		self.bmin, self.bmax = 0, 255
		self.gmin, self.gmax = 0, 255
		self.rmin, self.rmax = 0, 255

		# try to reach config file
		try:
			f = open(CONFIG_FILE, 'r')
			values = json.load(f)			
			a, self.bmin, self.bmax = values[0]
			a, self.gmin, self.gmax = values[1]
			a, self.rmin, self.rmax = values[2]
		except:
			print 'Not able to find configuration file, running calibration'
			self.calibrate_boundaries()
			f = open(CONFIG_FILE, 'w')
			json.dump([['b', self.bmin, self.bmax],['g', self.gmin, self.gmax],['r', self.rmin, self.rmax]], f)

	def calibrate_boundaries(self):
		window_name = 'Color filter calibration'
		cv2.namedWindow(window_name)

		# create filter trackbars
		cv2.createTrackbar('R-', window_name, 0, 255, self.setRmin)
		cv2.createTrackbar('R+', window_name, 255, 255, self.setRmax)
		cv2.createTrackbar('G-', window_name, 0, 255, self.setGmin)
		cv2.createTrackbar('G+', window_name, 255, 255, self.setGmax)
		cv2.createTrackbar('B-', window_name, 0, 255, self.setBmin)
		cv2.createTrackbar('B+', window_name, 255, 255, self.setBmax)

		while(1):
			img = self.camera.getFrame()
			filtered = self.filterColor(img,([self.bmin, self.gmin, self.bmin],[self.bmax, self.gmax, self.bmax]))
			cv2.imshow(window_name, filtered)
			k = cv2.waitKey(1) & 0xFF 
			if k == 27:
				break
			
			#get trackbar position
			test = cv2.getTrackbarPos('R-',window_name)	
		cv2.destroyAllWindows()	
	
	def setRmin(self, x):
		self.rmin = x
		if self.rmin >= self.rmax:
			cv2.setTrackbarPos('R+', 'Color filter calibration', self.rmin)

	def setGmin(self, x):
		self.gmin = x
		if self.gmin >= self.gmax:
			cv2.setTrackbarPos('G+', 'Color filter calibration', self.gmin)

	def setBmin(self, x):
		self.bmin = x
		if self.bmin >= self.bmax:
			cv2.setTrackbarPos('B+', 'Color filter calibration', self.bmin)

	def setRmax(self, x):
		self.rmax = x
		if self.rmax <= self.rmin:
			cv2.setTrackbarPos('R-', 'Color filter calibration', self.rmax)

	def setGmax(self, x):
		self.gmax = x
		if self.gmax <= self.gmin:
			cv2.setTrackbarPos('G-', 'Color filter calibration', self.gmax)

	def setBmax(self, x):
		self.bmax = x
		if self.bmax <= self.bmin:
			cv2.setTrackbarPos('B-', 'Color filter calibration', self.bmax)


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

	def filterColor(self, image, boundaries): 
		# define the list of boundaries
		#boundaries = 
		#	([17, 15, 100], [50, 56, 200])
		#

		# create NumPy arrays from the boundaries
		lower = np.array(boundaries[0], dtype = "uint8")
		upper = np.array(boundaries[1], dtype = "uint8")
		 
		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
		 
		# show the image
		return output

	def detectLines(self, image):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,100,200,apertureSize = 3)

		minLineLength = 30
		maxLineGap = 10
		lines = cv2.HoughLinesP(thresh,1,np.pi/180,15,minLineLength,maxLineGap)
		for x in range(0, len(lines)):
		    for x1,y1,x2,y2 in lines[x]:
			cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)

		#cv2.imshow('hough',img)
		#cv2.waitKey(0)
		return lines		

	def detectTriangle(self, image):
		# resize the image to a smaller factor so that
		# the shapes can be approximated better
		resized = imutils.resize(image, width=500)
		ratio = image.shape[0] / float(resized.shape[0])

		# convert the resized image to grayscale, blur it slightly,
		# and threshold it
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY_INV)[1]

		# find contours in the thresholded image and initialize the
		# shape detector
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# loop over the contours
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

			# multiply vertex coordinates by the resize ratio
			approx = approx.astype('float')
			approx *= ratio
			approx = approx.astype('int')

			# Draw centroid and direction vertex
			cv2.circle(image, (cX, cY), 10, (0, 0, 0), -1) 
			vertex = getVertex(approx)	
			cv2.circle(image, (vertex[0], vertex[1]), 10, (0,0,0), -1)
		 
		# show the output image
		#cv2.imshow("Image", image)
		#cv2.waitKey(0)
		
		return ((cX,cY), (vertex[0], vertex[1]))
