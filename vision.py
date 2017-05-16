# import the necessary packages
import imutils
import cv2

class Vision:
	def getVertex(vertices):
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

	def filterColor(image, boundaries): 
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
		cv2.imshow("images", np.hstack([image, output]))
		cv2.waitKey(0)

	def detectLines(image):
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

	def detectTriangle(image):
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
