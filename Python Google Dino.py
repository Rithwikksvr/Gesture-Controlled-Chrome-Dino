
import cv2
import numpy as np
import time

import pyautogui

#driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
#driver.get("http://apps.thecodepost.org/trex/trex.html")
#actions = ActionChains(driver)
#actions.send_keys(Keys.SPACE)
#actions.perform()
flag=0
fcount=1
count=0
jumped=0

def max_contour(contours):
    max_i=0 
    max_area = 0
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            max_area = area
            max_i = i
    if len(contours)>=1:
        return contours[max_i]
    else:
        return None




def nothing(x):
    pass

def down():
    pyautogui.press('down')
 
def jump():
    pyautogui.press('up')

def comedown():
    actions.key_down(Keys.ARROW_DOWN)
    actions.perform()

def find_centroid(contour):
    moments = cv2.moments(contour)    
    if moments['m00'] != 0:    
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        return (cx, cy)
    else:
        return None



# Capture video from file
        
cap = cv2.VideoCapture(0)   #Reading the IMage from Webcam 

last_time = time.time()

cv2.namedWindow('image')


img = np.zeros((300,512,3), np.uint8)
cv2.createTrackbar('H1','image',0,255,nothing)
cv2.createTrackbar('S1','image',0,255,nothing)
cv2.createTrackbar('V1','image',0,255,nothing)
cv2.createTrackbar('H2','image',0,255,nothing)
cv2.createTrackbar('S2','image',0,255,nothing)
cv2.createTrackbar('V2','image',0,255,nothing)
cv2.createTrackbar('C','image',0,3,nothing)


flag=0
flag2=0

try:
    while True:
    
        ret, frame = cap.read()
    
        if ret == True:
    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #Convert it to Gray
    
            img_copy = np.copy(frame)
            
            offset_top = 150
            
            cv2.rectangle(frame,(0,offset_top),(frame.shape[1],frame.shape[0]-offset_top),(0,255,0))    #Drawing a Rectangle
            
            frame_copy = np.copy(frame)
            
            
            frame_copy[frame.shape[0]-offset_top:,:,:] = [0,0,0]
            
            
            #cv2.imshow('frame_copy',frame_copy
            #        )
            frame_copy - cv2.blur(frame,(5,5))#Bluriing
            
            roi = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV)
        
        
            h1 = cv2.getTrackbarPos('H1','image')
            s1 = cv2.getTrackbarPos('S1','image')
            v1 = cv2.getTrackbarPos('V1','image')
            h2 = cv2.getTrackbarPos('H2','image')
            s2 = cv2.getTrackbarPos('S2','image')
            v2 = cv2.getTrackbarPos('V2','image')
            c = cv2.getTrackbarPos('C','image')
        
            #  print (h,s,v)
            
            
            if c==3:
            
                lower = np.array([h1, s1, v1], dtype="uint8")
        
                upper = np.array([0, 0, 255], dtype="uint8")
            else:
                
                lower = np.array([h1, s1, v1], dtype="uint8")
        
                upper = np.array([h2, s2, v2], dtype="uint8")
        
            roi = cv2.inRange(roi, lower, upper)
            
            kernel = np.ones((5,5))
            
            roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
            
            cv2.imshow('image',roi)
                  
            cnts = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(2,2))[1]
            
            
            big_cnt = max_contour(cnts)
            
    
            cv2.drawContours(frame,big_cnt,-1,(0,0,255))
            
            
            centroid = find_centroid(big_cnt)
    
            cv2.circle(frame,centroid,8,(255,0,0),-1)        
            
            if centroid:
                if centroid[1]<offset_top:
                    
                    #print ("Jump")
                    if time.time() - last_time>.1 and flag2==1:
                        flag2=0
                        last_time = time.time() 
                        
                        jump()
                elif centroid[1]>frame.shape[0]-offset_top :
                    if time.time() - last_time>.01 and flag2==1:
                        flag2=0
                        last_time = time.time()
                        down()
                        
                else:
                    flag2=1
            #cv2.imshow('img_copy',img_copy)
            
            
            
            cv2.imshow('frame',frame)
            '''
            if flag==0:
                cv2.waitKey(3000)
                flag=1
            '''
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
    
        else:
            break
except Exception as e:
    print (e)
    cap.release()
    cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()
