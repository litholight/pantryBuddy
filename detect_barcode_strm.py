
import numpy as np
import argparse
import cv2
#import zxing

#reader = zxing.BarCodeReader()
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help = "")
#args = vars(ap.parse_args())

cap = cv2.VideoCapture('windowClearner.mp4')

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('barcodeCaptured.mp4', fourcc, 20.0,(540,960))
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        count = count + 1 
#load the image and convert it to greyscale
        #image = cv2.imread(frame)
        height, width, layers = frame.shape
        resize = cv2.resize(frame, (int(width*.75), int(height*.75)))
        gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)

#computer the Scharr gradient magnitude representation of the images
#in both x and y direction
        gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
        gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

#subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)

#blur and threshold the image
        blurred = cv2.blur(gradient, (3,3))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

#construct a closing kernel and apply it to the threshold image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations = 4)
        closed = cv2.dilate(closed, None, iterations = 4)

#find the contours in the threshold image, then sort the contours
#by their area, keeping only the largest one.
        _, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
            rect = cv2.minAreaRect(c) 
            box = np.int0(cv2.boxPoints(rect))
            x, y, width, height = cv2.boundingRect(box)
            width = width + 20
            height = height + 20
            if (width != 0) or (height != 0):
                roi = resize[y-10:y+height, x-10:x+width]
            else:
                roi = resize
            if count % 20 == 0:
                cv2.imwrite("./frames/frame%d.jpg" % count, roi)

            cv2.drawContours(resize, [box], -1, (0, 255, 0), 3)
#compute the rotated bounding box of the largest contour

#draw a bounding box around the detected barcode and display
#the image


        
#        out.write(frame)
        cv2.imshow("Image", resize)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
#out.release()
cv2.destroyAllWindows()
