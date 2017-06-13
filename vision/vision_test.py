import vision
import camera
import cv2

vis = vision.Vision()
cam = camera.Camera()

while(1):
    img = cam.getFrame()
    cv2.imshow('img', img)
    cv2.waitKey(1)
    # lines are green
    lines = vis.detect_lines(img)

	# car is blue
	#car_pos = vis.detect_car(img)

	# other cars are red
	#other_cars = vis.detect_other_cars(img)

	# and so are you
