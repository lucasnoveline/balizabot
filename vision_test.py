import vision
import camera
import cv2

vis = vision.Vision()
seg = vision.Segmentation()
cam = camera.Camera()

img = cv2.imread('pokemon.jpg')
cv2.imshow('original_image', img)
cv2.waitKey(0)


img_r = seg.filter_color(img, 'r')
img_g = seg.filter_color(img, 'g')
img_b = seg.filter_color(img, 'b')

# lines are green
#lines = vis.detect_lines(img)

# car is blue
#car_pos = vis.detect_car(img)

# other cars are red
other_cars = vis.detect_other_cars(img)

# and so are you
