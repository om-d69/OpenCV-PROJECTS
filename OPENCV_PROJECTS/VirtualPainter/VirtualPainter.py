import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)          
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)


myColours = [[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
myColourValues = [[51,153,255],          ## BGR
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]
myPoints = []  


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def findColour(img, myColours, myColourValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for count, color in enumerate(myColours):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x != 0 and y != 0:
            cv2.circle(imgResult, (x, y), 15, myColourValues[count], cv2.FILLED)
            newPoints.append([x, y, count])
        
    return newPoints


def drawOnCanvas(myPoints, myColourValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColourValues[point[2]], cv2.FILLED)


def mouseClick(event, x, y, flags, param):
    global myPoints
    if event == cv2.EVENT_LBUTTONDOWN:
        myPoints = []   


cv2.namedWindow("Result")
cv2.setMouseCallback("Result", mouseClick)

while True:
    success, img = cap.read()
    if not success:
        break

    imgResult = img.copy()

    newPoints = findColour(img, myColours, myColourValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColourValues)

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()