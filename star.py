# import the opencv library
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

#def nothing(val):
#    pass


#cv2.namedWindow("frame")

#cv2.createTrackbar("lb", "frame",   7, 255, nothing)
#cv2.createTrackbar("lg", "frame",  14, 255, nothing)
#cv2.createTrackbar("lr", "frame",  78, 255, nothing)
#cv2.createTrackbar("hb", "frame",  25, 255, nothing)
#cv2.createTrackbar("hg", "frame",  80, 255, nothing)
#cv2.createTrackbar("hr", "frame", 185, 255, nothing)
#cv2.createTrackbar("ksz", "frame", 0, 20, nothing)

#img = cv2.imread("objects.jpg")

def find_target_center(frame):
    # cv2.imshow("real", frame)
    avarage_x = 0
    avarage_y = 0
    
#Switch to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#Detect blue circle
    mask_blue = cv2.inRange(hsv, (lb, lg, lr), (hb, hg, hr))
    
    blured_blue = cv2.medianBlur(mask_blue*gray, 5)
    
    kernel_blue = np.ones((5,5), np.uint8)
    img_erosion_blue = cv2.erode(blured_blue, kernel_blue, iterations=1)
    img_dilation_blue = cv2.dilate(img_erosion_blue, kernel_blue, iterations=1)
    
    canny_blue = cv2.Canny(img_dilation_blue, 350, 360)
    
    # cv2.imshow("blue", canny_blue)
    
    circle_blue = cv2.HoughCircles(canny_blue, cv2.HOUGH_GRADIENT, 1.4, 100)
    
#Detect yellow circle
    mask_yellow = cv2.inRange(hsv, (8,60,140), (32,162,229))
    
    blured_yellow = cv2.medianBlur(mask_yellow*gray, 5)
    
    kernel_yellow = np.ones((5,5), np.uint8)
    img_erosion_yellow = cv2.erode(blured_yellow, kernel_yellow, iterations=1)
    img_dilation_yellow = cv2.dilate(img_erosion_yellow, kernel_yellow, iterations=1)
    
    canny_yellow = cv2.Canny(img_dilation_yellow, 180, 190)
    
    # cv2.imshow("yellow", canny_yellow)
    
    circle_yellow = cv2.HoughCircles(canny_yellow, cv2.HOUGH_GRADIENT, 1.4, 100)
    
#Detect red circle
    mask_red = cv2.inRange(hsv, (0,52,93), (18,229,228))
    
    blured_red = cv2.medianBlur(mask_red*gray, 7)
    
    kernel_red = np.ones((7,7), np.uint8)
    img_erosion_red = cv2.erode(blured_red, kernel_red, iterations=1)
    img_dilation_red = cv2.dilate(img_erosion_red, kernel_red, iterations=1)
    
    canny_red = cv2.Canny(img_dilation_red, 350, 360) 
    
    # cv2.imshow("red", canny_red)
    
    circle_red = cv2.HoughCircles(canny_red, cv2.HOUGH_GRADIENT, 2.2, 100)
    
#Find center
    
#if circle_blue is not None and circle_yellow is not None and circle_red is not None:
    #convert the (x, y) coordinates and radius of the circles to integers
    counter = 0
    total_x = 0
    total_y = 0
    
    if circle_blue is not None:
        circle_blue = np.round(circle_blue[0, :]).astype("int")
        total_x += circle_blue[0][0]
        total_y += circle_blue[0][1]
        counter += 1
        
    if circle_yellow is not None:
        circle_yellow = np.round(circle_yellow[0, :]).astype("int")
        total_x += circle_yellow[0][0]
        total_y += circle_yellow[0][1]
        counter += 1
        
    if circle_red is not None:
        circle_red = np.round(circle_red[0, :]).astype("int")
        total_x += circle_red[0][0]
        total_y += circle_red[0][1]
        counter += 1
        
    if counter > 0:
        avarage_x = total_x // counter
        avarage_y = total_y // counter
        print(avarage_x, avarage_y)
        # # draw a rectangle
        # # corresponding to the center of the circles
        cv2.rectangle(frame, (avarage_x - 10, avarage_y - 10), (avarage_x + 10, avarage_y + 10), (0, 128, 255), -1)
        # # show the output image
        # cv2.imshow("output", np.hstack([frame, output]))
        # cv2.waitKey(10)
    return avarage_x , avarage_y

# define a video capture object
vid = cv2.VideoCapture('/home/sasha/Загрузки/Telegram Desktop/IMG_3036.MOV')

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    
    w, h, _ = frame_.shape
    
    frame = cv2.resize(frame_, (h // 4, w // 4))

    #ksz = cv2.getTrackbarPos("ksz", "frame") + 1
    #frame = cv2.blur(frame, (ksz, ksz))
    
    #lb = cv2.getTrackbarPos("lb", "frame")
    #lg = cv2.getTrackbarPos("lg", "frame")
    #lr = cv2.getTrackbarPos("lr", "frame")
    #hb = cv2.getTrackbarPos("hb", "frame")
    #hg = cv2.getTrackbarPos("hg", "frame")
    #hr = cv2.getTrackbarPos("hr", "frame")
        
    find_target_center(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()