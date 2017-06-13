import numpy as np
import cv2

properties=["CV_CAP_PROP_FRAME_WIDTH",# Width of the frames in the video stream.
            "CV_CAP_PROP_FRAME_HEIGHT",# Height of the frames in the video stream.
            "CV_CAP_PROP_BRIGHTNESS",# Brightness of the image (only for cameras).
            "CV_CAP_PROP_CONTRAST",# Contrast of the image (only for cameras).
            "CV_CAP_PROP_SATURATION",# Saturation of the image (only for cameras).
            "CV_CAP_PROP_GAIN"]

cap = cv2.VideoCapture(1)
for prop in properties:
    val=cap.get(eval("cv2.cv."+prop))
    print prop+": "+str(val)

gain=0
cap.set(cv2.cv.CV_CAP_PROP_GAIN,gain)

brightness=60
cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,brightness)

contrast=20
cap.set(cv2.cv.CV_CAP_PROP_CONTRAST,contrast)

saturation=20
cap.set(cv2.cv.CV_CAP_PROP_SATURATION,saturation)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb=frame

    # Display the resulting frame
    cv2.imshow('frame',rgb)
    key=cv2.waitKey(4)
    if key == ord('x'):
        break
    elif key == ord('w'):
        brightness+=0.1
        cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,brightness)
    elif key == ord('s'):
        brightness-=0.1
        cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,brightness)
    elif key == 1048676:
        contrast+=0.1
        cap.set(cv2.cv.CV_CAP_PROP_CONTRAST,contrast)
    elif key == ord('a'):
        contrast-=0.1
        cap.set(cv2.cv.CV_CAP_PROP_CONTRAST,contrast)
    elif key == ord('e'):
        saturation+=0.1
        cap.set(cv2.cv.CV_CAP_PROP_SATURATION,saturation)
    elif key == ord('q'):
        saturation-=0.1
        cap.set(cv2.cv.CV_CAP_PROP_SATURATION,saturation)
    else:
        continue

    print "\n\n"
    for prop in properties:
        val=cap.get(eval("cv2.cv."+prop))
        print prop+": "+str(val)

# When everything done, release the capture
cap.release()
#cv2.destroyAllWindows()